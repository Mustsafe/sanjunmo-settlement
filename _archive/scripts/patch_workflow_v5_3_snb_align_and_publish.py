# -*- coding: utf-8 -*-
"""
patch_workflow_v5_3_snb_align_and_publish.py  (레포 루트에서 실행)
A) 업무플로우(clean) 상시 감사 블록: 두 노드의 제목·결과 문구를 구분 + 노드 최소 폭
B) prototype/common-snb.js 의 SNB_GROUPS 배열만 clean 배열로 교체 (나머지 줄 유지)
C) prototype/ · prototype_clean/ *.html 의 crumb-group 텍스트 = 해당 화면의 SNB 그룹명
D) 6단계: prototype_clean/00_WORKFLOW_GUIDE → prototype/ 덮어쓰기
E) 플랜 결정 로그
B·C 오류 시 전체 중단(파일 미변경). A·D는 실패 시 해당 항목만 [WARN] 후 건너뜀.
"""
import re, sys, shutil, datetime
from pathlib import Path

ROOT = Path.cwd()
CLEAN, PROTO = ROOT / "prototype_clean", ROOT / "prototype"
WFN = "00_WORKFLOW_GUIDE_baseline.html"
WF = CLEAN / WFN
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
SKIP_HTML = {WFN, "patch_all_snb_v3.html"}
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_3_{TS}"

pending, errors, warns, log = {}, [], [], []
def read(p):
    with p.open(encoding="utf-8", newline="") as f: return f.read()
def write(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f: f.write(t)
def cur(p): return pending[p] if p in pending else read(p)
def fail(m): errors.append(m); print("[ERROR]", m)
def warn(m): warns.append(m); print("[WARN]", m)

for p in [WF, CLEAN / "common-snb.js", PROTO / "common-snb.js", PLAN]:
    if not p.exists(): print(f"[ERROR] 필수 파일 없음: {p}"); sys.exit(2)

# ---------- A) 상시 감사 블록 ----------
wf = read(WF)
i = wf.find('class="wf-sub is-always"')
if i < 0:
    warn("[A] 상시 감사 블록(.wf-sub.is-always) 미검출 → 건너뜀")
else:
    end = wf.find("</section>", i)
    end = end if end > 0 else len(wf)
    blk = wf[i:end]
    EDITS = [
        ("ADMN-CONF-010_baseline.html", "정산 변경 기록 확인", None),
        ("ADMN-CONF-005_baseline.html?view=ADMN-CONF-006", "열람·권한 기록 확인", "마스킹 해제·권한 변경 이력"),
    ]
    for href, do, out in EDITS:
        m = re.search(r'<a\b[^>]*href="' + re.escape(href) + r'"[^>]*>.*?</a>', blk, re.S)
        if not m: warn(f"[A] {href} 노드 미검출 → 건너뜀"); continue
        a = m.group(0)
        a2, n1 = re.subn(r'(wf-node-do">)[^<]*(<)', lambda x: x.group(1) + do + x.group(2), a, count=1)
        n2 = 1
        if out:
            a2, n2 = re.subn(r'(wf-node-out">)[^<]*(<)', lambda x: x.group(1) + out + x.group(2), a2, count=1)
        if n1 != 1 or n2 != 1: warn(f"[A] {href} 문구 영역 미검출 → 건너뜀"); continue
        blk = blk.replace(a, a2, 1)
        log.append(f"[A] {href}: 제목 '{do}'" + (f", 결과 '{out}'" if out else ""))
    wf = wf[:i] + blk + wf[end:]
    if 'id="wf-v53-fix"' not in wf:
        bi = wf.rfind("</body>")
        if bi < 0: warn("[A] </body> 미검출 → CSS 주입 건너뜀")
        else:
            wf = wf[:bi] + '<style id="wf-v53-fix">\n#wf-root .wf-sub.is-always .wf-node{min-width:260px}\n</style>\n' + wf[bi:]
            log.append("[A] 상시 감사 노드 최소 폭 260px")
    pending[WF] = wf

# ---------- B) prototype SNB_GROUPS 교체 ----------
def bounds(lines):
    s = [k for k, l in enumerate(lines) if re.match(r'\s*(const|let|var)\s+SNB_GROUPS\s*=\s*\[', l)]
    if len(s) != 1: return None
    for k in range(s[0] + 1, len(lines)):
        if lines[k].strip() == "];": return s[0], k
    return None
def keys(blk): return set(re.findall(r'\b([A-Za-z_]\w*)\s*:', "".join(blk)))
def groups(blk):
    h2g, titles, g = {}, [], None
    for line in blk:
        if re.search(r'\bcode:\s*"', line):
            h = re.search(r'href:\s*"([^"?#]+)', line)
            if g and h: h2g.setdefault(h.group(1), g)
            continue
        m = re.search(r'\b(?:title|group|groupTitle|name|heading|label)\s*:\s*"([^"]+)"', line)
        if m: g = m.group(1); titles.append(g)
    return titles, h2g

cl = read(CLEAN / "common-snb.js").splitlines(True)
pl = read(PROTO / "common-snb.js").splitlines(True)
bc, bp = bounds(cl), bounds(pl)
href2group = {}
if not bc or not bp:
    fail(f"SNB_GROUPS 범위 미검출 (clean={bc}, prototype={bp})")
else:
    cblk, pblk = cl[bc[0]:bc[1] + 1], pl[bp[0]:bp[1] + 1]
    if keys(cblk) != keys(pblk):
        fail(f"SNB_GROUPS 키 구조 불일치 → clean에만: {keys(cblk)-keys(pblk)} / prototype에만: {keys(pblk)-keys(cblk)}")
    titles, href2group = groups(cblk)
    if len(titles) != 9 or any("단계" in t for t in titles):
        fail(f"clean 그룹 제목 이상: {titles}")
    if not errors:
        newp = "".join(pl[:bp[0]] + cblk + pl[bp[1] + 1:])
        if newp != "".join(pl):
            pending[PROTO / "common-snb.js"] = newp
            log.append(f"[B] prototype SNB_GROUPS L{bp[0]+1}~{bp[1]+1} → clean 배열 (메뉴 {''.join(cblk).count('code:')}개, 그룹 {len(titles)}개)")
        else:
            log.append("[B] prototype SNB_GROUPS 이미 동일 → SKIP")

# ---------- C) 브레드크럼 ----------
CR = re.compile(r'(<(\w+)\b[^>]*class="[^"]*\bcrumb-group\b[^"]*"[^>]*>)(.*?)(</\2\s*>)', re.S)
if href2group:
    for folder in [PROTO, CLEAN]:
        for html in sorted(folder.glob("*.html")):
            if html.name in SKIP_HTML: continue
            t = cur(html); ms = list(CR.finditer(t))
            if not ms: continue
            g = href2group.get(html.name)
            if not g: warn(f"[C] {folder.name}/{html.name}: SNB에 없는 화면 → 유지"); continue
            out, last, ch = [], 0, False
            for m in ms:
                inner = m.group(3)
                if "<" in inner:
                    warn(f"[C] {folder.name}/{html.name}: crumb-group 안에 태그 → 유지. 원문: {inner.strip()[:200]}"); continue
                s = inner.strip()
                if s == g: continue
                lead, trail = inner[:len(inner) - len(inner.lstrip())], inner[len(inner.rstrip()):]
                out += [t[last:m.start(3)], lead + g + trail]; last = m.end(3); ch = True
                log.append(f"[C] {folder.name}/{html.name}: '{s}' → '{g}'")
            if ch: out.append(t[last:]); pending[html] = "".join(out)

# ---------- D) 6단계 덮어쓰기 ----------
wf_new = cur(WF)
missing = []
for r in set(re.findall(r'(?:src|href)="([^"]+)"', wf_new)):
    if re.match(r'(https?:|#|javascript:|data:|mailto:)', r) or "${" in r: continue
    base = r.split("?")[0].split("#")[0]
    if base and not (PROTO / base).exists(): missing.append(base)
if missing:
    warn(f"[D] prototype/에 없는 참조 파일 {sorted(set(missing))} → 덮어쓰기 건너뜀")
else:
    pending[PROTO / WFN] = wf_new
    log.append("[D] prototype/00_WORKFLOW_GUIDE_baseline.html ← clean 덮어쓰기")

# ---------- E) 플랜 ----------
plan = read(PLAN); MARK = "### v5.3 SNB 정렬·덮어쓰기 (2026-10-21)"
if MARK not in plan:
    pending[PLAN] = plan.rstrip() + f"""

{MARK}
- 상시 감사 블록 두 노드 구분: CONF-010 '정산 변경 기록 확인' / CONF-005 보안 감사로그 탭 '열람·권한 기록 확인'(마스킹 해제·권한 변경 이력)
- SNB는 두 폴더 동일 원칙: prototype/common-snb.js SNB_GROUPS 배열만 clean 기준으로 교체 (prototype 쪽은 치환표 없음, 나머지 줄 유지)
- 브레드크럼(crumb-group) = 화면이 속한 SNB 그룹명, 두 폴더 공통
- 6단계 완료: prototype/00_WORKFLOW_GUIDE_baseline.html = clean본 (이 페이지 한정 예외)
- 회원·수강 노드의 USER-003 라벨 3회 반복은 제목이 달라 유지
- 다음 과제: 정답지 정리 패치(BRD-005 정답지 탭·제목·SNB명, BRD-009 매핑, CONF-005 권한 문구·'정답지 등록' 배지), CONF-005 탭명 괄호 중복, 옛 groupTitle 잔재(BOOK-001·PROD-003~006·patch_all_snb_v3.html)
"""

# ---------- 저장 ----------
print("\n".join(log))
if errors:
    print(f"\n[ABORT] 오류 {len(errors)}건. 파일 미변경. 로그를 분석 AI에 반환하세요."); sys.exit(2)
for p in pending:
    if p == PLAN or not p.exists(): continue
    dst = BACKUP / p.relative_to(ROOT); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, dst)
for p, t in pending.items(): write(p, t)
print(f"\n[DONE] {len(pending)}개 파일 저장 · 경고 {len(warns)}건 · 백업: {BACKUP}")
