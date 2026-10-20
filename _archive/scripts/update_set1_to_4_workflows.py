# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(".")
SPEC_V4 = ROOT / "docs" / "산준모닷컴 구축 통합 상세 설계서.md"
PLAN_MD = ROOT / "docs" / "SET1_TO_4_ALIGNMENT_PLAN.md"
PROTO_DIRS = [ROOT / "prototype", ROOT / "prototype_clean"]

SET1_WORKFLOW_MD = """

#### **[D] Set 1 End-to-End 실무 업무 플로우 (프론트 출발 ➔ 백오피스 완결)**

1. **[Flow 1-1] 수험생 회원가입 · 본인인증 · 웰컴 혜택 자동 발급 플로우**
   - **[Step 1. 프론트 약관 동의 및 본인인증 (`USER-AUTH-002`)]** 수험생이 필수/선택 약관(마케팅 수신 동의 단일 플래그 `is_marketing_agreed`) 체크 후 휴대폰 PASS/SMS 본인인증 수행 ➔ 연계정보(`CI/DI`) 해시 대조로 탈퇴 후 30일 이내 재가입 어뷰징 여부 자동 검증
   - **[Step 2. 가입 완료 및 웰컴 혜택 즉시 지급 (`USER-AUTH-002` ➔ `ADMN-PROM-002/003`)]** 가입 확정 즉시 **웰컴 무상 포인트(`무상 P`, 5,000P · 유효기간 2년)** 및 **신규가입 웰컴 쿠폰(발급일로부터 `D+21` 만료)** 자동 발급 ➔ 가입 환영 알림톡(`ADMN-CONF-004`) 발송

2. **[Flow 1-2] 수강생 재생 오류 · 동시접속 잠김 · 진도율 왜곡 · 수강 홀딩 CS 처리 플로우**
   - **[Step 1. 수험생 불편 발생 및 문의 접수 (`USER-VOD-001` / `USER-CS-003` ➔ `ADMN-BRD-002`)]** 동영상 플레이어 재생 중 중복 접속 차단(1계정 1세션) 또는 OT 0초 강의로 인한 진도율 미달 문의 인입
   - **[Step 2. 회원 수강·기기 제어 및 진도율 수동 보정 (`ADMN-USER-001` ➔ `ADMN-USER-003` / `004`)]**
     - **[세션/기기 잠김 시 (`ADMN-USER-003`)]** 활성 세션의 접속 IP·브라우저 확인 후 `[강제 로그아웃]` 실행 또는 등록 단말기 `[기기 초기화]` 처리 (OBS 등 녹화 프로그램 감지 건은 경고 안내 후 블랙리스트 `ADMN-USER-005` 이관 검토)
     - **[진도율 왜곡 시 (`ADMN-USER-004`)]** 0초 영상(기본 60초 가중치) 또는 네트워크 오류로 미인정된 차시를 선택해 사유 입력 후 **`[진도율 100% 수동 보정]`** 실행 ➔ 즉시 합격환급 판정 모수(`ADMN-SETT-006`)에 실시간 반영
     - **[일시정지 요청 시 (`ADMN-USER-003`)]** 수험생 요청에 따라 수강 홀딩(최대 3회, 통산 30일 한도) 설정

3. **[Flow 1-3] 특가 기획전 오픈 · 중복할인 차단(`S1`) · 이벤트 당첨자 혜택 지급 플로우**
   - **[Step 1. 백오피스 기획전 생성 및 혜택 차단 스위치 설정 (`ADMN-PROM-001`)]** 마케터가 기획전 슬러그(`slug`)·배너·HTML 등록 후 대상 특가 상품 매핑 ➔ **`[프로모션 기간 중 쿠폰 사용 및 포인트 적립 차단(ADMN-PROM-001-S1)]`** 활성화
   - **[Step 2. 메인 배너 연결 및 프론트 결제창 통제 (`ADMN-CONF-001` ➔ `USER-PROM-001` ➔ `USER-PAY-001`)]** 메인/띠배너(`ADMN-CONF-001`)에 기획전 노출 ➔ 수험생이 기획전 상품 결제 진입 시 쿠폰 선택창 자동 비활성화 및 구매적립 포인트(`적립 P`) 0원 처리
   - **[Step 3. 이벤트 당첨자 발표 및 무상 포인트 일괄 지급 (`ADMN-BRD-010` ➔ `ADMN-PROM-003`)]** 당첨자 발표 게시글(`ADMN-BRD-010`) 등록 후 포인트 관리(`ADMN-PROM-003`)에서 당첨 회원에게 **`무상 P`(유효기간 2년)** 일괄 지급 및 안내 문자 발송
"""

SET2_WORKFLOW_MD = """

#### **[D] Set 2 End-to-End 실무 업무 플로우 (오프라인 계약 체결 출발 ➔ 상품·패키지 판매 오픈)**

1. **[Flow 2-1] 신규 파트너(강사·저자·위탁출판사) 오프라인 계약 체결 및 원장 최초 등록 플로우**
   - **[Step 1. 오프라인 계약서 날인 및 구비서류 수취 (오프라인 출발점)]** 사업/기획 담당자가 신규 강사·교재 저자·위탁출판사와 계약(강사료 R/S 요율, 도서 인세율, 위탁 정산 기준가, 선급금/개발지원금 한도, 합격환급 분담옵션 A/B/C 등) 체결 ➔ **날인 계약서 스캔본(PDF), 사업자등록증(또는 신분증), 정산 입금계좌 통장사본** 수취
   - **[Step 2. 국세청 과세유형 검증 및 권리자 계약 원장 등록 (`ADMN-INST-001` ↔ `ADMN-SETT-008`)]**
     - `ADMN-INST-001`에서 `[+ 신규 권리자/계약 등록]` 진입 ➔ 사업자등록번호 입력 후 국세청 API 실시간 상태·과세유형 조회 (API 장애·신규사업자·비영리 특수건은 **20자 이상 사유 + 사업자등록증 첨부 후 재무 수기 예외 지정** 허용)
     - 계약 기간(`effective_from ~ effective_to`), 정산 주기, 최소 지급/청구 기준액(계약별 변수), **위탁도서 정산 기준가(`실결제액` vs `도서 정가` 중 택1)** 입력 및 계약서 PDF 업로드
     - *(2계층 공동수취인 존재 시)* 수취인 분할 관리(`ADMN-SETT-007`)에서 배분율 등록 / *(선급금·지원금 약정 시)* 마일스톤 관리(`ADMN-INST-002`)에 지급 일정 등록
   - **[Step 3. 외부 파트너 전용 백오피스 계정 및 데이터 스코프 발급 (`ADMN-CONF-005`)]** 권한 관리에서 파트너 역할(`ROLE_PARTNER_INST` 또는 `ROLE_PARTNER_COPYRIGHT`) 계정을 생성하고, 방금 채번된 **권리자 ID(`INST-*` / `CR-*`)를 데이터 스코프로 강제 바인딩**(본인 데이터만 조회·답변·역발행 승인 가능)하여 파트너에게 전달

2. **[Flow 2-2] 기존 파트너 재계약 · 요율/과세유형 변경 시 이력 분기 플로우 (과거 마감월 보호)**
   - **[Step 1. 변경 합의서 날인 또는 과세유형 전환 감지 (`Offline` / `ADMN-SETT-008`)]** 재계약(요율·위탁수수료·지원금 한도 변경) 체결 또는 국세청 정기 조회에서 과세유형 전환 감지
   - **[Step 2. 기존 계약 행 보존 및 신규 효력일(`effective_from`) 버전 추가 (`ADMN-INST-001` / `ADMN-SETT-001`)]**
     - 이미 마감(`Locked`)된 과거 정산월 원장이 훼손되지 않도록 **기존 계약 행 직접 덮어쓰기(Overwrite)를 원천 차단**
     - 기존 계약의 종료일(`effective_to`)을 마감월 말일로 닫고, **변경 효력 시작일(`effective_from`)이 지정된 신규 계약 이력 행을 추가** ➔ 변경 합의서 첨부 및 감사 로그(`ADMN-CONF-010`) 자동 기록

3. **[Flow 2-3] 실물 도서 입고 · 단과 강좌 세팅 · 권리자 100% 매핑 · 패키지 판매 오픈 플로우**
   - **[Step 1. 도서 공급원장 및 전시 교재 등록 (`ADMN-BOOK-001` ➔ `ADMN-PROD-004`)]** 도서 공급원장(`ADMN-BOOK-001`)에 정식 SKU·ISBN·공급유형(자사발행/위탁/사입/사은품)·초기 재고 등록 ➔ 교재 관리(`ADMN-PROD-004`)에서 SKU를 불러와 **도서 정가 및 기본할인율(최대 10% 이내) 입력(실판매가 자동 계산)** 및 미리보기 PDF 업로드
   - **[Step 2. 단과 강좌 생성 및 VOD·교안 매핑 (`ADMN-PROD-003` ↔ `ADMN-PROD-006`)]** 강좌 메타정보·수강기간·판매가 입력 ➔ 커리큘럼 차시 구성 후 스타플레이어 영상(`ADMN-PROD-006`) 바인딩 및 차시별 교안 PDF(회원ID 워터마크 적용) 업로드
   - **[Step 3. 상품별 1계층 권리자 지분 100.00% 검증 (`ADMN-SETT-001`)]** 해당 강좌·교재 SKU의 권리자(강사·저자·자사) 지분 합계를 정확히 `100.00%`로 세팅 ➔ **미매핑(`NULL`) 판매대기 하드락 해제**
   - **[Step 4. 패키지 구성 및 프론트 전시 오픈 (`ADMN-PROD-005` ➔ `USER-CRS-002`)]** 패키지 관리(`ADMN-PROD-005`)에서 `[강좌 + 교재]`를 묶고, 합격환급반인 경우 **상품별 목표 진도율(예: 90%)·출석일 변수** 설정 후 `[판매중]`으로 전환하여 프론트 전시 오픈
"""

SET3_WORKFLOW_MD = """

#### **[D] Set 3 End-to-End 실무 업무 플로우 (수험생 결제 출발 ➔ 3PL 출고/송장 ➔ 반품/복합환불)**

1. **[Flow 3-1] 수험생 장바구니 복합결제 ➔ 일일 3PL 출고지시 엑셀 다운로드 ➔ 운송장 일괄 업로드 플로우 (일일 물류 루틴)**
   - **[Step 1. 프론트 장바구니 담기 및 복합결제 완료 (`USER-CART-001` ➔ `USER-PAY-001/002`)]**
     - 수험생이 강좌+실물교재 선택 ➔ **실물 교재는 기본할인(최대 10%)이 반영된 실판매가로만 계산되며 쿠폰·포인트 할인 및 적립 대상에서 0원 하드락 제외** / 실물 교재 **실결제액 합계 30,000원 이상 시 무료배송**(미만 시 3,000원, 도서산간 추가운임 자동 합산) 판정 후 토스페이먼츠 결제 완료
     - *(출고 지시 전 즉시취소)* 백오피스 출고 마감 전(`결제완료` 상태)에는 수험생이 마이페이지(`USER-MY-004`)에서 `[결제 즉시 취소]` 클릭 시 CS 개입 없이 PG 전액 즉시 취소
   - **[Step 2. 일일 출고 마감(컷오프) 및 3PL 출고지시서 엑셀 다운로드 (`ADMN-ORD-002`)]**
     - 매일 오전 출고 마감 시각에 운영자 또는 외부 3PL 담당자(`ROLE_PARTNER_3PL`, 결제금액·강좌내역 마스킹 격리)가 주문/출고 관리(`ADMN-ORD-002`)에서 `결제완료(출고대기)` 건 선택 후 **`[3PL 출고지시 엑셀 다운로드]`** 클릭
     - **다운로드 즉시 출고 배치 번호(`BATCH-*`)가 부여되며 주문 상태가 `배송준비중`으로 일괄 전환** ➔ 동시에 **프론트(`USER-MY-004`)의 수험생 직접 취소 버튼이 잠금(Lock)** 처리됨
   - **[Step 3. 3PL 창고 실물 포장 및 운송장 번호 엑셀 일괄 업로드 (`ADMN-ORD-002` ➔ `USER-MY-005`)]**
     - 3PL 물류창고에서 교재 피킹·포장 후 택배사 송장 번호 채번 ➔ `ADMN-ORD-002` 상단 **`[운송장 엑셀 일괄 업로드]`** 버튼을 눌러 주문번호별 택배사 코드·운송장 번호 엑셀 파일 업로드
     - 업로드 즉시 **주문 상태가 `배송중`으로 일괄 변경 + 도서 재고 실차감(20권 이하 시 안전재고 경고, 0권 시 자동 일시품절) + 수험생에게 배송출발 알림톡(`ADMN-CONF-004`) 자동 발송** ➔ 수험생이 마이페이지(`USER-MY-005`)에서 실시간 배송조회
   - **[Step 4. 배송완료 확정 및 월말 3PL 수수료 정산 집계 (`ADMN-ORD-002` ➔ `ADMN-SETT-011`)]** 택배사 배송완료 수신(또는 출고 후 D+3 자동 확정) 시 `배송완료` 전환 ➔ 월말 3PL 물류대행 정산(`ADMN-SETT-011`)의 건당 출고·포장 수수료 모수로 자동 인입

2. **[Flow 3-2] 프론트 환불신청(또는 1:1 문의 이관) ➔ 3PL 반품 입고 검수 ➔ 복합환불 및 적립 포인트 회수 플로우**
   - **[Step 1. 환불 요청 인입 (`USER-MY-006` 또는 `USER-CS-003` ➔ `ADMN-BRD-002` ➔ `ADMN-RFD-004`)]** 수험생이 마이페이지(`USER-MY-006`)에서 직접 환불을 신청하거나, 1:1 문의(`ADMN-BRD-002`)로 환불을 요청해 CS 담당자가 **`[환불 심사로 이관]`** 처리하면 환불 심사 목록(`ADMN-RFD-004`)에 접수됨
   - **[Step 2. 실물 교재 출고 여부 판별 및 3PL 반품 입고 검수 (`ADMN-ORD-002` ↔ `ADMN-RFD-002`)]**
     - 출고 전(`결제완료`) 건은 교재 차감 없이 즉시 강좌 환불 산식으로 진행
     - 이미 출고(`배송준비중/배송중/배송완료`)된 교재가 포함된 건은 `반품수거중` 전환 ➔ 3PL 창고에 반품 도서 도착 후 파손·필기·래핑 훼손 여부를 확인하여 **`[3PL 반품입고 검수완료]`** 입력 (정상 입고 시 교재비 환불, 훼손·미반품 시 **결제 당시 도서 실판매가 전액 차감** 자동 설정)
   - **[Step 3. 복합환불 계산기 산출 및 기적립 포인트(`적립 P`) 회수 (`ADMN-RFD-002`)]**
     - 시스템이 `[실결제액 - 강좌 기수강 차감액(결제 7일 이내 & 2강 이하 전액환불, 초과 시 일할/진도율 차감) - 미반품/훼손 교재 실판매가 - 반품 배송비]`를 자동 산출
     - 원결제로 적립되었던 **구매적립 포인트(`적립 P`, 1%)** 자동 회수 ➔ 만약 회원이 해당 포인트를 이미 사용해 잔액이 부족하면 **① 마이너스 포인트 부채(`Negative Balance`) 전환** 또는 **② 환불 지급 현금에서 직접 차감** 중 선택 처리 (환불로 복원되는 기사용 포인트는 유효기간이 긴 `적립 P`부터 LIFO 역순 복원)
   - **[Step 4. PG 부분취소 연동 및 환불 완료 통보 (`ADMN-RFD-002` ➔ `ADMN-RFD-003`)]** `[환불 확정 및 PG 취소]` 실행 시 토스페이먼츠 부분취소 API 즉시 호출 (가상계좌 결제 건은 `ADMN-USER-007`에서 환불계좌 수집 후 이체) 및 환불 완료 내역(`ADMN-RFD-003`) 영구 기록 (※ 확정 후 금액 오차 발견 시 원장 수정 없이 차액 보정 전표 `ADJ-*` 발행)
"""

SET4_WORKFLOW_MD = """

#### **[D] Set 4 End-to-End 실무 업무 플로우 (프론트 1:1 문의 분기 · 합격환급 심사 · 월간 정산 마감)**

1. **[Flow 4-1] 수험생 프론트 1:1 문의 등록부터 백오피스 5대 업무 화면 분기·완결 플로우 (CS 허브 루틴)**
   - **[Step 1. 프론트 수험생 1:1 문의 등록 (`USER-CS-003` / `USER-MY-010`)]**
     - 수험생이 고객센터 또는 마이페이지에서 `[1:1 문의하기]` 클릭 후 문의 유형 선택:
     - *(학습 질문 자동 분리)* `'학습/교재 내용 질문'` 선택 시 ➔ 백오피스로 접수하지 않고 **[산준모 네이버 공식 카페 질문게시판 바로가기]** 안내 모달 노출
     - *(운영/CS 5대 문의)* `'결제/취소/환불'`, `'교재/배송/파손'`, `'동영상 재생/기기잠김'`, `'합격환급/쿠폰/포인트'`, `'교재 정답지/기타'` 선택 시 ➔ 관련 주문번호(`ORD-*`)·강좌 선택 후 문의 등록
   - **[Step 2. 백오피스 1:1 문의 인입 및 통합 컨텍스트 열람 (`ADMN-BRD-002`)]**
     - `ADMN-BRD-002` 목록에 `미답변` 상태로 인입 ➔ CS 담당자가 문의 클릭 시 화면 우측에 **[수험생 요약 정보 + 바인딩된 주문/배송/수강/진도율 현황 + 5대 업무 화면 즉시 이관 버튼]** 표시
   - **[Step 3. 문의 유형별 5대 백오피스 업무 화면 즉시 분기 실행]**
     - **[분기 ① 환불/취소 요청]** 문의창 내 **`[환불 심사 이관 (`ADMN-RFD-002`)]`** 클릭 ➔ 해당 주문이 자동 로드된 복합환불 화면으로 넘어가 반품 수거 지시 또는 부분환불 즉시 실행
     - **[분기 ② 배송지 변경 / 출고 보류 / 파손 재출고]** **`[주문·출고 관리 (`ADMN-ORD-001/002`)]`** 클릭 ➔ `결제완료` 상태면 배송지 즉시 변경, `배송준비중` 이후면 3PL 출고보류/맞교환 재출고 등록
     - **[분기 ③ 동영상 오류 / 중복세션 차단 / 진도율 누락]** **`[회원 수강·기기 제어 (`ADMN-USER-003/004`)]`** 클릭 ➔ 중복 IP 세션 강제 로그아웃, 등록 기기 초기화, 또는 오류 차시 진도율 100% 수동 보정
     - **[분기 ④ 합격환급 서류 / 혜택 누락]** **`[환급반 심사 (`ADMN-SETT-006`)]`**에서 보완 서류 확인, 또는 **`[회원 포인트/쿠폰 (`ADMN-USER-002`)]`**에서 누락 혜택·CS 보상용 `무상 P` 지급
     - **[분기 ⑤ 교재 정답지 요청]** 무료 자료실 **`[정답지 관리 (`ADMN-BRD-009`)]`**의 최신 정답지 PDF 다운로드 경로 안내 또는 저작권자(`ROLE_PARTNER_COPYRIGHT`)에게 개정 정답지 업로드 요청
   - **[Step 4. 답변 완료 저장 및 수험생 알림톡 발송 (`ADMN-BRD-002` ➔ `USER-MY-010`)]** 분기 화면 처리 후 `ADMN-BRD-002`에 처리 결과 답변 등록 ➔ `[답변 완료]` 클릭 즉시 수험생에게 알림톡(`ADMN-CONF-004`) 발송 및 프론트 마이페이지(`USER-MY-010`) 답변 노출

2. **[Flow 4-2] 수험생 합격환급 신청 ➔ 진도율·4대 증빙 심사 ➔ 22% 원천징수 지급 및 강사 정산 차감 플로우**
   - **[Step 1. 프론트 수험생 합격환급 신청 (`USER-MY-011-S1`)]** 시험 합격 발표 후 수험생이 내 강의실에서 환급 신청 모달 진입 ➔ 해당 패키지에 설정된 **목표 진도율 변수(`target_progress_rate`, 예: 90%)** 달성 여부 실시간 확인 후 **4대 필수 증빙(합격증명서·수강후기·신분증 사본·본인명의 통장사본)** 업로드 제출
   - **[Step 2. 백오피스 환급 요건 및 4대 증빙 심사 (`ADMN-SETT-006`)]** 운영자가 환급반 관리(`ADMN-SETT-006`)에서 진도율 자동 판정 결과 및 첨부 서류 4종 검수 (서류 미비 시 `[보완 요청]` 알림톡 발송 ➔ 수험생 재업로드 / 이상 없을 시 `[심사 승인]`)
   - **[Step 3. 실지급액 확정 및 강사 정산 차감·지원금 한도 복원 연계 (`ADMN-SETT-006` ➔ `ADMN-SETT-002`)]**
     - 환급 대상액(패키지 실결제액에서 **실물 교재 실판매가를 차감한 순수 강좌 결제액**)에서 **기타소득 원천징수 세액(22%)**을 공제한 실지급액 확정 및 계좌 이체 실행
     - 귀속 강사 계약이 환급 분담형(옵션 B 50% 분담 / 옵션 C 전액 분담)인 경우 **승인월의 강사 정산 차감 대기열로 자동 이관** (최저보장 `MMG` 적용 강사는 보전금 산정 후 별도 차감, 매출연동 개발지원금 차감 발생 시 **차감액만큼 강사 약정 총한도 잔여분 즉시 복원**)

3. **[Flow 4-3] 매월 초 사전 대사 ➔ 1~11단계 월간 정산 배치 ➔ 파트너 확인·마감 및 마감 후 전기오류수정 플로우**
   - **[Step 1. 월마감 전 3대 사전 검증 게이트 통과 (`ADMN-SETT-004` / `009` / `008`)]**
     - ① PG 결제·취소 대사(`ADMN-SETT-004`) 불일치 `0건` 확인
     - ② 선급금·매절·2계층 분할 마일스톤(`ADMN-SETT-009`) 당월 지급 승인
     - ③ 국세청 사업자 상태/과세유형(`ADMN-SETT-008`) 유효기간(90일) 검증 완료
   - **[Step 2. 월간 정산 1~11단계 통합 배치 실행 (`ADMN-SETT-002`)]** 패키지 안분(실판매가 비율) ➔ 강사료 R/S 및 **도서 인세(자사발행은 실결제액 기준, 위탁은 계약원장 선택 기준가)** 산출 ➔ 합격환급 분담금 차감 ➔ 선급금 상계 ➔ **단 1회 원단위 절사** ➔ 계약원장 최소 지급/청구 기준액 대조 후 지급확정/이월 판정
   - **[Step 3. 파트너 정산서 열람·역발행 승인 및 최종 마감 (`ADMN-SETT-002` ➔ `Locked`)]** 파트너 강사(`ROLE_PARTNER_INST`)·저작권자(`ROLE_PARTNER_COPYRIGHT`)가 로그인하여 본인 정산서 확인 및 세금계산서 역발행 승인 ➔ 재무담당자가 최종 마감(`Locked = True`) 및 지급 이체 집행
   - **[Step 4. 마감 후 오류 발생 시 전기오류수정 및 4가지 과세유형별 증빙 정정 (`ADMN-SETT-005`)]** 이미 마감된 과거 정산월 데이터는 절대 직접 수정하지 않고, `ADMN-SETT-005`에서 차월 가감 정산전표(`ADJ-*`)를 생성한 뒤 수취인 과세유형에 따른 **4가지 증빙 정정 방식(① 일반/간이 세금계산서 수정세금계산서, ② 면세사업자 수정계산서, ③ 3.3%/8.8% 원천징수 차월 상계·수정신고, ④ 간이영수증·기타 증빙 재징구)**으로 처리
"""

# 1. Update docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md
spec_text = SPEC_V4.read_text(encoding="utf-8")

def inject_workflow_into_spec(text: str, marker_before: str, wf_block: str, check_str: str) -> str:
    if check_str in text:
        return text
    assert marker_before in text, f"Marker not found: {marker_before}"
    return text.replace(marker_before, wf_block.strip() + "\n\n---\n\n" + marker_before, 1)

spec_text = inject_workflow_into_spec(
    spec_text,
    "## **3.2 [Set 2]",
    SET1_WORKFLOW_MD,
    "[Flow 1-1] 수험생 회원가입"
)
spec_text = inject_workflow_into_spec(
    spec_text,
    "## **3.3 [Set 3]",
    SET2_WORKFLOW_MD,
    "[Flow 2-1] 신규 파트너"
)
spec_text = inject_workflow_into_spec(
    spec_text,
    "## **3.4 [Set 4]",
    SET3_WORKFLOW_MD,
    "[Flow 3-1] 수험생 장바구니 복합결제"
)

if "[Flow 4-1] 수험생 프론트 1:1 문의 등록부터" not in spec_text:
    spec_text = spec_text.rstrip() + "\n\n" + SET4_WORKFLOW_MD.strip() + "\n"

SPEC_V4.write_text(spec_text, encoding="utf-8")
print("[OK] Updated docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md with Set 1~4 End-to-End workflows.")

# 2. Update 00_WORKFLOW_GUIDE_baseline.html in both prototype/ and prototype_clean/
E2E_HTML_SECTION = """
        <!-- Set 1 ~ Set 4 전사 End-to-End 실무 운영 플로우 (프론트/오프라인 출발 ➔ 백오피스 분기·완결) -->
        <section class="section" id="set1-4-e2e-workflows" style="margin-top: 28px;">
            <div class="sec-head">
                <div>
                    <span class="badge b-pri" style="margin-bottom:6px;">통합 상세 설계서 v4.0 · Set 1 ~ Set 4 기준</span>
                    <h2 style="margin:0; font-size:18px; font-weight:800;">0️⃣ [Set 1 ~ Set 4] 실무자 End-to-End 표준 업무 플로우 (프론트/오프라인 출발 ➔ 백오피스 완결)</h2>
                    <p style="margin:4px 0 0; font-size:13px; color:var(--muted);">
                        수험생의 프론트 화면 액션(1:1 문의·결제·환불·환급신청) 및 오프라인 신규/변경 계약 체결에서 출발하여 백오피스 각 화면으로 분기·처리·완결되는 핵심 실무 SOP입니다.
                    </p>
                </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap:16px; margin-top:14px;">
                <!-- Set 1 Card -->
                <div style="background:#fff; border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:var(--shadow);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span class="badge b-pri">Set 1 · 회원 / 수강제어 / 프로모션</span>
                        <span style="font-size:12px; color:var(--sub); font-weight:600;">USER-AUTH/VOD/PROM ↔ ADMN-USER/PROM</span>
                    </div>
                    <h3 style="margin:0 0 8px; font-size:15px; font-weight:800;">회원 혜택 발급 · 수강 불편(세션/진도율/홀딩) · 기획전 통제</h3>
                    <ol style="margin:0; padding-left:18px; font-size:13px; color:var(--ink); line-height:1.65;">
                        <li><strong>[가입/웰컴혜택]</strong> 프론트 본인인증 가입(<code>USER-AUTH-002</code>, 탈퇴 30일 재가입 검증) ➔ 웰컴 <strong>무상 P(5,000P·2년)</strong> + 웰컴쿠폰(<code>D+21</code>) 자동 발급</li>
                        <li><strong>[세션/기기 잠김 CS]</strong> 프론트 1세션 중복차단 문의 인입 ➔ <a href="ADMN-USER-001_baseline.html" style="color:var(--pri); font-weight:700;">회원관리(ADMN-USER-001/003)</a> 진입 ➔ 비정상 IP <strong>[강제 로그아웃]</strong> 또는 <strong>[기기 초기화]</strong></li>
                        <li><strong>[0초 OT 진도율 보정 / 홀딩]</strong> 플레이어 오류·0초 강의 왜곡 시 <code>ADMN-USER-004</code>에서 <strong>[진도율 100% 수동 보정]</strong>(환급반 판정 즉시 연동) / 수강 홀딩(최대 3회·30일) 처리</li>
                        <li><strong>[기획전 혜택 잠금]</strong> <a href="ADMN-PROM-001_baseline.html" style="color:var(--pri); font-weight:700;">이벤트 관리(ADMN-PROM-001)</a>에서 특가 기획전 등록 시 <code>쿠폰/적립 차단(S1)</code> 스위치 ON ➔ 프론트 결제창 혜택 자동 잠금</li>
                    </ol>
                </div>

                <!-- Set 2 Card -->
                <div style="background:#fff; border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:var(--shadow);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span class="badge b-ok">Set 2 · 오프라인 계약 / 도서 / 강좌 / 패키지</span>
                        <span style="font-size:12px; color:var(--sub); font-weight:600;">오프라인 계약서 ↔ ADMN-INST/BOOK/PROD/SETT-001</span>
                    </div>
                    <h3 style="margin:0 0 8px; font-size:15px; font-weight:800;">신규/변경 파트너 계약 체결 · 도서(10% 할인) · 패키지 판매 오픈</h3>
                    <ol style="margin:0; padding-left:18px; font-size:13px; color:var(--ink); line-height:1.65;">
                        <li><strong>[신규 계약 체결 출발]</strong> 오프라인 계약서 날인 및 사업자등록증·통장사본 수취 ➔ <a href="ADMN-INST-001_baseline.html" style="color:var(--pri); font-weight:700;">권리자 계약원장(ADMN-INST-001)</a> 등록 + <a href="ADMN-SETT-008_baseline.html" style="color:var(--pri); font-weight:700;">국세청 조회(SETT-008)</a>(장애 시 증빙첨부 수기지정) + <a href="ADMN-CONF-005_baseline.html" style="color:var(--pri); font-weight:700;">파트너 계정 스코프 발급(CONF-005)</a></li>
                        <li><strong>[계약 조건 변경(재계약)]</strong> 변경 합의서 날인 시 과거 마감월 보호를 위해 기존 행 덮어쓰기 금지 ➔ <code>ADMN-INST-001</code>에 <strong>신규 효력 시작일(<code>effective_from</code>) 이력 행 추가</strong></li>
                        <li><strong>[도서/강좌/패키지 오픈]</strong> <a href="ADMN-BOOK-001_baseline.html" style="color:var(--pri); font-weight:700;">도서원장(BOOK-001)</a> SKU 등록 ➔ <a href="ADMN-PROD-004_baseline.html" style="color:var(--pri); font-weight:700;">교재관리(PROD-004)</a> <strong>정가 및 최대 10% 할인율(실판매가)</strong> 세팅 ➔ <a href="ADMN-SETT-001_baseline.html" style="color:var(--pri); font-weight:700;">지분 100% 매핑(SETT-001)</a> 잠금해제 ➔ <a href="ADMN-PROD-005_baseline.html" style="color:var(--pri); font-weight:700;">패키지(PROD-005)</a> 환급 진도율 변수 설정 후 판매 오픈</li>
                    </ol>
                </div>

                <!-- Set 3 Card -->
                <div style="background:#fff; border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:var(--shadow);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span class="badge" style="background:var(--warn-soft); color:var(--warn); border:1px solid var(--warn-line);">Set 3 · 복합결제 / 3PL 출고·송장 / 반품·환불</span>
                        <span style="font-size:12px; color:var(--sub); font-weight:600;">USER-PAY/MY ↔ ADMN-ORD-001/002/RFD-002</span>
                    </div>
                    <h3 style="margin:0 0 8px; font-size:15px; font-weight:800;">일일 교재 출고 · 운송장 엑셀 업로드 · 반품검수 및 복합환불</h3>
                    <ol style="margin:0; padding-left:18px; font-size:13px; color:var(--ink); line-height:1.65;">
                        <li><strong>[출고지시 엑셀 다운로드 & 취소 잠금]</strong> 프론트 복합결제(도서 실결제액 3만원↑ 무료배송) ➔ 매일 오전 <a href="ADMN-ORD-001_baseline.html" style="color:var(--pri); font-weight:700;">주문/출고(ADMN-ORD-002)</a>에서 <strong>[3PL 출고지시 엑셀 다운로드]</strong> 클릭 ➔ 즉시 <code>배송준비중</code> 전환 및 프론트 수험생 직접취소 잠금(Lock)</li>
                        <li><strong>[운송장 엑셀 일괄 업로드]</strong> 3PL 창고 포장 후 송장 채번 ➔ <code>ADMN-ORD-002</code>에 <strong>[운송장 엑셀 일괄 업로드]</strong> 실행 ➔ 즉시 <code>배송중</code> 전환 + 재고 차감 + 수험생 배송출발 알림톡 발송</li>
                        <li><strong>[반품 입고 검수 & 복합환불]</strong> 프론트(<code>USER-MY-006</code>) 또는 1:1 문의발 환불 접수 ➔ 3PL 반품 도서 도착 시 <strong>[반품입고 검수완료]</strong> 체크 ➔ <a href="ADMN-RFD-002_baseline.html" style="color:var(--pri); font-weight:700;">복합환불(ADMN-RFD-002)</a>에서 기수강 공제 + 훼손교재 실판매가 공제 + <strong>기적립 <code>적립 P</code> 회수(부족 시 현금차감/마이너스 부채 전환)</strong> 후 PG 취소</li>
                    </ol>
                </div>

                <!-- Set 4 Card -->
                <div style="background:#fff; border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:var(--shadow);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span class="badge" style="background:var(--purple-soft); color:var(--purple); border:1px solid #ddd6fe;">Set 4 · 1:1 문의 분기 / 합격환급 / 월간정산</span>
                        <span style="font-size:12px; color:var(--sub); font-weight:600;">USER-CS-003/MY-011 ↔ ADMN-BRD-002/SETT-006/002</span>
                    </div>
                    <h3 style="margin:0 0 8px; font-size:15px; font-weight:800;">프론트 1:1 문의 5대 분기 처리 · 합격환급 심사 · 월간 정산 마감</h3>
                    <ol style="margin:0; padding-left:18px; font-size:13px; color:var(--ink); line-height:1.65;">
                        <li><strong>[프론트 1:1 문의 접수 & 5대 분기]</strong> 수험생이 프론트(<code>USER-CS-003</code>) 문의 등록(학습질문은 네이버 카페 아웃링크 분리) ➔ <a href="ADMN-BRD-006_baseline.html" style="color:var(--pri); font-weight:700;">1:1 문의 허브(ADMN-BRD-002)</a> 인입 후 <strong>①환불이관(<code>RFD-002</code>) ②배송/출고제어(<code>ORD-002</code>) ③기기/진도율보정(<code>USER-003/004</code>) ④환급/혜택(<code>SETT-006</code>) ⑤정답지(<code>BRD-009</code>)</strong>로 즉시 분기 처리 후 답변 알림톡 발송</li>
                        <li><strong>[합격환급 심사 & 강사 차감]</strong> 프론트 환급신청(<code>USER-MY-011-S1</code>) ➔ <a href="ADMN-SETT-006_baseline.html" style="color:var(--pri); font-weight:700;">환급반 관리(ADMN-SETT-006)</a>에서 상품별 목표 진도율 및 4대 증빙 승인 ➔ 22% 세액 공제 지급 + 강사 분담 차감(지원금 한도 자동 복원)</li>
                        <li><strong>[월간 정산 마감 & 사후 보정]</strong> 사전 대사(<code>SETT-004/008/009</code>) ➔ <a href="ADMN-SETT-002_baseline.html" style="color:var(--pri); font-weight:700;">1~11단계 배치(SETT-002)</a> ➔ 파트너 역발행 승인 후 마감(<code>Locked</code>) / 마감 후 오류는 <a href="ADMN-SETT-005_baseline.html" style="color:var(--pri); font-weight:700;">전기오류수정(SETT-005)</a>에서 4가지 과세유형별 증빙 정정 처리</li>
                    </ol>
                </div>
            </div>
        </section>
"""

for pdir in PROTO_DIRS:
    wf_file = pdir / "00_WORKFLOW_GUIDE_baseline.html"
    if not wf_file.exists():
        continue
    html = wf_file.read_text(encoding="utf-8")
    if 'id="set1-4-e2e-workflows"' not in html:
        target_anchor = "1️⃣ 전체 12개 화면의 4단계 업무 여정 맵"
        section_pos = html.find(target_anchor)
        assert section_pos != -1, f"Anchor not found in {wf_file}"
        sec_start = html.rfind("<section", 0, section_pos)
        assert sec_start != -1, f"<section not found before anchor in {wf_file}"
        html = html[:sec_start] + E2E_HTML_SECTION.strip() + "\n\n        " + html[sec_start:]
        wf_file.write_text(html, encoding="utf-8")
        print(f"[OK] Injected Set 1~4 End-to-End workflows into {wf_file}")

print("[DONE] All workflow updates applied successfully.")
