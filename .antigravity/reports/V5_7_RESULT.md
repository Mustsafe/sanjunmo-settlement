# v5.7 괄호 중복 2차(런타임 보완 및 clean 원문 수정) 결과 리포트

> **작성일시:** 2026-10-21  
> **대상 파일:** `prototype_clean/common-snb.js`, `prototype_clean/*.html` 10개 파일  
> **백업 디렉터리:** `_archive/backup/v5_7_20261021_202220/`  
> **검증 도구:** Playwright Chromium (1440px 뷰포트 E2E 자동 검수)

---

## 원문

### 1. patch_v5_7_paren_fix2.py 실행 터미널 출력
```
[OK] 수정 11개 · 백업 _archive\backup\v5_7_20261021_202220
  - common-snb.js · 괄호 앞 공백 허용
  - common-snb.js · 코드 밖·이름 안 패턴 정의
  - common-snb.js · 코드 밖·이름 안 적용
  - common-snb.js · strong·b·small 감싼 코드
  - common-snb.js · 요소 앞 공백 허용
  - ADMN-BOOK-001 · "공급형태(book_supply_type)" 2건
  - ADMN-BOOK-001 · "정가 이력(book_price_history)" 1건
  - ADMN-CONF-005 · "\((?:ROLE_)?PARTNER_[A-Z0-9_]+ — " 3건
  - ADMN-INST-001 · "도서(자사 저작권 보유)" 1건
  - ADMN-INST-002 · "매출연동(<code>매출연동 (REVENUE_SHARE)</code>)" 1건
  - ADMN-ORD-001 · " (수강권 직권부여 · 구 ADMN-ORD-003 통합)" 1건
  - ADMN-PROD-005 · " (ADMN-SETT-006 연동)" 3건
  - ADMN-PROD-007 · "일반 상품 판매매출 일반상품 매출)" 1건
  - ADMN-PROD-007 · "일반 상품 판매매출(<code>일반상품 매출</code>)" 1건
  - ADMN-SETT-002 · "온라인 강좌 수익배분 (강좌 수익배분)" 1건
  - ADMN-SETT-002 · "산출 명세 (강좌 수익배분)" 1건
  - ADMN-SETT-002 · "자사 발행 도서 인세 (도서 인세)" 1건
  - ADMN-SETT-002 · "위탁 도서 판매대금 정산 (위탁도서 정산)" 1건
  - ADMN-SETT-002 · "일시정산(LUMP_SETTLE, 7단계)" 1건
  - ADMN-SETT-002 · "단독 (Pipeline 5.1 · 무한도형)" 1건
  - ADMN-SETT-004 · "매입 재판매 도서(<code>매입 재판매 도서 (PURCHASED_RES" 1건
  - ADMN-SETT-004 · "사은품(<code>강좌 부속·사은품 (BUNDLED)</code>)" 1건
  - ADMN-SETT-009 · "온라인 강좌 수익배분 (강좌 수익배분)" 1건
  - ADMN-SETT-009 · "자사저작권 (도서 인세)" 1건
  - ADMN-SETT-009 · "위탁 도서 판매대금 정산 (위탁도서 정산)" 1건
  - ADMN-SETT-009 · "(일반상품 매출 · 소비재)" 1건
  - ADMN-SETT-009 · "(일반상품 매출, <code>TX-13</code>)" 1건
  - ADMN-SETT-009 · "(일반상품 매출 · TX-13)" 1건
  - ADMN-SETT-009 · "일반 상품 판매매출 (일반상품 매출)" 2건
  - ADMN-SETT-009 · "사건 성립(<code>payment_event_date IS NOT NU" 1건
```

### 2. scan_paren_dup.py 재실행 터미널 출력
```
[A] prototype_clean: 3건
[A] prototype: 6건
[B] prototype_clean (ADMN-코드) 자리: 251건
[SIZE] PAREN_DUP_SCAN.md: 1152자
[SIZE] PAREN_DUP_STATIC.md: 27468자
```

---

## 1. 괄호 중복 탐지 건수 추이 (PAREN_DUP_SCAN.md)

| 구분 | 최초 (v5.5 직후) | v5.6 (1차 보정) | v5.7 (2차 보정) | 누적 감소율 |
| :--- | :---: | :---: | :---: | :---: |
| **`prototype_clean` 중복 건수** | 163건 | 36건 | **3건** | **-98.2% (160건 해소)** |
| **`prototype` 중복 건수** | 6건 | 6건 | 6건 | 0건 (정본 병기 유지) |
| **`PAREN_DUP_SCAN.md` 크기** | 16,909자 | 4,449자 | 1,152자 | -15,757자 |

> **prototype_clean 잔여 3건 현황:**
> 1. `ADMN-BOOK-001`: "도서 공급형태(공급 형태)" (출고 이력 1건이라도 발생 시 사후 변경 불가 안내)
> 2. `ADMN-ORD-001`: "인세 도서(인세도서)"
> 3. `ADMN-SETT-006`: "플랫폼 보전금(120만원)" (금액 단위 괄호 표기)

---

## 2. E2E 검수 결과

| 대상 환경 | 실행 명령어 | 전체 화면 수 | PASS 수 | 콘솔 에러 수 | 판정 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`prototype_clean`** | `python scripts/qa/skill_playwright_e2e.py prototype_clean` | 37개 | 37개 | 0건 | **PASS** |
| **`prototype`** | `python scripts/qa/skill_playwright_e2e.py prototype` | 37개 | 37개 | 0건 | **PASS** |

---

## 3. git diff --ignore-cr-at-eol --stat 출력 전문

```
 .antigravity/WORKFLOW_REDESIGN_PLAN.md      |  5 +++++
 .antigravity/reports/PAREN_DUP_SCAN.md      | 35 +----------------------------
 prototype_clean/ADMN-BOOK-001_baseline.html |  4 ++--
 prototype_clean/ADMN-CONF-005_baseline.html |  6 ++---
 prototype_clean/ADMN-INST-001_baseline.html |  2 +-
 prototype_clean/ADMN-INST-002_baseline.html |  2 +-
 prototype_clean/ADMN-ORD-001_baseline.html  |  2 +-
 prototype_clean/ADMN-PROD-005_baseline.html |  6 ++---
 prototype_clean/ADMN-PROD-007_baseline.html |  4 ++--
 prototype_clean/ADMN-SETT-002_baseline.html | 12 +++++-----
 prototype_clean/ADMN-SETT-004_baseline.html |  2 +-
 prototype_clean/ADMN-SETT-009_baseline.html | 18 +++++++--------
 prototype_clean/common-snb.js               |  9 ++++----
 13 files changed, 40 insertions(+), 67 deletions(-)
```
