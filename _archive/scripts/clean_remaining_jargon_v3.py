#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 잔여 DOM 35건 + JS 내부 고정 문자열 핀셋 클린업 (clean_remaining_jargon_v3.py)
- 대상: prototype/ 및 prototype_clean/ 양쪽 모두 동기화 적용
- JS 문법 파손 위험이 있는 정규식(빈 괄호 삭제 등)을 <script>에 절대 쓰지 않고,
  검증된 고정 문자열(Exact String) 1:1 치환만으로 남은 내부 암호와 중복어를 제거합니다.
"""

import re
from pathlib import Path

TARGET_DIRS = [Path("prototype"), Path("prototype_clean")]

EXACT_SAFE_REPLACEMENTS = [
    # 중복 번역어(DUP_PAREN) 제거
    ("개발지원금(개발지원금)", "개발지원금"),
    ("개발지원금 (개발지원금)", "개발지원금"),
    ("정산 기준 · 정산 기준", "정산 기준"),
    # <script> 및 DOM 내 Pipeline 표기 정리
    ("온라인 강좌 수익배분 (Pipeline 1.1)", "온라인 강좌 수익배분"),
    ("온라인 강좌 수익배분(Pipeline 1.1)", "온라인 강좌 수익배분"),
    ("자사 발행 도서 인세 (Pipeline 2.1)", "자사 발행 도서 인세"),
    ("자사 발행 도서 인세(Pipeline 2.1)", "자사 발행 도서 인세"),
    ("위탁 도서 판매대금 정산 (Pipeline 2.2 · 수수료 차감지급)", "위탁 도서 판매대금 정산 (수수료 차감지급)"),
    ("위탁 도서 판매대금 정산 (Pipeline 2.2)", "위탁 도서 판매대금 정산"),
    ("위탁 도서 판매대금(Pipeline 2.2)", "위탁 도서 판매대금"),
    ("위탁 정산(Pipeline 2.2)", "위탁 정산"),
    ("위탁정산 분리(Pipeline 2.2)", "위탁정산 분리"),
    ("일반 상품 판매매출 Pipeline 2.3", "일반 상품 판매매출"),
    ("일반 상품 판매매출(Pipeline 2.3)", "일반 상품 판매매출"),
    ("매출연동 개발지원금 (Pipeline 5.1)", "매출연동 개발지원금"),
    ("매출연동 개발지원금(Pipeline 5.1)", "매출연동 개발지원금"),
    ("매출연동(Pipeline 5.1)", "매출연동"),
    ("개발지원금(Pipeline 5.1)", "개발지원금"),
    ("개발지원금 (Pipeline 5.1)", "개발지원금"),
    ("Pipeline 5.1 매출연동 약정", "매출연동 지원금 약정"),
    ("Pipeline 5.1 (R/S 1회)", "매출연동 지원금 (1회)"),
    ("Pipeline 5.1 전용 구분", "개발지원금 전용 구분"),
    ("Pipeline 2.2로 별도 정산", "위탁 판매대금으로 별도 정산"),
    ("· Pipeline 2.3", "· 일반상품 매출"),
    ("(Pipeline 1.1)", "(강좌 수익배분)"),
    ("(Pipeline 2.1)", "(도서 인세)"),
    ("(Pipeline 2.2)", "(위탁도서 정산)"),
    ("(Pipeline 2.3)", "(일반상품 매출)"),
    ("(Pipeline 5.1)", "(개발지원금)"),
    ("정산 입력 구분 (Pipeline)", "정산 입력 구분"),
    ("적용 정산 조항 (Pipeline)", "적용 정산 조항"),
    (" Pipeline 5.1 ", " 개발지원금 "),
    # <script> 및 DOM 내 DB 컬럼명 정리
    ("(own_copyright_yn = true)", "(자사 저작권 보유)"),
    ("(own_copyright_yn=true)", "(자사 저작권 보유)"),
    ("own_copyright_yn = true", "자사 저작권 보유"),
    ("own_copyright_yn=true", "자사 저작권 보유"),
    ("users.cafe_member_id IS NOT NULL", "산준모 카페 ID 등록 완료"),
    ("settlement_recipient_id", "정산수취인번호"),
    ("유효 계약(contract_id)", "유효 계약"),
    ("바인딩 계약 (contract_id)", "바인딩 계약"),
    ("바인딩 계약 선택 (contract_id NOT NULL)", "바인딩 계약 선택 (필수)"),
    # <script> 및 DOM 내 D-코드 / C-코드 / 장절 문구 정리
    ("(부록 D-12)", ""),
    ("· 부록 D-12", ""),
    ("(D-15·D-16)", ""),
    ("· QA D-11", ""),
    (", D-11)", ")"),
    ("[QA D-13 검증 완료] ", ""),
    ("D-12 · 17장 · 6장", "정산 감사 기준"),
    ("USER-007 · 3.5절", "민감정보 보호 기준"),
    ("통합 상세 설계서 3.2.2절", "통합 상세 설계서 기준"),
    ("8.2절 · 24시간 기한", "24시간 입금 기한"),
    ("5.5절 우편번호 판정", "도서산간 우편번호 판정"),
    ("8.1절 연동", "도서정가제 연동"),
    ("16.1절 · 정산 기준 필수 규격", "정산 기준 필수 규격"),
    ("7.4절 carryover_ledger", "이월 원장"),
    ("7.4절 연속성 등식:", "이월 잔액 연속성 등식:"),
    ("제9장 · 정산 기준 매트릭스", "세무 판정 매트릭스"),
    ("10.4절 도서 공급형태 오등록 규칙:", "도서 공급형태 정정 규칙:"),
    ("16.1절 · D-1", "권리 승계 기준"),
    ("5.3절 하드락", "선급금 상계 보호"),
    ("Case 7 / 검증규칙 / D-2", "공동 계약 분할 검증"),
    ("4.1절 / 13.1절", "원 단위 절사 및 역산 기준"),
    ("5.3절 상호 차단", "선급금 미상계 시 분할 차단"),
    ("17.5절 하드락", "국세청 과세유형 검증"),
    ("제18장 정산 기준", "내부 정산 손익 기준"),
    ("제3장 3.2절", "개인정보 보호 기준"),
    ("제14장 정산 기준", "정산 마감 기준"),
    ("SSOT: 02권 정산 기준 8.3절", "통합 정산 1~11단계 연산 기준"),
    ("제6장 정산 기준", "도서 정산 기준"),
    (" (6.5절)", ""),
    (" (6.6절 · 8.3절 9단계)", ""),
    (" (7.3~7.4절)", ""),
    (" (8.3절 SSOT 정본)", ""),
    ("[6.5절 과세표준", "[과세표준"),
    (" (7.3절)", ""),
    (" (3.4절 · TTL 30초)", " (30초 열람 제한)"),
    (" (4.3절)", ""),
    (" (4.1절 · Case 7)", ""),
    (" (7.2절)", ""),
    (" (17.5절)", ""),
    (" (5.2절)", ""),
    (" (3.5절)", ""),
    (" (16.1절)", ""),
    ("· 3.3절)", ")"),
    (" (6.2절)", ""),
    ("[6.4절 · ", "["),
    (" (5.2절 · 7.2절)", ""),
    ("[7.2절] ", ""),
    ("국세청 API 연동(제17장)", "국세청 API 연동"),
    ("[7.0절 마감 상태별 인입 통제]", "[마감 상태별 인입 통제]"),
    ("[7.2절 담당자 수기 소명형 검수 규칙]", "[담당자 수기 소명형 검수 규칙]"),
    ("기획서 4.2절 정책에 따라 ", ""),
    ("기획서 4.2절에 따라 ", ""),
    ("(4.2절)", ""),
    ("(제6장 6.1절)", ""),
    ("(5.2절)", ""),
]


def clean_dom_text_nodes_only(html: str) -> str:
    """<script>와 <style>, HTML 태그(<...>)를 100% 보호한 상태에서 DOM 텍스트의 잔여 N.N절, 제N장 제거"""
    protected = []

    def protect(m):
        protected.append(m.group(0))
        return f"__PROT_{len(protected)-1}__"

    temp = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", protect, html)
    temp = re.sub(r"(?s)<[^>]+>", protect, temp)

    temp = re.sub(r"\b\d+(?:\.\d+)+\s*절\b", "정산 기준", temp)
    temp = re.sub(r"\b제\s*\d+\s*장\b", "정산 기준", temp)

    for i in range(len(protected) - 1, -1, -1):
        temp = temp.replace(f"__PROT_{i}__", protected[i])

    return temp


def main():
    for folder in TARGET_DIRS:
        if not folder.exists():
            continue
        modified = 0
        for f in sorted(folder.glob("*.html")):
            orig = f.read_text(encoding="utf-8")
            txt = orig

            for old, new in EXACT_SAFE_REPLACEMENTS:
                txt = txt.replace(old, new)

            txt = clean_dom_text_nodes_only(txt)

            if txt != orig:
                f.write_text(txt, encoding="utf-8")
                modified += 1

        print(f"[핀셋 클린업 완료] {folder}/ 내 {modified}개 파일 정제 완료.")


if __name__ == "__main__":
    main()
