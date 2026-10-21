# probe_v61_sett005_entry.py — 읽기 전용 진단 (파일 수정 없음)
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CUT = 400

def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read().split("\n")

def show(tag, i, s):
    s = s.rstrip("\r")
    print(f"  [{tag}] L{i+1}: {s[:CUT]}{' …(trunc)' if len(s) > CUT else ''}")

hrefs = {}
for fd in ["prototype", "prototype_clean"]:
    s5, s2 = Path(fd) / "ADMN-SETT-005_baseline.html", Path(fd) / "ADMN-SETT-002_baseline.html"
    print(f"\n===== [{fd}]")

    L = rd(s5)
    print(f"--- (A) {s5} URL 파라미터 처리 줄 (+이후 25줄)")
    a = [i for i, s in enumerate(L) if re.search(r'URLSearchParams|location\.search|location\.hash|sessionStorage|localStorage', s)]
    if not a: print("  0건")
    for i in a:
        for j in range(i, min(len(L), i + 26)): show("A", j, L[j])
        print("  ---")

    L2 = rd(s2)
    print(f"--- (B) {s2} 에서 SETT-005 이동 줄 (±3줄)")
    b = [i for i, s in enumerate(L2) if "SETT-005" in s and re.search(r'href|location|open\(|navigate|go\w*\(', s)]
    if not b: print("  0건")
    for i in b:
        for j in range(max(0, i - 3), min(len(L2), i + 4)): show("B", j, L2[j])
        print("  ---")
        for m in re.findall(r"ADMN-SETT-005_baseline\.html[^'\"`\s)]*", L2[i]):
            hrefs.setdefault(fd, []).append(m)
    print(f"  추출 URL: {hrefs.get(fd) or '0건'}")

print("\n===== (C) Playwright: 추출 URL로 직접 진입 시 newAdjModal 상태")
from playwright.sync_api import sync_playwright
DETAIL = """() => { const m = document.getElementById('newAdjModal'); if (!m) return 'newAdjModal 없음';
  return `class="${m.className}" style="${m.getAttribute('style')||''}" computed=${getComputedStyle(m).display}`; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for fd, urls in hrefs.items():
        for u in sorted(set(urls)):
            if "?" not in u and "#" not in u:
                print(f"  [{fd}] {u} → 파라미터 없음, SKIP"); continue
            base = (Path(fd) / "ADMN-SETT-005_baseline.html").resolve().as_uri()
            full = base + u[len("ADMN-SETT-005_baseline.html"):]
            full = re.sub(r"\$\{[^}]*\}|'\s*\+.*$", "TEST01", full)
            pg = b.new_page(); errs = []
            pg.on("pageerror", lambda er: errs.append(str(er)))
            pg.goto(full)
            for t in (300, 1000, 2000):
                pg.wait_for_timeout(t if t == 300 else t - (300 if t == 1000 else 1000))
                print(f"  [{fd}] {full.split('/')[-1]} @{t}ms: {pg.evaluate(DETAIL)}")
            print(f"  pageerror {len(errs)}건"); [print(f"    {x[:300]}") for x in errs]
            pg.close()
    b.close()
print("\n[PROBE v6.1 DONE]")
