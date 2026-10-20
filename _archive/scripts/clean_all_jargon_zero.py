#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] JARGON_SCAN_REPORT 기반 내부 암호 · 금지어 · 원문자 일괄 클린업 (clean_all_jargon_zero.py)
- 대상: prototype/ (금지어·진도율·원문자 교정) 및 prototype_clean/ (기획서 장절·C/D코드·Pipeline·DB컬럼명 추가 제거)
- 안전장치: HTML 태그 속성(id, class, value, onclick 등)은 건드리지 않고 가시 텍스트 및 안전한 한글 리터럴만 치환
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

# 1. prototype/ & prototype_clean/ 공통 교정 (금지어 '기출', 진도율 80%->90%, 원문자 제거)
COMMON_FIXES = [
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


def apply_common_fixes(text: str) -> str:
    for old, new in COMMON_FIXES:
        text = text.replace(old, new)
    for c_char, rep in CIRCLED_MAP.items():
        text = text.replace(c_char, rep)
    # 남은 단독 '기출'도 '빈출'로 교정
    text = text.replace("기출", "빈출")
    return text


# 2. prototype_clean/ 전용: 운영자 화면에서 기획서 장·절, C/D 케이스 코드, Pipeline, DB 컬럼명 제거
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


def strip_spec_jargon_in_text(s: str) -> str:
    # 1) Pipeline 및 P코드 치환
    for old, new in PIPELINE_MAP:
        s = s.replace(old, new)

    # 2) DB 스네이크케이스 치환
    for old, new in DB_COL_MAP:
        s = s.replace(old, new)

    # 3) C-01~04, D-1~16 코드 제거/정리
    s = re.sub(r"\s*·?\s*SETT-006\s+C-0[1-4]", "", s)
    s = re.sub(r"\(\s*ADMN-SETT-006\s+C-0[1-4]\s*\)", "(합격환급 정산 연동)", s)
    s = re.sub(r"\(\s*C-0[1-4][^)]*\)", "", s)
    s = re.sub(r"\(\s*(?:QA\s*|부록\s*)?D-(?:1[0-6]|[1-9])[^)]*\)", "", s)
    s = re.sub(r"\bC-0[1-4]\b", "정산규칙", s)
    s = re.sub(r"\bD-(?:1[0-6]|[1-9])\b", "검증규칙", s)

    # 4) 제N장, N.N절 제거
    # 먼저 괄호 안에 장/절만 있는 경우 통째로 제거: 예: (5.2절), (제6장 6.1~6.6절), (합의서 6.1절 · 8.1절)
    s = re.sub(r"\(\s*(?:합의서\s*|정본\s*|0[1-4]권\s*)?(?:제\s*\d+\s*장\s*)?(?:\d+(?:\.\d+)+(?:~\d+(?:\.\d+)+)?\s*절[\s·,~]*)+(?:정본|기준|참조|연동)?\s*\)", "", s)
    s = re.sub(r"\b제\s*\d+\s*장\s*\d+(?:\.\d+)*\s*절\b", "정산 기준", s)
    s = re.sub(r"\b제\s*\d+\s*장\b", "정산 기준", s)
    s = re.sub(r"\b\d+(?:\.\d+)+(?:~\d+(?:\.\d+)+)?\s*절\b", "정산 기준", s)

    # 5) 빈 괄호나 어색한 구분자 정리
    s = re.sub(r"\(\s*[·,\s]+\s*\)", "", s)
    s = re.sub(r"\(\s*\)", "", s)
    return s


def clean_html_for_prototype_clean(html: str) -> str:
    """
    1) HTML 태그(<...>)는 보호하고 텍스트 노드에 strip_spec_jargon_in_text 적용
    2) <script> 내부에서는 한글이 포함된 문자열 리터럴("...", '...', `...`) 내부의 설명 문구만 안전하게 정제
    """
    def clean_script_block(match):
        full_script = match.group(0)
        # 한글이 1글자 이상 포함된 따옴표/백틱 문자열만 정제 (순수 영문 식별자/키값은 절대 보존)
        def replace_kr_literal(m):
            quote = m.group(1)
            body = m.group(2)
            if re.search(r"[가-힣]", body):
                body = strip_spec_jargon_in_text(body)
            return f"{quote}{body}{quote}"

        full_script = re.sub(r'(["\'`])((?:\\.|(?!\1)[^\\])*?)\1', replace_kr_literal, full_script)
        return full_script

    # script 블록 내부 한글 리터럴 정제
    html = re.sub(r"(?is)<script\b[^>]*>.*?</script>", clean_script_block, html)

    # script, style 및 HTML 태그 보호 후 순수 DOM 텍스트 노드 정제
    protected = []
    def protect(m):
        protected.append(m.group(0))
        return f"__PROT_{len(protected)-1}__"

    temp = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", protect, html)
    temp = re.sub(r"(?s)<[^>]+>", protect, temp)

    temp = strip_spec_jargon_in_text(temp)

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
