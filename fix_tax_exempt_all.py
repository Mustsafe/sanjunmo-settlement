#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 인터넷강의(교육용역 면세) + 교재(도서 면세) 과세 오표기 전수 교정 스크립트 v2 (심층 완결본)
- 대상 폴더: prototype/, prototype_clean/
- 핵심 교정:
  1) ADMN-ORD-001:
     - 강좌 라인의 '과세 10%' -> '교육용역 면세 0%' (ORDERS_DATA 및 직권부여 모달, 상세 테이블 전수 교정)
     - 강좌+교재 주문의 'MIXED' -> 'EXEMPT (교육·도서 통합면세)'
     - detailExemptionBadge 헤더 표기 일원화
  2) ADMN-PROD-003:
     - 단과 강좌 '과세 (VAT 10% 포함 · 온라인 교육용역)' -> '면세 (VAT 0% · 원격평생교육시설 온라인 교육용역)'
     - 판매가 입력 단위 '원 (VAT 포함)' -> '원 (교육면세 VAT 0%)'
     - 과세 구분 배지 '과세 상품 (부가세 10% 포함 · 온라인 단과 강좌 고정)' -> '면세 상품 (VAT 0% · 원격평생교육시설 온라인 단과 강좌 고정)'
  3) ADMN-PROD-005:
     - 패키지 상세 '과세 240,000원 + 면세 72,000원' -> '교육면세 240,000원 + 도서면세 72,000원'
     - '(VAT 10% 포함)' -> '(교육용역 면세 · VAT 0%)'
     - 'PG 복합과세 결제 승인' 잔재 정제
     - 계산기 라벨 '복합상품 가격 설정 (과세 강좌 할인 + 면세 교재 정가 합산)' -> '복합상품 가격 설정 (강좌 교육면세 할인 + 교재 도서면세 정가 합산)'
     - 강좌 실결제액 단위 '원 (과세)' -> '원 (교육면세)'
     - 패키지 총 판매가 단위 '원 (과세+면세 합산)' -> '원 (교육면세+도서면세 합산)'
  4) ADMN-BRD-002:
     - 1:1 고객 문의 상세 및 데모 데이터 내 '[과세 강좌]' -> '[교육면세 강좌]', '[면세 교재]' -> '[도서면세 교재]'
  5) ADMN-SETT-004:
     - 대사 메모 내 'PG사 복합과세 부가세 역산 및 수수료...' -> 'PG사 복합결제 수수료 원단위 절사 차이 15원 발생'
"""

import re
from pathlib import Path

TARGET_DIRS = [Path("prototype"), Path("prototype_clean")]

# 1. 전 파일 공통 단순 치환 테이블
COMMON_REPLACEMENTS = [
    # ADMN-PROD-003 단과 강좌 과세 오표기 교정
    (
        "과세 (VAT 10% 포함 · 온라인 교육용역)",
        "면세 (VAT 0% · 원격평생교육시설 온라인 교육용역)"
    ),
    (
        "과세 (VAT 10% 포함)",
        "면세 (VAT 0% · 교육용역)"
    ),
    (
        '<span class="input-unit">원 (VAT 포함)</span>',
        '<span class="input-unit">원 (교육면세 VAT 0%)</span>'
    ),
    (
        "과세 상품 (부가세 10% 포함 · 온라인 단과 강좌 고정)",
        "면세 상품 (VAT 0% · 원격평생교육시설 온라인 단과 강좌 고정)"
    ),

    # ADMN-PROD-005 패키지 상품 과세 오표기 교정
    (
        "패키지 · 환급반 상품 관리 (복합과세 분할 · 안분 가중치)",
        "패키지 · 환급반 상품 관리 (강좌·교재 면세 분리 · 안분 가중치)"
    ),
    (
        "PG 복합과세 결제 승인 및 정산 원장(ADMN-SETT-002) 매출 분리 기준",
        "도서정가제 준수를 위한 강좌(교육면세)·교재(도서면세) 결제 분리 및 정산 원장(ADMN-SETT-002) 안분 기준"
    ),
    (
        "PG 복합과세 결제 승인 및 정산 원장(월간 정산 산출·마감) 매출 분리 기준",
        "도서정가제 준수를 위한 강좌(교육면세)·교재(도서면세) 결제 분리 및 정산 원장 안분 기준"
    ),
    (
        "PG 복합과세 결제 승인 및 정산 원장 매출 분리 기준",
        "도서정가제 준수를 위한 강좌(교육면세)·교재(도서면세) 결제 분리 및 정산 원장 안분 기준"
    ),
    (
        "패키지 강좌 할인 -100,000원 (VAT 10% 포함)",
        "패키지 강좌 할인 -100,000원 (교육용역 면세 · VAT 0%)"
    ),
    (
        "과세 240,000원 + 면세 72,000원 자동 분리",
        "교육면세 240,000원 + 도서면세 72,000원 자동 분리"
    ),
    (
        "복합상품 과세·면세 분할 및 환급반 연동",
        "패키지(강좌·교재) 결제 금액 분할 및 환급반 연동"
    ),
    (
        "복합상품 가격 설정 (과세 강좌 할인 + 면세 교재 정가 합산) 및 판매 상태",
        "복합상품 가격 설정 (강좌 교육면세 할인 + 교재 도서면세 정가 합산) 및 판매 상태"
    ),
    (
        '<span class="input-unit">원 (과세)</span>',
        '<span class="input-unit">원 (교육면세)</span>'
    ),
    (
        '<span class="input-unit">원 (과세+면세 합산)</span>',
        '<span class="input-unit">원 (교육면세+도서면세 합산)</span>'
    ),

    # ADMN-BRD-002 1:1 고객 문의
    (
        "[과세 강좌] 210,000원 + [면세 교재] 38,000원",
        "[교육면세 강좌] 210,000원 + [도서면세 교재] 38,000원"
    ),
    (
        "[과세 강좌] 정종대",
        "[교육면세 강좌] 정종대"
    ),

    # ADMN-SETT-004 대사
    (
        "PG사 복합과세 부가세 역산 및 수수료 원단위 절사 차이 15원 발생",
        "PG사 복합결제 수수료 원단위 절사 차이 15원 발생"
    ),
]


def patch_ord_001(text: str) -> str:
    """
    ADMN-ORD-001 (및 prototype_clean 버전) 내 강좌+교재 주문을
    MIXED(과·면세 복합) / 강좌(과세 10%)로 잘못 표기한 부분 정밀 교정
    """
    # 1) 강좌 라인에 붙은 '(과세 10%)' 또는 '과세 10%'를 '교육용역 면세 0%'로 교정
    text = re.sub(
        r"(산업안전기사[^\n<]*?)\(과세\s*10%\)",
        r"\1(교육용역 면세 0%)",
        text
    )
    text = re.sub(
        r"(강좌[^\n<]{1,60}?)\(과세\s*10%\)",
        r"\1(교육용역 면세 0%)",
        text
    )
    text = re.sub(
        r"(올패스[^\n<]{0,40}?)\(과세\s*10%\)",
        r"\1(교육용역 면세 0%)",
        text
    )
    text = re.sub(
        r"(필기\+실기[^\n<]{0,40}?)\(과세\s*10%\)",
        r"\1(교육용역 면세 0%)",
        text
    )

    # JS 객체나 HTML 테이블에서 강좌 라인의 tax/과세 표기가 "과세 10%"로 들어간 경우 교정
    text = re.sub(
        r"(type\s*:\s*['\"]강좌['\"][^\}]*?)과세\s*10%",
        r"\1교육용역 면세 0%",
        text
    )
    text = re.sub(
        r"(badge[^>]*>강좌<[\s\S]{0,180}?)\(과세\s*10%\)",
        r"\1(교육용역 면세 0%)",
        text
    )

    # ORDERS_DATA 내 강좌 라인 sub: "과세 10%" -> sub: "교육용역 면세 0%"
    text = text.replace(
        'tag: "강좌", cls: "b-blue", name: "산업안전기사 필기 올패스(2026)", status: "수강중", sCls: "b-green", sub: "과세 10%"',
        'tag: "강좌", cls: "b-blue", name: "산업안전기사 필기 올패스(2026)", status: "수강중", sCls: "b-green", sub: "교육용역 면세 0%"'
    )

    # 직권부여 모달 sub
    text = text.replace(
        'basis: "LECTURE_TAX (0원 직권)"',
        'basis: "LECTURE_EDU (0원 직권)"'
    )
    text = text.replace(
        'sub: `과세 10% (0원 직권부여 · ${days}일)`',
        'sub: `교육용역 면세 0% (0원 직권부여 · ${days}일)`'
    )

    # ORD-001-S1 상세 모달 내 테이블
    text = text.replace(
        '<span class="badge b-blue">과세 10% (공급가 142,727)</span>',
        '<span class="badge b-blue">교육용역 면세 0% (면세 157,000원)</span>'
    )

    # 2) 강좌+교재 주문 과세근거 치환
    text = text.replace(
        "MIXED (과·면세 복합)",
        "EXEMPT (교육·도서 통합면세)"
    )
    text = text.replace(
        "과·면세 복합 (MIXED)",
        "교육·도서 통합면세 (EXEMPT)"
    )
    text = text.replace(
        "과·면세 복합",
        "교육·도서 통합면세"
    )
    text = text.replace(
        "헤더 표기: MIXED (강좌 교육면세 0% + 도서 면세 0% 복합 분할)",
        "헤더 표기: EXEMPT (교육·도서 통합면세 · 강좌 교육면세 0% + 도서 면세 0% 분할)"
    )

    # 3) 상세 화면(ORD-001-S1) 또는 안내 문구에서 "강좌(과세)" / "인강(과세)"로 적힌 잔재 교정
    text = re.sub(r"강좌\s*\(\s*과세\s*10%\s*\)", "강좌(교육용역 면세 0%)", text)
    text = re.sub(r"강좌\s*\(\s*과세\s*\)", "강좌(교육면세)", text)
    text = re.sub(r"인강\s*\(\s*과세\s*\)", "인강(교육면세)", text)

    return text


def patch_prod_003_and_005(text: str) -> str:
    """ADMN-PROD-003 / 005 내 JS 템플릿 및 옵션 텍스트의 강좌 과세 잔재 교정"""
    text = re.sub(
        r"과세\s*\(\s*VAT\s*10%\s*포함\s*·\s*온라인\s*교육용역\s*\)",
        "면세 (VAT 0% · 원격평생교육시설 온라인 교육용역)",
        text
    )
    text = re.sub(
        r"과세\s*\$\{([^}]+)\}\s*원\s*\+\s*면세\s*\$\{([^}]+)\}\s*원\s*자동\s*분리",
        r"교육면세 ${\1}원 + 도서면세 ${\2}원 자동 분리",
        text
    )
    return text


def main():
    modified_files = []

    for folder in TARGET_DIRS:
        if not folder.exists():
            continue
        for html_file in sorted(folder.glob("*.html")):
            original = html_file.read_text(encoding="utf-8")
            updated = original

            # 공통 치환
            for old, new in COMMON_REPLACEMENTS:
                updated = updated.replace(old, new)

            # 파일별 정밀 치환
            if "ADMN-ORD-001" in html_file.name:
                updated = patch_ord_001(updated)
            if "ADMN-PROD-003" in html_file.name or "ADMN-PROD-005" in html_file.name:
                updated = patch_prod_003_and_005(updated)

            if updated != original:
                html_file.write_text(updated, encoding="utf-8")
                modified_files.append(str(html_file))

    print(f"[완료] 총 {len(modified_files)}개 파일 교정됨:")
    for f in modified_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
