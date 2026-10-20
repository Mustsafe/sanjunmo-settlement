#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[정본 8.1절 세무 정합성 교정 스크립트]
- 원격평생교육시설 신고 지위에 따라 온라인 강좌(EDU)는 부가가치세 '면세(교육용역 면세 0%)'가 정본임
- ADMN-ORD-001, ADMN-PROD-003, ADMN-PROD-005, ADMN-RFD-002, ADMN-PROM-002 등에서 강좌를 '과세(10%)'로 잘못 표기한 문구를
  전수 '면세(교육용역 면세)'로 바로잡고, 과세(10%)는 '일반상품(소비재)'에만 적용되도록 교정 (prototype/ 및 prototype_clean/ 동시 반영)
"""

import os
from pathlib import Path

script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)

TAX_EXEMPT_FIXES = [
    # 1. ADMN-ORD-001 (주문/배송 관리)
    ("🔵 강좌(과세) · 교재(면세) 분리", "🔵 강좌(교육면세) · 교재(도서면세) · 일반상품(과세) 라인 분리"),
    ("인강 단독 (과세 10%)", "인강 단독 (교육용역 면세 0%)"),
    ("일반상품</button>", "일반상품 (과세 10%)</button>"),
    ("복합과세 (강좌과세+교재면세)", "면세 복합 (강좌 교육면세 + 교재 도서면세)"),
    ("복합과세(강좌+교재)", "복합주문(강좌+교재 면세)"),
    ("강좌(과세 10%)", "강좌(교육용역 면세 0%)"),
    ("강좌(과세)", "강좌(교육면세)"),
    ("인강(과세)", "인강(교육면세)"),
    ("과세(강좌) + 면세(교재)", "교육면세(강좌) + 도서면세(교재)"),
    ("과세(강좌)", "교육면세(강좌)"),
    ("헤더 표기: MIXED (강좌 과세 10% + 도서 면세 0% 복합 분할)", "헤더 표기: MIXED (강좌 교육면세 0% + 도서 면세 0% 복합 분할)"),
    ('basis: "LECTURE_TAX (강좌 과세)"', 'basis: "LECTURE_EDU (강좌 교육면세)"'),
    ("과세 10% (공급가 117,273 + VAT 11,727)", "교육용역 면세 0% (부가가치세 면세 129,000원)"),

    # 2. ADMN-PROD-003 (단과 강좌 관리) & ADMN-PROD-005 (패키지·환급반 관리)
    ("(A) 포함 강좌 정가 합계 (과세)", "(A) 포함 강좌 정가 합계 (교육용역 면세 · 할인 적용 대상)"),
    ("(B) 강좌 할인 적용 후 결제액 (과세)", "(B) 강좌 할인 적용 후 결제액 (교육용역 면세 · VAT 0%)"),
    ("(C) 포함 교재 결제액 (면세 · 할인 0%)", "(C) 포함 교재 결제액 (도서 면세 · 도서정가제 할인 0%)"),
    ("① 포함 강좌 정가 합계 (과세)", "(A) 포함 강좌 정가 합계 (교육용역 면세 · 할인 적용 대상)"),
    ("② 강좌 할인 적용 후 결제액 (과세)", "(B) 강좌 할인 적용 후 결제액 (교육용역 면세 · VAT 0%)"),
    ("③ 포함 교재 결제액 (면세 · 할인 0%)", "(C) 포함 교재 결제액 (도서 면세 · 도서정가제 할인 0%)"),
    ("강좌(과세 VAT 10%)와 실물 교재(면세 VAT 0% · 할인 0% 고정)", "강좌(교육용역 면세 VAT 0%)와 실물 교재(도서 면세 VAT 0% · 도서정가제 할인 0% 고정)"),
    ("단과 강좌(과세 VAT 10%)", "단과 강좌(교육용역 면세 VAT 0%)"),
    ("강좌 결제액(과세)", "강좌 결제액(교육면세)"),
    ("(강좌 과세 + 교재 면세)", "(강좌 교육면세 + 교재 도서면세)"),
    ("강좌 정가 합계 (과세)", "강좌 정가 합계 (교육면세)"),
    ("강좌 실결제액 (과세 VAT포함)", "강좌 실결제액 (교육면세 VAT 0%)"),
    ("과세(강좌) / 면세(교재) 복합결제", "강좌(교육면세·할인허용) / 교재(도서면세·할인0%) 복합결제"),
    ("과세 (VAT 10% 포함)", "면세 (원격평생교육시설 교육용역 · VAT 0%)"),
    (">과세 (부가세 10% 포함)<", ">면세 (교육용역 면세 · VAT 0%)<"),

    # 3. ADMN-PROM-002 (프로모션/쿠폰)
    ("강좌 라인 합계 (과세)", "강좌 라인 합계 (교육면세)"),

    # 4. ADMN-RFD-002 / ADMN-SETT-004 등 공통
    ("강좌 과세 / 교재 면세", "강좌(교육면세) / 교재(도서면세) / 일반상품(과세)"),
]


def apply_fixes_to_folder(folder: Path):
    if not folder.exists():
        return
    html_files = sorted(folder.glob("*.html"))
    updated_files = 0
    total_count = 0

    for hf in html_files:
        orig = hf.read_text(encoding="utf-8")
        updated = orig
        cnt = 0
        for old, new in TAX_EXEMPT_FIXES:
            if old in updated:
                c = updated.count(old)
                updated = updated.replace(old, new)
                cnt += c
        if updated != orig:
            hf.write_text(updated, encoding="utf-8")
            updated_files += 1
            total_count += cnt
            print(f"  - [{folder.name}] {hf.name}: {cnt}건 교정 완료")

    print(f"[OK] '{folder}' 폴더 내 총 {updated_files}개 파일 ({total_count}건) 강좌 교육용역 면세(VAT 0%) 정합화 완료")


if __name__ == "__main__":
    apply_fixes_to_folder(Path("prototype"))
    apply_fixes_to_folder(Path("prototype_clean"))
    print("\n[SUCCESS] 정본 8.1절 기준 온라인 강좌(교육용역 면세) · 교재(도서 면세) · 일반상품(과세 10%) 표기 일원화 완료!")
