# -*- coding: utf-8 -*-
from pathlib import Path

readme = Path("README.md")
text = readme.read_text(encoding="utf-8")

# 1. Section 2에 오늘 확정된 핵심 표준 정책 & 용어(슬롭 제외, 정답 기준만) 보강
old_sec2_4 = """4. 도서정가제 하드락 및 3PL 출고지시 Lock
   - 실물 교재(BOOK, 면세): 도서정가제 범위 내 상품 기본 할인 최대 10% 허용(정가 취소선 + 할인가 노출), 추가 쿠폰·포인트 사용 0원 및 포인트 적립 0% 하드락. 인세·정산·무료배송(30,000원↑) 판정은 모두 할인 후 실결제액 기준(단, 위탁도서는 계약원장에서 실결제액/정가 기준 선택). 패키지(MIXED) 할인액은 100% 강좌(LECTURE, 과세) 라인에만 배분.
   - 3PL 발주 엑셀 다운로드 즉시 ship_ordered_at 기록 및 출고지시 완료 잠금(배송지 변경 409 차단, 상위 권한 [출고지시 회수]로만 해제)."""

new_sec2_4 = """4. 도서정가제 하드락 및 3PL 출고지시 Lock
   - 실물 교재(BOOK, 면세): 도서정가제 범위 내 상품 기본 할인 최대 10% 허용(정가 취소선 + 실판매가 노출), 추가 쿠폰·포인트 사용 0원 및 포인트 적립 0% 하드락. 자사발행 도서 인세·개발지원금·무료배송(실결제액 30,000원↑) 판정은 모두 할인 후 실결제액 기준(단, 위탁도서는 계약원장 `ADMN-INST-001`에서 실결제액/도서 정가 기준 선택). 패키지(MIXED) 할인액은 100% 강좌(LECTURE, 면세) 라인에만 배분.
   - 3PL 발주 엑셀 다운로드 즉시 `ship_ordered_at` 기록 및 `배송준비중` 전환 잠금(프론트 직접취소 및 배송지 변경 차단), 이후 3PL 운송장 엑셀 일괄 업로드 시 `배송중` 전환·재고 차감·알림톡 발송.
5. 표준 용어 및 Set 1~4 핵심 정책 고정 기준 (UI/문서 공통)
   - **포인트 2원장 표준 명칭:** 유상 거래 연동 적립분은 **`구매적립 포인트(적립 P)`**(코드 `PAID`, 유효기간 5년), 이벤트·보상 지급분은 **`무상 포인트(무상 P)`**(코드 `FREE`, 유효기간 2년)로 표기한다. 환불 시 기적립 `적립 P`를 회수하며 잔액 부족 시 마이너스 부채 전환 또는 환불 현금 차감으로 처리한다.
   - **콘텐츠 표준 명칭:** 시험 대비 문제 표기는 **`빈출`**(빈출문제)을 사용하고, 도서/강좌 부가 해답 자료는 무료 콘텐츠인 **`정답지`**(`ANSWER_SHEET`, `ADMN-BRD-009`)로 표기한다.
   - **합격환급반(`ADMN-SETT-006`) 및 정산/권한:** 환급 인정 진도율·출석일은 패키지(`ADMN-PROD-005`)별 설정 변수를 참조하며, 교재 실판매가를 제외한 순수 강좌 결제액에서 제세공과금 22% 공제 후 지급한다(강사 분담 차감 시 개발지원금 약정 한도 자동 복원). 국세청(`ADMN-SETT-008`) 조회 장애·특수건은 증빙 첨부 후 재무 수기 예외 지정을 허용하며, 외부 파트너 3종(`ROLE_PARTNER_INST`, `COPYRIGHT`, `3PL`)은 메뉴 접근 + 데이터 스코프(본인 ID 바인딩)/기능 스코프 2단 통제를 적용한다."""

assert old_sec2_4 in text, "Section 2.4 anchor not found"
text = text.replace(old_sec2_4, new_sec2_4, 1)

# 2. Section 3 & 4를 prototype/ vs prototype_clean/ 2폴더 구조 및 38개 전체 화면 인벤토리로 최신화
old_sec3_head = "## 3. 백오피스 프로토타입(prototype/) 아키텍처 및 필수 마크업 규칙"
new_sec3_head = """## 3. 백오피스 프로토타입(`prototype/` & `prototype_clean/`) 2폴더 구조 및 마크업 규칙

- **2개 폴더의 역할 구분 및 동시 패치 원칙 (필수):**
  1. **`prototype/` (기획·검수용 폴더):** 화면 상단 정책 배너·기획 의도·SSOT 참조 가이드가 함께 포함된 검수용 버전.
  2. **`prototype_clean/` (실제 서비스 UI 클린 폴더):** 기획 설명 배너·정책 주석 박스를 제거하고 실제 운영 어드민 UI만 남긴 클린 배포 버전 (`https://whiteceo.github.io/sanjunmo-settlement/prototype_clean/{화면코드}_baseline.html`).
  3. **동시 반영:** HTML 화면 수정 시 반드시 두 폴더의 성격 차이를 유지하며 `prototype/`과 `prototype_clean/` 양쪽의 동명 파일을 동시에 패치하고 `python3 scripts/qa/skill_playwright_e2e.py` (38개 전수 검사)를 통과해야 한다."""

assert old_sec3_head in text, "Section 3 header not found"
text = text.replace(old_sec3_head, new_sec3_head, 1)

old_sec4 = """## 4. 완료된 프로토타입 화면 인벤토리 (prototype/, 총 24개 파일)

- 0단계 가이드: 00_WORKFLOW_GUIDE_baseline.html
- 주문·배송·환불·CS (ORD/RFD/BRD):
  - ADMN-ORD-001_baseline.html (주문목록 001 + 상세·배송지Lock·가상계좌연장 001-S1 + 3PL 배송·출고·반품검수 002/S1~S3 + 모달 P1~P3)
  - ADMN-RFD-002_baseline.html (환불목록 004 + 통합 상세 002/002-S1 + 마이너스포인트 모달 P1 + 완료내역 003)
  - ADMN-BRD-002_baseline.html (1:1 문의 목록 002 + 5대 문의유형 분기·이관 워크스페이스 002-S1)
- 상품·강좌·교재 (PROD 7종): ADMN-PROD-001 ~ ADMN-PROD-007_baseline.html
- 정산·계약·도서·보안·감사 (1~4단계 13종): ADMN-INST-001, ADMN-INST-002, ADMN-BOOK-001, ADMN-SETT-001, ADMN-SETT-002, ADMN-SETT-004, ADMN-SETT-005, ADMN-SETT-006, ADMN-SETT-007, ADMN-SETT-008, ADMN-SETT-009, ADMN-USER-007, ADMN-CONF-010 (ADMN-SETT-003은 결번 안내용 시트)"""

new_sec4 = """## 4. 백오피스 프로토타입 전체 인벤토리 (`prototype/` & `prototype_clean/`, 총 38개 화면)

- **플로우 허브 (1종):** `00_WORKFLOW_GUIDE_baseline.html` (Set 1~4 End-to-End 실무 플로우 및 정산 4단계 여정 런처)
- **로그인 · 대시보드 · 통계 (4종):** `ADMN-LOGIN-001`, `ADMN-DASH-001`, `ADMN-STAT-001`, `ADMN-STAT-002`
- **회원 · 수강제어 · 블랙리스트 · 민감정보 (4종):** `ADMN-USER-001`(상세·수강/기기 003·진도율 보정 004·태그 006 통합), `ADMN-USER-005`, `ADMN-USER-006`, `ADMN-USER-007`
- **마케팅 · 프로모션 · 쿠폰/포인트 (2종):** `ADMN-PROM-001`, `ADMN-PROM-002`(쿠폰 002·포인트 003 통합)
- **상품 · 강좌 · 교재 · 패키지 · VOD · 도서원장 (8종):** `ADMN-PROD-001` ~ `ADMN-PROD-007`, `ADMN-BOOK-001`
- **주문 · 3PL 출고/송장 · 복합환불 (4종):** `ADMN-ORD-001`(주문 001 + 3PL 출고/송장/반품검수 002 통합), `ADMN-RFD-002`, `ADMN-RFD-003`, `ADMN-RFD-004`
- **권리자 계약 · 월간 정산 · 세무 · 3PL 정산 (9종):** `ADMN-INST-001`, `ADMN-INST-002`, `ADMN-SETT-001`, `ADMN-SETT-002`, `ADMN-SETT-004` ~ `ADMN-SETT-009`, `ADMN-SETT-011` (`ADMN-SETT-003` 결번 제외)
- **게시판/CS · 사이트 환경설정 · RBAC 권한 (6종):** `ADMN-BRD-001`, `ADMN-BRD-006`(1:1 문의 분기 허브 `BRD-002` 포함), `ADMN-BRD-009`(정답지), `ADMN-CONF-001` ~ `ADMN-CONF-005`, `ADMN-CONF-007`"""

assert old_sec4 in text, "Section 4 anchor not found"
text = text.replace(old_sec4, new_sec4, 1)

readme.write_text(text, encoding="utf-8")
print("[OK] README.md permanently updated as the single AI context hub.")
