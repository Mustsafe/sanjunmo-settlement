# probe_v60b_sett005.py — 읽기 전용 진단 (파일 수정 없음)
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

FILES = {
    "prototype": "prototype/ADMN-SETT-005_baseline.html",
    "prototype_clean": "prototype_clean/ADMN-SETT-005_baseline.html",
}
CUT = 400

def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")

def show(tag, i, s):
    s = s.rstrip("\r")
    print(f"  [{tag}] L{i+1}: {s[:CUT]}{' …(trunc)' if len(s) > CUT else ''}")

for fd, fp in FILES.items():
    L = rd(fp)
    print(f"\n===== [{fd}] {fp} (총 {len(L)}줄)")

    print("\n--- (A) CSS L355~L470 원문")
    for i in range(354, min(len(L), 470)):
        show("A", i, L[i])

    print("\n--- (B) 전체 파일에서 hidden / modal-backdrop / display 관련 선택자·대입 줄")
    pat = re.compile(r'(\.hidden\b|\.modal-backdrop|\[hidden\]|style\.display|\.style\.cssText|setProperty\(\s*["\']display|classList\.(add|remove|toggle)\(\s*["\'](open|show|active|is-open|visible)["\'])')
    hit = [i for i, s in enumerate(L) if pat.search(s)]
    if not hit: print("  0건")
    for i in hit:
        show("B", i, L[i])

    print("\n--- (C) 두 번째 <script> 블록 L1405~L1479 원문")
    for i in range(1404, min(len(L), 1479)):
        show("C", i, L[i])

    print("\n--- (D) 첫 번째 <script> 블록 끝부분 L1340~L1404 원문")
    for i in range(1339, min(len(L), 1404)):
        show("D", i, L[i])

js_pat = re.compile(r'(modal-backdrop|closeAllModals|forceCloseModal|style\.display\s*=\s*["\']none|\.hidden\b)')
for fd in FILES:
    js = Path(fd) / "common-snb.js"
    print(f"\n===== (E) {js} 모달/숨김 관련 줄")
    if not js.exists():
        print("  파일 없음"); continue
    J = rd(js)
    hit = [i for i, s in enumerate(J) if js_pat.search(s)]
    if not hit: print("  0건")
    for i in hit[:40]:
        show("E", i, J[i])

print("\n\n===== (F) Playwright 런타임: 클릭 전후 newAdjModal 상세")
from playwright.sync_api import sync_playwright

DETAIL_JS = """() => {
  const m = document.getElementById('newAdjModal');
  if (!m) return ['newAdjModal 없음'];
  const cs = getComputedStyle(m);
  const out = [
    `class="${m.className}"`,
    `style attr="${m.getAttribute('style') || ''}"`,
    `inline display="${m.style.display}"`,
    `hidden attr=${m.hasAttribute('hidden')}`,
    `computed display=${cs.display} position=${cs.position} z-index=${cs.zIndex}`,
  ];
  const rules = [];
  for (const sh of document.styleSheets) {
    let rs; try { rs = sh.cssRules; } catch (e) { continue; }
    for (const r of rs) {
      if (r.selectorText && r.style && r.style.display) {
        try { if (m.matches(r.selectorText)) rules.push(`${r.selectorText} { display:${r.style.display}${r.style.getPropertyPriority('display') ? ' !important' : ''} } @${(sh.href || 'inline').split('/').pop()}`); } catch (e) {}
      }
    }
  }
  out.push('매칭 display 규칙: ' + (rules.length ? '' : '0건'));
  rules.forEach(x => out.push('   ' + x));
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for fd, fp in FILES.items():
        print(f"\n### [{fd}]")
        for label, sel in [("상단 버튼", "#btnOpenNewAdjModal"), ("카드 버튼", "button[onclick='openNewAdjModal()']")]:
            pg = b.new_page()
            pg.goto(Path(fp).resolve().as_uri())
            pg.wait_for_timeout(1000)
            print(f"  -- {label} ({sel})")
            print("   클릭 전:")
            for x in pg.evaluate(DETAIL_JS): print(f"     {x}")
            try:
                pg.locator(sel).first.click(timeout=3000)
                pg.wait_for_timeout(700)
                print("   클릭 수행: OK")
            except Exception as ex:
                print(f"   클릭 실패: {str(ex)[:CUT]}")
            print("   클릭 후:")
            for x in pg.evaluate(DETAIL_JS): print(f"     {x}")
            pg.close()
    b.close()
print("\n[PROBE B DONE]")
