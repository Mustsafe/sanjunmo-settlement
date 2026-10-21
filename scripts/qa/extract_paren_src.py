# scripts/qa/extract_paren_src.py — 읽기 전용. 레포 루트에서 실행.
# PAREN_DUP_SCAN 잔여 36건의 prototype_clean HTML 원문 위치 추출 (script 블록 포함)
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.cwd()
DIR = ROOT / "prototype_clean"
OUT = ROOT / ".antigravity" / "reports" / "PAREN_FIX_SRC_02.md"
MAX_HITS = 6

TARGETS = [
    ("ADMN-BOOK-001", "도서 공급형태"),
    ("ADMN-CONF-005", "파트너 강사"),
    ("ADMN-CONF-005", "외부 물류 3PL"),
    ("ADMN-CONF-010", "상품별 권리자 매핑"),
    ("ADMN-CONF-010", "수취인 분할 관리"),
    ("ADMN-CONF-010", "약정금 마일스톤 검수"),
    ("ADMN-CONF-010", "정산 수동 조정"),
    ("ADMN-CONF-010", "도서 공급 원장"),
    ("ADMN-CONF-010", "민감정보 열람통제"),
    ("ADMN-INST-001", "자사저작권 도서"),
    ("ADMN-INST-002", "매출연동("),
    ("ADMN-INST-002", "매출연동<"),
    ("ADMN-INST-002", "매출연동 ("),
    ("ADMN-LOGIN-001", "보안 감사 로그"),
    ("ADMN-ORD-001", "인세 도서"),
    ("ADMN-ORD-001", "수강권 직권부여"),
    ("ADMN-PROD-003", "권리자 계약 원장"),
    ("ADMN-PROD-004", "도서 공급 원장 연결"),
    ("ADMN-PROD-004", "예약판매 설정"),
    ("ADMN-PROD-005", "정산 차감 정책 설정"),
    ("ADMN-PROD-007", "일반 상품 판매매출"),
    ("ADMN-SETT-002", "온라인 강좌 수익배분"),
    ("ADMN-SETT-002", "자사 발행 도서 인세"),
    ("ADMN-SETT-002", "위탁 도서 판매대금 정산"),
    ("ADMN-SETT-002", "지원금 종료 일시정산"),
    ("ADMN-SETT-002", "매출연동 개발지원금 단독"),
    ("ADMN-SETT-004", "매입 재판매 도서"),
    ("ADMN-SETT-009", "온라인 강좌 수익배분"),
    ("ADMN-SETT-009", "자사 발행 도서 인세"),
    ("ADMN-SETT-009", "위탁 도서 판매대금 정산"),
    ("ADMN-SETT-009", "일반 상품 판매매출"),
    ("ADMN-SETT-009", "원천징수 사건 성립"),
    ("ADMN-USER-007", "정산 감사로그"),
]

out = ["# PAREN_FIX_SRC_02 — 잔여 괄호 중복 원문 위치 (prototype_clean, 원문)", ""]
missing = 0
for code, needle in TARGETS:
    p = DIR / f"{code}_baseline.html"
    out.append(f"## {code} · \"{needle}\"")
    if not p.exists():
        out += ["파일 없음", ""]; missing += 1; continue
    hits = []
    for ln, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        i = line.find(needle)
        if i < 0:
            continue
        s = max(0, i - 40)
        hits.append(f"- L{ln}: `{line[s:i + len(needle) + 160].strip()}`")
    if not hits:
        out.append("0건"); missing += 1
    else:
        out += hits[:MAX_HITS]
        if len(hits) > MAX_HITS:
            out.append(f"- (외 {len(hits) - MAX_HITS}건 생략)")
    out.append("")

OUT.write_text("\n".join(out), encoding="utf-8")
n = len(OUT.read_text(encoding="utf-8"))
print(f"[OK] 대상 {len(TARGETS)}개 · 0건 {missing}개 · {OUT.name} {n}자" + ("  [WARN] 30,000자 초과" if n > 30000 else ""))
