# patch_v61_sett005_autoopen.py — v6.1 SETT-005 ?fromStmt= 자동 오픈 수정
import sys, re, shutil, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

FILES = ["prototype/ADMN-SETT-005_baseline.html",
         "prototype_clean/ADMN-SETT-005_baseline.html"]
MARK = "v6.1 SETT-005"

# (1) openNewAdjModal: v6.0 잠금 해제 줄 바로 아래 open 클래스 부여
P_OPEN = re.compile(r'^([ \t]*)modal\.style\.removeProperty\("display"\); // v6\.0 SETT-005[^\r\n]*(\r?\n)', re.M)
# (2) closeNewAdjModal: 함수 첫 줄에 open 클래스 제거
P_CLOSE = re.compile(r'(function closeNewAdjModal\([^)]*\)\s*\{\r?\n)([ \t]*)')
# 전제 확인: 핫픽스가 open 클래스 보유 백드롭을 예외 처리하는지
P_PRE = re.compile(r"UNIVERSAL-MODAL-CLOSER-HOTFIX")

def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f: f.write(t)

orig, new, errs = {}, {}, []
for fp in FILES:
    if not Path(fp).exists(): errs.append(f"{fp}: 파일 없음"); continue
    t = rd(fp); orig[fp] = t
    if MARK in t: errs.append(f"{fp}: 이미 적용됨({MARK})"); continue
    no, nc, npre = len(P_OPEN.findall(t)), len(P_CLOSE.findall(t)), len(P_PRE.findall(t))
    print(f"[{fp}] open 앵커 {no}건 / close 앵커 {nc}건 / 핫픽스 마커 {npre}건 (기대 1/1/≥1)")
    if no != 1 or nc != 1 or npre < 1:
        errs.append(f"{fp}: 앵커 불일치 OPEN={no} CLOSE={nc} PRE={npre}")
        for i, s in enumerate(t.split("\n")):
            if "closeNewAdjModal" in s and ("function" in s or "=" in s):
                print(f"    참고 L{i+1}: {s.rstrip()[:300]}")
        continue
    t2 = P_OPEN.sub(lambda m: m.group(0)
        + f'{m.group(1)}modal.classList.add("open"); // {MARK}: 공통 핫픽스 로드 시점 잠금 예외 대상{m.group(2)}', t, count=1)
    t2 = P_CLOSE.sub(lambda m: m.group(1) + m.group(2)
        + f'document.getElementById("newAdjModal").classList.remove("open"); // {MARK}\n'.replace("\n", "\r\n" if "\r\n" in m.group(1) else "\n")
        + m.group(2), t2, count=1)
    new[fp] = t2

if errs:
    for e in errs: print(f"[ABORT] {e}")
    print("[ABORT] 파일 미변경"); sys.exit(1)

bk = Path(f"_archive/backup/v6.1_{datetime.datetime.now():%Y%m%d_%H%M%S}")
for fp in FILES:
    d = bk / Path(fp).parent; d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fp, d / Path(fp).name)
print(f"[BACKUP] {bk}")
for fp, t in new.items(): wr(fp, t); print(f"[SAVED] {fp}")

def rollback(msg):
    for fp, t in orig.items(): wr(fp, t)
    print(f"[ABORT][ROLLBACK] {msg} → 원본 복원 완료"); sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
except Exception as ex:
    rollback(f"playwright import 실패: {ex}")

DISP = "() => getComputedStyle(document.getElementById('newAdjModal')).display"
fail = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for fp in FILES:
        uri = Path(fp).resolve().as_uri()
        print(f"\n### 검증 [{fp}]")
        def page(url):
            pg = b.new_page(); pe = []
            pg.on("pageerror", lambda er: pe.append(str(er)))
            pg.goto(url); pg.wait_for_timeout(900); return pg, pe
        def check(label, got, want):
            ok = got == want
            print(f"  {'PASS' if ok else 'FAIL'} {label}: display={got} (기대 {want})")
            if not ok: fail.append(f"{fp} {label}")
        def cancel(pg):
            c = pg.locator("#newAdjModal button", has_text="취소")
            if c.count(): c.first.click(); pg.wait_for_timeout(400); return True
            return False

        pg, pe = page(uri)
        pg.locator("button[onclick='openNewAdjModal()']").first.click(); pg.wait_for_timeout(500)
        check("T1 카드 버튼 열기", pg.evaluate(DISP), "flex")
        pg.evaluate("closeNewAdjModal()"); pg.wait_for_timeout(300)
        check("T2 closeNewAdjModal() 닫기", pg.evaluate(DISP), "none")
        pg.locator("#btnOpenNewAdjModal").click(); pg.wait_for_timeout(500)
        check("T3 상단 버튼 재열기", pg.evaluate(DISP), "flex")
        if cancel(pg): check("T4 취소 버튼 닫기", pg.evaluate(DISP), "none")
        else: print("  SKIP T4 취소 버튼 0건")
        if pe: fail.append(f"{fp} pageerror"); [print(f"    pageerror {x[:300]}") for x in pe]
        pg.close()

        pg, pe = page(uri)
        pg.locator("#btnOpenNewAdjModal").click(); pg.wait_for_timeout(500)
        check("T5 새로고침 직후 상단 버튼 열기", pg.evaluate(DISP), "flex")
        pg.close()

        pg, pe = page(uri + "?fromStmt=STMT-TEST01")
        pg.wait_for_timeout(1100)
        check("T6 ?fromStmt= 진입 자동 오픈(2초 시점)", pg.evaluate(DISP), "flex")
        if cancel(pg): check("T7 자동 오픈 후 취소 닫기", pg.evaluate(DISP), "none")
        else: print("  SKIP T7 취소 버튼 0건")
        if pe: fail.append(f"{fp} pageerror(T6)"); [print(f"    pageerror {x[:300]}") for x in pe]
        pg.close()
    b.close()

if fail: rollback("검증 실패: " + ", ".join(fail))
print("\n[OK] v6.1 SETT-005 자동 오픈 수정 완료 (2파일)")
