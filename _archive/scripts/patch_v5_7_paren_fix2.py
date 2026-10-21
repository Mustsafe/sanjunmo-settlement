# patch_v5_7_paren_fix2.py — 레포 루트에서 실행 (prototype_clean 전용)
# A) common-snb.js v5.6 프렐류드 보완  B) clean HTML 원문 중복 문구 직접 수정
import re, sys, shutil, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.cwd()
CLEAN = ROOT / "prototype_clean"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_7_{TS}"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"

def abort(msg):
    print(f"[ABORT] {msg}\n파일 미변경. 이 출력 전문을 분석 AI에 그대로 전달하세요.")
    sys.exit(2)

def rd(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()

def wr(p, s):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

changes, log = {}, []

# ---------- A. 런타임 보완 ----------
snb = CLEAN / "common-snb.js"
if not snb.exists(): abort(f"파일 없음: {snb}")
t = rd(snb)
if "__wfStripCodeParens" not in t: abort("v5.6 프렐류드 없음")
if "CODE_OUT" in t: abort("이미 적용됨 (CODE_OUT 존재)")
EOL = "\r\n" if "\r\n" in t else "\n"

JS_EDITS = [
    ("괄호 앞 공백 허용",
     '      if (!LEAD.test(whole.slice(0, off))) return m;',
     '      var pre = whole.slice(0, off); if (pre.trim() && !LEAD.test(pre)) return m;'),
    ("코드 밖·이름 안 패턴 정의",
     r'  var PAREN = /\s*\(\s*([^()]{2,80}?)\s*\)/g;',
     r'  var PAREN = /\s*\(\s*([^()]{2,80}?)\s*\)/g;' + EOL
     + r'  var CODE_OUT = /\b(?:ADMN-)?[A-Z]{2,5}-\d{3}(?:-S\d+)?\s*\(\s*([^()]{2,40}?)\s*\)/g;'),
    ("코드 밖·이름 안 적용",
     '    if (!str || typeof str !== "string" || str.indexOf("(") === -1) return str;',
     '    if (!str || typeof str !== "string" || str.indexOf("(") === -1) return str;'
     ' str = str.replace(CODE_OUT, function (m, inner) { return /[가-힣]/.test(inner) && !isCode(inner, src) ? inner : m; });'),
    ("strong·b·small 감싼 코드",
     '    var els = root.querySelectorAll("code");',
     '    var els = root.querySelectorAll("code,strong,b,small");'),
    ("요소 앞 공백 허용",
     '      if (!LEAD.test(before)) continue;',
     '      if (before.trim() && !LEAD.test(before)) continue;'),
]
for label, old, new in JS_EDITS:
    n = t.count(old)
    if n != 1: abort(f"common-snb.js · {label}: 매칭 {n}건 (1건이어야 함)")
    t = t.replace(old, new)
    log.append(f"common-snb.js · {label}")
changes[snb] = t

# ---------- B. clean HTML 원문 수정 (파일, 찾을 문구, 바꿀 문구) — 0건이면 중단 ----------
HTML_EDITS = [
    ("ADMN-BOOK-001", "공급형태(book_supply_type)", "공급형태"),
    ("ADMN-BOOK-001", "정가 이력(book_price_history)", "정가 이력"),
    ("ADMN-CONF-005", "RE:\\((?:ROLE_)?PARTNER_[A-Z0-9_]+ — ", "("),
    ("ADMN-INST-001", "도서(자사 저작권 보유)", "도서"),
    ("ADMN-INST-002", "매출연동(<code>매출연동 (REVENUE_SHARE)</code>)", "매출연동"),
    ("ADMN-ORD-001", " (수강권 직권부여 · 구 ADMN-ORD-003 통합)", ""),
    ("ADMN-PROD-005", " (ADMN-SETT-006 연동)", ""),
    ("ADMN-PROD-007", "일반 상품 판매매출 일반상품 매출)", "일반 상품 판매매출)"),
    ("ADMN-PROD-007", "일반 상품 판매매출(<code>일반상품 매출</code>)", "일반 상품 판매매출"),
    ("ADMN-SETT-002", "온라인 강좌 수익배분 (강좌 수익배분)", "온라인 강좌 수익배분"),
    ("ADMN-SETT-002", "산출 명세 (강좌 수익배분)", "산출 명세"),
    ("ADMN-SETT-002", "자사 발행 도서 인세 (도서 인세)", "자사 발행 도서 인세"),
    ("ADMN-SETT-002", "위탁 도서 판매대금 정산 (위탁도서 정산)", "위탁 도서 판매대금 정산"),
    ("ADMN-SETT-002", "일시정산(LUMP_SETTLE, 7단계)", "일시정산(7단계)"),
    ("ADMN-SETT-002", "단독 (Pipeline 5.1 · 무한도형)", "단독 (무한도형)"),
    ("ADMN-SETT-004", "매입 재판매 도서(<code>매입 재판매 도서 (PURCHASED_RESALE)</code>)", "매입 재판매 도서"),
    ("ADMN-SETT-004", "사은품(<code>강좌 부속·사은품 (BUNDLED)</code>)", "강좌 부속 사은품"),
    ("ADMN-SETT-009", "온라인 강좌 수익배분 (강좌 수익배분)", "온라인 강좌 수익배분"),
    ("ADMN-SETT-009", "자사저작권 (도서 인세)", "자사저작권"),
    ("ADMN-SETT-009", "위탁 도서 판매대금 정산 (위탁도서 정산)", "위탁 도서 판매대금 정산"),
    ("ADMN-SETT-009", "(일반상품 매출 · 소비재)", "(소비재)"),
    ("ADMN-SETT-009", "(일반상품 매출, <code>TX-13</code>)", "(<code>TX-13</code>)"),
    ("ADMN-SETT-009", "(일반상품 매출 · TX-13)", "(TX-13)"),
    ("ADMN-SETT-009", "일반 상품 판매매출 (일반상품 매출)", "일반 상품 판매매출"),
    ("ADMN-SETT-009", "사건 성립(<code>payment_event_date IS NOT NULL</code>)", "사건 성립"),
]
texts = {}
for code, old, new in HTML_EDITS:
    p = CLEAN / f"{code}_baseline.html"
    if not p.exists(): abort(f"파일 없음: {p}")
    s = texts.get(p) or rd(p)
    if old.startswith("RE:"):
        s, n = re.subn(old[3:], new, s)
        shown = old[3:]
    else:
        n = s.count(old)
        s = s.replace(old, new)
        shown = old
    if n == 0: abort(f"{code} · \"{shown}\" 매칭 0건")
    texts[p] = s
    log.append(f"{code} · \"{shown[:40]}\" {n}건")
changes.update(texts)

# ---------- 기록 ----------
for p, s in changes.items():
    dst = BACKUP / p.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    wr(p, s)

if PLAN.exists():
    note = "\n".join([
        "", "### v5.7 괄호 중복 2차 (2026-10-21)",
        "- 런타임 보완: 코드 밖·이름 안 패턴('ADMN-X (이름)')은 이름만 남김, 줄바꿈 뒤 괄호·strong/b/small로 감싼 코드도 괄호째 제거.",
        "- clean HTML 원문 중복(이름(이름 (CODE)) 등)·코드+설명 혼합 괄호 직접 수정. prototype/은 정본 용어 병기 의도로 유지.",
        "- 보류: USER-007 '정산 감사로그(감사 로그)', ORD-001 '인세 도서(인세도서)' — 재스캔 후 확인.", "",
    ])
    with open(PLAN, "a", encoding="utf-8", newline="") as fp:
        fp.write(note)

print(f"[OK] 수정 {len(changes)}개 · 백업 {BACKUP.relative_to(ROOT)}")
for l in log: print("  -", l)
