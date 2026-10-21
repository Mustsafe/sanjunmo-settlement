# -*- coding: utf-8 -*-
"""
patch_workflow_v5_2_fix.py  (레포 루트에서 실행)
A) v5.1 브레드크럼 부작용 복구 (prototype_clean/*.html, 업무플로우 제외)
   - 최신 _archive/backup/v5_1_* 백업과 줄 단위 비교
   - 텍스트 노드 '전체'가 옛 단계명인 경우만 브레드크럼 → 중복 제거 후 SNB 기준 그룹명으로 재계산
   - 그 외(문장 중간 치환: SETT-002 L1962 등) → 백업 원문 복원
B) 업무플로우 노드 화면명·코드 = 링크 대상 href의 SNB 메뉴 label·code로 동기화
C) 레이아웃 3건: 회원·수강 마지막 칸 / STAGE 01 출발 노드를 줄 머리로 / 상시 감사 블록 배경
D) 플랜 결정 로그
A·B 오류 시 전체 중단(파일 미변경). C는 대상 미검출 시 [WARN] 후 해당 항목만 건너뜀.
"""
import re, sys, shutil, datetime
from pathlib import Path

ROOT = Path.cwd()
CLEAN = ROOT / "prototype_clean"
WF = CLEAN / "00_WORKFLOW_GUIDE_baseline.html"
SNB = CLEAN / "common-snb.js"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_2_{TS}"
STAGE_RE = re.compile(r'[0-4]단계\s*·\s*[^<›/|\n]*[^<›/|\s]')
KEEP_HREF = {"ADMN-CONF-005_baseline.html?view=ADMN-CONF-006"}  # 탭 이름 유지

pending, errors, warns, log = {}, [], [], []
def read(p):
    with p.open(encoding="utf-8", newline="") as f: return f.read()
def write(p, t):
    with p.open("w", encoding="utf-8", newline="") as f: f.write(t)
def fail(m): errors.append(m); print("[ERROR]", m)
def warn(m): warns.append(m); print("[WARN]", m)

for p in [WF, SNB, PLAN]:
    if not p.exists(): print(f"[ERROR] 필수 파일 없음: {p}"); sys.exit(2)

# ---------- SNB 파싱 (현재 = 중복 제거 후) ----------
js = read(SNB)
href2group, menu_full, menu_base, cur_g = {}, {}, {}, None
for line in js.splitlines():
    if re.search(r'\bcode:\s*"', line):
        c = re.search(r'\bcode:\s*"([^"]+)"', line)
        l = re.search(r'\blabel:\s*"([^"]+)"', line)
        h = re.search(r'\bhref:\s*"([^"]+)"', line)
        if c and l and h:
            full = h.group(1); base = full.split("?")[0].split("#")[0]
            menu_full.setdefault(full, (c.group(1), l.group(1)))
            menu_base.setdefault(base, (c.group(1), l.group(1)))
            if cur_g: href2group.setdefault(base, cur_g)
        continue
    m = re.search(r'\b(?:title|group|groupTitle|name|heading|label)\s*:\s*"([^"]+)"', line)
    if m: cur_g = m.group(1)
if href2group.get("ADMN-USER-007_baseline.html") != "개인정보 · 보안 감사":
    fail(f"SNB 파싱: USER-007 그룹이 '개인정보 · 보안 감사'가 아님 ({href2group.get('ADMN-USER-007_baseline.html')})")

# ---------- A) 브레드크럼 부작용 복구 ----------
bk_root = ROOT / "_archive" / "backup"
v51 = sorted(bk_root.glob("v5_1_*")) if bk_root.exists() else []
if not v51:
    fail("v5.1 백업 폴더(_archive/backup/v5_1_*) 없음")
else:
    bdir = v51[-1] / "prototype_clean"
    print(f"[INFO] 비교 기준 백업: {bdir}")
    for bak in sorted(bdir.glob("*.html")):
        if bak.name == WF.name: continue
        cur_p = CLEAN / bak.name
        if not cur_p.exists(): fail(f"{bak.name}: 현재 파일 없음"); continue
        cl = read(cur_p).splitlines(True); bl = read(bak).splitlines(True)
        if len(cl) != len(bl): fail(f"{bak.name}: 줄 수 불일치 {len(bl)}→{len(cl)}"); continue
        g = href2group.get(bak.name)
        changed = False
        for i, (c, b) in enumerate(zip(cl, bl)):
            if c == b: continue
            def fx(m):
                t = m.group(1); s = t.strip()
                if s and STAGE_RE.fullmatch(s):
                    if not g: fail(f"{bak.name}: SNB 그룹 미검출"); return m.group(0)
                    return ">" + t[:len(t) - len(t.lstrip())] + g + t[len(t.rstrip()):] + "<"
                return m.group(0)
            if "<" not in b and ">" not in b:
                s = b.strip()
                new = b.replace(s, g) if (s and g and STAGE_RE.fullmatch(s)) else b
            else:
                new = re.sub(r'>([^<]+)<', fx, b)
            if new != c:
                kind = "복원" if new == b else "그룹 재계산"
                log.append(f"[A] {bak.name} L{i+1} ({kind})\n      현재: {c.strip()[:160]}\n      변경: {new.strip()[:160]}")
                cl[i] = new; changed = True
        if changed: pending[cur_p] = "".join(cl)

# ---------- B) 노드 화면명·코드 동기화 ----------
wf = read(WF)
r0 = wf.find('id="wf-root"'); d0 = wf.find('id="wf-dir-grid"', r0)
if r0 < 0 or d0 < 0:
    fail("업무플로우: wf-root 또는 wf-dir-grid 미검출")
else:
    seg = wf[r0:d0]
    A_RE = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.S)
    SCR_RE = re.compile(r'(<span class="wf-node-scr">)([^<]*)((<code\b[^>]*>)([^<]*)(</code>))?')
    def sync(m):
        attrs, inner = m.group(1), m.group(2)
        if not re.search(r'class="[^"]*\b(wf-node|wf-pair|wf-fan-item)\b', attrs): return m.group(0)
        h = re.search(r'href="([^"]+)"', attrs)
        if not h or not h.group(1).startswith("ADMN-") or h.group(1) in KEEP_HREF: return m.group(0)
        href = h.group(1)
        ent = menu_full.get(href) or menu_base.get(href.split("?")[0].split("#")[0])
        dt = re.search(r'wf-node-do">([^<]*)<', inner) or re.search(r'<b>([^<]*)</b>', inner)
        who = dt.group(1).strip() if dt else href
        if not ent: warn(f"[B] '{who}' 링크 {href} 가 SNB에 없음 → 유지"); return m.group(0)
        sm = SCR_RE.search(inner)
        if not sm: warn(f"[B] '{who}' 화면명 영역 없음 → 유지"); return m.group(0)
        code, label = ent
        old_name, old_code = sm.group(2).strip(), sm.group(5)
        if old_name == label and old_code == code: return m.group(0)
        code_html = (sm.group(4) if sm.group(3) else '<code class="wf-code">') + code + "</code>"
        inner2 = inner[:sm.start()] + sm.group(1) + label + code_html + inner[sm.end():]
        log.append(f"[B] {who}: '{old_name}' {old_code or '(코드 없음)'} → '{label}' {code}")
        return f"<a{attrs}>{inner2}</a>"
    wf = wf[:r0] + A_RE.sub(sync, seg) + wf[d0:]

# ---------- C) 레이아웃 ----------
css = ['#wf-root .wf-pairs>.wf-pair:last-child:nth-child(odd){grid-column:1/-1}']
log.append("[C1] 회원·수강 홀수 마지막 칸 전체 폭")

s1 = wf.find('id="wf-stage-01"'); s2 = wf.find('id="wf-stage-02"')
if s1 < 0 or s2 < 0: warn("[C2] STAGE 01/02 미검출 → 건너뜀")
else:
    sub = wf[s1:s2]
    lis = list(re.finditer(r'<li\b[^>]*class="[^"]*\bis-start\b[^"]*"[^>]*>(.*?)</li>', sub, re.S))
    if len(lis) != 1: warn(f"[C2] STAGE 01 출발 노드 {len(lis)}건 (1건이어야 함) → 건너뜀")
    else:
        m = lis[0]
        do = re.search(r'wf-node-do">([^<]*)<', m.group(1))
        out = re.search(r'wf-node-out">([^<]*)<', m.group(1))
        ol_i = sub.rfind("<ol", 0, m.start())
        if not do or ol_i < 0: warn("[C2] 출발 노드 문구 또는 <ol> 미검출 → 건너뜀")
        else:
            lead = (f'<p class="wf-row-lead"><span class="wf-chip">출발</span><b>{do.group(1).strip()}</b>'
                    + (f'<span>{out.group(1).strip()}</span>' if out else "") + "</p>\n")
            sub = sub[:ol_i] + lead + sub[ol_i:m.start()] + sub[m.end():]
            wf = wf[:s1] + sub + wf[s2:]
            css.append('#wf-root .wf-row-lead{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:0 0 10px;font-size:13px;color:var(--wf-sub)}'
                       '#wf-root .wf-row-lead b{color:var(--wf-ink);font-weight:800}')
            log.append(f"[C2] STAGE 01 출발 노드 → 줄 머리 문구: {do.group(1).strip()}")

s3 = wf.find('id="wf-stage-03"')
if s3 < 0: warn("[C3] STAGE 03 미검출 → 건너뜀")
else:
    end = wf.find("</section>", s3)
    hits = []
    for m in re.finditer(r'<div class="wf-sub"', wf[s3:end]):
        hd = re.search(r'<div class="wf-sub-hd">(.*?)</div>', wf[s3 + m.end(): s3 + m.end() + 1500], re.S)
        if hd and "상시" in re.sub(r"<[^>]+>", "", hd.group(1)): hits.append(s3 + m.start())
    if len(hits) != 1:
        cls = sorted(set(re.findall(r'class="([^"]+)"', wf[s3:end])))
        warn(f"[C3] 상시 블록 {len(hits)}건 (1건이어야 함) → 건너뜀. STAGE 03 클래스: {cls[:40]}")
    else:
        i = hits[0]
        wf = wf[:i] + '<div class="wf-sub is-always"' + wf[i + len('<div class="wf-sub"'):]
        css.append('#wf-root .wf-sub.is-always{background:#fff;border:1px dashed var(--slate-300,#CBD5E1);border-left:3px solid var(--slate-500,#64748B)}')
        log.append("[C3] 상시 감사 블록 is-always 적용")

if 'id="wf-v52-fix"' not in wf:
    bi = wf.rfind("</body>")
    if bi < 0: fail("업무플로우: </body> 미검출")
    else: wf = wf[:bi] + '<style id="wf-v52-fix">\n' + "\n".join(css) + "\n</style>\n" + wf[bi:]
pending[WF] = wf

# ---------- D) 플랜 ----------
plan = read(PLAN); MARK = "### v5.2 보정 (2026-10-21)"
if MARK not in plan:
    pending[PLAN] = plan.rstrip() + f"""

{MARK}
- v5.1 브레드크럼 부작용 복구: 문장 중간 치환(SETT-002 '당월 정산서(1단계·11단계)…' 등) 원문 복원, USER-007 브레드크럼 = '개인정보 · 보안 감사'
- 업무플로우 노드 화면명·코드 = 링크 대상의 SNB 메뉴명·코드 (ORD-002→SNB 기준, USER-003/004 '일반 회원 관리' 불일치 해소). 예외: 보안 감사로그 탭 링크는 탭 이름 유지
- 레이아웃: 회원·수강 홀수 마지막 칸 전체 폭 / STAGE 01 '오프라인 계약 체결' 출발 노드를 줄 머리 문구로 / 상시 감사 블록 흰 배경+점선
- 대기: SNB_DIFF_01 결과 후 prototype/ SNB 그룹명·브레드크럼 정렬, 이후 6단계 덮어쓰기
"""

# ---------- 저장 ----------
print("\n".join(log))
if errors:
    print(f"\n[ABORT] 오류 {len(errors)}건. 파일 미변경. 로그를 분석 AI에 반환하세요."); sys.exit(2)
for p in pending:
    if p == PLAN: continue
    dst = BACKUP / p.relative_to(ROOT); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, dst)
for p, t in pending.items(): write(p, t)
print(f"\n[DONE] {len(pending)}개 파일 저장 · 경고 {len(warns)}건 · 백업: {BACKUP}")
