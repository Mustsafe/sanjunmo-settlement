# -*- coding: utf-8 -*-
"""
patch_workflow_v5_1_snb_breadcrumb.py  (레포 루트에서 실행)
1) prototype/ · prototype_clean/ common-snb.js : 중복 메뉴 2줄 제거
   - CONF-006 메뉴 항목 (CONF-005 보안 감사로그 탭과 같은 화면)
   - USER-007 '회원 · 수강 관리' 그룹 항목 ("파기" 포함 줄) → 보안 그룹 항목만 유지
   - 문구 치환표 ([...] 튜플 줄)는 건드리지 않음
2) prototype_clean/00_WORKFLOW_GUIDE : CONF-005 라벨 교체, 상시 감사 블록에 보안 감사로그 탭 링크 추가,
   디렉터리 카드 열 배치 + 화면 코드 줄바꿈 금지
3) prototype_clean/*.html : 브레드크럼 옛 단계명(0~4단계 ·) → 해당 화면의 SNB 그룹명
4) 리포트 .antigravity/reports/WORKFLOW_MARKUP_V5_DUMP.md (다음 레이아웃 패치용, 읽기 전용)
5) 플랜 파일 결정 로그 추가
모든 변경은 메모리에서 계산·검증 후 일괄 저장. 오류 1건이라도 있으면 어떤 파일도 쓰지 않음.
"""
import re, sys, shutil, datetime
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path.cwd()
CLEAN = ROOT / "prototype_clean"
PROTO = ROOT / "prototype"
WF = CLEAN / "00_WORKFLOW_GUIDE_baseline.html"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
DUMP = ROOT / ".antigravity" / "reports" / "WORKFLOW_MARKUP_V5_DUMP.md"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_1_{TS}"

EXPECTED_GROUPS = [
    "대시보드 · 통계", "회원 · 수강 관리", "주문 · 환불 · CS · 프로모션",
    "상품 · 강좌 · 교재 관리", "권리자 계약 · 지분 매핑", "정산 마감 전 사전 대사",
    "월간 정산 · 지급 · 조회", "개인정보 · 보안 감사", "사이트 · 약관 · 메시지 설정",
]
CONF005_LABEL = "운영자 계정 · 역할 권한(RBAC)"
AUDIT_TAB_HREF = "ADMN-CONF-005_baseline.html?view=ADMN-CONF-006"
AUDIT_TAB_NAME = "개인정보 열람 및 보안 감사로그"

pending = {}   # Path -> new text
errors, log = [], []

def norm(s): return re.sub(r"\s+", "", s)
def fail(msg): errors.append(msg); print("[ERROR]", msg)
def read(p):
    with p.open(encoding="utf-8", newline="") as f: return f.read()
def write(p, t):
    with p.open("w", encoding="utf-8", newline="") as f: f.write(t)
def cur(p): return pending.get(p) if p in pending else read(p)

for p in [CLEAN / "common-snb.js", WF, PLAN]:
    if not p.exists():
        print(f"[ERROR] 필수 파일 없음: {p}"); sys.exit(2)

# ---------- 1) SNB 중복 메뉴 제거 ----------
CONF006_RE = re.compile(r'^[ \t]*\{\s*code:\s*"CONF-006"[^\n]*\}[ \t]*,?[ \t]*\r?\n', re.M)
USER007_DUP_RE = re.compile(r'^[ \t]*\{\s*code:\s*"USER-007"[^\n]*파기[^\n]*\}[ \t]*,?[ \t]*\r?\n', re.M)

for snb in [CLEAN / "common-snb.js", PROTO / "common-snb.js"]:
    if not snb.exists():
        print(f"[SKIP] {snb} 없음"); continue
    t = read(snb); name = f"{snb.parent.name}/{snb.name}"
    n1 = len(CONF006_RE.findall(t)); n2 = len(USER007_DUP_RE.findall(t))
    if n1 != 1: fail(f"{name}: CONF-006 메뉴 항목 {n1}건 (1건이어야 함)")
    if n2 != 1: fail(f"{name}: USER-007 '파기' 메뉴 항목 {n2}건 (1건이어야 함)")
    if n1 == 1 and n2 == 1:
        t2 = USER007_DUP_RE.sub("", CONF006_RE.sub("", t, 1), 1)
        left = len(re.findall(r'\{\s*code:\s*"USER-007"', t2))
        if left != 1: fail(f"{name}: 제거 후 USER-007 메뉴 {left}건 (보안 그룹 1건만 남아야 함)")
        else:
            pending[snb] = t2; log.append(f"[SNB] {name}: CONF-006 1줄, USER-007(회원 그룹) 1줄 제거")

# ---------- SNB 그룹 매핑 (clean 원본 기준) ----------
def parse_groups(js):
    href2group, titles, cur_g = {}, [], None
    for line in js.splitlines():
        if re.search(r'\bcode:\s*"', line):
            h = re.search(r'href:\s*"([^"?#]+)', line)
            if cur_g and h and h.group(1) not in href2group:
                href2group[h.group(1)] = cur_g
            continue
        m = re.search(r'\b(?:title|group|groupTitle|name|heading|label)\s*:\s*"([^"]+)"', line)
        if m: cur_g = m.group(1); titles.append(cur_g)
    return titles, href2group

titles, href2group = parse_groups(read(CLEAN / "common-snb.js"))
found = {norm(x) for x in titles}
missing = [g for g in EXPECTED_GROUPS if norm(g) not in found]
if missing:
    fail(f"common-snb.js에서 SNB 그룹명 미검출: {missing} / 검출된 제목: {titles[:30]}")
expected_norm = {norm(g) for g in EXPECTED_GROUPS}

# ---------- 2) 업무플로우 페이지 보정 ----------
wf = read(WF)
ri = wf.find('id="wf-root"')
if ri < 0:
    fail("업무플로우: id=\"wf-root\" 미검출")
else:
    head, seg = wf[:ri], wf[ri:]
    # 2-1 CONF-005 라벨
    lab_re = re.compile(r'>(\s*)권한 관리(\s*)<')
    n = len(lab_re.findall(seg))
    if n == 0: fail("업무플로우: CONF-005 라벨 '권한 관리' 텍스트 노드 미검출")
    else:
        seg = lab_re.sub(lambda m: f">{m.group(1)}{CONF005_LABEL}{m.group(2)}<", seg)
        log.append(f"[WF] CONF-005 라벨 교체 {n}건")
    # 2-2 상시 감사 블록에 보안 감사로그 탭 링크
    if "view=ADMN-CONF-006" in seg:
        log.append("[WF] 보안 감사로그 탭 링크 이미 있음 → SKIP")
    else:
        bi = seg.find("월마감 주기")
        a_re = re.compile(r'<a\b[^>]*href="ADMN-CONF-010_baseline\.html"[^>]*>.*?</a>', re.S)
        m = a_re.search(seg, bi) if bi >= 0 else None
        if bi < 0: fail("업무플로우: 상시 블록 표지 '월마감 주기' 미검출")
        elif not m: fail("업무플로우: 상시 블록 뒤 CONF-010 링크 미검출")
        else:
            clone = m.group(0).replace("ADMN-CONF-010_baseline.html", AUDIT_TAB_HREF)
            if "정산 감사 로그" not in clone:
                fail(f"업무플로우: CONF-010 링크에 '정산 감사 로그' 문구 없음 → 복제 중단. 원문: {m.group(0)[:400]}")
            else:
                clone = clone.replace("정산 감사 로그", AUDIT_TAB_NAME).replace("CONF-010", "CONF-005")
                seg = seg[:m.end()] + "\n" + clone + seg[m.end():]
                log.append(f"[WF] 보안 감사로그 탭 링크 추가:\n      {clone[:400]}")
    wf = head + seg
    # 2-3 디렉터리 보정
    if 'id="wf-v51-fix"' not in wf:
        inject = '''
<style id="wf-v51-fix">
#wf-dir-grid{display:block!important;column-width:300px;column-gap:16px}
#wf-dir-grid>.wf-dir-card{break-inside:avoid;display:inline-block;width:100%;margin:0 0 16px!important;vertical-align:top}
</style>
<script id="wf-v51-js">
(function(){
  var grid=document.getElementById('wf-dir-grid'); if(!grid) return;
  var CODE=/^[A-Z]{2,6}-\\d{3}(-[A-Z0-9]+)?$/;
  function fix(){ grid.querySelectorAll('*').forEach(function(el){
    if(el.children.length===0 && CODE.test((el.textContent||'').trim())){ el.style.whiteSpace='nowrap'; el.style.flexShrink='0'; }
  }); }
  fix(); new MutationObserver(fix).observe(grid,{childList:true,subtree:true});
})();
</script>
'''
        bi = wf.rfind("</body>")
        if bi < 0: fail("업무플로우: </body> 미검출")
        else:
            wf = wf[:bi] + inject + wf[bi:]
            log.append("[WF] 디렉터리 열 배치 + 코드 라벨 nowrap 주입")
    pending[WF] = wf

# ---------- 3) 브레드크럼 (clean) ----------
STAGE_RE = re.compile(r'[0-4]단계\s*·\s*[^<›/|\n]*[^<›/|\s]')
residue = []
for html in sorted(CLEAN.glob("*.html")):
    t = cur(html)
    spans = [(m.start(), m.end()) for m in re.finditer(r'<(script|style)\b.*?</\1\s*>', t, re.S | re.I)]
    inside = lambda i: any(a <= i < b for a, b in spans)
    hits = [m for m in re.finditer(r'>([^<]+)<', t) if not inside(m.start()) and STAGE_RE.search(m.group(1))]
    if any(STAGE_RE.search(t[a:b]) for a, b in spans): residue.append(html.name)
    if not hits: continue
    g = href2group.get(html.name)
    if not g or norm(g) not in expected_norm:
        fail(f"브레드크럼: {html.name} 의 SNB 그룹을 찾지 못함 (검출값: {g})"); continue
    out, last = [], 0
    for m in hits:
        new = STAGE_RE.sub(g, m.group(1))
        log.append(f"[BC] {html.name}: '{m.group(1).strip()}' → '{new.strip()}'")
        out += [t[last:m.start(1)], new]; last = m.end(1)
    out.append(t[last:])
    pending[html] = "".join(out)

# ---------- 4) 마크업 덤프 (항상 생성, 읽기 전용) ----------
class Skel(HTMLParser):
    VOID = {"br", "img", "input", "hr", "meta", "link", "wbr", "source"}
    def __init__(s):
        super().__init__(); s.d = 0; s.on = False; s.r = 0; s.lines = []; s.txt = False
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if not s.on and a.get("id") == "wf-root": s.on = True; s.r = s.d
        if s.on and s.d - s.r <= 9:
            idp = f"#{a['id']}" if a.get("id") else ""
            cl = "." + ".".join(a["class"].split()) if a.get("class") else ""
            s.lines.append("  " * (s.d - s.r) + f"<{tag}{idp}{cl}>"); s.txt = False
        if tag not in s.VOID: s.d += 1
    def handle_endtag(s, tag):
        if tag in s.VOID: return
        s.d -= 1
        if s.on and s.d == s.r: s.on = False
    def handle_data(s, data):
        t = data.strip()
        if s.on and t and s.lines and not s.txt:
            s.lines[-1] += f'  "{t[:24]}"'; s.txt = True

src = pending.get(WF, read(WF)) if not errors else read(WF)
sk = Skel(); sk.feed(src)
css = []
for st in re.findall(r'<style\b[^>]*>(.*?)</style>', src, re.S | re.I):
    css += [r.strip() for r in re.findall(r'[^{}]*wf-[^{}]*\{[^{}]*\}', st)]
dump = "# 업무플로우 v5 마크업 덤프 (레이아웃 보정용)\n\n## 1. wf- CSS 규칙\n```css\n" + "\n".join(css) + \
       "\n```\n\n## 2. #wf-root 뼈대 (depth 9, 텍스트 24자)\n```\n" + "\n".join(sk.lines) + "\n```\n"
if len(dump) > 30000:
    print("[WARN] 30,000자 초과 — 뒤쪽 잘림"); dump = dump[:30000] + "\n...(잘림)\n```\n"
DUMP.parent.mkdir(parents=True, exist_ok=True); write(DUMP, dump)
print(f"[REPORT] {DUMP} ({len(dump):,}자)")

# ---------- 5) 플랜 결정 로그 ----------
plan = read(PLAN)
MARK = "### v5.1 보정 (2026-10-21)"
if MARK in plan:
    log.append("[PLAN] 이미 기록됨 → SKIP")
else:
    pending[PLAN] = plan.rstrip() + f"""

{MARK}
- SNB 중복 메뉴 제거 (prototype/·prototype_clean/ 공통): CONF-006(운영·보안 통합 감사 로그)은 CONF-005 '개인정보 열람 및 보안 감사로그' 탭(?view=ADMN-CONF-006)과 같은 화면 → 메뉴 삭제. USER-007은 '개인정보 · 보안 감사' 그룹에만 유지, '회원 · 수강 관리' 그룹 항목 삭제
- common-snb.js 문구 치환표('감사·보안 로그 (ADMN-CONF-006/010)', 'ADMN-CONF-006' 튜플)는 유지
- 업무플로우 CONF-005 라벨 = '{CONF005_LABEL}'(SNB 원문). 상시 감사 블록에 보안 감사로그 탭 링크 추가
- 브레드크럼: 옛 단계명(0~4단계 ·) → 해당 화면의 SNB 그룹명. prototype_clean/만 적용, prototype/는 SNB 그룹명 자체가 옛 단계명이라 보류(white 결정 대기)
- 디렉터리: 열 기반 배치(카드 높이 불균형 해소), 화면 코드 라벨 줄바꿈 금지
- 남은 레이아웃 3건(회원·수강 마지막 칸 / STAGE 01 노드 밀도 / 상시 감사 블록 배경)은 WORKFLOW_MARKUP_V5_DUMP.md 확인 후 다음 패치

### 범위 밖 후속 과제 (추가 · 2026-10-21)
- 정답지를 시스템 유형으로 쓴 곳: CONF-005 저작권 파트너 권한 문구·감사로그 '정답지 등록' 배지(7건, 그중 2건 ADMN-BRD-009 참조), BRD-005 '정답지 관리(ADMN-BRD-009)' 탭(파일 없이 탭으로 존재), common-snb.js 정답지 매핑 줄
- CONF-005 탭명 괄호 중복('… (관리자 권한 관리)', '… (보안 감사로그)')
- BOOK-001·PROD-003~006·patch_all_snb_v3.html 스크립트 안 옛 단계명 groupTitle 잔재 (사용 여부 미확인)
- prototype/common-snb.js 그룹명이 옛 단계명('1단계 · 계약 · 상품 · 매핑 설정' 등)
"""

# ---------- 저장 ----------
print("\n".join(log))
if residue: print(f"[INFO] script/style 안 옛 단계명 잔재(미수정): {', '.join(residue)}")
if errors:
    print(f"\n[ABORT] 오류 {len(errors)}건. 파일 미변경(덤프 리포트만 생성). 로그를 분석 AI에 반환하세요.")
    sys.exit(2)
for p in pending:
    if p == PLAN: continue
    dst = BACKUP / p.relative_to(ROOT); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, dst)
for p, t in pending.items(): write(p, t)
print(f"\n[DONE] {len(pending)}개 파일 저장, 백업: {BACKUP}")
