# patch_v5_4_answersheet_cleanup.py — 레포 루트에서 실행
# 모든 변경을 메모리에서 계산하고, [ABORT]가 없을 때만 파일에 씀. CRLF 보존.
import re, sys, shutil, subprocess, datetime
from pathlib import Path

ROOT = Path.cwd()
FOLDERS = ["prototype", "prototype_clean"]
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_4_{TS}"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
E2E = ROOT / "scripts" / "qa" / "skill_playwright_e2e.py"
NL = r"\r?\n"

# ANSWERSHEET_SRC_01 4번 실측값 (MASTER_NAV_GROUPS 시작, 끝, renderMasterSnb 시작, 끝) — 양쪽 폴더 동일
DEAD = {
    "ADMN-BOOK-001_baseline.html": (1346, 1398, 1402, 1422),
    "ADMN-PROD-003_baseline.html": (1336, 1388, 1392, 1412),
    "ADMN-PROD-004_baseline.html": (1524, 1576, 1580, 1600),
    "ADMN-PROD-005_baseline.html": (1281, 1333, 1337, 1357),
    "ADMN-PROD-006_baseline.html": (984, 1036, 1040, 1060),
}

changes, warns, log = {}, [], []

def rd(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()

def wr(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

def abort(msg):
    print(f"[ABORT] {msg}\n파일 미변경. 이 로그를 분석 AI에 그대로 전달하세요.")
    sys.exit(2)

def sub1(t, pat, repl, label):
    new, n = re.subn(pat, repl, t, count=1)
    if n == 0:
        abort(f"{label}: 매칭 0건")
    return new

def cut_block(t, s, e):
    """s~e를 줄 단위로 삭제. 바로 윗줄이 '정답지' 주석이면 함께 삭제."""
    ls = t.rfind("\n", 0, s) + 1
    m = re.match(r"[ \t]*\r?\n", t[e:])
    le = e + (m.end() if m else 0)
    if ls > 0:
        ps = t.rfind("\n", 0, ls - 1) + 1
        if re.fullmatch(r"[ \t]*<!--[^\n]*정답지[^\n]*-->[ \t]*\r?", t[ps:ls - 1]):
            ls = ps
    return t[:ls] + t[le:]

# ---------- A. BRD-005 정답지 탭 제거 ----------
def patch_brd005(t, folder):
    tag = f"{folder}/ADMN-BRD-005"
    t = sub1(t, r"(<title>[^<]*무료특강\(빈출문제\))·정답지", r"\1", f"{tag} title")
    t = sub1(t, r'(<h1 id="current-screen-title">[^<]*무료특강\(빈출문제\))·정답지', r"\1", f"{tag} h1")
    t = sub1(t, r"무료특강/빈출문제 및 정답지\(웹 에디터\)를 관리합니다\.",
             "무료특강·빈출문제 등 무료 콘텐츠를 관리합니다.", f"{tag} 설명문")
    t = sub1(t, NL + r'[ \t]*<button[^>]*id="tab-btn-errata"[^>]*>[\s\S]*?</button>', "", f"{tag} 탭 버튼")

    s = t.find('<section id="view-errata"')
    if s < 0: abort(f"{tag} 정답지 섹션 없음")
    e = t.find("</section>", s)
    if e < 0: abort(f"{tag} 정답지 섹션 끝 없음")
    t = cut_block(t, s, e + len("</section>"))

    d = t.find('<div class="modal-backdrop" id="modal-errata">')
    if d < 0: abort(f"{tag} 정답지 모달 없음")
    depth, end = 0, None
    for m in re.finditer(r"<div\b|</div>", t[d:]):
        depth += -1 if m.group() == "</div>" else 1
        if depth == 0:
            end = d + m.end(); break
    if end is None: abort(f"{tag} 모달 div 짝 불일치")
    t = cut_block(t, d, end)

    t = sub1(t, NL + r"[ \t]*// 4\. 정답지 \(ADMN-BRD-009\) - 웹 에디터 본문 포함" + NL
             + r"[ \t]*let ERRATA_LIST = \[[\s\S]*?" + NL + r"[ \t]*\];", "", f"{tag} ERRATA_LIST")
    t = re.sub(NL + r"[ \t]*errata:\s*\[[^\r\n]*\],?[ \t]*(?=\r?\n)", "", t)
    t = sub1(t, NL + r"[ \t]*// 4\. 정답지 \(ADMN-BRD-009\)[ \t]*" + NL
             + r"[ \t]*function renderErrata\(\)[\s\S]*?(?=" + NL + r"[ \t]*// 5\. 신고 렌더링)",
             "", f"{tag} 정답지 함수 묶음")
    t = re.sub(NL + r"[ \t]*renderErrata\(\);?[ \t]*(?=\r?\n)", "", t)

    t, n = re.subn(r"'errata',\s*", "", t)
    if n != 1: abort(f"{tag} ?view= 허용 목록의 'errata' {n}건 (1건이어야 함)")
    KEEP = ("정답지 해설을 반복 회독",)  # 합격수기 더미: 수험생 표현이라 유지
    pat = r"errata|Errata|ERRATA|er-form|er-tbody|er-type|er-keyword|AnswerTable|QuickAnswer|정답지|ANSWER_SHEET|BRD-009"
    left = [f"L{i}: {l.strip()[:110]}" for i, l in enumerate(t.split("\n"), 1)
            if re.search(pat, l) and not any(k in l for k in KEEP)]
    if left:
        abort(f"{tag} 잔여 참조 {len(left)}건\n  " + "\n  ".join(left))
    return t

# ---------- B. SNB 문구·치환표 ----------
def patch_snb(t, folder):
    tag = f"{folder}/common-snb.js"
    t, n = re.subn(r"수강·합격수기 · 무료특강\(빈출\)·정답지", "수강·합격수기 · 무료특강(빈출)", t)
    if n == 0: abort(f"{tag} BRD-005 메뉴명 매칭 0건")
    log.append(f"{tag}: BRD-005 메뉴명 {n}건")
    t, n = re.subn(r"타겟 메시지 발송 · 내역 \(알림톡·문자·메일\)", "타겟 메시지 발송 · 내역", t)
    (log if n else warns).append(f"{tag}: 타겟 메시지 괄호 삭제 {n}건")
    t, n = re.subn(r"내부 정산 조회\s*[-–—]\s*조회 전용", "내부 정산 조회 · 조회 전용", t)
    (log if n else warns).append(f"{tag}: 내부 정산 조회 가운뎃점 {n}건")

    out, dropped = [], []
    for i, l in enumerate(t.split("\n"), 1):
        one_entry = re.fullmatch(r'\s*(\[\s*"[^"]*"\s*,\s*"[^"]*"\s*\]|"[^"]*"\s*:\s*"[^"]*")\s*,?\s*', l)
        if one_entry and ("ANSWER_SHEET" in l or '"ADMN-BRD-009"' in l):
            dropped.append(f"L{i}: {l.strip()}"); continue
        if "ADMN-BRD-005" in l and "·정답지" in l:
            l = l.replace("·정답지", "")
        out.append(l)
    t = "\n".join(out)
    log.append(f"{tag}: 치환표 항목 삭제 {len(dropped)}건 " + " | ".join(dropped))
    rest = [f"L{i}: {l.strip()[:110]}" for i, l in enumerate(t.split("\n"), 1) if "정답지" in l]
    if rest: warns.append(f"{tag}: '정답지' 잔여 {len(rest)}건 → " + " | ".join(rest))
    return t

# ---------- C. 미실행 옛 SNB 코드 삭제 ----------
def patch_dead(t, folder, name):
    a, b, c, d = DEAD[name]
    L = t.split("\n")
    ok = (len(L) >= d and "MASTER_NAV_GROUPS" in L[a - 1] and L[b - 1].strip() == "];"
          and "renderMasterSnb" in L[c - 1] and L[d - 1].strip() in ("}", "};"))
    if not ok:
        warns.append(f"{folder}/{name}: 줄 번호 검증 실패 — 건너뜀"); return None
    del L[c - 1:d]
    del L[a - 1:b]
    L = [l for l in L if not re.fullmatch(r"\s*renderMasterSnb\(\);?\s*", l)]
    rest = [i for i, l in enumerate(L, 1) if "renderMasterSnb" in l or "MASTER_NAV_GROUPS" in l]
    if rest:
        warns.append(f"{folder}/{name}: 잔여 참조 L{rest} — 건너뜀"); return None
    log.append(f"{folder}/{name}: 옛 SNB 코드 삭제")
    return "\n".join(L)

# ---------- D. E2E 검수 폴더 인자 ----------
def patch_e2e(t):
    if "WF_TARGET_DIR" in t:
        warns.append("E2E: 이미 패치됨"); return None
    if "argparse" in t or "sys.argv" in t:
        warns.append("E2E: 기존 인자 처리 있음 — 건너뜀"); return None
    m = re.search(r"^CLEAN_DIR\s*=.*$", t, re.M)
    if not m:
        warns.append("E2E: CLEAN_DIR 줄 없음 — 건너뜀"); return None
    eol = "\r\n" if "\r\n" in t else "\n"
    block = eol.join([
        "", "# v5.4 검수 폴더 인자 — python scripts/qa/skill_playwright_e2e.py prototype  # WF_TARGET_DIR",
        "import sys as _sys, os as _os",
        "if len(_sys.argv) > 1:",
        "    CLEAN_DIR = type(CLEAN_DIR)(_os.path.abspath(_sys.argv[1]))",
    ])
    log.append("E2E: 검수 폴더 인자 지원 추가")
    return t[:m.end()] + block + t[m.end():]

# ---------- 실행 ----------
for f in FOLDERS:
    p = ROOT / f / "ADMN-BRD-005_baseline.html"
    if not p.exists(): abort(f"파일 없음: {p}")
    changes[p] = patch_brd005(rd(p), f)
    s = ROOT / f / "common-snb.js"
    if not s.exists(): abort(f"파일 없음: {s}")
    changes[s] = patch_snb(rd(s), f)
    for name in DEAD:
        q = ROOT / f / name
        if q.exists():
            r = patch_dead(rd(q), f, name)
            if r is not None: changes[q] = r
        else:
            warns.append(f"{f}/{name}: 파일 없음")

if E2E.exists():
    r = patch_e2e(rd(E2E))
    if r is not None: changes[E2E] = r
else:
    warns.append("E2E 스크립트 없음")

for p, s in changes.items():
    dst = BACKUP / p.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    wr(p, s)

for f in FOLDERS:
    src = ROOT / f / "patch_all_snb_v3.html"
    if src.exists():
        dst = ROOT / "_archive" / "legacy" / f / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "mv", str(src), str(dst)], capture_output=True, text=True)
        if r.returncode != 0: shutil.move(str(src), str(dst))
        log.append(f"{f}/patch_all_snb_v3.html → _archive/legacy/{f}/")

if PLAN.exists():
    note = "\n".join([
        "", "### v5.4 정답지 정리 (2026-10-21)",
        "- 정답지는 별도 화면이 아니라 무료 콘텐츠의 한 종류. 운영자가 등록할 때 제목에 \"[정답지]\"를 붙여 구분한다.",
        "- BRD-005 정답지 탭(구 ADMN-BRD-009)·모달·더미·함수 제거, 화면 제목·SNB에서 \"·정답지\" 삭제. ADMN-BRD-009 코드 폐기.",
        "- SNB 문구: \"타겟 메시지 발송 · 내역\" 괄호 삭제, \"내부 정산 조회 · 조회 전용\" 가운뎃점 통일.",
        "- 치환표 ANSWER_SHEET·BRD-009 항목 삭제(docs/ 0건 확인).",
        "- BOOK-001, PROD-003~006 미실행 옛 SNB 코드 삭제. patch_all_snb_v3.html → _archive/legacy/.",
        "- E2E 스크립트 검수 폴더 인자 지원.",
        "- 보류: CONF-005 교재 저작권자 권한의 정답지 문구(white 결정 대기).", "",
    ])
    with open(PLAN, "a", encoding="utf-8", newline="") as fp:
        fp.write(note)

print(f"[OK] 수정 {len(changes)}개 · 백업 {BACKUP.relative_to(ROOT)}")
for l in log: print("  -", l)
for w in warns: print("  [WARN]", w)
