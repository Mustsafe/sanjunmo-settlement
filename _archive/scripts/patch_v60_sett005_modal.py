# patch_v60_sett005_modal.py — v6.0 SETT-005 신규 수동 조정 모달 표시 수정
import sys, re, shutil, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

FILES = ["prototype/ADMN-SETT-005_baseline.html",
         "prototype_clean/ADMN-SETT-005_baseline.html"]
MARK = "v6.0 SETT-005"

# (1) CSS: .hidden 규칙 바로 아래에 ID 우선 표시 규칙 추가
P_CSS = re.compile(r'^([ \t]*)\.hidden \{ display: none !important; \}(\r?\n)', re.M)
# (2) openNewAdjModal: hidden 제거 직후 인라인 display 잠금 해제
P_OPEN = re.compile(r'(const modal = document\.getElementById\("newAdjModal"\);\r?\n([ \t]*)modal\.classList\.remove\("hidden"\);)(\r?\n)')

def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)

orig, new, errs = {}, {}, []
for fp in FILES:
    if not Path(fp).exists():
        errs.append(f"{fp}: 파일 없음"); continue
    t = rd(fp); orig[fp] = t
    if MARK in t:
        errs.append(f"{fp}: 이미 적용됨({MARK})"); continue
    nc, no = len(P_CSS.findall(t)), len(P_OPEN.findall(t))
    print(f"[{fp}] CSS 앵커 {nc}건 / open 앵커 {no}건 (기대 1/1)")
    if nc != 1 or no != 1:
        errs.append(f"{fp}: 앵커 건수 불일치 CSS={nc} OPEN={no}"); continue
    t2 = P_CSS.sub(lambda m: m.group(0)
                   + f"{m.group(1)}/* {MARK}: 공통 모달 숨김 규칙보다 우선해 신규 조정 모달 표시 */{m.group(2)}"
                   + f"{m.group(1)}#newAdjModal.modal-backdrop:not(.hidden) {{ display: flex !important; }}{m.group(2)}",
                   t, count=1)
    t2 = P_OPEN.sub(lambda m: m.group(1) + m.group(3)
                    + f'{m.group(2)}modal.style.removeProperty("display"); // {MARK}: 공통 모달 인라인 잠금 해제'
                    + m.group(3),
                    t2, count=1)
    new[fp] = t2

if errs:
    for e in errs: print(f"[ABORT] {e}")
    print("[ABORT] 파일 미변경")
    sys.exit(1)

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bk = Path(f"_archive/backup/v6.0_{stamp}")
for fp in FILES:
    d = bk / Path(fp).parent; d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fp, d / Path(fp).name)
print(f"[BACKUP] {bk}")
for fp, t in new.items():
    wr(fp, t)
    print(f"[SAVED] {fp}")

# ---- 저장 후 런타임 검증 (실패 시 자동 롤백) ----
def rollback(msg):
    for fp, t in orig.items(): wr(fp, t)
    print(f"[ABORT][ROLLBACK] {msg} → 원본 복원 완료")
    sys.exit(1)

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
            pg = b.new_page(); errs_ = []
            pg.on("pageerror", lambda er: errs_.append(str(er)))
            pg.goto(url); pg.wait_for_timeout(900)
            return pg, errs_

        def check(label, got, want, gate=True):
            ok = (got == want)
            print(f"  {'PASS' if ok else ('FAIL' if gate else 'INFO')} {label}: display={got} (기대 {want})")
            if gate and not ok: fail.append(f"{fp} {label}")

        pg, pe = page(uri)
        pg.locator("button[onclick='openNewAdjModal()']").first.click(); pg.wait_for_timeout(500)
        check("T1 카드 버튼 열기", pg.evaluate(DISP), "flex")
        pg.evaluate("closeNewAdjModal()"); pg.wait_for_timeout(300)
        check("T2 closeNewAdjModal() 닫기", pg.evaluate(DISP), "none")
        pg.locator("#btnOpenNewAdjModal").click(); pg.wait_for_timeout(500)
        check("T3 닫은 뒤 상단 버튼 재열기", pg.evaluate(DISP), "flex")
        cancel = pg.locator("#newAdjModal button", has_text="취소")
        if cancel.count():
            cancel.first.click(); pg.wait_for_timeout(400)
            check("T4 모달 내 취소 버튼 닫기", pg.evaluate(DISP), "none")
        else:
            print("  SKIP T4 취소 버튼 0건")
        print(f"  pageerror {len(pe)}건"); [print(f"    {x[:300]}") for x in pe]
        if pe: fail.append(f"{fp} pageerror")
        pg.close()

        pg, pe = page(uri)
        pg.locator("#btnOpenNewAdjModal").click(); pg.wait_for_timeout(500)
        check("T5 새로고침 직후 상단 버튼 열기", pg.evaluate(DISP), "flex")
        pg.close()

        pg, pe = page(uri + "?fromStmt=PROBE")
        check("T6 ?fromStmt= 진입 자동 오픈(참고)", pg.evaluate(DISP), "flex", gate=False)
        pg.close()
    b.close()

if fail:
    rollback("검증 실패: " + ", ".join(fail))
print("\n[OK] v6.0 SETT-005 모달 표시 수정 완료 (2파일)")
