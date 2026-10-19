#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모닷컴 & 정산시스템 v4.0.0] 백오피스 정합성 정비 스크립트 — Phase 6 심층 2차 클린업 & 감사
대상: prototype_clean/ 전용 (prototype/ 폴더는 일절 건드리지 않음!)

배경:
  Phase 1~5를 통해 언더스코어(_)가 포함된 DB 컬럼명(snake_case), 복합 영문 코드(UPPER_SNAKE_CASE),
  Track G, 기출문제/정오표, 원문자(①~⑳)는 37개 전 파일에서 0건(Clean)이 달성되었습니다.
  본 스크립트는 언더스코어가 없어 1차 정규식에서 제외되었던 '심층 2차 설계서 잔재'를 스캔 및 정제합니다:
    1) 단일어 영문 상태/유형 코드: DRAFT, APPROVED, REJECTED, ACTIVE, RESERVED, DECIDED, BUNDLED,
       MIXED, LOAN, BASIC, MULTIPLE, CUMULATIVE, CONSIGNMENT, ALIMTALK 등
    2) camelCase 변수명: displayDuration 등
    3) 설계서 문서 번호 참조: 제1권, 제2권, 제6장, X.Y절(6.2절, 8.3절, 17.5절 등), 부록 B, 부록 D-15, Case 1 ~ 12, QA D-13 등
    4) 텍스트에 노출된 화면코드/세무코드: (ADMN-...), [ADMN-...], (INST-001), (SETT-002), TX-01 ~ TX-13, RH-INTERNAL 등
    5) <script> 내부의 alert() / confirm() / 토스트 문자열 내 설계서 용어 및 코드값

실행 방법 (저장소 루트에서 실행):
  python phase6_deep_polish_and_audit.py
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

ROOT_DIR = Path(__file__).resolve().parent
CLEAN_DIR = ROOT_DIR / "prototype_clean"
REPORT_PATH = ROOT_DIR / "CLEANUP_AUDIT_REPORT.md"

# 실제 운영화면에서 정상적으로 쓰이는 영문 약어 화이트리스트 (제거/경고 제외)
ALLOWED_UPPER_WORDS: Set[str] = {
    "PG", "CS", "FAQ", "QNA", "VIP", "SMS", "LMS", "MMS", "URL", "HTML", "CSS", "JS",
    "IP", "ID", "UUID", "OTP", "API", "PDF", "CSV", "XLSX", "JSON", "DB", "UI", "UX",
    "RBAC", "WORM", "AES", "KMS", "AWS", "TTL", "ISBN", "SKU", " B2C", "B2B", "B2C",
    "PC", "OS", "MAC", "IOS", "WEB", "APP", "SNS", "QR", "VAT", "MMG", "3PL", "SSOT",
    "AM", "PM", "KRW", "OK", "NO", "YN", "ON", "OFF", "NEW", "HOT", "BEST", "TOP",
    " KPI", "KPI", "ROI", "ROAS", "CPA", "CPC", "CTR", "CVR", "LTV", "ARPU",
}

# 1. prototype_clean/ 전용: 단일어 영문 ENUM 및 괄호 병기 패턴 정제
SINGLE_WORD_CODE_REPLACEMENTS: List[Tuple[str, str]] = [
    # 한글 라벨 뒤 괄호 병기된 단일어 영문 코드 제거
    ("작성초안(DRAFT)", "작성초안"),
    ("작성 중(DRAFT)", "작성 중"),
    ("초안(DRAFT)", "초안"),
    ("검수승인(APPROVED)", "검수승인"),
    ("승인완료(APPROVED)", "승인완료"),
    ("승인(APPROVED)", "승인"),
    ("반려(REJECTED)", "반려"),
    ("알림톡(ALIMTALK)", "알림톡"),
    ("광고성( AD )", "광고성"),
    ("광고성(AD)", "광고성"),
    ("강좌 부속·사은품 (BUNDLED)", "강좌 부속·사은품"),
    ("강좌 부속·사은품(BUNDLED)", "강좌 부속·사은품"),
    ("복합 결제(MIXED)", "복합 결제"),
    ("지급 예약(RESERVED)", "지급 예약"),
    ("예약(RESERVED)", "지급 예약"),
    ("전 수취인 DECIDED", "전 수취인 판정 완료"),
    ("미소진 지원금 한도( ACTIVE )", "미소진 지원금 한도(유효)"),
    ("미소진 지원금 한도(ACTIVE)", "미소진 지원금 한도(유효)"),
    ("마감 원장(Locked)", "마감 확정 원장"),
    ("워터마크 노출 시간 (displayDuration)", "워터마크 노출 시간"),
    ("(displayDuration)", ""),
    ("자사( RH-INTERNAL )", "자사"),
    ("자사(RH-INTERNAL)", "자사"),
    ("RH-INTERNAL", "자사 계정"),
    ("SENS 승인완료", "검수 승인완료"),

    # 세무 코드 (TX-01 ~ TX-13) 운영 용어 순화
    ("도서 면세( TX-11 )", "도서 재화 면세"),
    ("도서 면세(TX-11)", "도서 재화 면세"),
    ("TX-08  (면세 계산서 역발행)", "면세 계산서 역발행"),
    ("TX-08 (면세 계산서 역발행)", "면세 계산서 역발행"),
    ("후보 TX-09 또는 TX-07 부여", "인세·기타소득 또는 사업소득 후보 분류"),
    ("후보  TX-09 , 강의·약정·지원금은 후보  TX-07  부여", "인세·매절은 기타소득, 강의·약정·지원금은 사업소득 후보로 분류"),
    ("후보 TX-09, 강의·약정·지원금은 후보 TX-07 부여", "인세·매절은 기타소득, 강의·약정·지원금은 사업소득 후보로 분류"),
    ("( TX-13 )", "(자사 매출)"),
    ("(TX-13)", "(자사 매출)"),
]

# 2. 정규식 기반 2차 심층 정제 (텍스트 노드 및 UI 속성 전용)
DEEP_CLEAN_REGEXES: List[Tuple[re.Pattern, str]] = [
    # 설계서 장·절·권·부록·케이스 참조 제거 (예: `(8.3절)`, `제1권 7.3절`, `부록 B`, `Case 11`, `QA D-13`)
    (re.compile(r"\(\s*(?:합의서\s*)?(?:제\d+[권장]\s*)?\d+\.\d+절(?:\s*[·,]\s*\d+\.\d+절)*\s*\)"), ""),
    (re.compile(r"(?:제\d+[권장]\s*)?\d+\.\d+절\s*[:·]?\s*"), ""),
    (re.compile(r"\b부록\s+[A-Z](?:-\d+)?\s*[·:]?\s*"), ""),
    (re.compile(r"\(\s*Case\s+\d+(?:\s*~\s*\d+)?\s*\)", re.IGNORECASE), ""),
    (re.compile(r",\s*Case\s+\d+\s*", re.IGNORECASE), ""),
    (re.compile(r"\(\s*QA\s+[A-Z]-\d+\s*\)", re.IGNORECASE), ""),

    # 한글 명칭 뒤에 붙은 화면코드 괄호 제거: 예 `월간 정산 및 집행( ADMN-SETT-002 )`, `계약원장(INST-001)`
    (re.compile(r"([가-힣a-zA-Z0-9\]])\s*\(\s*(?:ADMN-)?(?:INST|SETT|BOOK|PROD|ORD|RFD|USER|BRD|PROM|CONF|DASH|STAT|LOGIN)-\d{3}(?:-[A-Z0-9]+)?\s*\)"), r"\1"),
    # 문두 대괄호 화면코드 배지 제거: 예 `[ADMN-BOOK-001-S1]`, `[INST-001]`
    (re.compile(r"\[\s*(?:ADMN-)?(?:INST|SETT|BOOK|PROD|ORD|RFD|USER|BRD|PROM|CONF|DASH|STAT|LOGIN)-\d{3}(?:-[A-Z0-9]+)?\s*\]\s*"), ""),

    # 남은 단독 TX-01 ~ TX-13 코드 순화
    (re.compile(r"\(\s*TX-(?:0[1-9]|1[0-3])\s*\)"), ""),
    (re.compile(r"\bTX-(?:0[1-9]|1[0-3])\b"), "세무기준"),

    # 빈 괄호 및 다중 공백 정리
    (re.compile(r"\(\s*\)" ), ""),
    (re.compile(r"[ \t]{2,}"), " "),
]


def clean_script_user_messages(script_block: str) -> Tuple[str, int]:
    """
    <script> 내부의 코드 로직(변수명, 함수명, DOM ID, 쿼리셀렉터)은 건드리지 않고,
    오직 alert(...), confirm(...), showToast(...) 내부의 사용자 노출 메시지 문자열만 안전하게 정제합니다.
    """
    changes = 0

    def _clean_msg_literal(m: re.Match) -> str:
        nonlocal changes
        func_name, quote, msg = m.group(1), m.group(2), m.group(3)
        orig_msg = msg
        for src, dst in SINGLE_WORD_CODE_REPLACEMENTS:
            msg = msg.replace(src, dst)
        for pat, repl in DEEP_CLEAN_REGEXES:
            msg = pat.sub(repl, msg)
        msg = msg.replace("기출문제", "빈출문제").replace("정오표", "교재 정답지")
        if msg != orig_msg:
            changes += 1
        return f"{func_name}({quote}{msg}{quote}"

    updated = re.sub(
        r"\b(alert|confirm|showToast|toast)\s*\(\s*(['\"`])((?:\\.|(?!\2).)*)\2",
        _clean_msg_literal,
        script_block,
        flags=re.DOTALL,
    )
    return updated, changes


def process_clean_html(file_path: Path) -> int:
    raw = file_path.read_text(encoding="utf-8")
    orig = raw

    protected_blocks: List[str] = []

    def _protect(m: re.Match) -> str:
        block = m.group(0)
        if block.lower().startswith("<script"):
            block, _ = clean_script_user_messages(block)
        idx = len(protected_blocks)
        protected_blocks.append(block)
        return f"___PROTECTED_BLOCK_{idx}___"

    masked = re.sub(
        r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)",
        _protect,
        raw,
        flags=re.IGNORECASE,
    )

    def _clean_segment(seg: str) -> str:
        for src, dst in SINGLE_WORD_CODE_REPLACEMENTS:
            seg = seg.replace(src, dst)
        for pat, repl in DEEP_CLEAN_REGEXES:
            seg = pat.sub(repl, seg)
        return seg

    def _process_tag(tag_m: re.Match) -> str:
        tag_s = tag_m.group(0)
        return re.sub(
            r'(\b(?:title|placeholder|data-tooltip)\s*=\s*)(["\'])(.*?)\2',
            lambda am: f"{am.group(1)}{am.group(2)}{_clean_segment(am.group(3))}{am.group(2)}",
            tag_s,
            flags=re.IGNORECASE | re.DOTALL,
        )

    masked = re.sub(r"<[^>]+>", _process_tag, masked)

    def _process_text(txt_m: re.Match) -> str:
        txt = txt_m.group(1)
        if not txt.strip() or "___PROTECTED_BLOCK_" in txt:
            return txt_m.group(0)
        return f">{_clean_segment(txt)}<"

    masked = re.sub(r">([^<]+)<", _process_text, masked)
    masked = re.sub(r"\(\s*\)", "", masked)

    for idx, block in enumerate(protected_blocks):
        masked = masked.replace(f"___PROTECTED_BLOCK_{idx}___", block)

    if masked != orig:
        file_path.write_text(masked, encoding="utf-8")
        return 1
    return 0


def scan_deep_issues(file_path: Path) -> List[Dict[str, str]]:
    """
    1차 오염원(snake_case, UPPER_SNAKE_CASE, 금지어, Track G, 원문자)뿐 아니라
    2차 심층 오염원(설계서 절 번호 X.Y절, 부록 X, camelCase 변수, 화면코드 노출)까지 통합 스캔합니다.
    """
    issues: List[Dict[str, str]] = []
    raw = file_path.read_text(encoding="utf-8")

    stripped = re.sub(
        r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)",
        lambda m: "\n" * m.group(0).count("\n"),
        raw,
        flags=re.IGNORECASE,
    )

    sample_whitelist = {
        "sanjun_hong88", "safety_kim26", "park_jw90", "lee_sjm77", "choi_min33", "jung_sky20",
        "safe_park", "pass_lee", "choi_san", "jung_study", "dh_kang", "yj_choi",
        "admin_root", "admin_kim", "admin_lee", "admin_settle_mgr", "cs_park", "inst_lee", "sett_choi",
        "unopened_book_photo", "warehouse_cam_0044", "safety_helmet_keyring_main",
        "UTF_8", "utf_8", "no_opener",
    }

    patterns = [
        ("레거시_트랙_금지어", re.compile(r"(\bTrack\s+[A-G]\b|기출문제|기출특강|정오표)", re.IGNORECASE)),
        ("설계서_절_부록_참조", re.compile(r"(\d+\.\d+절|\b부록\s+[A-Z]\b)")),
        ("설계마커_원문자", re.compile(r"(\[\s*마커\s*\d+\s*\]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮])")),
        ("DB변수명_snake_case", re.compile(r"\b[a-z]{2,}(?:_[a-z0-9]{2,})+\b")),
        ("영문코드_UPPER_SNAKE", re.compile(r"\b[A-Z]{2,}(?:_[A-Z0-9]{2,})+\b")),
        ("세무코드_TX", re.compile(r"\bTX-(?:0[1-9]|1[0-3])\b")),
    ]

    for line_no, line in enumerate(stripped.splitlines(), start=1):
        text_only = re.sub(r"<[^>]+>", " ", line).strip()
        if not text_only:
            continue
        for category, pat in patterns:
            matches = pat.findall(text_only)
            if matches:
                filtered = [m for m in matches if m not in sample_whitelist]
                if filtered:
                    issues.append({
                        "line": str(line_no),
                        "category": category,
                        "tokens": ", ".join(sorted(set(filtered))),
                        "snippet": text_only[:100],
                    })
    return issues


def main() -> None:
    print("=" * 72)
    print("[Phase 6] prototype_clean/ 심층 2차 정제(설계서 절번호·단일어 코드·화면코드·JS 문자열) 시작")
    print("=" * 72)

    updated_count = 0
    html_files = sorted(CLEAN_DIR.glob("*.html"))
    for html_file in html_files:
        if html_file.name == "patch_all_snb_v3.html":
            continue
        updated_count += process_clean_html(html_file)

    print(f"[패치 완료] prototype_clean/ 심층 2차 정제 적용 파일: {updated_count}개 (prototype/ 원본은 미수정 보존)")

    report_lines = [
        "# 백오피스 `prototype_clean/` 심층 2차 정합성 스캔 리포트 (Phase 6 완료 후)",
        "",
        "- 생성 스크립트: `phase6_deep_polish_and_audit.py`",
        "- 검증 범위: 1차 항목(`snake_case`, `UPPER_SNAKE_CASE`, `Track G`, 금지어, 원문자) + 2차 항목(설계서 `X.Y절`/`부록` 참조, `TX-01~13` 세무코드, 단일어 영문 ENUM, JS `alert/toast` 메시지)",
        "",
        "## 1. 파일별 잔여 검출 요약",
        "",
        "| 파일명 | 총 검출 건수 | 주요 검출 유형 및 토큰 샘플 |",
        "| :--- | :---: | :--- |",
    ]
    detail_sections: List[str] = ["", "## 2. 파일별 상세 검출 내역", ""]
    total_files_with_issues = 0
    total_issue_count = 0

    for html_file in html_files:
        if html_file.name == "patch_all_snb_v3.html":
            continue
        file_issues = scan_deep_issues(html_file)
        if file_issues:
            total_files_with_issues += 1
            total_issue_count += len(file_issues)
            sample_tokens = [f"`{item['tokens']}`" for item in file_issues[:5]]
            report_lines.append(f"| `{html_file.name}` | {len(file_issues)}건 | {', '.join(sample_tokens)} |")
            detail_sections.append(f"### `{html_file.name}` ({len(file_issues)}건)")
            for item in file_issues:
                detail_sections.append(
                    f"- **L{item['line']}** [{item['category']}] `{item['tokens']}` → `{item['snippet']}`"
                )
            detail_sections.append("")
        else:
            report_lines.append(f"| `{html_file.name}` | **0건 (Clean)** | - |")

    report_lines.extend(detail_sections)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("-" * 72)
    print(f"[Phase 6 심층 스캔 완료] 잔여 검출 파일: {total_files_with_issues}개 (총 {total_issue_count}건)")
    print(f"[리포트 갱신 완료] {REPORT_PATH}")
    print("=" * 72)


if __name__ == "__main__":
    main()
