#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모닷컴 & 정산시스템 v4.0.0] 백오피스 정합성 정비 스크립트 — Phase 2~4 전 도메인 일괄 클린업 & Phase 5 검증
기반 데이터: CLEANUP_AUDIT_REPORT.md (37개 HTML 전수 검출 결과 반영)

핵심 분리 원칙:
  1. [prototype/ (원본 프로토타입) — 코드값·화면코드·DB변수명·설계마커 100% 보존!]
     - prototype/ 폴더는 설계 정본이므로 화면코드(ADMN-*), 영문 ENUM 코드(CARRY_IN 등),
       DB 컬럼명(snake_case), 절 번호(8.3절 등), 원문자(①~⑳)를 일절 건드리지 않고 그대로 보존합니다.
     - 오직 확정된 금지 용어 교정('기출문제' -> '빈출문제', '정오표' -> '교재 정답지', 'Track G' 제거)만 동기화합니다.
  2. [prototype_clean/ (운영자용 클린 프로토타입) 전용 정제]
     - 운영자 화면에 노출되는 DB 컬럼명(snake_case), 영문 ENUM 코드(UPPER_SNAKE_CASE),
       SQL 조건식(IS NOT NULL, = true 등), 테이블 메타 표기(Table: ...), 설계서 절 번호, 원문자(①~⑳)만
       한글 운영 용어로 정제합니다. (HTML id/class/href 및 <script> 내부 로직 코드는 100% 보존)
  3. [Phase 5 검증 리포트 갱신]
     - 정상 운영 샘플 데이터(회원 로그인 ID, 관리자 ID, 이미지 파일명 *.jpg)는 제외하고,
       prototype_clean/ 내 실제 잔여 코드/변수 오염원만 정밀 재검출하여 CLEANUP_AUDIT_REPORT.md를 갱신합니다.

실행 방법 (저장소 루트에서 실행):
  python phase2_to_5_full_clean.py
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

ROOT_DIR = Path(__file__).resolve().parent
PROTO_DIR = ROOT_DIR / "prototype"
CLEAN_DIR = ROOT_DIR / "prototype_clean"
REPORT_PATH = ROOT_DIR / "CLEANUP_AUDIT_REPORT.md"

# ---------------------------------------------------------------------------
# 1. 정상 운영 샘플 데이터 화이트리스트 (회원 ID, 관리자 계정 ID, 첨부 이미지 파일명 등)
# ---------------------------------------------------------------------------
SAMPLE_DATA_WHITELIST: Set[str] = {
    # 샘플 회원 로그인 ID (ADMN-USER-001, ADMN-BRD-002, ADMN-RFD-002)
    "sanjun_hong88", "safety_kim26", "park_jw90", "lee_sjm77", "choi_min33", "jung_sky20",
    "safe_park", "pass_lee", "choi_san", "jung_study", "dh_kang", "yj_choi",
    # 샘플 관리자/파트너 계정 ID (ADMN-DASH-001, ADMN-CONF-003, ADMN-USER-001, ADMN-USER-007)
    "admin_root", "admin_kim", "admin_lee", "admin_settle_mgr", "cs_park", "inst_lee", "sett_choi",
    # 샘플 첨부파일명 (ADMN-BRD-002, ADMN-ORD-001, ADMN-PROD-007)
    "unopened_book_photo", "warehouse_cam_0044", "safety_helmet_keyring_main",
    # 표준 기술 약어 (HTML/인코딩)
    "UTF_8", "utf_8", "no_opener",
}

# ---------------------------------------------------------------------------
# 2. prototype/ & prototype_clean/ 공통: 순수 도메인 금지어 교정만 수행
#    (주의: prototype/의 화면코드 ADMN-*, 코드값, 변수명은 절대 건드리지 않음!)
# ---------------------------------------------------------------------------
BOTH_POLICY_REPLACEMENTS: List[Tuple[str, str]] = [
    ("기출문제집", "빈출문제집"),
    ("기출문제", "빈출문제"),
    ("기출특강", "빈출특강"),
    ("[기출]", "[빈출]"),
    ("정오표", "교재 정답지"),
    ("Vimeo", "StarPlayer+"),
    ("일반상품 (Track G)", "일반상품"),
    ("(Track G)", ""),
]

# ---------------------------------------------------------------------------
# 3. prototype_clean/ 전용: 구문·복합 패턴 우선 치환 사전 (prototype/에는 미적용)
# ---------------------------------------------------------------------------
CLEAN_PHRASE_REPLACEMENTS: List[Tuple[str, str]] = [
    # 폐지 화면 참조 문구 순화 (prototype_clean 전용)
    ("· 구 ADMN-ORD-003 통합", ""),
    ("폐지 화면(구 ADMN-ORD-003) 통합 및 ", "수강권 직권 부여 및 "),
    ("구 ADMN-ORD-003 통합", ""),

    # 00_WORKFLOW_GUIDE_baseline.html 잔여분
    ("( refund_promo_burden_type : A/B/C)", "(환불·할인 분담 유형 A/B/C)"),
    ("(refund_promo_burden_type : A/B/C)", "(환불·할인 분담 유형 A/B/C)"),
    ("refund_promo_burden_type", "환불·프로모션 분담 유형"),
    ("( payment_event_date IS NOT NULL )", "(원천징수 지급사건 성립분)"),
    ("(payment_event_date IS NOT NULL)", "(원천징수 지급사건 성립분)"),
    ("payment_event_date IS NOT NULL", "원천징수 지급사건 성립"),
    ("(QA D-13)", ""),
    ("(10.1절)", ""),
    ("(10.4절, 1:N 복수 작업 허용)", "(1:N 복수 정정 작업 지원)"),
    ("부가세 별도 VAT_EXCLUDED / 총액 역산 VAT_INCLUDED", "부가세 별도 / 부가세 포함 총액 역산"),
    ("부가세 별도  VAT_EXCLUDED  / 총액 역산 VAT_INCLUDED", "부가세 별도 / 부가세 포함 총액 역산"),
    ("RESERVED 예약", "지급 예약"),
    ("RESERVED  예약", "지급 예약"),

    # ADMN-BOOK-001 (도서 공급 원장)
    ("OWN_PUBLISHED (자사발행)", "자사발행 도서"),
    ("OWN_PUBLISHED (자사저작권)", "자사저작권 도서"),
    ("OWN_PUBLISHED · 자사발행 (Pipeline 2.1 인세 / 5.1 지원금)", "자사발행 도서 (저자 인세 / 매출연동 지원금 대상)"),
    ("PURCHASED_RESALE · 매입 재판매 (외부정산 비대상 · SETT-009/011)", "매입 재판매 도서 (외부정산 비대상 · 내부손익/물류대사 관리)"),
    ("PURCHASED_RESALE (사입)", "매입 재판매(사입)"),
    ("NET_DEDUCT (수수료 차감지급)", "수수료 차감지급"),
    ("· 6.6절 등식 적용", ""),
    ("Table: book_supply_ledger", "도서 공급 원장 목록"),
    ("[제6장 6.2절 정가 변경 이력 관리 원칙]", "[도서 정가 변경 이력 관리 원칙]"),
    ("[ADMN-BOOK-001-S1] ", ""),

    # ADMN-BRD-002 (1:1 문의 관리) & ADMN-BRD-005 (후기/빈출/정답지 관리)
    ("ship_ordered_at = 2026-10-16 11:00:12", "출고지시 일시: 2026-10-16 11:00:12"),
    ("3PL 발주 엑셀 다운로드 완료( ship_ordered_at 기록)", "3PL 발주서 다운로드(출고지시 확정)"),
    ("3PL 발주 엑셀 다운로드 완료(ship_ordered_at 기록)", "3PL 발주서 다운로드(출고지시 확정)"),
    ("[ADMN-BRD-006] ", ""),
    ("[ADMN-BRD-009] ", ""),
    ("USER-FREE-001 ~ 003", "무료특강·빈출문제 코너"),

    # ADMN-CONF-001 ~ 010 (사이트·약관·메시지·권한·감사)
    ("(?preview_token)", "(미리보기 전용)"),
    ("user_agreements (term_code='T04')", "회원 약관 동의 이력(필수 제4호)"),
    ("📤 저장 후 카카오 검수 요청 (INSPECT_REQ)", "📤 저장 후 카카오 검수 요청"),
    ("is_marketing_agreed = true", "마케팅 수신 동의"),
    ("is_marketing_agreed=Y", "마케팅 수신 동의"),
    ("ROLE_PARTNER_INST — 본인 강좌 Q&amp;A 및 강의 정산서", "본인 강좌 Q&amp;A 및 강의 정산서 열람"),
    ("ROLE_PARTNER_INST — 본인 강좌 Q&A 및 강의 정산서", "본인 강좌 Q&A 및 강의 정산서 열람"),
    ("ROLE_PARTNER_COPYRIGHT — 도서 인세 정산서 및 정답지 관리", "도서 인세 정산서 및 교재 정답지 관리"),
    ("ROLE_PARTNER_3PL — 교재 출고지시서 및 송장 등록", "교재 출고지시서 조회 및 송장 등록"),
    ("PRE↔POST 대체", "세전↔세후 계정 대체"),

    # ADMN-DASH-001 (대시보드·통계)
    ("최고관리자 (SUPER_ADMIN · 전 블록 열람)", "최고관리자 (전 블록 열람)"),
    ("운영관리자 (OP_ADMIN · 전 블록 열람)", "운영관리자 (전 블록 열람)"),
    ("CS담당자 (CS_ADMIN · 매출/통계 블록 마스킹)", "CS담당자 (매출/통계 블록 마스킹)"),
    ("물류담당자 (LOGIS_ADMIN · 출고/3PL 중심)", "물류담당자 (출고/3PL 중심)"),
    ("매출 열람 권한(SUPER_ADMIN / OP_ADMIN / SETT_ADMIN)", "매출 열람 권한(최고·운영·정산 관리자)"),

    # ADMN-INST-001 & ADMN-INST-002 (권리자 계약 원장 / 약정금 마일스톤 검수)
    ("CONTRACT_LINKED  (계약 종료일 동기화)", "계약 종료일 자동 동기화"),
    ("CONTRACT_LINKED (계약 종료일 동기화)", "계약 종료일 자동 동기화"),
    ("CONTRACT_LINKED  (무기한)", "계약 연동 (무기한)"),
    ("CONTRACT_LINKED (무기한)", "계약 연동 (무기한)"),
    ("PROD-BK-1004  ·  own_copyright_yn=true", "자사 저작권 도서"),
    ("PROD-BK-1004 · own_copyright_yn=true", "자사 저작권 도서"),
    ("own_copyright_yn=true", "자사 저작권 보유"),
    ("own_copyright_yn = true", "자사 저작권 보유"),
    ("cap_restore_on_refund = true", "환불 시 한도 복원 적용"),
    ("BASIC은 agreement_id = NULL입니다.", "기본 정산(BASIC) 라인은 별도 약정 ID 없이 운영됩니다."),
    ("on_termination_policy = LUMP_SETTLE", "종료 시 일시정산 적용"),
    ("penalty_calc_type = MULTIPLE (200%) ,  penalty_base = TOTAL_AGREED ,  CUMULATIVE", "위약벌 산정: 총 약정액 기준 배수(200%) · 누적 청구"),
    ("penalty_calc_type = MULTIPLE (200%) , penalty_base = TOTAL_AGREED , CUMULATIVE", "위약벌 산정: 총 약정액 기준 배수(200%) · 누적 청구"),
    ("(5.2절)", ""),

    # ADMN-ORD-001 (주문·배송·3PL 관리)
    ("ORD-001 · paid_amount", "실결제 합계 기준"),
    ("payment.paid_amount", "실결제금액"),
    ("ROYALTY_BOOK(인세도서)", "인세도서"),
    ("(합의서 6.1절 · 8.1절)", ""),
    ("[ADMN-ORD-001-P4] ", ""),
    ("ORDER_TYPE:  DIRECT_GRANT", "수강권 직권부여"),
    ("ORDER_TYPE: DIRECT_GRANT", "수강권 직권부여"),
    ("DIRECT_GRANT  (수강권 직권부여)", "수강권 직권부여"),
    ("DIRECT_GRANT (수강권 직권부여)", "수강권 직권부여"),

    # ADMN-PROD-004 ~ 007 (상품·교재·패키지·강사·일반상품)
    ("book_discount_rate_limit = 0% (할인 불가)", "도서정가제 0% 할인 고정 (할인 불가)"),
    ("book_discount_rate_limit = 0%", "도서정가제 0% 할인 고정"),
    ("Table: package_product", "패키지·환급반 상품 목록"),
    ("Table: instructor_display", "강사 노출 정보 목록"),
    ("is_internal=true", "자사 권리자"),
    ("is_internal = true", "자사 권리자"),
    ("INVENTORY_PURCHASE  (재고 매입 계정 🔒)", "재고 매입 계정 🔒"),
    ("INVENTORY_PURCHASE (재고 매입 계정 🔒)", "재고 매입 계정 🔒"),
    ("(ADMN-PROD-007-P2 · goods_stock_log)", "(재고 수불 원장)"),

    # ADMN-PROM-001 & ADMN-PROM-002 (이벤트·기획전 / 쿠폰·포인트)
    ("현재 편집 컬럼: promotion.html_content", "현재 편집 영역: 상세 HTML 소스"),
    ("저장 테이블: coupon · user_coupon", "쿠폰 마스터 및 회원 발급 원장 연동"),
    ("FLOOR(MIN(base × rate, 200000, base))", "최대 할인 한도(200,000원) 자동 절사"),
    ("(coupon.exclude_book = 1)", "(도서 상품 쿠폰 적용 제외 강제)"),
    ("order_discount.cap_applied = 1", "최대 할인 한도(Cap) 적용 이력"),

    # ADMN-RFD-002 (환불 요청·심사 관리)
    ("SHIPPING_DEDUCT (실물 교재 반품 회수택배비 3,000원 사후 추가 차감)", "실물 교재 반품 회수택배비(3,000원) 사후 추가 차감"),
    ("PG_DIFF_ADJ (연동 PG사 부분취소 정산 차액 보정)", "연동 PG사 부분취소 정산 차액 보정"),
    ("LECTURE_PRORATE_ADJ (강좌 수강일수/가중평균 진도율 재산정 차액 보정)", "강좌 수강일수·진도율 재산정 차액 보정"),
    ("MINUS_POINT_ADJ (환불 복원 LIFO / 마이너스 포인트 부채 사후 보정)", "환불 복원(선입선출) 및 마이너스 포인트 부채 사후 보정"),
    ("(origin_month / applied_month)", "(원 귀속월·반영월 분리)"),

    # ADMN-SETT-002 ~ 011 (정산·대사·세무·내부손익)
    ("UNKNOWN_MISMATCH = 0건  (7.4절)", "원인 미분류 불일치 0건"),
    ("UNKNOWN_MISMATCH = 0건 (7.4절)", "원인 미분류 불일치 0건"),
    ("PENDING_REVIEW = 0건  (전 수취인 DECIDED)", "세무 판정 보류 0건 (전 수취인 판정 완료)"),
    ("PENDING_REVIEW = 0건 (전 수취인 DECIDED)", "세무 판정 보류 0건 (전 수취인 판정 완료)"),
    ("7.4절 carryover_ledger", "이월 원장 마감 연속성 검증"),
    ("이월 원장(carryover_ledger) 7.4절 마감 연속성 검증", "이월 원장 마감 연속성 검증"),
    ("전체 계정 (PRE_TAX / POST_TAX / CONSIGNMENT)", "전체 이월 계정 (세전 / 세후 / 위탁도서)"),
    ("세전 이월 계정 (PRE_TAX · 1단계 합산/상쇄)", "세전 이월 계정 (1단계 합산·상쇄)"),
    ("세후 지급대기 계정 (POST_TAX · 11단계 합산)", "세후 지급대기 계정 (11단계 합산)"),
    ("위탁 도서 전용 잔액 (CONSIGNMENT_BAL)", "위탁 도서 전용 잔액"),
    ("7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치)", "이월 원장 연속성 검증: 기초잔액 + 당월변동 + 신규이월 = 기말잔액 (100% 일치)"),
    ("※ 정본 근거: 제1권 7.3절(최소 지급/청구 하한) · 7.4절(이월 원장 마감 연속성 등식) · 제2권 8.3절 1단계(CARRY_IN) 및 11단계(PAYOUT)", "※ 지급·청구 최소 하한선 및 전월 이월(1단계) ~ 지급 확정(11단계) 연속성 검증 기준 적용"),
    ("(pg_recon_unclassified_max = 0건)", "(미분류 허용 건수 0건)"),
    ("(pg_recon_tolerance_company = 1,000원)", "(단수차 허용 오차 1,000원)"),
    ("UNKNOWN_MISMATCH (미분류)", "원인 미분류 불일치"),
    ("TIMING_GAP (기간 귀속차)", "기간 귀속 시차"),
    ("PARTIAL_CANCEL_PENDING (부분취소 대기)", "부분취소 처리 대기"),
    ("PG_FEE_DIFF (PG 수수료 차감차)", "PG 수수료 차감 차액"),
    ("REFUND_TIMING_DIFF (환불 처리 시차)", "환불 처리 시차"),
    ("(TIMING_GAP 소명)", "(기간 귀속 시차 소명)"),
    ("BOOK (OWN_PUBLISHED)", "자사발행 도서"),
    ("(8.1절)", ""),
    ("( Locked = True )", "(마감 잠금)"),
    ("(Locked = True)", "(마감 잠금)"),
    ("(adj_reason_code · 10.2절 표준 13종)", "(표준 조정 사유 13종)"),
    ("(SUPPORT_CAP_ERR · 2차승인 필수)", "(2차 승인 필수)"),
    ("(PRO_RATA · 2차승인 필수)", "(2차 승인 필수)"),
    ("(ACCOUNT_TRANSFER · 2차승인 필수)", "(2차 승인 필수)"),
    ("(origin_settlement_id · 필수)", "(필수)"),
    ("(applied_month · 미마감월 고정)", "(미마감 당월 고정)"),
    ("(PRE_TAX · 과세표준 반영)", "(과세표준 반영)"),
    ("(POST_TAX · 세후 실지급액 직접 가감)", "(세후 실지급액 직접 가감)"),
    ("[15.2절 · 부록 B] ", ""),
    ("mmg_promo_overlap_flag = true", "최저보장·환급반 중복 발생 감지"),
    ("split_ratio  내림차순 →  payee_id  오름차순", "분할 비율 내림차순 → 수취인 번호 오름차순"),
    ("split_ratio 내림차순 → payee_id 오름차순", "분할 비율 내림차순 → 수취인 번호 오름차순"),
    ("(17.3절 · 읽기 전용)", "(읽기 전용)"),
    ("17.5절 하드락 규칙:", "과세유형 전환일자 검증 규칙:"),
    ("17.5절 행 분할 승인 및 PENDING_REVIEW 해제 확정", "과세전환 행 분할 승인 및 판정 보류 해제 확정"),
    ("[규격 검증 1] 부록 D-15 · ", ""),
    ("book_authors 에 자사( RH-INTERNAL ) 100%", "자사 저작권자 100%"),
    ("item_type = GOODS_ITEM", "품목유형: 일반상품"),
    ("taxable_base IS NOT NULL  및 원천징수 사건 성립( payment_event_date IS NOT NULL )", "과세표준 확정 및 원천징수 지급사건 성립"),
    ("taxable_base IS NOT NULL 및 원천징수 사건 성립(payment_event_date IS NOT NULL)", "과세표준 확정 및 원천징수 지급사건 성립"),
    ("income_clause = C19", "인적용역 일시 제공"),
    ("( C15 )", ""),
    ("( C05 )", ""),
    ("( C17 )", ""),
    ("( LOAN )", "(대여금 방식)"),
    ("ADMN-ORD-002.tracking_no", "출고 운송장번호"),

    # ADMN-USER-001 & ADMN-USER-007 (회원 관리 / 민감정보 열람·파기 통제)
    ("is_locked=false", "잠금 없음"),
    ("users.is_marketing_agreed = true", "마케팅 수신 동의"),
    ("users.cafe_member_id IS NOT NULL", "네이버 카페 연동 회원"),
    ("[TPL_CS_GUIDE] ", ""),
    ("[TPL_VBANK_ISSUED] ", ""),
    ("[TPL_DLV_START] ", ""),
    ("[TPL_RFD_DONE] ", ""),
    ("pii_unmask_ttl_seconds = 30초", "열람 유지 시간 30초"),
    ("destruction_hold = true", "파기 보류 예외 적용"),
    ("rights_holders.rrn_encrypted", "권리자 주민등록번호 (암호화)"),
    ("rights_holders.bank_account_enc", "권리자 계좌번호 (암호화)"),
    ("rights_holders.holder_name", "권리자 성명·상호"),
    ("s3://private-bucket/id_cards/*", "보안 스토리지 (신분증·통장 사본)"),
    ("settlement_statements.*", "정산서 원장 전체 항목"),
    ("부록 B 파라미터: ", "보안 설정 기준: "),
    ("/ ROLE_FINANCE_ADMIN", "/ 재무·정산 관리자"),
]

# ---------------------------------------------------------------------------
# 4. prototype_clean/ 전용: 단독 토큰(영문 ENUM & DB 컬럼명) 한글 치환 사전
# ---------------------------------------------------------------------------
CLEAN_TOKEN_MAP: Dict[str, str] = {
    # 영문 ENUM 코드
    "CARRY_IN": "전월 이월 승계",
    "ACCRUAL": "순 발생액 산출",
    "MMG_ADJ": "월 보장액 보정",
    "DEDUCT": "환불·할인 공제",
    "SUPPORT_CAP": "지원금 한도 캡",
    "PREPAY_OFFSET": "선급금 상한선 상계",
    "LUMPSUM_ADD": "비정기 약정·매절 가산",
    "PAYEE_SPLIT": "수취인 분할",
    "CLAIM": "반환·최소 청구 검증",
    "PAYOUT": "최소 지급 검증·펌뱅킹 확정",
    "UNKNOWN_MISMATCH": "원인 미분류 불일치",
    "REVENUE_SHARE": "매출 비례 정산",
    "LUMP_SUM": "일시금",
    "LUMP_SETTLE": "종료 일시정산",
    "PRO_RATA": "이행률 비례 정산",
    "ACCOUNT_TRANSFER": "계정 간 대체",
    "NON_OFFSET": "비상계 순수 지원",
    "CONDITIONAL": "조건부 상계 허용",
    "UNCONDITIONAL": "무조건 상계 허용",
    "FORBIDDEN": "상계 불가",
    "PENDING_REVIEW": "판정 보류(검토 대기)",
    "PRE_TAX": "세전 이월",
    "POST_TAX": "세후 이월",
    "CONSIGNMENT_BAL": "위탁 도서 잔액",
    "VAT_EXCLUDED": "부가세 별도",
    "VAT_INCLUDED": "부가세 포함",
    "NET_DEDUCT": "수수료 차감지급",
    "OWN_PUBLISHED": "자사발행 도서",
    "PURCHASED_RESALE": "매입 재판매",
    "ROYALTY_BOOK": "인세 도서",
    "DIRECT_SALE": "자사 직접 판매",
    "INVENTORY_PURCHASE": "재고 매입",
    "GOODS_ITEM": "일반상품(굿즈)",
    "SHIPPING_FEE": "배송비",
    "MARKETING_EXPENSE": "판촉비",
    "CONTRACT_LINKED": "계약 종료일 연동",
    "CLAIMED_ON_TERMINATION": "중도해지 반환청구",
    "TOTAL_AGREED": "총 약정액 기준",
    "DIRECT_GRANT": "수강권 직권부여",
    "ORDER_TYPE": "주문 유형",
    "SHIPPING_DEDUCT": "반품 회수택배비 차감",
    "PG_DIFF_ADJ": "PG 부분취소 차액 보정",
    "LECTURE_PRORATE_ADJ": "수강일수·진도율 재산정 보정",
    "MINUS_POINT_ADJ": "마이너스 포인트 사후 보정",
    "TIMING_GAP": "기간 귀속 시차",
    "PARTIAL_CANCEL_PENDING": "부분취소 대기",
    "PG_FEE_DIFF": "PG 수수료 차감 차액",
    "REFUND_TIMING_DIFF": "환불 처리 시차",
    "RATE_ERR": "요율 오류",
    "SHARE_ERR": "지분율 오류",
    "REFUND_OMIT": "환불 반영 누락",
    "BOOK_SUPPLY_ERR": "도서 공급형태 오등록",
    "CONSIGN_FEE_ERR": "위탁 수수료율 오류",
    "TAX_TYPE_ERR": "과세유형 오인",
    "PREPAY_OFFSET_ERR": "선급금 상계액 오류",
    "MMG_CALC_ERR": "최저보장 산출 오류",
    "SUPPORT_CAP_ERR": "지원금 한도 판정 오류",
    "WITHHOLDING_RATE_ERR": "원천징수 세율 오류",
    "BOOK_COUNT_DIFF": "도서 확정 판매부수 차이",
    "SIMPLIFIED_RECEIPT": "간이과세자(영수증발급)",
    "SIMPLIFIED_INVOICE": "간이과세자(세금계산서발급)",
    "NON_PROFIT_ORG": "비영리·고유번호 단체",
    "CLOSED_BY_TRANSITION": "과세전환 종결",
    "CANCELLED_BILLED": "출고회수건 과오청구",
    "EVIDENCE_FILE": "증빙 첨부파일",
    "MANUAL_NOTE": "수기 확인 소명",
    "ADMN_AUDIT_LOG": "시스템 감사 로그",
    "FREE_LECTURE": "무료특강 영상",
    "FREQ_EXAM": "빈출문제 해설",
    "ANSWER_SHEET": "교재 정답지",
    "COURSE_REVIEW": "수강후기",
    "PASS_ESSAY": "합격수기",
    "INSPECT_REQ": "카카오 검수중",
    "FIN_MANAGER": "재무·정산책임자",
    "SUPER_ADMIN": "최고관리자",
    "OP_ADMIN": "운영관리자",
    "CS_ADMIN": "CS담당자",
    "LOGIS_ADMIN": "물류담당자",
    "SETT_ADMIN": "정산관리자",
    "ROLE_SUPER_ADMIN": "최고관리자",
    "ROLE_FINANCE_DIRECTOR": "재무 총괄 책임자",
    "ROLE_FINANCE_ADMIN": "재무·정산 관리자",
    "ROLE_OPS_ADMIN": "서비스·콘텐츠 운영자",
    "ROLE_CS_ADMIN": "고객센터 CS 전담",
    "ROLE_CONTENT_ADMIN": "콘텐츠·상품 관리자",
    "ROLE_PARTNER_INST": "파트너 강사",
    "ROLE_PARTNER_COPYRIGHT": "교재 저작권자·출판사",
    "ROLE_PARTNER_3PL": "외부 물류(3PL)",
    "PARTNER_INST": "파트너 강사",
    "PARTNER_3PL": "외부 물류(3PL)",
    "TPL_PAY_DONE": "결제완료 알림톡",
    "PAY_DONE": "결제완료 알림톡",
    "EML_TERMS_NOTICE": "약관개정 안내 메일",
    "TPL_DLV_START": "출고·송장 안내 알림톡",
    "TPL_CS_GUIDE": "고객센터 안내 알림톡",
    "TPL_VBANK_ISSUED": "가상계좌 안내 알림톡",
    "TPL_RFD_DONE": "환불완료 안내 알림톡",

    # DB 컬럼명 및 시스템 변수명 (snake_case)
    "order_items": "주문 품목",
    "order_item_id": "주문품목번호",
    "refund_promo_burden_type": "환불·할인 분담유형",
    "origin_month": "원 발생 귀속월",
    "applied_month": "반영 기준월",
    "origin_settlement_id": "참조 원 정산서",
    "adj_reason_code": "조정 사유 코드",
    "adj_account_type": "반영 계정 구분",
    "carryover_ledger": "이월 원장",
    "payment_event_date": "원천징수 성립일",
    "pii_unmask_ttl_seconds": "열람 유지시간(30초)",
    "book_price_history": "도서 정가 이력",
    "book_supply_type": "도서 공급형태",
    "book_supply_type_snapshot": "도서 공급형태 스냅샷",
    "book_supply_ledger": "도서 공급 원장",
    "own_copyright_yn": "자사 저작권 여부",
    "effective_from": "적용 시작일",
    "effective_to": "적용 종료일",
    "ship_ordered_at": "출고지시 일시",
    "preview_token": "미리보기 토큰",
    "term_code": "약관 코드",
    "user_agreements": "회원 약관동의 원장",
    "terms_version_history": "약관 버전 이력",
    "is_marketing_agreed": "마케팅 수신동의",
    "before_snapshot_json": "변경 전 스냅샷",
    "after_snapshot_json": "변경 후 스냅샷",
    "contract_status": "계약 상태",
    "contract_id": "적용 계약",
    "end_basis": "매핑 종료 기준",
    "payment_method": "지급 방식",
    "offset_type": "상계 처리 유형",
    "cap_type": "한도 유형",
    "on_termination_policy": "약정 종료 처리 정책",
    "cap_restore_on_refund": "환불 시 한도 복원",
    "agreement_id": "약정 번호",
    "target_month": "귀속월",
    "penalty_calc_type": "위약벌 산정방식",
    "penalty_base": "위약벌 기준금액",
    "paid_amount": "실결제금액",
    "book_discount_rate_limit": "도서 할인율 상한",
    "is_preorder": "예약판매 여부",
    "release_date": "출고 예정일",
    "package_product": "패키지 상품 원장",
    "instructor_display": "강사 노출 원장",
    "goods_supply_type": "상품 공급 형태",
    "is_internal": "자사 귀속 여부",
    "goods_stock_log": "재고 수불 이력",
    "html_content": "HTML 소스",
    "css_content": "CSS 스타일",
    "js_content": "JS 스크립트",
    "user_coupon": "회원 발급 쿠폰",
    "cap_applied": "최대할인 캡 적용",
    "order_discount": "주문 할인 원장",
    "exclude_book": "도서 적용 제외",
    "payment_status": "지급 상태",
    "pg_recon_unclassified_max": "미분류 허용 상한",
    "pg_recon_tolerance_company": "단수차 허용 오차",
    "item_type": "품목 유형",
    "mmg_promo_overlap_flag": "최저보장·환급반 중복 감지",
    "payee_is_author": "저작자 본인 여부",
    "payee_split_base": "2계층 분할 기준",
    "payee_id": "수취인 번호",
    "split_ratio": "분할 지분율",
    "active_contracts": "유효 계약 원장",
    "tax_type_cd": "국세청 과세유형",
    "nts_tax_type_map": "국세청 과세유형 매핑표",
    "nts_check_validity_days": "국세청 조회 유효기간(30일)",
    "nts_batch_chunk_size": "배치 묶음 단위(100건)",
    "nts_batch_interval_ms": "호출 간격(1,000ms)",
    "nts_retry_max_count": "최대 재시도 횟수(3회)",
    "nts_periodic_check_schedule": "정기 휴폐업 점검 스케줄",
    "tax_type_change_dt": "과세유형 전환일자",
    "book_authors": "도서 저자 매핑",
    "goods_master": "일반상품 마스터",
    "taxable_base": "과세표준",
    "pending_negative_base": "음수 이월 과세표준",
    "income_clause": "기타소득 구분코드",
    "tracking_no": "운송장번호",
    "admin_access_log": "개인정보 접근 감사 로그",
    "is_locked": "계정 잠금 상태",
    "cafe_member_id": "카페 연동 ID",
    "unpaid_points_blacklist": "마이너스 포인트 미납 제재",
    "destruction_hold": "파기 보류 예외",
    "pii_destruction_field_map": "개인정보 파기 기준표",
    "rights_holder_id": "권리자 고유번호",
    "rights_holders": "권리자 원장",
    "rrn_encrypted": "주민등록번호(암호화)",
    "bank_account_enc": "계좌번호(암호화)",
    "holder_name": "권리자 성명",
    "id_cards": "신분증 사본",
    "settlement_statements": "정산서 원장",
    "settlement_recipient_id": "권리자 대체 식별번호",
}

SORTED_CLEAN_TOKENS = sorted(CLEAN_TOKEN_MAP.keys(), key=len, reverse=True)
TOKEN_ALTERNATION = "|".join(re.escape(k) for k in SORTED_CLEAN_TOKENS)


def process_html_file(file_path: Path, is_clean_dir: bool) -> int:
    raw = file_path.read_text(encoding="utf-8")
    orig = raw

    # 1) <script>, <style>, <!-- --> 블록 임시 보호
    protected_blocks: List[str] = []

    def _protect(m: re.Match) -> str:
        idx = len(protected_blocks)
        protected_blocks.append(m.group(0))
        return f"___PROTECTED_BLOCK_{idx}___"

    masked = re.sub(
        r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)",
        _protect,
        raw,
        flags=re.IGNORECASE,
    )

    # 2) prototype_clean/에서만 <code>TOKEN</code> 언래핑 수행 (prototype/은 <code> 태그까지 100% 보존)
    if is_clean_dir:
        def _unwrap_code_tag(m: re.Match) -> str:
            inner = m.group(1).strip()
            for tok in SORTED_CLEAN_TOKENS:
                if tok in inner:
                    return inner
            return m.group(0)

        masked = re.sub(r"<code\b[^>]*>(.*?)</code>", _unwrap_code_tag, masked, flags=re.IGNORECASE | re.DOTALL)

    # 3) 텍스트 노드 및 UI 속성 정제 함수
    def _clean_text_segment(seg: str) -> str:
        # 양방향 공통 금지어('기출문제'->'빈출문제', '정오표'->'교재 정답지', 'Track G' 제거)만 반영
        for src, dst in BOTH_POLICY_REPLACEMENTS:
            seg = seg.replace(src, dst)

        # prototype/ 폴더는 여기서 즉시 반환 (화면코드·코드값·변수명 100% 보존)
        if not is_clean_dir:
            return seg

        # 이하 prototype_clean/ 전용 클린업
        for src, dst in CLEAN_PHRASE_REPLACEMENTS:
            seg = seg.replace(src, dst)

        seg = re.sub(
            rf"([가-힣a-zA-Z0-9\]])\s*\(\s*(?:{TOKEN_ALTERNATION})\s*\)",
            r"\1",
            seg,
        )

        for tok in SORTED_CLEAN_TOKENS:
            if tok in seg:
                seg = re.sub(rf"\b{re.escape(tok)}\b", CLEAN_TOKEN_MAP[tok], seg)

        seg = re.sub(r"\[\s*마커\s*\d+\s*\]\s*", "", seg)
        seg = re.sub(r"[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\s*", "", seg)
        seg = re.sub(r"\bTrack\s+[A-G]\b\s*[:·-]?\s*", "", seg, flags=re.IGNORECASE)
        seg = re.sub(r"\(\s*Pipeline\s+\d+\.\d+\s*\)", "", seg, flags=re.IGNORECASE)
        seg = re.sub(r"\bPipeline\s+\d+\.\d+\s*·?\s*", "", seg, flags=re.IGNORECASE)
        seg = re.sub(r"\(\s*\)", "", seg)
        seg = re.sub(r"[ \t]{2,}", " ", seg)
        return seg

    def _process_tag(tag_m: re.Match) -> str:
        tag_s = tag_m.group(0)
        return re.sub(
            r'(\b(?:title|placeholder|data-tooltip)\s*=\s*)(["\'])(.*?)\2',
            lambda am: f"{am.group(1)}{am.group(2)}{_clean_text_segment(am.group(3))}{am.group(2)}",
            tag_s,
            flags=re.IGNORECASE | re.DOTALL,
        )

    masked = re.sub(r"<[^>]+>", _process_tag, masked)

    def _process_text(txt_m: re.Match) -> str:
        txt = txt_m.group(1)
        if not txt.strip() or "___PROTECTED_BLOCK_" in txt:
            return txt_m.group(0)
        return f">{_clean_text_segment(txt)}<"

    masked = re.sub(r">([^<]+)<", _process_text, masked)

    if is_clean_dir:
        masked = re.sub(r"\(\s*\)", "", masked)

    for idx, block in enumerate(protected_blocks):
        if is_clean_dir and block.startswith("<!--"):
            block = re.sub(r"\bTrack\s+[A-G]\b", "", block, flags=re.IGNORECASE)
        masked = masked.replace(f"___PROTECTED_BLOCK_{idx}___", block)

    if masked != orig:
        file_path.write_text(masked, encoding="utf-8")
        return 1
    return 0


def scan_visible_issues(file_path: Path) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    raw = file_path.read_text(encoding="utf-8")

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
        text_only = re.sub(r"<[^>]+>", " ", line).strip()
        if not text_only:
            continue
        for category, pat in patterns:
            matches = pat.findall(text_only)
            if matches:
                filtered = [m for m in matches if m not in SAMPLE_DATA_WHITELIST]
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
    print("[Phase 2~5] 전 도메인(37개 HTML) 일괄 정밀 클린업 및 양방향 동기화 시작")
    print("=" * 72)

    proto_updated = 0
    clean_updated = 0

    for html_file in sorted(PROTO_DIR.glob("*.html")):
        if html_file.name == "patch_all_snb_v3.html":
            continue
        proto_updated += process_html_file(html_file, is_clean_dir=False)

    for html_file in sorted(CLEAN_DIR.glob("*.html")):
        if html_file.name == "patch_all_snb_v3.html":
            continue
        clean_updated += process_html_file(html_file, is_clean_dir=True)

    print(f"[패치 완료] prototype/ 금지어 동기화 파일: {proto_updated}개 (코드값·화면코드 100% 보존)")
    print(f"[패치 완료] prototype_clean/ 클린업 파일: {clean_updated}개")

    clean_snb = CLEAN_DIR / "common-snb.js"
    if clean_snb.exists():
        snb_txt = clean_snb.read_text(encoding="utf-8")
        marker = "/* [PHASE1_CLEAN_ENHANCEMENT_V4] */"
        if marker in snb_txt:
            snb_txt = snb_txt.split(marker)[0].rstrip()
        extra_js = f"""
{marker}
(function enhanceCleanDomTranslator() {{
  const EXTRA_MAP = {json.dumps(CLEAN_TOKEN_MAP, ensure_ascii=False, indent=2)};
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
      if (parentTag === 'SCRIPT' || parentTag === 'STYLE') continue;
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
        clean_snb.write_text(snb_txt + "\n" + extra_js, encoding="utf-8")
        print("[패치 완료] prototype_clean/common-snb.js 런타임 사전 최신화 완료")

    report_lines = [
        "# 백오피스 `prototype_clean/` 전수 정합성 스캔 리포트 (Phase 2~5 완료 후)",
        "",
        "- 생성 스크립트: `phase2_to_5_full_clean.py`",
        "- 목적: 전 도메인(37개 HTML) 클린업 후 잔여 오염원 Zero-Defect 검증",
        "",
        "## 1. 파일별 잔여 검출 요약",
        "",
        "| 파일명 | 총 검출 건수 | 주요 검출 유형 및 토큰 샘플 |",
        "| :--- | :---: | :--- |",
    ]
    detail_sections: List[str] = ["", "## 2. 파일별 상세 검출 내역", ""]
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
    print(f"[Phase 5 재스캔 완료] 잔여 검출 파일: {total_files_with_issues}개 (총 {total_issue_count}건)")
    print(f"[리포트 갱신 완료] {REPORT_PATH}")
    print("=" * 72)


if __name__ == "__main__":
    main()
