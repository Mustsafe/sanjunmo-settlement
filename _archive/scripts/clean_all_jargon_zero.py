#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] JARGON_SCAN_REPORT 기반 내부 암호 · 금지어 · 원문자 안전 클린업 (v2 - JS 100% 보호)
- 수정 사항: <script> 및 <style> 블록을 정규식 치환에서 100% 보호하여 JS 함수 괄호() 파손 원천 차단
"""

import re
from pathlib import Path

PROTO_DIR = Path("prototype")
CLEAN_DIR = Path("prototype_clean")

CIRCLED_MAP = {
    "①": "[1]", "②": "[2]", "③": "[3]", "④": "[4]", "⑤": "[5]",
    "⑥": "[6]", "⑦": "[7]", "⑧": "[8]", "⑨": "[9]", "⑩": "[10]",
    "⑪": "[11]", "⑫": "[12]", "⑬": "[13]", "⑭": "[14]",
}

# JS 코드 문법(괄호/따옴표)에 전혀 영향을 주지 않는 순수 한글 고정 단어 치환
SAFE_LITERAL_FIXES = [
    ("기출특강", "빈출특강"),
    ("기출문제", "빈출문제"),
    ("이론+기출", "이론+빈출"),
    ("기출복원", "빈출복원"),
    ("기출 풀이", "빈출 풀이"),
    ("기출 해설", "빈출 해설"),
    ("러닝타임 80% 이상", "러닝타임 90% 이상"),
    ("재생시간 80% 이상", "재생시간 90% 이상"),
    ("출석률 88.0% (기준 80% 충족)", "진도율 92.4% (기준 90% 충족)"),
    ("기준 80% 충족", "기준 90% 충족"),
]

PIPELINE_MAP = [
    ("온라인 강좌 수익배분(Pipeline 1.1)", "온라인 강좌 수익배분"),
    ("자사 발행 도서 인세(Pipeline 2.1)", "자사 발행 도서 인세"),
    ("위탁 도서 판매대금 정산(Pipeline 2.2)", "위탁 도서 판매대금 정산"),
    ("일반 상품 판매매출(Pipeline 2.3)", "일반 상품 판매매출"),
    ("매출연동 개발지원금(Pipeline 5.1)", "매출연동 개발지원금"),
    ("매출연동 지원금(Pipeline 5.1)", "매출연동 개발지원금"),
    ("매출연동(Pipeline 5.1)", "매출연동 지원금"),
    ("(Pipeline 1.1)", "(강좌 수익배분)"),
    ("(Pipeline 2.1)", "(도서 인세)"),
    ("(Pipeline 2.2)", "(위탁도서 정산)"),
    ("(Pipeline 2.3)", "(일반상품 매출)"),
    ("(Pipeline 5.1)", "(개발지원금)"),
    ("Pipeline 1.1", "강좌 수익배분"),
    ("Pipeline 2.1", "도서 인세"),
    ("Pipeline 2.2", "위탁도서 정산"),
    ("Pipeline 2.3", "일반상품 매출"),
    ("Pipeline 5.1", "개발지원금"),
    ("P1.1", "강좌정산"),
    ("P2.1", "도서인세"),
    ("P2.2", "위탁정산"),
    ("P2.3", "일반상품"),
    ("P5.1", "개발지원금"),
]

DB_COL_MAP = [
    ("own_copyright_yn = true", "자사 저작권 보유"),
    ("own_copyright_yn=true", "자사 저작권 보유"),
    ("own_copyright_yn = false", "외부 저작권"),
    ("own_copyright_yn=false", "외부 저작권"),
    ("(own_copyright_yn)", ""),
    ("own_copyright_yn", "자사저작권여부"),
    ("(contract_id)", ""),
    ("contract_id", "계약번호"),
    ("(order_item_id)", ""),
    ("order_item_id", "품목번호"),
    ("origin_settlement_id", "원정산번호"),
    ("rights_holder_id", "권리자번호"),
    ("payee_id", "수취인번호"),
    ("agreement_id = NULL", "별도 약정 없음"),
    ("agreement_id", "약정번호"),
]


def apply_common_fixes(text: str) -> str:
    for old, new in SAFE_LITERAL_FIXES:
        text = text.replace(old, new)
    for c_char, rep in CIRCLED_MAP.items():
        text = text.replace(c_char, rep)
    text = text.replace("기출", "빈출")
    return text


def strip_spec_jargon_in_text(s: str) -> str:
    for old, new in PIPELINE_MAP:
        s = s.replace(old, new)
    for old, new in DB_COL_MAP:
        s = s.replace(old, new)

    s = re.sub(r"\s*·?\s*SETT-006\s+C-0[1-4]", "", s)
    s = re.sub(r"\(\s*ADMN-SETT-006\s+C-0[1-4]\s*\)", "(합격환급 정산 연동)", s)
    s = re.sub(r"\(\s*C-0[1-4][^)]*\)", "", s)
    s = re.sub(r"\(\s*(?:QA\s*|부록\s*)?D-(?:1[0-6]|[1-9])[^)]*\)", "", s)
    s = re.sub(r"\bC-0[1-4]\b", "정산규칙", s)
    s = re.sub(r"\bD-(?:1[0-6]|[1-9])\b", "검증규칙", s)

    s = re.sub(r"\(\s*(?:합의서\s*|정본\s*|0[1-4]권\s*)?(?:제\s*\d+\s*장\s*)?(?:\d+(?:\.\d+)+(?:~\d+(?:\.\d+)+)?\s*절[\s·,~]*)+(?:정본|기준|참조|연동)?\s*\)", "", s)
    s = re.sub(r"\b제\s*\d+\s*장\s*\d+(?:\.\d+)*\s*절\b", "정산 기준", s)
    s = re.sub(r"\b제\s*\d+\s*장\b", "정산 기준", s)
    s = re.sub(r"\b\d+(?:\.\d+)+(?:~\d+(?:\.\d+)+)?\s*절\b", "정산 기준", s)

    s = re.sub(r"\(\s*[·,\s]+\s*\)", "", s)
    s = re.sub(r"\(\s*\)", "", s)
    return s


def clean_html_for_prototype_clean(html: str) -> str:
    """
    <script> 및 <style>은 일체의 JS 코드 훼손을 방지하기 위해 100% 완전 보호하고,
    순수 DOM 가시 텍스트 노드에만 strip_spec_jargon_in_text 적용
    """
    protected = []

    def protect(m):
        protected.append(m.group(0))
        return f"__PROT_{len(protected)-1}__"

    # 1. script와 style은 1바이트도 정규식 건드리지 않고 통째로 보호 (JS 파괴 원천 차단)
    temp = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", protect, html)
    # 2. HTML 태그(<...>) 보호
    temp = re.sub(r"(?s)<[^>]+>", protect, temp)
    # 3. 안전한 순수 DOM 텍스트 노드만 기획서 암호/장절/코드 정제
    temp = strip_spec_jargon_in_text(temp)
    # 4. 보호된 태그 및 스크립트 복원
    for i in range(len(protected) - 1, -1, -1):
        temp = temp.replace(f"__PROT_{i}__", protected[i])

    return temp


def main():
    p_cnt = 0
    c_cnt = 0

    for f in sorted(PROTO_DIR.glob("*.html")):
        orig = f.read_text(encoding="utf-8")
        updated = apply_common_fixes(orig)
        if updated != orig:
            f.write_text(updated, encoding="utf-8")
            p_cnt += 1

    for f in sorted(CLEAN_DIR.glob("*.html")):
        orig = f.read_text(encoding="utf-8")
        updated = apply_common_fixes(orig)
        updated = clean_html_for_prototype_clean(updated)
        if updated != orig:
            f.write_text(updated, encoding="utf-8")
            c_cnt += 1

    print(f"[클린업 완료] prototype/: {p_cnt}개 파일, prototype_clean/: {c_cnt}개 파일 정제됨.")


if __name__ == "__main__":
    main()
