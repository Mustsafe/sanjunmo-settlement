# 업무플로우 개편용 정본 추출 리포트

> extract_workflow_sources.py 자동 생성 · 읽기 전용

## 1. 03권 용어·화면 대조표 (원문)

| 코드 | 노출 메뉴명 | 역할 구분 | 한 줄 설명 |
| :---- | :---- | :---- | :---- |
| ADMN-INST-001 | 권리자 계약 원장 | 설정 | 권리자·계약·요율·상계·최저보장 보전금(MMG)·최소지급 기준 등록 |
| ADMN-INST-002 | 약정금 마일스톤 검수 및 승인 원장 | 검증 | 비정기 약정금·매절 대금 이행 검수 및 귀속월 승인 (출금 기능 배제) |
| ADMN-BOOK-001 | 도서 공급 원장 | 설정 | 도서 공급 형태(book\_supply\_type)와 정가·수수료·재고 경로 관리 |
| ADMN-SETT-001 | 상품별 권리자 매핑 | 설정 | 강의·도서 상품(SKU) 단위 1계층 지분(합계 100%) 단일 편집 화면 |
| ADMN-SETT-002 | 월간 정산 및 집행 | 집행 | 1\~11단계 배치, 정산서 생성, 마감 잠금, 펌뱅킹 이체 단일 창구 |
| ADMN-SETT-003 | 결번 | 결번 | 예약 없이 결번 유지, 신규 화면에 재사용하지 않음 |
| ADMN-SETT-004 | PG 정산 원장 대사 | 검증 | 결제대행사(PG) 원장 대사 및 차이 원인 소명 통제 |
| ADMN-SETT-005 | 정산 수동 조정 | 집행 보조 | 수기 정산 병행 및 전기오류수정 조정 라인 등록 |
| ADMN-SETT-006 | 합격 환급반 관리 | 운영 | 조건부 환급 판정 및 계약별 분담 옵션(A/B/C) 연동 |
| ADMN-SETT-007 | 수취인 분할 지분 설정 | 설정 | 계약·권리자 단위 2계층 수취인 분할 비율(합계 100%) 관리 |
| ADMN-SETT-008 | 사업자등록 확인 이력 | 검증 | 국세청 API 응답값 기반 세무 유형 판정 및 상태 감지 |
| ADMN-SETT-009 | 내부 정산 조회 | 조회 전용 | 자사 매출(일반 상품 판매매출(Pipeline 2.3)) 포함 전체 정산 라인 조회 (자금 집행 기능 없음) |
| ADMN-USER-007 | 민감 정보 열람 사유 입력 팝업 | 통제 | 마스킹 해제 시 10자 이상 열람 사유 입력 강제 |
| ADMN-CONF-010 | 시스템 감사 로그 | 통제 | 민감 정보 조회, 지분율 변경(변경 사유 포함), 마감 및 승인 이력 전수 보존 |

## 2. 화면 코드 통합 대조

| 코드 | 03 대조표 화면명 | 03 코드값사전 명칭 | 통합설계서[A] | README | SNB | HTML 파일 | docs 등장 파일 수 |
| :--- | :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| ADMN-BOOK-001 | 도서 공급 원장 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-BRD-001 |  |  | – | ✓ | ✓ | ✓ | 4 |
| ADMN-BRD-002 |  |  | – | ✓ | ✓ | ✓ | 7 |
| ADMN-BRD-004 |  |  | – | – | ✓ | – | 4 |
| ADMN-BRD-005 |  |  | – | – | ✓ | ✓ | 3 |
| ADMN-BRD-006 |  |  | – | ✓ | ✓ | – | 3 |
| ADMN-BRD-009 |  |  | – | ✓ | ✓ | – | 3 |
| ADMN-BRD-010 |  |  | – | – | ✓ | – | 3 |
| ADMN-CONF-001 |  |  | ✓ | ✓ | ✓ | ✓ | 5 |
| ADMN-CONF-002 |  |  | ✓ | – | ✓ | ✓ | 3 |
| ADMN-CONF-003 |  |  | ✓ | – | ✓ | ✓ | 4 |
| ADMN-CONF-004 |  |  | ✓ | – | ✓ | ✓ | 8 |
| ADMN-CONF-005 |  |  | – | ✓ | ✓ | ✓ | 11 |
| ADMN-CONF-006 |  |  | – | – | ✓ | – | 10 |
| ADMN-CONF-007 |  |  | – | ✓ | – | – | 3 |
| ADMN-CONF-008 |  |  | – | – | ✓ | – | 4 |
| ADMN-CONF-010 | 시스템 감사 로그 |  | – | – | ✓ | ✓ | 5 |
| ADMN-CRS-002 |  |  | – | – | ✓ | – | 0 |
| ADMN-DASH-001 |  |  | ✓ | ✓ | ✓ | ✓ | 10 |
| ADMN-FREE-001 |  |  | – | – | ✓ | – | 0 |
| ADMN-INFO-001 |  |  | – | – | ✓ | – | 0 |
| ADMN-INST-001 | 권리자 계약 원장 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-INST-002 | 약정금 마일스톤 검수 및 승인 원장 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-JOIN-002 |  |  | – | – | ✓ | – | 0 |
| ADMN-LECT-002 |  |  | – | – | ✓ | – | 0 |
| ADMN-LOGIN-001 |  |  | ✓ | ✓ | ✓ | ✓ | 3 |
| ADMN-LOGIN-002 |  |  | ✓ | – | ✓ | – | 3 |
| ADMN-LOGIN-003 |  |  | ✓ | – | ✓ | – | 3 |
| ADMN-ORD-001 |  |  | ✓ | ✓ | ✓ | ✓ | 13 |
| ADMN-ORD-002 |  |  | ✓ | ✓ | ✓ | – | 7 |
| ADMN-ORD-003 |  |  | – | – | ✓ | – | 1 |
| ADMN-PAY-001 |  |  | – | – | ✓ | – | 0 |
| ADMN-PROD-001 |  |  | ✓ | ✓ | ✓ | ✓ | 7 |
| ADMN-PROD-002 |  |  | ✓ | – | ✓ | ✓ | 4 |
| ADMN-PROD-003 |  |  | ✓ | – | ✓ | ✓ | 4 |
| ADMN-PROD-004 |  |  | ✓ | – | ✓ | ✓ | 8 |
| ADMN-PROD-005 |  |  | ✓ | ✓ | ✓ | ✓ | 7 |
| ADMN-PROD-006 |  |  | ✓ | – | ✓ | ✓ | 4 |
| ADMN-PROD-007 |  |  | ✓ | ✓ | ✓ | ✓ | 3 |
| ADMN-PROM-001 |  |  | ✓ | ✓ | ✓ | ✓ | 5 |
| ADMN-PROM-002 |  |  | ✓ | ✓ | ✓ | ✓ | 5 |
| ADMN-PROM-003 |  |  | ✓ | – | ✓ | – | 3 |
| ADMN-RFD-001 |  |  | – | – | ✓ | – | 9 |
| ADMN-RFD-002 |  |  | ✓ | ✓ | ✓ | ✓ | 12 |
| ADMN-RFD-003 |  |  | – | ✓ | ✓ | – | 5 |
| ADMN-RFD-004 |  |  | ✓ | ✓ | ✓ | – | 4 |
| ADMN-SETT-001 | 상품별 권리자 매핑 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-SETT-002 | 월간 정산 및 집행 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 15 |
| ADMN-SETT-003 | 결번 | 화면 코드 | – | ✓ | ✓ | – | 4 |
| ADMN-SETT-004 | PG 정산 원장 대사 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 8 |
| ADMN-SETT-005 | 정산 수동 조정 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-SETT-006 | 합격 환급반 관리 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 7 |
| ADMN-SETT-007 | 수취인 분할 지분 설정 | 화면 코드 | – | – | ✓ | ✓ | 7 |
| ADMN-SETT-008 | 사업자등록 확인 이력 | 화면 코드 | – | ✓ | ✓ | ✓ | 7 |
| ADMN-SETT-009 | 내부 정산 조회 | 화면 코드 | ✓ | ✓ | ✓ | ✓ | 9 |
| ADMN-SETT-010 |  |  | – | – | ✓ | – | 2 |
| ADMN-SETT-011 |  |  | – | ✓ | ✓ | ✓ | 7 |
| ADMN-STAT-001 |  |  | – | ✓ | ✓ | – | 2 |
| ADMN-STAT-002 |  |  | – | ✓ | – | – | 3 |
| ADMN-USER-001 |  |  | ✓ | ✓ | ✓ | ✓ | 5 |
| ADMN-USER-002 |  |  | – | – | ✓ | – | 7 |
| ADMN-USER-003 |  |  | ✓ | ✓ | ✓ | – | 6 |
| ADMN-USER-004 |  |  | ✓ | ✓ | – | – | 8 |
| ADMN-USER-005 |  |  | – | ✓ | ✓ | – | 5 |
| ADMN-USER-006 |  |  | ✓ | ✓ | ✓ | – | 5 |
| ADMN-USER-007 | 민감 정보 열람 사유 입력 팝업 |  | – | ✓ | ✓ | ✓ | 4 |

## 3. 불일치 요약

- SNB에 있으나 정본(03권·통합설계서[A])에 없음: ADMN-BRD-001, ADMN-BRD-002, ADMN-BRD-004, ADMN-BRD-005, ADMN-BRD-006, ADMN-BRD-009, ADMN-BRD-010, ADMN-CONF-005, ADMN-CONF-006, ADMN-CONF-008, ADMN-CRS-002, ADMN-FREE-001, ADMN-INFO-001, ADMN-JOIN-002, ADMN-LECT-002, ADMN-ORD-003, ADMN-PAY-001, ADMN-RFD-001, ADMN-RFD-003, ADMN-SETT-010, ADMN-SETT-011, ADMN-STAT-001, ADMN-USER-002, ADMN-USER-005
- 정본에 있으나 README에 없음: ADMN-CONF-002, ADMN-CONF-003, ADMN-CONF-004, ADMN-CONF-010, ADMN-LOGIN-002, ADMN-LOGIN-003, ADMN-PROD-002, ADMN-PROD-003, ADMN-PROD-004, ADMN-PROD-006, ADMN-PROM-003, ADMN-SETT-007
- 정본에 있으나 SNB에 없음: ADMN-USER-004
- 03권 내부 명칭 불일치: ADMN-BOOK-001: 대조표 '도서 공급 원장' / 코드값사전 '화면 코드'; ADMN-INST-001: 대조표 '권리자 계약 원장' / 코드값사전 '화면 코드'; ADMN-INST-002: 대조표 '약정금 마일스톤 검수 및 승인 원장' / 코드값사전 '화면 코드'; ADMN-SETT-001: 대조표 '상품별 권리자 매핑' / 코드값사전 '화면 코드'; ADMN-SETT-002: 대조표 '월간 정산 및 집행' / 코드값사전 '화면 코드'; ADMN-SETT-003: 대조표 '결번' / 코드값사전 '화면 코드'; ADMN-SETT-004: 대조표 'PG 정산 원장 대사' / 코드값사전 '화면 코드'; ADMN-SETT-005: 대조표 '정산 수동 조정' / 코드값사전 '화면 코드'; ADMN-SETT-006: 대조표 '합격 환급반 관리' / 코드값사전 '화면 코드'; ADMN-SETT-007: 대조표 '수취인 분할 지분 설정' / 코드값사전 '화면 코드'; ADMN-SETT-008: 대조표 '사업자등록 확인 이력' / 코드값사전 '화면 코드'; ADMN-SETT-009: 대조표 '내부 정산 조회' / 코드값사전 '화면 코드'

## 4. 통합설계서 [A] 페어 매핑표 행

- [3.1.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **관리자 게이트웨이** | *(백오피스 전용 진입점 — 사용자 계정 로그인 차단)* | • `ADMN-LOGIN-001` (`-P1`) : 관리자/파트너 통합 로그인 및 5회 실패 잠금<br>• `ADMN-LOGIN-002` : 관리자 아이디 찾기 (이름+SMS 인증, 앞 3자리 외 마스킹)<br>• `ADMN-LOGIN-003` : 관리자 비밀번호 찾기 (이메일+SMS 인증 후 즉시 재설정·잠금 해제) | • 로그인 시도/실패/잠금 전 이벤트 `ADMN-
- [3.1.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **회원 인증 · 가입** | • `USER-AUTH-001` : 통합 로그인 (이메일 + 카카오/네이버 소셜 원클릭)<br>• `USER-AUTH-002` : 회원가입 (약관동의 · 휴대폰 본인인증 DI · 관심 자격증 선택)<br>• `USER-AUTH-003` : 아이디/비밀번호 찾기 (SMS 본인인증 원스톱 재설정) | • `ADMN-USER-001` (`-P1`) : 회원 목록 조회 및 10자 사유 기반 엑셀 다운로드<br>• `ADMN-USER-0
- [3.1.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **내 정보 · 수강/진도 · 제재 관리** | • `USER-MY-009` : 내 정보 수정 · 소셜 연동 관리 · 회원 탈퇴 신청<br>• `USER-MY-001~003` : 내 강의실 수강 및 StarPlayer+ 재생 (수강/진도 데이터 원천) | • `ADMN-USER-003` : 회원 수강기간 강제 조정 · 동시접속 1세션 강제 초기화 (2차 기기슬롯)<br>• `ADMN-USER-004` (`-P1`) : 강의별 가중평균 진도율·이어보기 조회 및
- [3.1.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **타겟팅 · 기획전 · 이벤트** | • `USER-PROM-001` : 기획전(`[기획전]` 탭) · 이벤트(`[이벤트]` 탭) 통합 목록<br>• `USER-PROM-002` : 동적 슬러그(`/event/{slug}`) 랜딩 상세 및 매핑 특가 상품 카드 | • `ADMN-USER-006` (`-S1~S3`, `-P1`) : 수평적 그룹·태그 관리 (동적 06:00 배치 / 정적 그룹)<br>• `ADMN-PROM-001` (`-S1~S3`) : 기획
- [3.1.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **쿠폰 · 포인트 원장** | • `USER-MY-007` : 마이페이지 > 내 쿠폰함 (난수 쿠폰 등록 · 만료일 표시)<br>• `USER-MY-008` : 마이페이지 > 내 포인트 내역 (`적립 P` / `무상 P` 잔액 · 적립/사용/소멸예정) | • `ADMN-PROM-002` (`-P1`) : 쿠폰 마스터 등록·관리 (정률 `40%` / 정액 `200,000원` Cap 하드락 · 도서정가제 자동 바인딩)<br>• `ADMN-PROM-003` : 
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **카테고리 체계** | • GNB 수강신청 직무·자격증 메뉴 트리 및 과정 분류 필터 | • `ADMN-PROD-001` : 카테고리 관리 (자격증 대분류 · 과정 중분류 2Depth 동적 트리 및 드래그 정렬) | • 노출(`Y`) 상태의 1·2차 분류만 프론트 GNB 및 강좌/교재 등록 폼에 동적 바인딩 (하위 상품 존재 시 삭제 차단) |
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **영상(Unit) · 내 강의실 · VOD 플레이어** | • `USER-MY-001~003` : 내 강의실 (수강중/일시정지/종료 탭 · **StarPlayer+ DRM 플레이어** · 교안 PDF 다운로드 · 불합격 무상 연장 신청) | • `ADMN-PROD-002` (`-S1`) : 강의(영상 Unit) 마스터 관리 (VOD Key · 초 단위 재생시간 · 맛보기 Y/N · 교안 PDF 첨부) | • 30초 Heartbeat API 기반 이어보기·가
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **단과 강좌 · 무료특강** | • `USER-CRS-001~002` : 단과 강좌 목록/상세 (맛보기 재생 · 연관 주/부교재 함께 구매 선택)<br>• `USER-FREE-001` : 무료특강 (기본이론/합격전략/**빈출문제**/개정법령) | • `ADMN-PROD-003` (`-S1` 커리큘럼 조립, `-S2` 단과 강좌 등록·수정) | • 평생교육시설 온라인 교육용역 **면세(`VAT 0%`)** 고정<br>• `ADMN-SETT-001` 1계층 권
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **실물 교재 · 도서 공급 원장** | • `USER-BOOK-001~002` : 교재 목록/상세 (**도서 정가 취소선 + 최대 10% 기본할인가 노출** · 미리보기 · 연관 강좌 역노출) | • `ADMN-PROD-004` (`-S1` 교재 등록·수정, `-P1` 재고 수동조정)<br>• `ADMN-BOOK-001` (`-S1`) : 도서 공급 원장 (4대 공급형태 · 원가/인세율/위탁수수료 · 정가 스냅샷 이력) | • 도서 면세(`VAT 0%`),
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **패키지 (올패스 · 합격환급반)** | • `USER-PKG-001~002` : 패키지/합격환급반 목록 및 상세 (포함 강좌·교재 구성 및 교재 혜택 제외 고지) | • `ADMN-PROD-005` (`-S1`) : 패키지 상품 구성 (강좌 결제액 + 교재 실판매가 자동 분리 렌더링 · 단과 기준가 비율 안분 · 환급 조건 설정) | • 장바구니/주문서 인입 시 강좌 라인(할인 적용)과 교재 라인(최대 10% 기본할인가 고정) 자동 분할 생성 |
- [3.2.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **강사관 전시 · 일반 소비재** | • `USER-INST-001~002` : 강사관 목록 및 강사 개별 홈 (홍보 VOD · 약력 · 담당 강좌/저서 · 수강후기)<br>• 일반 상품(굿즈/학습용품) 구매 라인 | • `ADMN-PROD-006` (`-S1`) : 강사 노출 정보 관리 (`ADMN-INST-001` 권리자 바인딩)<br>• `ADMN-PROD-007` (`-S1`, `-P1` 재고, `-P2` 매입처) : 일반 소비재 마스터 | • 강사
- [3.3.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **장바구니 · 복합 PG 주문/결제** | • `USER-CART-001` : 장바구니 목록 (강좌/교재/일반상품 분리 · 선택 합산)<br>• `USER-PAY-001` : 주문서 작성 · 혜택 적용 · 토스페이먼츠 결제창 호출<br>• `USER-PAY-002` : 주문 완료 및 가상계좌 채번 안내 | • `ADMN-ORD-001` : 주문 내역 통합 관리 (실결제금액 기준 조회)<br>• `ADMN-ORD-001-S1` : 주문 상세 · 배송지 수동 
- [3.3.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **주문/배송 조회 · 3PL 풀필먼트** | • `USER-MY-004` : 마이페이지 > 주문/결제 내역 조회<br>• `USER-MY-005` : 배송 상태 추적 및 출고지시 전 배송지 직접 변경 | • `ADMN-ORD-002` : 3PL 풀필먼트 배송 관리 (출고대기 목록 · 발주 엑셀 다운로드)<br>• `ADMN-ORD-002-S1/S2` : 배송중(운송장 추적·정정) / 배송완료 탭<br>• `ADMN-ORD-002-S3` : 반품 수거 및 창
- [3.3.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **취소 · 부분환불 · 마이너스 부채 · 사후보정** | • `USER-MY-006` : 취소 · 부분환불 · 교재 반품 신청 및 예상 환불금 조회 | • `ADMN-RFD-004` : 환불/반품 통합 요청 목록 (처리기한 5영업일 SLA)<br>• `ADMN-RFD-002` (`-S1`) : 법정 기준 인강·교재 부분환불 자동 계산기 및 1:1 문의 이관 연동<br>• `ADMN-RFD-002-P1/P2` : 기적립 포인트 회수 부족분 **마이너스(`-`
- [3.4.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **합격환급 신청 · 심사 · 정산 분담** | • `USER-MY-011` (`-S1`) : 마이페이지 > 합격환급 신청 (상품별 설정 목표 진도율 달성 자가진단 · 4대 증빙 제출 · 제세공과금 22% 고지) | • `ADMN-SETT-006` : 합격환급반 심사 · 지급 및 권리자 정산 분담 관리 (상하 분리형 목록 + 4대 증빙·명의 3중 대조 상세 모달) | • 패키지 상품(`ADMN-PROD-005`)에 설정된 **목표 진도율(`target_pro
- [3.4.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **1:1 문의 분기 허브 · 커뮤니티 · 정답지** | • `USER-BRD-001~003` : 공지사항 · FAQ · 1:1 문의 접수<br>• `USER-BRD-004` : 학습 Q&A (1차 오픈: **산준모 공식 네이버 카페 질문게시판 아웃링크**)<br>• `USER-BRD-005` : 수강·합격후기<br>• `USER-BRD-006` : 무료 콘텐츠 시리즈 **'정답지'** 다운로드/열람<br>• `USER-BRD-007~010` : 시험일정/합
- [3.4.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **권리자 계약 · 1/2계층 지분 · 국세청 연동** | • 외부 파트너/사업자 수취인 전용 : 본인 계약 현황 및 정산내역서 조회 · 역발행 세금계산서/계산서 전자 승인 | • `ADMN-INST-001` : 권리자 계약 원장 (R/S · 도서 실결제액 인세 · 위탁 기준가 선택 · 선급금 · 개발지원금 · MMG · **계약별 최소 지급/청구 기준액 변수 설정**)<br>• `ADMN-INST-002` : 약정금 마일스톤 검수 원장 (즉시 출금 배제 ·
- [3.4.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **월간 정산(1~11단계) · 대사 · 마감 후 조정** | *(내부 재무/정산 전용 — 외부 비노출)* | • `ADMN-SETT-002` : 월간 정산 배치(1~11단계) · 마감 잠금 · 펌뱅킹 이체<br>• `ADMN-SETT-004` : PG 정산 원장 대사<br>• `ADMN-SETT-005` : 마감 후 수동 조정 및 **과세유형별 4가지 세무증빙 정정 처리**<br>• `ADMN-SETT-009` : 자사 내부 정산 조회 (`RH-INTERN
- [3.4.1 [A] 프론트엔드(`USER-*`) ↔ 백오피스(`ADMN-*`) 1:1 페어 매핑표] | **메인 홈 · 대시보드 · 사이트/권한/감사 관리** | • `USER-MAIN-001` : 메인 홈 (히어로/띠배너 · 레이어팝업 · 추천강사/강좌 캐러셀)<br>• `USER-TERM-001` : 이용약관 · 개인정보처리방침 버전별 열람 | • `ADMN-DASH-001` / `STAT-001~002` : 통합 대시보드 및 매출/수강 통계<br>• `ADMN-CONF-001~004` : 배너/팝업 · 약관 버전 · StarPlayer+ DRM 설정 · 

## 5. SNB 코드별 첫 등장 라인

SNB 파일: prototype_clean\common-snb.js
- ADMN-BOOK-001: `{ code: "BOOK-001", label: "도서 공급 원장", href: "ADMN-BOOK-001_baseline.html", screenCode: "ADMN-BOOK-001" },`
- ADMN-BRD-001: `{ code: "BRD-001", label: "공지사항 · FAQ · 당첨자 발표", href: "ADMN-BRD-001_baseline.html?view=notice", screenCode: "ADMN-BRD-001" },`
- ADMN-BRD-002: `{ code: "BRD-002", label: "1:1 문의 관리 (문의 분기 허브)", href: "ADMN-BRD-002_baseline.html", screenCode: "ADMN-BRD-002" },`
- ADMN-BRD-004: `["ADMN-BRD-004", "수험 자료실"],`
- ADMN-BRD-005: `{ code: "BRD-005", label: "수강·합격수기 · 무료특강(빈출)·정답지", href: "ADMN-BRD-005_baseline.html?view=review", screenCode: "ADMN-BRD-005" },`
- ADMN-BRD-006: `["ADMN-BRD-006", "무료특강·빈출문제"],`
- ADMN-BRD-009: `["ADMN-BRD-009", "정답지 관리"],`
- ADMN-BRD-010: `["ADMN-BRD-010", "당첨자 발표 관리"],`
- ADMN-CONF-001: `{ code: "CONF-001", label: "전시 배너 · 띠배너 · 팝업 관리", href: "ADMN-CONF-001_baseline.html?view=banner", screenCode: "ADMN-CONF-001" },`
- ADMN-CONF-002: `{ code: "CONF-002", label: "약관 · 개인정보처리방침 관리", href: "ADMN-CONF-002_baseline.html", screenCode: "ADMN-CONF-002" },`
- ADMN-CONF-003: `{ code: "CONF-003", label: "플레이어 · 동시접속 · 인증 설정", href: "ADMN-CONF-003_baseline.html?view=player", screenCode: "ADMN-CONF-003" },`
- ADMN-CONF-004: `{ code: "CONF-004", label: "메시지 템플릿 관리 (알림톡·문자·메일)", href: "ADMN-CONF-004_baseline.html?view=template", screenCode: "ADMN-CONF-004" },`
- ADMN-CONF-005: `{ code: "CONF-005", label: "운영자 계정 · 역할 권한(RBAC)", href: "ADMN-CONF-005_baseline.html", screenCode: "ADMN-CONF-005" }`
- ADMN-CONF-006: `{ code: "CONF-006", label: "운영 · 보안 통합 감사 로그", href: "ADMN-CONF-005_baseline.html?view=ADMN-CONF-006", screenCode: "ADMN-CONF-006" }`
- ADMN-CONF-008: `["ADMN-CONF-008", "환경설정 연동"],`
- ADMN-CONF-010: `{ code: "CONF-010", label: "정산 감사 로그", href: "ADMN-CONF-010_baseline.html", screenCode: "ADMN-CONF-010" },`
- ADMN-CRS-002: `["USER-CRS-002", "프론트 강좌상세"],`
- ADMN-DASH-001: `{ code: "DASH-001", label: "통합 대시보드 홈 (현황·큐·연동)", href: "ADMN-DASH-001_baseline.html?view=dash", screenCode: "ADMN-DASH-001" },`
- ADMN-FREE-001: `["USER-FREE-001", "무료특강/빈출문제"],`
- ADMN-INFO-001: `["USER-INFO-001", "하단 푸터"],`
- ADMN-INST-001: `{ code: "INST-001", label: "권리자 계약 원장", href: "ADMN-INST-001_baseline.html", screenCode: "ADMN-INST-001" },`
- ADMN-INST-002: `{ code: "INST-002", label: "약정금 마일스톤 검수", href: "ADMN-INST-002_baseline.html", screenCode: "ADMN-INST-002" },`
- ADMN-JOIN-002: `["USER-JOIN-002", "회원가입 화면"],`
- ADMN-LECT-002: `["USER-LECT-002-S1", "프론트 강좌상세"],`
- ADMN-LOGIN-001: `{ code: "LOGIN-001", label: "관리자 · 파트너 로그인 게이트", href: "ADMN-LOGIN-001_baseline.html", screenCode: "ADMN-LOGIN-001" }`
- ADMN-LOGIN-002: `["ADMN-LOGIN-002", "비밀번호 재설정"],`
- ADMN-LOGIN-003: `["ADMN-LOGIN-003", "계정 잠금 해제"],`
- ADMN-ORD-001: `{ code: "ORD-001", label: "주문 · 배송 · 3PL 관리", href: "ADMN-ORD-001_baseline.html" },`
- ADMN-ORD-002: `["2. 3PL 배송·출고·반품검수 (ORD-002)", "3PL 배송 · 출고 · 반품검수"],`
- ADMN-ORD-003: `["수강권 직권 부여 (0원 주문 · 구 ORD-003)", "수강권 직권 부여 (0원 주문)"],`
- ADMN-PAY-001: `["USER-PAY-001", "주문/결제서"],`
- ADMN-PROD-001: `{ code: "PROD-001", label: "카테고리 관리", href: "ADMN-PROD-001_baseline.html", screenCode: "ADMN-PROD-001" },`
- ADMN-PROD-002: `{ code: "PROD-002", label: "강의 관리 (영상 단품)", href: "ADMN-PROD-002_baseline.html", screenCode: "ADMN-PROD-002" },`
- ADMN-PROD-003: `{ code: "PROD-003", label: "단과 강좌 관리", href: "ADMN-PROD-003_baseline.html", screenCode: "ADMN-PROD-003" },`
- ADMN-PROD-004: `{ code: "PROD-004", label: "교재 관리", href: "ADMN-PROD-004_baseline.html", screenCode: "ADMN-PROD-004" },`
- ADMN-PROD-005: `{ code: "PROD-005", label: "패키지 · 환급반 상품 관리", href: "ADMN-PROD-005_baseline.html", screenCode: "ADMN-PROD-005" },`
- ADMN-PROD-006: `{ code: "PROD-006", label: "강사 노출 정보 관리", href: "ADMN-PROD-006_baseline.html", screenCode: "ADMN-PROD-006" },`
- ADMN-PROD-007: `{ code: "PROD-007", label: "일반상품 관리", href: "ADMN-PROD-007_baseline.html", screenCode: "ADMN-PROD-007" }`
- ADMN-PROM-001: `{ code: "PROM-001", label: "이벤트 · 기획전 관리 (Slug·특가)", href: "ADMN-PROM-001_baseline.html", screenCode: "ADMN-PROM-001" },`
- ADMN-PROM-002: `{ code: "PROM-002", label: "쿠폰 마스터 등록 · 발급 관리", href: "ADMN-PROM-002_baseline.html?view=list", screenCode: "ADMN-PROM-002" },`
- ADMN-PROM-003: `{ code: "PROM-003", label: "포인트 적립 정책 및 원장 관리", href: "ADMN-PROM-002_baseline.html?view=point", screenCode: "ADMN-PROM-003" }`
- ADMN-RFD-001: `["2. 합격환급반 심사 (RFD-001)", "합격환급반 심사"],`
- ADMN-RFD-002: `{ code: "RFD-002", label: "환불 요청 · 심사 관리", href: "ADMN-RFD-002_baseline.html" },`
- ADMN-RFD-003: `["4. 환불 완료 내역 (RFD-003)", "환불 완료 내역"],`
- ADMN-RFD-004: `["1. 환불 요청 목록 (RFD-004)", "환불 요청 목록"],`
- ADMN-SETT-001: `{ code: "SETT-001", label: "상품별 권리자 매핑", href: "ADMN-SETT-001_baseline.html", screenCode: "ADMN-SETT-001" }`
- ADMN-SETT-002: `{ code: "SETT-002", label: "월간 정산 및 집행", href: "ADMN-SETT-002_baseline.html", screenCode: "ADMN-SETT-002" },`
- ADMN-SETT-003: `["ADMN-SETT-003", "정산 마감 확정"],`
- ADMN-SETT-004: `{ code: "SETT-004", label: "PG 정산 원장 대사", href: "ADMN-SETT-004_baseline.html", screenCode: "ADMN-SETT-004" },`
- ADMN-SETT-005: `{ code: "SETT-005", label: "정산 수동 조정", href: "ADMN-SETT-005_baseline.html", screenCode: "ADMN-SETT-005" },`
- ADMN-SETT-006: `{ code: "SETT-006", label: "합격 환급반 관리", href: "ADMN-SETT-006_baseline.html", screenCode: "ADMN-SETT-006" },`
- ADMN-SETT-007: `{ code: "SETT-007", label: "수취인 분할 관리", href: "ADMN-SETT-007_baseline.html", screenCode: "ADMN-SETT-007" },`
- ADMN-SETT-008: `{ code: "SETT-008", label: "사업자등록 확인 이력", href: "ADMN-SETT-008_baseline.html", screenCode: "ADMN-SETT-008" }`
- ADMN-SETT-009: `{ code: "SETT-009", label: "내부 정산 조회 - 조회 전용", href: "ADMN-SETT-009_baseline.html", screenCode: "ADMN-SETT-009" },`
- ADMN-SETT-010: `{ code: "SETT-010", label: "원천세 · 지급명세서 신고 산출물", href: "ADMN-SETT-009_baseline.html?view=tax-report", screenCode: "ADMN-SETT-010" },`
- ADMN-SETT-011: `{ code: "SETT-011", label: "택배 대리점 운임 · 배송비 대사", href: "ADMN-SETT-011_baseline.html", screenCode: "ADMN-SETT-011" }`
- ADMN-STAT-001: `{ code: "STAT-001", label: "매출 · 상품 통계 (결제·환불·순위)", href: "ADMN-DASH-001_baseline.html?view=stat-sales", screenCode: "ADMN-STAT-001" },`
- ADMN-USER-001: `{ code: "USER-001", label: "일반 회원 관리 (목록·상세)", href: "ADMN-USER-001_baseline.html?view=list", screenCode: "ADMN-USER-001" },`
- ADMN-USER-002: `["ADMN-USER-002", "회원 상세"],`
- ADMN-USER-003: `{ code: "USER-003", label: "회원 수강 · 기간 · 기기 제어", href: "ADMN-USER-001_baseline.html?view=course", screenCode: "ADMN-USER-003" },`
- ADMN-USER-005: `{ code: "USER-005", label: "블랙리스트 · 부정사용 제재 관리", href: "ADMN-USER-001_baseline.html?view=blacklist", screenCode: "ADMN-USER-005" },`
- ADMN-USER-006: `{ code: "USER-006", label: "회원 그룹 · 다중 태그 관리", href: "ADMN-USER-001_baseline.html?view=tags", screenCode: "ADMN-USER-006" },`
- ADMN-USER-007: `{ code: "USER-007", label: "민감 정보 열람 · 파기 통제", href: "ADMN-USER-007_baseline.html", screenCode: "ADMN-USER-007" }`

## 6. docs 내 코드 등장 파일 (정본 외 코드만)

- ADMN-BRD-001: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-002: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-003: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-BRD-004: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/01_로그인_ADMN-LOGIN.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-BRD-005: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-006: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-007: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-008: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-009: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-BRD-010: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/10_게시판관리_ADMN-BRD.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-CONF-005: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/01_로그인_ADMN-LOGIN.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/04_권리자관리_ADMN-INST.md, screen_spec/05_상품관리_ADMN-PROD_BOOK.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/09_마케팅_프로모션_ADMN-PROM.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-CONF-006: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/01_로그인_ADMN-LOGIN.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/04_권리자관리_ADMN-INST.md, screen_spec/05_상품관리_ADMN-PROD_BOOK.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-CONF-007: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-CONF-008: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-CS-001: screen_spec/03_회원관리_ADMN-USER.md
- ADMN-DASH-002: screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-INST-003: screen_spec/04_권리자관리_ADMN-INST.md
- ADMN-LOGI-001: screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/09_마케팅_프로모션_ADMN-PROM.md, screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-MKT-001: screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-MKT-002: screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-ORD-003: screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-RFD-001: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/05_상품관리_ADMN-PROD_BOOK.md, screen_spec/06_주문배송관리_ADMN-ORD.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md
- ADMN-RFD-003: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-SETT-010: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/08_정산관리_ADMN-SETT.md
- ADMN-SETT-011: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/06_주문배송관리_ADMN-ORD.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/08_정산관리_ADMN-SETT.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-SETT-012: screen_spec/08_정산관리_ADMN-SETT.md
- ADMN-STAT-001: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md
- ADMN-STAT-002: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/09_마케팅_프로모션_ADMN-PROM.md
- ADMN-USER-002: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/07_환불관리_ADMN-RFD.md, screen_spec/09_마케팅_프로모션_ADMN-PROM.md, screen_spec/10_게시판관리_ADMN-BRD.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md
- ADMN-USER-005: screen_spec/00_INDEX_화면설계서_라우팅맵.md, screen_spec/02_대시보드_통계_ADMN-DASH_STAT.md, screen_spec/03_회원관리_ADMN-USER.md, screen_spec/11_사이트관리_ADMN-CONF.md, 산준모닷컴 구축 통합 상세 설계서.md