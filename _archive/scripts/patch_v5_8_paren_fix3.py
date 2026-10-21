import sys, os, shutil, datetime
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = os.path.join(ROOT, "_archive", "backup", f"v5_8_{TS}")

PATCHES = {
    "prototype_clean/ADMN-BOOK-001_baseline.html": [
        ("<code>book_supply_type</code>(공급 형태)을 사후 변경",
         "<code>book_supply_type</code>를 사후 변경"),
    ],
    "prototype_clean/ADMN-ORD-001_baseline.html": [
        ("<code>ROYALTY_BOOK(인세도서)</code>",
         "<code>ROYALTY_BOOK</code>"),
        (">도서 인세 도서 인세 (+1권)<",
         ">도서 인세 (+1권)<"),
    ],
}

PLAN = ".antigravity/WORKFLOW_REDESIGN_PLAN.md"
PLAN_NOTE = (
    "\n### v5.8 괄호 중복 마무리\n"
    "- BOOK-001: <code>book_supply_type</code>(공급 형태)을 → <code>book_supply_type</code>를\n"
    "- ORD-001: <code>ROYALTY_BOOK(인세도서)</code> → <code>ROYALTY_BOOK</code>\n"
    "- ORD-001: '도서 인세 도서 인세 (+1권)' → '도서 인세 (+1권)' (원 문구 미확인, 판단값)\n"
    "- 잔여: SETT-006 '플랫폼 보전금(120만원)'은 금액 표기로 유지\n"
    "- prototype/ 은 기획 검수용 기준에 따라 미수정\n"
)

def read(p):
    with open(os.path.join(ROOT, p), "r", encoding="utf-8", newline="") as f:
        return f.read()

def write(p, t):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(t)

errors, results = [], {}
for path, rules in PATCHES.items():
    if not os.path.exists(os.path.join(ROOT, path)):
        errors.append(f"{path}: 파일 없음")
        continue
    t = read(path)
    for old, new in rules:
        n = t.count(old)
        if n != 1:
            errors.append(f"{path}: 대상 {n}건 (기대 1건) → {old}")
            continue
        t = t.replace(old, new)
    results[path] = t

if not os.path.exists(os.path.join(ROOT, PLAN)):
    errors.append(f"{PLAN}: 파일 없음")

if errors:
    print("[ABORT]")
    for e in errors:
        print("  " + e)
    print("파일 미변경. 이 출력 전문을 분석 AI에 그대로 전달하세요.")
    sys.exit(1)

for path in list(results) + [PLAN]:
    dst = os.path.join(BACKUP, path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(ROOT, path), dst)

for path, t in results.items():
    write(path, t)

plan = read(PLAN)
nl = "\r\n" if "\r\n" in plan else "\n"
write(PLAN, plan.rstrip("\r\n") + nl + PLAN_NOTE.replace("\n", nl))

print(f"[OK] 수정 {len(results)}개 파일 · 치환 3건 · 플랜 노트 추가 · 백업 {os.path.relpath(BACKUP, ROOT)}")
