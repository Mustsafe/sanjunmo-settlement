#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모닷컴 & 정산시스템 v4.0.0] 백오피스 정합성 정비 스크립트 — Phase 1
대상:
  1. prototype/ 및 prototype_clean/ 공통 정책 동기화 (레거시 금지어·폐지 화면 참조 제거)
  2. prototype_clean/ Phase 1 대상 파일 정밀 클린업:
     - common-snb.js (공통 좌측 내비게이션 스크립트)
     - 00_WORKFLOW_GUIDE_baseline.html (전체 업무 플로우 가이드)
     - ADMN-LOGIN-001_baseline.html (관리자·파트너 로그인 게이트)
     - ADMN-DASH-001_baseline.html (통합 대시보드 홈 / 매출·상품 통계)
  3. Phase 2~4 정밀 타겟팅을 위한 전 파일 잔여 오염원(변수명·코드값·과거 용어) 전수 스캔 리포트(CLEANUP_AUDIT_REPORT.md) 자동 생성

실행 방법 (저장소 루트에서 실행):
  python phase1_clean_and_audit.py
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent
PROTO_DIR = ROOT_DIR / "prototype"
CLEAN_DIR = ROOT_DIR / "prototype_clean"
REPORT_PATH = ROOT_DIR / "CLEANUP_AUDIT_REPORT.md"

# ---------------------------------------------------------------------------
# 1. 양방향(prototype/ & prototype_clean/) 공통 확정 정책 치환 사전
#    (되돌리기 금지: 기출문제 -> 빈출문제, 정오표 -> 교재 정답지, Vimeo -> StarPlayer+)
# ---------------------------------------------------------------------------
BOTH_POLICY_REPLACEMENTS: List[Tuple[str, str]] = [
    ("기출문제", "빈출문제"),
    ("기출특강", "빈출특강"),
    ("[기출]", "[빈출]"),
    ("정오표", "교재 정답지"),
    ("Vimeo", "StarPlayer+"),
]

# ---------------------------------------------------------------------------
# 2. prototype_clean/ 전용: 운영자 노출 화면 텍스트 치환 사전
#    (HTML 태그 내부 속성/스크립트 식별자는 건드리지 않고 텍스트 노드 및 title/placeholder만 정제)
# ---------------------------------------------------------------------------
CLEAN_UI_REPLACEMENTS: List[Tuple[str, str]] = [
    # 결번 및 설계서 메타 표기 제거/순화
    ("결번 ADMN-SETT-003 영구 제외 (16.2절)", "패키지 안분은 월간 정산(SETT-002) 통합 운영"),
    ("결번 ADMN-SETT-003 영구 제외", "월간 정산 통합 운영"),
    ("(SSOT v4.0.0 Baseline)", ""),
    ("SSOT v4.0.0 Baseline", "통합 운영 가이드"),
    ("8.3절 통합 연산 엔진(1~11단계)", "월간 정산 통합 연산 엔진(1~11단계)"),
    ("8.3절 통합 연산 엔진", "월간 정산 통합 연산 엔진"),
    ("(16.2절)", ""),
    ("(8.3절)", ""),
    ("(10.4절)", ""),
    ("Track G", ""),
    ("Track F", ""),

    # 1~11단계 정산 연산 파이프라인 영문 ENUM 병기/단독 노출 순화
    ("(CARRY_IN)", "(전월 이월)"),
    ("(ACCRUAL)", "(발생액 산출)"),
    ("(MMG_ADJ)", "(최저보장 보정)"),
    ("(DEDUCT)", "(환불·할인 공제)"),
    ("(SUPPORT_CAP)", "(지원금 한도)"),
    ("(PREPAY_OFFSET)", "(선급금 상계)"),
    ("(LUMPSUM_ADD)", "(약정·매절 가산)"),
    ("(PAYEE_SPLIT)", "(수취인 분할)"),
    ("(TAX: TX-01~TX-13)", "(세무 자동 판정)"),
    ("(TAX)", "(세무 판정)"),
    ("(CLAIM)", "(청구 검증)"),
    ("(PAYOUT)", "(지급·이체 확정)"),
    ("CARRY_IN", "전월 이월 승계"),
    ("ACCRUAL", "순 발생액 산출"),
    ("MMG_ADJ", "월 보장액 보정"),
    ("SUPPORT_CAP", "지원금 한도 캡"),
    ("PREPAY_OFFSET", "선급금 상한선 상계"),
    ("LUMPSUM_ADD", "비정기 약정·매절 가산"),
    ("PAYEE_SPLIT", "수취인 분할"),
    ("UNKNOWN_MISMATCH", "원인 미분류 불일치"),
    ("REVENUE_SHARE", "매출 비례 정산"),
    ("PENDING_REVIEW", "수동 검토 대기"),
    ("CONDITIONAL", "조건부 상계 허용"),
    ("UNCONDITIONAL", "무조건 상계 허용"),
    ("FORBIDDEN", "상계 불가"),

    # 게시판 / 메시지 / 권한 ENUM 순화
    ("(FREQ_EXAM)", ""),
    ("FREQ_EXAM", "빈출문제"),
    ("(ANSWER_SHEET)", ""),
    ("ANSWER_SHEET", "교재 정답지"),
    ("(COURSE_REVIEW)", ""),
    ("COURSE_REVIEW", "수강후기"),
    ("(PASS_ESSAY)", ""),
    ("PASS_ESSAY", "합격수기"),
    ("ROLE_SUPER_ADMIN", "최고 관리자"),
    ("ROLE_FINANCE_DIRECTOR", "재무 총괄 책임자"),
    ("ROLE_FINANCE_ADMIN", "재무·정산 관리자"),
    ("ROLE_CS_ADMIN", "CS·운영 관리자"),
    ("ROLE_CONTENT_ADMIN", "콘텐츠·상품 관리자"),
    ("ROLE_PARTNER_INST", "파트너 강사"),
    ("ROLE_PARTNER_COPYRIGHT", "교재 저작권자·출판사"),
    ("ROLE_PARTNER_3PL", "외부 물류(3PL)"),
    ("INSPECT_REQ", "검수중"),

    # DB 컬럼명 / 변수명(snake_case) 운영자 용어 순화
    ("payee_splits", "수취인 분할 비율"),
    ("payee_is_author", "저작권자 여부"),
    ("book_supply_type", "도서 공급 유형"),
    ("own_copyright_yn", "자사 저작권 여부"),
    ("is_internal", "자사 귀속 여부"),
    ("tax_type", "과세 유형"),
    ("goods_stock_log", "재고 변동 이력"),
    ("member_status", "회원 상태"),
    ("settlement_status", "정산 상태"),
    ("contract_type", "계약 유형"),
    ("supply_rate", "공급률"),
    ("royalty_rate", "인세율"),
    ("rs_rate", "정산 요율"),
]

# 정규식 기반 클린업 (텍스트 노드 전용)
CLEAN_TEXT_REGEXES: List[Tuple[re.Pattern, str]] = [
    # [마커 1], [마커 12] 등 설계서 마커 제거
    (re.compile(r"\[\s*마커\s*\d+\s*\]\s*"), ""),
    # 원문자 ①~⑳ 제거 (뒤따르는 공백 포함)
    (re.compile(r"[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\s*"), ""),
    # Track A~G 표기 제거
    (re.compile(r"\bTrack\s+[A-G]\b\s*[:·-]?\s*", re.IGNORECASE), ""),
    # (TX-01 ~ TX-13) 또는 TX-01~TX-13 단독 코드 표기 순화
    (re.compile(r"\bTX-01\s*[~∼-]\s*TX-13\b"), "세무 판정 기준(13종)"),
    # BK-REQ-* 가채번 코드 표기 순화
    (re.compile(r"`?BK-REQ-\*`?"), "출간 전 도서 가채번"),
    # 다중 공백 정리 (줄바꿈 유지)
    (re.compile(r"[ \t]{2,}"), " "),
]

PHASE1_HTML_FILES = [
    "00_WORKFLOW_GUIDE_baseline.html",
    "ADMN-LOGIN-001_baseline.html",
    "ADMN-DASH-001_baseline.html",
]


def clean_html_text_nodes_only(html_content: str, is_clean_dir: bool = True) -> Tuple[str, int]:
    """
    <script>, <style> 블록과 HTML 태그 속성(id, class, href, onclick 등)을 완벽히 보존하면서
    화면에 렌더링되는 텍스트 노드와 UI 속성(placeholder, title)만 안전하게 치환합니다.
    """
    change_count = 0

    # 1) <script>...</script> 및 <style>...</style> 임시 마스킹 보호
    protected_blocks: List[str] = []

    def _protect(match: re.Match) -> str:
        idx = len(protected_blocks)
        protected_blocks.append(match.group(0))
        return f"___PROTECTED_BLOCK_{idx}___"

    masked = re.sub(
        r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)",
        _protect,
        html_content,
        flags=re.IGNORECASE,
    )

    # 2) 태그 내부의 title="", placeholder="" 속성값만 선별 정제
    def _clean_ui_attr(attr_match: re.Match) -> str:
        nonlocal change_count
        prefix, quote, val = attr_match.group(1), attr_match.group(2), attr_match.group(3)
        orig_val = val
        for src, dst in BOTH_POLICY_REPLACEMENTS:
            val = val.replace(src, dst)
        if is_clean_dir:
            for src, dst in CLEAN_UI_REPLACEMENTS:
                val = val.replace(src, dst)
            for pattern, repl in CLEAN_TEXT_REGEXES:
                val = pattern.sub(repl, val)
        if val != orig_val:
            change_count += 1
        return f"{prefix}{quote}{val}{quote}"

    def _process_tag(tag_match: re.Match) -> str:
        tag_str = tag_match.group(0)
        return re.sub(
            r'(\b(?:title|placeholder|data-tooltip)\s*=\s*)(["\'])(.*?)\2',
            _clean_ui_attr,
            tag_str,
            flags=re.IGNORECASE | re.DOTALL,
        )

    masked = re.sub(r"<[^>]+>", _process_tag, masked)

    # 3) 태그 바깥의 순수 텍스트 노드(>와 < 사이)만 정제
    def _process_text_node(text_match: re.Match) -> str:
        nonlocal change_count
        text = text_match.group(1)
        if not text.strip() or "___PROTECTED_BLOCK_" in text:
            return text_match.group(0)
        orig_text = text
        for src, dst in BOTH_POLICY_REPLACEMENTS:
            text = text.replace(src, dst)
        if is_clean_dir:
            for src, dst in CLEAN_UI_REPLACEMENTS:
                text = text.replace(src, dst)
            for pattern, repl in CLEAN_TEXT_REGEXES:
                text = pattern.sub(repl, text)
        if text != orig_text:
            change_count += 1
        return f">{text}<"

    masked = re.sub(r">([^<]+)<", _process_text_node, masked)

    # 4) 보호된 <script>/<style>/주석 복원 (단, clean 폴더의 HTML 주석 내 Track G 등은 제거)
    for idx, block in enumerate(protected_blocks):
        if is_clean_dir and block.startswith("<!--"):
            block = re.sub(r"\bTrack\s+[A-G]\b", "", block, flags=re.IGNORECASE)
        masked = masked.replace(f"___PROTECTED_BLOCK_{idx}___", block)

    return masked, change_count


def patch_common_snb_js(snb_path: Path, is_clean_dir: bool) -> int:
    """
    common-snb.js 내 레거시 주석(Track G 등)을 정리하고,
    prototype_clean/common-snb.js의 경우 런타임 DOM 클리너 사전을 대폭 보강하며
    placeholder/title 속성 정제 및 MutationObserver 실시간 감시를 추가합니다.
    """
    if not snb_path.exists():
        return 0

    content = snb_path.read_text(encoding="utf-8")
    orig = content

    # 공통 정책 용어 동기화
    for src, dst in BOTH_POLICY_REPLACEMENTS:
        content = content.replace(src, dst)

    if is_clean_dir:
        # 주석에 남아있는 Track G / Track F 문구 제거 (정규식 패턴 내부 문자열은 유지)
        content = re.sub(r"(//.*?)Track\s+[A-G]", r"\1", content)

        # 추가 런타임 치환 규칙 주입 (아직 주입되지 않은 경우에만 1회 주입)
        injection_marker = "/* [PHASE1_CLEAN_ENHANCEMENT_V4] */"
        if injection_marker not in content:
            extra_map_entries = {
                "CARRY_IN": "전월 이월 승계",
                "ACCRUAL": "순 발생액 산출",
                "MMG_ADJ": "월 보장액 보정",
                "SUPPORT_CAP": "지원금 한도 캡",
                "PREPAY_OFFSET": "선급금 상한선 상계",
                "LUMPSUM_ADD": "비정기 약정·매절 가산",
                "PAYEE_SPLIT": "수취인 분할",
                "UNKNOWN_MISMATCH": "원인 미분류 불일치",
                "REVENUE_SHARE": "매출 비례 정산",
                "PENDING_REVIEW": "수동 검토 대기",
                "CONDITIONAL": "조건부 상계 허용",
                "UNCONDITIONAL": "무조건 상계 허용",
                "FORBIDDEN": "상계 불가",
                "FREQ_EXAM": "빈출문제",
                "ANSWER_SHEET": "교재 정답지",
                "COURSE_REVIEW": "수강후기",
                "PASS_ESSAY": "합격수기",
                "ROLE_PARTNER_INST": "파트너 강사",
                "ROLE_PARTNER_COPYRIGHT": "교재 저작권자·출판사",
                "ROLE_PARTNER_3PL": "외부 물류(3PL)",
                "payee_splits": "수취인 분할 비율",
                "payee_is_author": "저작권자 여부",
                "book_supply_type": "도서 공급 유형",
                "own_copyright_yn": "자사 저작권 여부",
                "is_internal": "자사 귀속 여부",
                "tax_type": "과세 유형",
                "goods_stock_log": "재고 변동 이력",
                "member_status": "회원 상태",
                "SSOT v4.0.0 Baseline": "통합 운영 가이드",
            }
            extra_js = f"""
{injection_marker}
(function enhanceCleanDomTranslator() {{
  const EXTRA_MAP = {json.dumps(extra_map_entries, ensure_ascii=False, indent=2)};
  const MARKER_RE = /\\[\\s*마커\\s*\\d+\\s*\\]\\s*/g;
  const CIRCLED_RE = /[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\\s*/g;
  const TRACK_RE = /\\bTrack\\s+[A-G]\\b\\s*[:·-]?\\s*/gi;

  function cleanString(str) {{
    if (!str || typeof str !== 'string') return str;
    let out = str;
    for (const [k, v] of Object.entries(EXTRA_MAP)) {{
      if (out.includes(k)) out = out.split(k).join(v);
    }}
    out = out.replace(MARKER_RE, '').replace(CIRCLED_RE, '').replace(TRACK_RE, '');
    return out;
  }}

  function runEnhancedClean(root) {{
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while ((node = walker.nextNode())) {{
      const parentTag = node.parentNode && node.parentNode.tagName;
      if (parentTag === 'SCRIPT' || parentTag === 'STYLE' || parentTag === 'CODE') continue;
      const cleaned = cleanString(node.nodeValue);
      if (cleaned !== node.nodeValue) node.nodeValue = cleaned;
    }}
    if (root.querySelectorAll) {{
      root.querySelectorAll('[placeholder],[title],[data-tooltip]').forEach(el => {{
        ['placeholder', 'title', 'data-tooltip'].forEach(attr => {{
          const val = el.getAttribute(attr);
          if (val) {{
            const cleaned = cleanString(val);
            if (cleaned !== val) el.setAttribute(attr, cleaned);
          }}
        }});
      }});
    }}
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    runEnhancedClean(document.body);
    let timer = null;
    const observer = new MutationObserver(() => {{
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => runEnhancedClean(document.body), 80);
    }});
    observer.observe(document.body, {{ childList: true, subtree: true }});
  }});
}})();
"""
            content = content.rstrip() + "\n" + extra_js

    if content != orig:
        snb_path.write_text(content, encoding="utf-8")
        return 1
    return 0


def scan_visible_issues(file_path: Path) -> List[Dict[str, str]]:
    """
    HTML 파일의 렌더링 텍스트 노드(script/style 제외)에서
    남아 있는 오염원(snake_case 변수명, UPPER_SNAKE_CASE 코드값, Track G, 폐지 화면 코드 등)을 검출합니다.
    """
    issues: List[Dict[str, str]] = []
    raw = file_path.read_text(encoding="utf-8")

    # script / style 제거 후 라인별 텍스트만 추출
    stripped = re.sub(
        r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)",
        lambda m: "\n" * m.group(0).count("\n"),
        raw,
        flags=re.IGNORECASE,
    )

    patterns = [
        ("레거시_트랙_표기", re.compile(r"\bTrack\s+[A-G]\b", re.IGNORECASE)),
        ("금지어_기출_정오표", re.compile(r"(기출문제|기출특강|정오표)")),
        ("폐지화면_코드", re.compile(r"\bADMN-(?:SETT-003|ORD-003)\b")),
        ("설계마커_원문자", re.compile(r"(\[\s*마커\s*\d+\s*\]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮])")),
        ("DB변수명_snake_case", re.compile(r"\b[a-z]{2,}(?:_[a-z0-9]{2,})+\b")),
        ("영문코드_UPPER_SNAKE", re.compile(r"\b[A-Z]{2,}(?:_[A-Z0-9]{2,})+\b")),
    ]

    for line_no, line in enumerate(stripped.splitlines(), start=1):
        # 태그 제거 후 순수 텍스트만 추출
        text_only = re.sub(r"<[^>]+>", " ", line).strip()
        if not text_only:
            continue
        for category, pat in patterns:
            matches = pat.findall(text_only)
            if matches:
                # HTML 엔티티나 일반 CSS/레이아웃 용어 제외
                filtered = [
                    m for m in matches
                    if m not in {"UTF_8", " utf_8", "no_opener"}
                ]
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
    print("[Phase 1] 백오피스 공통 코어 & 워크플로우 가이드 정비 및 전수 스캔 시작")
    print("=" * 72)

    # 1. common-snb.js 패치 (prototype/ & prototype_clean/)
    p_snb = patch_common_snb_js(PROTO_DIR / "common-snb.js", is_clean_dir=False)
    c_snb = patch_common_snb_js(CLEAN_DIR / "common-snb.js", is_clean_dir=True)
    print(f"[완료] common-snb.js 패치: prototype({p_snb}건), prototype_clean({c_snb}건)")

    # 2. Phase 1 대상 HTML 파일 정제 (prototype/ 정책 동기화 + prototype_clean/ UI 클린업)
    for fname in PHASE1_HTML_FILES:
        p_file = PROTO_DIR / fname
        c_file = CLEAN_DIR / fname

        if p_file.exists():
            new_p, cnt_p = clean_html_text_nodes_only(p_file.read_text(encoding="utf-8"), is_clean_dir=False)
            if cnt_p > 0:
                p_file.write_text(new_p, encoding="utf-8")
            print(f"  - prototype/{fname}: 정책 용어 동기화 {cnt_p}개 영역")

        if c_file.exists():
            new_c, cnt_c = clean_html_text_nodes_only(c_file.read_text(encoding="utf-8"), is_clean_dir=True)
            if cnt_c > 0:
                c_file.write_text(new_c, encoding="utf-8")
            print(f"  - prototype_clean/{fname}: 운영자 UI 클린업 {cnt_c}개 영역")

    # 3. 전체 HTML 파일(Phase 1~4) 잔여 오염원 전수 스캔 및 리포트 생성
    report_lines = [
        "# 백오피스 `prototype_clean/` 전수 정합성 스캔 리포트",
        "",
        "- 생성 스크립트: `phase1_clean_and_audit.py`",
        "- 목적: Phase 1 정제 결과 검증 및 Phase 2~4 도메인별 잔여 변수명(`snake_case`)·영문 ENUM(`UPPER_SNAKE_CASE`)·과거 용어(`Track G` 등) 타겟팅",
        "",
        "## 1. 파일별 잔여 검출 요약",
        "",
        "| 파일명 | 총 검출 건수 | 주요 검출 유형 및 토큰 샘플 |",
        "| :--- | :---: | :--- |",
    ]

    detail_sections: List[str] = ["", "## 2. 파일별 상세 검출 내역 (라인 번호 기준)", ""]
    total_files_with_issues = 0
    total_issue_count = 0

    html_files = sorted(CLEAN_DIR.glob("*.html"))
    for html_file in html_files:
        if html_file.name == "patch_all_snb_v3.html":
            continue
        file_issues = scan_visible_issues(html_file)
        if file_issues:
            total_files_with_issues += 1
            total_issue_count += len(file_issues)
            sample_tokens = []
            for item in file_issues[:5]:
                sample_tokens.append(f"`{item['tokens']}`")
            sample_str = ", ".join(sample_tokens)
            report_lines.append(f"| `{html_file.name}` | {len(file_issues)}건 | {sample_str} |")

            detail_sections.append(f"### `{html_file.name}` ({len(file_issues)}건)")
            for item in file_issues[:30]:
                detail_sections.append(
                    f"- **L{item['line']}** [{item['category']}] `{item['tokens']}` → `{item['snippet']}`"
                )
            if len(file_issues) > 30:
                detail_sections.append(f"- ... 외 {len(file_issues) - 30}건")
            detail_sections.append("")
        else:
            report_lines.append(f"| `{html_file.name}` | **0건 (Clean)** | - |")

    report_lines.extend(detail_sections)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("-" * 72)
    print(f"[전수 스캔 완료] 대상 HTML {len(html_files)}개 중 잔여 검출 파일: {total_files_with_issues}개 (총 {total_issue_count}건)")
    print(f"[리포트 저장] {REPORT_PATH}")
    print("=" * 72)


if __name__ == "__main__":
    main()
