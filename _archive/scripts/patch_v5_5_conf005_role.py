# patch_v5_5_conf005_role.py — 레포 루트에서 실행
# CONF-005 교재 저작권자 권한에서 정답지 문구 제거 + E2E 스크립트 LF 복원
# 모든 변경을 메모리에서 계산 후 [ABORT] 없을 때만 기록. 원래 줄바꿈 보존.
import re, sys, shutil, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.cwd()
FOLDERS = ["prototype", "prototype_clean"]
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_5_{TS}"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
E2E = ROOT / "scripts" / "qa" / "skill_playwright_e2e.py"

# (라벨, 패턴, 치환) — 긴 문구부터 순서대로
RULES = [
    ("역할 카드 항목", r"\s*[,·/]\s*정답지\((?:<code>)?ADMN-BRD-009(?:</code>)?\)\s*등록·수정", ""),
    ("역할 카드 항목(앞)", r"정답지\((?:<code>)?ADMN-BRD-009(?:</code>)?\)\s*등록·수정\s*[,·/]?\s*", ""),
    ("권한표 행 이름", r"학습 Q&amp;A / 정답지 \(BRD\)", "학습 Q&amp;A (BRD)"),
    ("권한표 행 이름(raw)", r"학습 Q&A / 정답지 \(BRD\)", "학습 Q&A (BRD)"),
    ("권한표 저작권자 칸", r"<strong>✓ 본인 정답지 등록</strong>", "✕ 접근불가"),
    ("자동 범위", r"도서 인세 정산서 및 정답지 관리 전용", "도서 인세 정산서 열람 전용"),
    ("역할 옵션", r"도서 인세 정산서 및 정답지 관리", "도서 인세 정산서 열람"),
    ("계정 샘플 범위", r"정답지\s*ADMN-BRD-009\s*전용", "도서 인세 정산서 전용"),
    ("감사 로그 유형", r"(type:\s*['\"])정답지 등록(['\"])", r"\1정산서 열람\2"),
    ("감사 로그 내용", r"정답지\(ANSWER_SHEET\)\s*웹 에디터 수정", "도서 인세 정산서 PDF 다운로드"),
]
RESIDUE = re.compile(r"정답지|ANSWER_SHEET|BRD-009")

changes, log, warns = {}, [], []

def rd(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()

def wr(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

def abort(msg):
    print(f"[ABORT] {msg}\n파일 미변경. 이 출력 전문을 분석 AI에 그대로 전달하세요.")
    sys.exit(2)

# ---------- A. CONF-005 ----------
for f in FOLDERS:
    p = ROOT / f / "ADMN-CONF-005_baseline.html"
    if not p.exists():
        abort(f"파일 없음: {p}")
    t = rd(p)
    before = [(i, l.strip()[:120]) for i, l in enumerate(t.split("\n"), 1) if RESIDUE.search(l)]
    log.append(f"{f}/CONF-005: 대상 줄 {len(before)}건 " + " | ".join(f"L{i}" for i, _ in before))
    total = 0
    for label, pat, rep in RULES:
        t, n = re.subn(pat, rep, t)
        if n:
            log.append(f"  {f} · {label}: {n}건")
            total += n
    left = [f"L{i}: {l.strip()[:140]}" for i, l in enumerate(t.split("\n"), 1) if RESIDUE.search(l)]
    if left:
        abort(f"{f}/CONF-005 잔여 {len(left)}건\n  " + "\n  ".join(left))
    if total == 0:
        warns.append(f"{f}/CONF-005: 변경 0건 (이미 정리됨?)")
    else:
        changes[p] = t

# ---------- B. E2E 스크립트 LF 복원 ----------
if E2E.exists():
    s = rd(E2E)
    if "\r\n" in s:
        changes[E2E] = s.replace("\r\n", "\n")
        log.append("E2E: CRLF → LF 복원")
    else:
        warns.append("E2E: 이미 LF")
else:
    warns.append("E2E 스크립트 없음")

# ---------- 기록 ----------
for p, s in changes.items():
    dst = BACKUP / p.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    wr(p, s)

if PLAN.exists() and changes:
    note = "\n".join([
        "", "### v5.5 CONF-005 교재 저작권자 권한 정리 (2026-10-21)",
        "- 정답지는 운영자가 등록하는 무료 콘텐츠이므로 교재 저작권자(ROLE_PARTNER_COPYRIGHT)의 정답지 등록·수정 권한 삭제.",
        "- 저작권자 파트너 권한은 도서 인세 정산서 열람으로 한정. 권한표 BRD 칸 '✕ 접근불가'.",
        "- E2E 스크립트 줄바꿈 LF 복원(v5.4 저장 과정에서 CRLF로 바뀜).", "",
    ])
    with open(PLAN, "a", encoding="utf-8", newline="") as fp:
        fp.write(note)

print(f"[OK] 수정 {len(changes)}개 · 백업 {BACKUP.relative_to(ROOT)}")
for l in log: print("  -", l)
for w in warns: print("  [WARN]", w)
