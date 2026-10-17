# [산준모 어드민 화면설계서 v12] 00_INDEX 라우팅 맵 (참고용)

- **원본 기준:** 산준모닷컴 (관리자) 화면설계서 v12 확정본 (문서 11건 · 화면 121건 · 참고 45건)
- **활용 원칙:**
  1. 본 폴더(`docs/screen_spec/`)의 문서는 백오피스 화면 설계 시 필드·탭·모달·예외처리를 누락 없이 챙기기 위한 **참고용(Reference)**입니다.
  2. 화면설계서 특유의 원형 번호 배지(`①~⑭`, `[마커 N]`)는 디스크립션 대조용이므로 실제 프로토타입 UI(`prototype/*_baseline.html`)에 렌더링하지 않습니다.
  3. 11월 16일 1차 오픈 조정 스펙(동시접속 1세션 제어 우선, 학습 Q&A 네이버 카페 아웃링크, PG 토스페이먼츠 5대 결제수단, 정산 Pipeline 명칭 등)은 루트 `README.md` 및 통합 상세 설계서 정본을 따릅니다.

## 1. 도메인별 분할 문서 목록 (`docs/screen_spec/`)
| 번호 | 파일명 | 도메인 범위 | 수록 섹션 수 | 크기(자) |
| :---: | :--- | :--- | :---: | :---: |
| 01 | `01_로그인_ADMN-LOGIN.md` | 관리자 > 로그인 (ADMN-LOGIN-001~003) | 8건 | 20,683 |
| 02 | `02_대시보드_통계_ADMN-DASH_STAT.md` | 관리자 > 대시보드 · 통계 (ADMN-DASH-001, STAT-001~002) | 8건 | 24,145 |
| 03 | `03_회원관리_ADMN-USER.md` | 관리자 > 회원관리 (ADMN-USER-001~006) | 19건 | 64,446 |
| 04 | `04_권리자관리_ADMN-INST.md` | 관리자 > 권리자 관리 (ADMN-INST-001~002) | 10건 | 74,743 |
| 05 | `05_상품관리_ADMN-PROD_BOOK.md` | 관리자 > 상품관리 (ADMN-PROD-001~007, BOOK-001) | 23건 | 86,476 |
| 06 | `06_주문배송관리_ADMN-ORD.md` | 관리자 > 주문/배송 관리 (ADMN-ORD-001~002) | 15건 | 47,734 |
| 07 | `07_환불관리_ADMN-RFD.md` | 관리자 > 환불 관리 (ADMN-RFD-001~004) | 16건 | 68,355 |
| 08 | `08_정산관리_ADMN-SETT.md` | 관리자 > 정산 관리 (ADMN-SETT-001~011) | 26건 | 185,649 |
| 09 | `09_마케팅_프로모션_ADMN-PROM.md` | 관리자 > 마케팅/프로모션 (ADMN-PROM-001~003) | 11건 | 40,974 |
| 10 | `10_게시판관리_ADMN-BRD.md` | 관리자 > 게시판 관리 (ADMN-BRD-001~010) | 24건 | 64,504 |
| 11 | `11_사이트관리_ADMN-CONF.md` | 관리자 > 사이트 관리 (ADMN-CONF-001~008) | 17건 | 64,885 |

## 2. 전체 화면 코드(ADMN-*) → 파일 라우팅 테이블
| 도메인 키 | 화면 코드 | 화면명 | 수록 파일 |
| :--- | :--- | :--- | :--- |
| `admin-login` | `doc-admin-login` | doc-admin-login | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `ADMN-LOGIN-001` | 관리자 로그인 — 사내 운영자(최고 관리자 · CS담당 · 물류팀) · 강사/조교 파트너 공용 | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `ADMN-LOGIN-001-P1` | 5회 오입력 계정 강제 잠금 안내 | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `ADMN-LOGIN-002` | 아이디 찾기 — 이메일 · 휴대전화 본인인증(SMS) 기반 관리자 계정 조회 | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `ADMN-LOGIN-003` | 비밀번호 찾기 — 이메일 소유 인증 + SMS 본인인증 후 화면에서 즉시 재설정(원스톱) | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `` | 참고 · 관리자 보안 정책 | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `` | 참고 · 파일 구성 | `01_로그인_ADMN-LOGIN.md` |
| `admin-login` | `` | 참고 · 확인 필요 사항 | `01_로그인_ADMN-LOGIN.md` |
| `admin-dashboard` | `doc-admin-dashboard` | doc-admin-dashboard | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `ADMN-DASH-001` | 대시보드 홈 — 전체 운영 현황 요약 · 처리 대기 큐 · 외부 연동 상태 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `ADMN-STAT-001` | 매출 통계 — 기간별 결제 · 환불 · 실 수익 추이 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `ADMN-STAT-002` | 상품 통계 — 인기 상품 순위 · 점유율 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `` | 참고 · 통계 항목표 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `` | 참고 · 지표 정의 및 집계 규칙 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `` | 참고 · 파일 구성 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-dashboard` | `` | 참고 · 확인 필요 사항 | `02_대시보드_통계_ADMN-DASH_STAT.md` |
| `admin-user` | `doc-admin-user` | doc-admin-user | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-001` | 회원 목록 조회 — 다중 조건 검색 · 마스킹 기본 · 사유 기반 엑셀 추출 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-001-P1` | 개인정보 엑셀 다운로드 사유 입력 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-002` | 회원 상세 정보 — 마스킹 해제 · 비밀번호 초기화 · 수동 포인트 · CS 원스톱 이력 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-002-P1` | 수동 무상 포인트 지급 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-002-P2` | 소셜 연동 해제 — 소셜별 개별 해제 · 사유 필수 · 마지막 로그인 수단 보호 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-003` | 회원 수강 및 기기 제어 — 수강 기간 강제 조정 · StarPlayer+ DRM 단말 리셋 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-004` | 진도율 · 이어보기 조회 — 강의별 진도율과 최종 재생 지점(초) 실시간 확인 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-004-P1` | 진도율 보정 — 사유 · 근거 입력 후 즉시 반영 · 감사 로그 기록 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-005` | 블랙리스트 관리 — 동시 접속 IP · 불법 캡처 적발 · 마이너스 포인트 강제 탈퇴 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-006` | 그룹 · 태그 관리 — 수평적 태그 체계 · 일괄 부여 · 타겟팅 필터 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-006-S1` | 태그 생성 · 수정 — 수동 태그 · 자동 태그 규칙 · 평가 주기 · 조건 이탈 처리 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-006-P1` | 조건 추가 — 마케팅 타겟 조건 선택 · 구매 · 수강 · 접속 · 수신 동의 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-006-S2` | 조건 그룹 저장 — 태그 조합을 이름 붙여 재사용 · 동적 / 정적 갱신 방식 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `ADMN-USER-006-S3` | 태그 일괄 처리 결과 — 실제 부여된 회원 · 처리 결과 요약 · 실패 재처리 · 일괄 해제 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `` | 참고 · 개인정보 접근 통제 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `` | 참고 · 프로세스맵 원본 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `` | 참고 · 파일 구성 | `03_회원관리_ADMN-USER.md` |
| `admin-user` | `` | 참고 · 확인 필요 사항 | `03_회원관리_ADMN-USER.md` |
| `admin-instructor` | `doc-admin-instructor` | doc-admin-instructor | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-001` | 권리자 계약 원장 — 권리자 유형 · 세무 유형(국세청) · 사업자 상태 · 유효 계약 일람 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-001-S1` | 권리자 · 세무 확인 — 권리자 식별 · 사업자 진위 확인 · 세무 속성 · 세무 판정 · 국세청 확인 이력 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-001-S2` | 계약 조건 — 계약 기간 · 조항 카드(전속계약금 · 개발지원금 · 온라인 R/S · 교재 인세 · 매절 · 위탁 · 기타 수당 · 선급금) · 증빙 · 저장 검증 · 변경·열람 이력 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-001-P1` | 요율 잠금 안내 / 상태 변경 영향 확인 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-001-P2` | 계약 저장 검증 상세 — 저장 차단 · 주의 목록 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `ADMN-INST-002` | 약정금 마일스톤 검수 및 승인 원장 — 증빙 · 수기 소명 검수 · 승인 게이트 · 귀속월 확정 · 당월 정산서 이관 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `` | 참고 · 계약 상태 · 제약 규칙 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `` | 참고 · 파일 구성 | `04_권리자관리_ADMN-INST.md` |
| `admin-instructor` | `` | 참고 · 확인 필요 사항 | `04_권리자관리_ADMN-INST.md` |
| `admin-product` | `doc-admin-product` | doc-admin-product | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-001` | 카테고리 관리 — 자격증 종목 · 과정 분류 2Depth 동적 트리 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-002` | 강의(영상) 관리 — 개별 영상 Unit 등록 · VOD Key · 재생시간 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-002-S1` | 강의(영상 Unit) 등록 · 수정 — VOD Key · 재생시간 · 맛보기 · 교안 PDF | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-003` | 단과 강좌 관리 — 강좌 목록 · 판매 단위 강좌 등록 · 수강 기준 기간 · 가격 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-003-S2` | 단과 강좌 등록 · 수정 — 기본 정보 · 수강 기준 기간 · 가격 · 커리큘럼 · 연관 교재 · 상세 콘텐츠 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-003-S1` | 커리큘럼 구성 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-004` | 교재 관리 — 교재 목록 · 실물 도서 등록 · 재고 · 배송 정책 · 도서정가제 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-004-S1` | 교재 등록 · 수정 — 도서 기본 정보 · ISBN · 자격증 매핑 · 공급 형태 · 재고 · 배송 정책 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-BOOK-001` | 도서 공급 원장 — 공급 형태 · 정가 이력 · 매입처 · 위탁 도서 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-BOOK-001-S1` | 도서 공급 정보 조회 — 공급 형태 · 저작권 귀속 · 정산 대상 여부 파생 · 공급 형태 변경 차단(조회 전용) | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-005` | 패키지(올패스) 구성 — 패키지 목록 · 강좌+교재 복합 상품 · 자동 분할 렌더링 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-005-S1` | 패키지(올패스) 등록 · 수정 — 기본 정보 · 환급 설정 · 구성품 매핑 · 자동 분할 렌더링 · 할인 배분 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-006` | 강사 프로필 / 전시 관리 — 프로필 목록 · 권리자 계약 원장 연동 · 계약 상태 기반 강제 블라인드 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-006-S1` | 강사 프로필 등록 · 수정 — 권리자 계약 원장 연동 · 전시 프로필 · 전시 제어 · 강제 블라인드 판정 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-007` | 상품 마스터 — 일반 소비재 목록 · 공급 형태 · 재고 · 일반 상품 판매매출(Pipeline 2.3) | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-007-S1` | 일반상품 등록 · 수정 — 공급 형태 · 판매가(VAT 포함) · 과세 판정 · 재고 · 매입처 · 상세 콘텐츠 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-007-P1` | 재고 조정 — 증감 수량 · 조정 사유 · 조정 후 재고 미리 계산 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `ADMN-PROD-007-P2` | 입출고 이력 — 재고 원장 조회 · 기간 · 구분 필터 · 엑셀 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `` | 참고 · 상품 아키텍처 · 분할 인서트 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `` | 참고 · 프로세스맵 원본 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `` | 참고 · 파일 구성 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-product` | `` | 참고 · 확인 필요 사항 | `05_상품관리_ADMN-PROD_BOOK.md` |
| `admin-order` | `doc-admin-order` | doc-admin-order | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-001` | 주문 내역 관리 — 실결제금액 기준 주문 조회 · 결제/배송지 수동 보정 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-001-S1` | 주문 상세 · 수동 보정 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002` | 배송 관리 · 3PL 풀필먼트 연동 — 발주 엑셀 다운로드 · 송장 벌크 업로드 · 반품 검수 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-S1` | 배송 관리 — 배송중 탭 — 운송장 · 배송 추적 · 운송장 정정 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-S2` | 배송 관리 — 배송완료 탭 — 배송완료일 · 완료 근거 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-S3` | 배송 관리 — 반품 수거 · 검수 탭 — 검수 대상 선택 · 하단 검수 입력 · 환불 심사 전달 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-P1` | 송장 벌크 업로드 (Bulk Tracking Import) | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-P2` | 송장 단건 등록 — 3PL 회신 누락 · 운송장 정정 예외 처리 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `ADMN-ORD-002-P3` | 발주 배치 이력 — 발주 다운로드 · 송장 업로드 이력 · 파일 재다운로드 · 알림톡 발송 실패 재시도 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `` | 참고 · 주문 · 배송 상태 전이 정의 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `` | 참고 · 3PL 발주 엑셀 · 송장 회신 엑셀 규격 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `` | 참고 · 프로세스맵 원본 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `` | 참고 · 파일 구성 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-order` | `` | 참고 · 확인 필요 사항 | `06_주문배송관리_ADMN-ORD.md` |
| `admin-refund` | `doc-admin-refund` | doc-admin-refund | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-001` | 올패스 100% 환급 신청 심사 — 합격 환급 미션 자격 수동 심사 목록 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-001-S1` | 증빙 대조 · 승인/반려 처리 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-004` | 환불 요청 목록 — 취소 · 환불 · 반품 요청 통합 · 상태 탭(환불보류 조회) · 처리 기한 5영업일 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-002` | 환불 처리 상세 — 법정 기준 환불금 계산 · 어뷰징 방지 공제 — 적립 포인트 선사용 환불 시 현금 선차감 및 마이너스 전환 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-002-S1` | 환불 관리 상세 뷰 — 1:1 결제/환불 문의 확인 · 부서 이관 · 금융 취소 처리 (좌-우 2분할) | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-002-P1` | 포인트 마이너스 전환 확인 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-002-P2` | 포인트 사용 내역 모달 — 유상 / 무상 구분 · 원 적립 건 · 환불 복원 대상 표기 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-003` | 환불 내역 조회 — 목록 · LIFO 유상 포인트 부활 및 만료 D+7 유예 이력 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-003-S1` | 환불 내역 상세 — 환불 건 요약 · LIFO 복원 명세 · 보정 거래 이력 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `ADMN-RFD-003-S2` | 보정 거래 등록 — 완료된 환불의 추가 환불 · 환불 회수 · 포인트 보정 (원 거래 불변) | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `` | 참고 · 환불 및 반품 마스터 프로세스 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `` | 참고 · 환불금 연산 규칙 및 검산 예시 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `` | 참고 · 프로세스맵 원본 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `` | 참고 · 파일 구성 | `07_환불관리_ADMN-RFD.md` |
| `admin-refund` | `` | 참고 · 확인 필요 사항 | `07_환불관리_ADMN-RFD.md` |
| `admin-settlement` | `doc-admin-settlement` | doc-admin-settlement | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-001` | 상품별 권리자 매핑 — 강의 · 도서 SKU 단위 1계층 지분 배치 편집 · 합계 100.00% 하드락 · 유효일자 이력 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-001-S1` | 상품별 권리자 매핑 편집 — 강의 선택 · 적용 계약 · 1계층 지분 · 합계 100.00% 하드락 · 유효일자 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-001-P1` | 지분율 100% 검증 실패 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-002` | 월간 정산 및 집행 — 11단계 배치 · 통합 정산서 · 정산 마감(Lock) · 증빙 승인 현황 · 펌뱅킹 단일 게이트웨이 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-002-S1` | 통합 정산서 상세 · 마감 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-002-S2` | 권리자 제공 정산서 — 외부 제공본 PDF · 메일 발송 · 자사 라인 제외 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-002-P1` | 이월 잔액 상세 — 계약 · 수취인 · 정산 입력 구분 · 원거래 · 구성요소 · 세무 및 증빙 상태 · 상계 범위 · 예약 · 지급 이력 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-003` | 결번 — 정산 요율 관리 기능은 ADMN-INST-001 로 통합 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-004` | PG 정산 원장 대사 — PG 원장 · 결제 DB 1대1 대사 · 차이 원인 코드 소명 · 이원화 임계값 마감 판정 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-004-S1` | PG 대사 차이 상세 — 선택 행 원인 코드 지정 · 소명 입력 · 확정 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-005` | 정산 수동 조정 — 전월 정정 라인(원 발생월/반영월) · 계정 간 대체 · 승인 임계 · 증빙 정정 4채널 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-005-S1` | 조정 라인 등록 · 수정 — 조정 유형 · 원 발생월/반영월 · 사유 · 소명 · 금액 · 증빙 정정 채널 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-006` | 합격 환급반 관리 — 환급 확정 건 수신 · 계약별 부담 방식(A/B/C) 정산 연동 · MMG 중복 플래그 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-007` | 수취인 분할 지분 설정 — 2계층 Payee Split · 계약 서명인 한정 · 합계 100% 저장 하드락 · 유효일자 이력 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-007-S1` | 수취인 분할 편집 — 2계층 Payee Split · 계약 서명인 한정 · 합계 100% 하드락 · 유효일자 이력 · 연산 미리보기 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-008` | 사업자등록 확인 이력 — 국세청 API 조회 이력 · 과세유형 변경 감지 · 폐업/휴업 감지 · 재시도 큐 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-009` | 내부 정산 조회 — 자사 매출(일반 상품 판매매출(Pipeline 2.3)) 포함 전체 정산 라인 조회 전용 · 자금 집행 기능 없음 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-011` | 물류비 대사(3PL) — 출고·수수료 명세서 대사 · 배송비/반품 검수 · 도서 매입 계산서 대조 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `ADMN-SETT-011-S1` | 물류비 대사 상세 — 배송비 · 반품 대사 · 반품 귀책 판정 · 도서 매입 계산서 대조 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 정산 연산 규칙 · 11단계 엔진 · 절사 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 세무 판정 매트릭스 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 재무 마감 · Lock · 정정 정책 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 프로세스맵 원본 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 파일 구성 | `08_정산관리_ADMN-SETT.md` |
| `admin-settlement` | `` | 참고 · 확인 필요 사항 | `08_정산관리_ADMN-SETT.md` |
| `admin-marketing` | `doc-admin-marketing` | doc-admin-marketing | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-001` | 이벤트 관리 — 구분자 · Slug 자동 라우팅 · S3 에셋 호스팅 · CodeMirror 3분할 빌더 · 중복 할인 차단 제어 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-001-S3` | 기획전 등록 · 수정 — 구분자 · Slug 라우팅 · 대상 상품군 · 랜딩 콘텐츠 · 에셋 · 3분할 소스 에디터 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-001-S1` | 중복 할인 일괄 차단(Bulk Disable) 스케줄 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-001-S2` | 이벤트 상세 조회 — 3분할 소스 읽기 전용 뷰어 · 미리보기 · 주소 복사 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-002` | 쿠폰 마스터 등록 — 정률 40% / 정액 20만원 Cap 하드코딩 · 도서정가제 자동 바인딩 · 발급 통제 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-002-P1` | 정액 감면 Cap 초과 경고 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `ADMN-PROM-003` | 포인트 정책 설정 — 가입 축하금 5,000P · 유상 적립율 1% 올림 · 소멸/환불 규칙 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `` | 참고 · 혜택 적용 우선순위 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `` | 참고 · 파일 구성 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-marketing` | `` | 참고 · 확인 필요 사항 | `09_마케팅_프로모션_ADMN-PROM.md` |
| `admin-board` | `doc-admin-board` | doc-admin-board | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-001` | 공지사항 관리 — 등록 · 기기별 노출 통제 · 예약 발행 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-001-S1` | 공지사항 등록 · 수정 — 기기별 노출 통제 · 상단 고정 · 예약 발행 · 본문 에디터 · 첨부 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-002` | 1:1 문의 관리 — 회원 · 결제 · 배송 일반 VOC 처리 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-002-S1` | 답변 등록 · 카카오 알림톡 발송 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-002-P1` | 회원 컨텍스트 모달 — 답변 화면을 떠나지 않고 회원 정보 · 최근 주문 · 수강 현황 확인 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-003` | 상품 Q&A 관리 — 상품 ID 자동 매핑 문의 독립 관리 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-003-S1` | 상품 Q&amp;A 답변 등록 — 대상 상품 확인 · 답변 본문 · 공개 설정 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-004` | 학습 Q&A 관리 — 강사 · 조교 전용 수험 질문 · 강의/진도율 실시간 연동 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-004-S1` | 학습 Q&amp;A 질문 상세 · 답변 — 학습 컨텍스트 패널 · 강사 에스컬레이션 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-005` | 수기 / 합격 후기 관리 — 합격 증빙 검증 · 카페 공유 확인 · 포인트 지급 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-005-S1` | 합격 후기 검증 — 합격 증빙 대조 · 카페 공유 확인 · 승인 / 반려 · 포인트 지급 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-006` | FAQ 관리 — 카테고리 트리 · 가중치 정렬 · 아코디언 확장 패널 1:1 결합 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-006-S1` | FAQ 등록 · 수정 — 카테고리 선택 · 가중치 정렬 · 질문 · 답변 HTML 에디터 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-007` | 1:1 문의 분류 관리 — VoC 분류 마스터 · 화면 코드 매핑 · 담당 부서 큐 라우팅 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-007-S1` | 1:1 문의 분류 등록 · 수정 — 대 / 소분류 · 분류 코드 자동 채번 · 화면 매핑 · 담당 부서 큐 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-008` | 이벤트 관리 — 폐지 · 마케팅/프로모션 이벤트 관리(ADMN-PROM-001)로 통합 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-009` | 당첨자 발표 관리 — 이벤트 연결 · 명단 엑셀 일괄 등록 · 예약 발행 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-009-S1` | 당첨자 발표 등록 · 수정 — 이벤트 연결 · 명단 엑셀 일괄 등록 · 예약 발행 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-010` | 무료콘텐츠 관리 — 빈출자료실 · 정조교의 매일 1문제 등록 · 자격증/연도/회차 구분 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `ADMN-BRD-010-S1` | 무료콘텐츠 등록 · 수정 — 구분 · 자격증 · 연도 · 회차 · 본문 · PDF 첨부 · 전시 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `` | 참고 · 문의 분류 → 관리자 화면 → 담당 역할 → 알림 발송 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `` | 참고 · 파일 구성 | `10_게시판관리_ADMN-BRD.md` |
| `admin-board` | `` | 참고 · 확인 필요 사항 | `10_게시판관리_ADMN-BRD.md` |
| `admin-config` | `doc-admin-config` | doc-admin-config | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-001` | 전시/메뉴 관리 — 배너 · 팝업 관리 (메인 슬라이드 배너 탭) | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-001-S1` | 전시/메뉴 관리 — 띠배너 (텍스트 + 배경색 · 노출 위치 · 노출 대상별 1건 노출) | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-001-S2` | 전시/메뉴 관리 — 모달 팝업 (게시물 선택 · 링크 직접 입력) | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-002` | 약관 관리 — 이용약관 · 개인정보처리방침 · 환불 규정 버전 개정 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-003` | 플레이어/DRM 설정 — StarPlayer+ 워터마크 · 건너뛰기 · 배속 · 단말 제한 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-004` | 메시지 템플릿 관리 — 발송 조건별 치환코드 템플릿 · 알림톡/LMS | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-004-S1` | 타겟 단체 알림톡/LMS 예약 발송 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-005` | 운영자 권한 관리 — 역할 그룹별 메뉴 접근 권한(읽기/쓰기/엑셀) 매핑 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-006` | 이력/보안 로그 — 개인정보 열람 · 정보 수정 · 엑셀 다운로드 감사 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-007` | 알림톡 SENS 템플릿 관리 — 승인 템플릿 조회 · 치환 변수 크로스 체크 · 모바일 미리보기 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `ADMN-CONF-008` | 인증 발송 설정 — 계정 · IP 한도 · 롤링 24시간 · IP 예외 · 수동 초기화 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `` | 참고 · 역할별 권한 매트릭스 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `` | 참고 · 알림 템플릿 · 치환코드 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `` | 참고 · 프로세스맵 원본 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `` | 참고 · 파일 구성 | `11_사이트관리_ADMN-CONF.md` |
| `admin-config` | `` | 참고 · 확인 필요 사항 | `11_사이트관리_ADMN-CONF.md` |