# probe_v60_sett005.py — 읽기 전용 진단 (파일 수정 없음)
import sys, re, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

FOLDERS = ["prototype", "prototype_clean"]
KEY = "신규 수동 조정"
CUT = 400

def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")

def show(tag, i, s):
    s = s.rstrip("\r")
    print(f"  [{tag}] L{i+1}: {s[:CUT]}{' …(trunc)' if len(s) > CUT else ''}")

targets = {}
for fd in FOLDERS:
    hits = sorted(glob.glob(f"{fd}/ADMN-SETT-005*.html"))
    print(f"\n===== [{fd}] 대상 파일: {hits if hits else '0건'}")
    if not hits:
        continue
    fp = hits[0]
    targets[fd] = fp
    L = rd(fp)

    print(f"\n--- (A) '{KEY}' 포함 줄")
    a = [i for i, s in enumerate(L) if KEY in s]
    if not a: print("  0건")
    for i in a:
        for j in range(max(0, i-2), min(len(L), i+3)):
            show("A", j, L[j])
        print("  ---")

    print("\n--- (B) 버튼 핸들러 / id 추출")
    names, ids = set(), set()
    for i in a:
        blob = " ".join(L[max(0, i-2):i+3])
        for h in re.findall(r'onclick\s*=\s*"([^"]*)"', blob) + re.findall(r"onclick\s*=\s*'([^']*)'", blob):
            print(f"  onclick: {h}")
            for n in re.findall(r'([A-Za-z_$][\w$.]*)\s*\(', h):
                names.add(n.split(".")[-1])
        for d in re.findall(r'\bid\s*=\s*"([^"]+)"', blob):
            ids.add(d)
        for d in re.findall(r'data-[\w-]+\s*=\s*"([^"]+)"', blob):
            print(f"  data-attr: {d}")
    print(f"  함수명: {sorted(names) or '0건'} / 주변 id: {sorted(ids) or '0건'}")

    print("\n--- (C) 함수 정의 (정의 줄 + 이후 30줄)")
    if not names: print("  0건")
    for n in sorted(names):
        pat = re.compile(rf'(function\s+{re.escape(n)}\b|\b{re.escape(n)}\s*=\s*(async\s*)?(function|\()|window\.{re.escape(n)}\s*=)')
        d = [i for i, s in enumerate(L) if pat.search(s)]
        print(f"  ## {n}: 정의 {len(d)}건")
        for i in d:
            for j in range(i, min(len(L), i+31)):
                show("C", j, L[j])
            print("  ---")

    print("\n--- (D) 주변 id 참조 (getElementById / querySelector / addEventListener)")
    if not ids: print("  0건")
    for d in sorted(ids):
        r = [i for i, s in enumerate(L) if d in s]
        print(f"  ## id '{d}': {len(r)}건")
        for i in r[:15]:
            show("D", i, L[i])

    print("\n--- (E) 모달 요소 / 모달 함수 줄")
    e = [i for i, s in enumerate(L) if re.search(r'(id\s*=\s*"[^"]*modal[^"]*"|class\s*=\s*"[^"]*modal|<dialog|role\s*=\s*"dialog"|function\s+\w*[Mm]odal\w*|[Mm]odal\w*\s*=\s*(function|\())', s)]
    if not e: print("  0건")
    for i in e[:60]:
        show("E", i, L[i])

    print("\n--- (F) 인라인 <script> 블록 위치")
    sc = [i for i, s in enumerate(L) if re.search(r'<script|</script>', s)]
    for i in sc:
        show("F", i, L[i])
    print(f"  총 줄 수: {len(L)}")

    js = Path(fd) / "common-snb.js"
    print(f"\n--- (G) {js} 내 '수동 조정' / 'SETT-005' 관련 줄")
    if js.exists():
        J = rd(js)
        g = [i for i, s in enumerate(J) if ("수동 조정" in s or "수동조정" in s)]
        if not g: print("  0건")
        for i in g[:30]:
            show("G", i, J[i])
    else:
        print("  파일 없음")

print("\n\n===== (H) Playwright 런타임 클릭 테스트")
try:
    from playwright.sync_api import sync_playwright
except Exception as ex:
    print(f"  playwright import 실패: {ex}")
    sys.exit(0)

MODAL_JS = """() => [...document.querySelectorAll('[id*="modal" i],[class*="modal" i],dialog,[role="dialog"]')]
 .slice(0,40).map(e=>{const s=getComputedStyle(e);
 return `${e.tagName}#${e.id||'-'} .${(e.className+'').slice(0,60)} display=${s.display} vis=${s.visibility} opacity=${s.opacity} open=${e.open===undefined?'':e.open}`})"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for fd, fp in targets.items():
        print(f"\n### [{fd}] {fp}")
        pg = b.new_page()
        logs = []
        pg.on("console", lambda m, logs=logs: logs.append(f"console.{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda er, logs=logs: logs.append(f"pageerror: {er}"))
        pg.goto(Path(fp).resolve().as_uri())
        pg.wait_for_timeout(1000)
        print(f"  로드 직후 에러/경고: {len(logs)}건")
        for x in logs: print(f"    {x[:CUT]}")
        n0 = len(logs)

        btn = pg.locator("button, a, [onclick], [role=button]", has_text=KEY)
        cnt = btn.count()
        print(f"  버튼 매칭: {cnt}건")
        for k in range(cnt):
            oh = btn.nth(k).evaluate("e=>e.outerHTML")
            print(f"    [{k}] visible={btn.nth(k).is_visible()} {oh[:CUT]}")

        print("  클릭 전 모달 상태:")
        for x in pg.evaluate(MODAL_JS) or ["0건"]: print(f"    {x}")

        if cnt:
            try:
                btn.first.click(timeout=3000)
                pg.wait_for_timeout(700)
                print("  클릭 수행: OK")
            except Exception as ex:
                print(f"  클릭 실패: {str(ex)[:CUT]}")
            print("  클릭 후 모달 상태:")
            for x in pg.evaluate(MODAL_JS) or ["0건"]: print(f"    {x}")
            print(f"  클릭 이후 신규 에러/경고: {len(logs)-n0}건")
            for x in logs[n0:]: print(f"    {x[:CUT]}")
        pg.close()
    b.close()
print("\n[PROBE DONE]")
