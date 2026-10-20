# JARGON SCAN REPORT — 기획서 내부 암호 · SSOT 금지어 전수 스캔

- 생성 시각: `2026-10-20 16:30:19`
- 실행 스킬: `scripts/qa/skill_jargon_scan.py` (Skill 2, 읽기 전용)
- 스캔 대상: `prototype_clean/*.html` — **38개 화면**
- **[A] DOM 가시 텍스트 탐지: 37건** (텍스트 노드 + placeholder/title/alt/aria-label/버튼 value)
- **[B] JS 동적 렌더링 후보 탐지: 200건** (`<script>` 내 한글 포함 문자열 리터럴)
- 무결 화면(탐지 0건): 17개

> [A]는 정적 화면에 그대로 노출되는 텍스트이므로 우선 정비 대상이다. [B]는 innerHTML/모달 렌더링 시 노출될 수 있는 후보로, 분석 AI가 노출 여부를 판단한다.
> 본 스킬은 HTML을 수정하지 않는다. 치환 패치는 분석 AI + 코딩 AI가 작성한다.

## 1. 규칙별 탐지 요약

| 분류 | 규칙 | 설명 | [A] DOM | [B] JS | 대표 매칭어 |
| :--- | :--- | :--- | ---: | ---: | :--- |
| 내부암호 | CODE_C | C-01~04 (정산 케이스 코드) | 0 | 10 | `C-03`×5, `C-02`×3, `C-04`×2 |
| 내부암호 | CODE_H | H-01~05 (하드락 코드) | 0 | 0 | - |
| 내부암호 | CODE_D | D-1~16 (회귀테스트 코드) | 4 | 13 | `D-15`×3, `D-12`×3, `D-1`×3, `D-16`×2, `D-11`×2, `D-13`×2 |
| 내부암호 | CODE_P | P1.1~5.1 (Phase 코드) | 0 | 2 | `P5.1`×2 |
| 내부암호 | PIPELINE | Pipeline 표기 | 1 | 61 | `Pipeline 1.1`×14, `Pipeline 2.2`×14, `Pipeline 5.1`×13, `Pipeline 2.1`×8, `pipeline`×5, `Pipeline`×4 |
| 내부암호 | CHAPTER | 제N장 (기획서 장 번호) | 5 | 3 | `제14장`×2, `제6장`×2, `제17장`×1, `제9장`×1, `제18장`×1, `제3장`×1 |
| 내부암호 | SECTION | N.N절 (기획서 절 번호) | 17 | 83 | `17.5절`×7, `5.3절`×7, `4.1절`×6, `5.2절`×6, `10.4절`×6, `7.2절`×5 |
| 내부암호 | SNAKE_FLAG | *_flag DB 컬럼명 | 0 | 0 | - |
| 내부암호 | SNAKE_YN | *_yn DB 컬럼명 | 0 | 6 | `own_copyright_yn`×6 |
| 내부암호 | SNAKE_ID | *_id DB 컬럼명 | 2 | 4 | `contract_id`×3, `payee_id`×1, `cafe_member_id`×1, `settlement_recipient_id`×1 |
| 금지어 | BAN_GICHUL | 기출 | 0 | 0 | - |
| 금지어 | BAN_ERRATA | 정오표 | 0 | 0 | - |
| 금지어 | BAN_VIMEO | Vimeo | 0 | 0 | - |
| 금지어 | BAN_80PCT | 80% | 2 | 18 | `80%`×20 |
| 금지어 | BAN_CIRCLED | ①~⑭ 원문자 번호 | 0 | 0 | - |
| 금지어 | BAN_MARKER | [마커 표기 | 0 | 0 | - |
| 번역중복 | DUP_PAREN | 동일어 괄호 중복 (예: 실결제금액(실결제금액)) | 6 | 0 | `개발지원금(개발지원금)`×3, `개발지원금 (개발지원금)`×3 |

## 2. 화면별 탐지 요약

| 화면 | [A] DOM | [B] JS | 내부암호 | 금지어 | 번역중복 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `00_WORKFLOW_GUIDE_baseline.html` | 2 | 0 | 2 | 0 | 0 |
| `ADMN-BOOK-001_baseline.html` | 1 | 0 | 1 | 0 | 0 |
| `ADMN-BRD-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-BRD-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-BRD-005_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-001_baseline.html` | 0 | 1 | 1 | 0 | 0 |
| `ADMN-CONF-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-003_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-004_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-005_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-010_baseline.html` | 2 | 15 | 17 | 0 | 0 |
| `ADMN-DASH-001_baseline.html` | 3 | 0 | 1 | 2 | 0 |
| `ADMN-INST-001_baseline.html` | 1 | 3 | 4 | 0 | 0 |
| `ADMN-INST-002_baseline.html` | 0 | 13 | 13 | 0 | 0 |
| `ADMN-LOGIN-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-ORD-001_baseline.html` | 2 | 0 | 2 | 0 | 0 |
| `ADMN-PROD-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-003_baseline.html` | 0 | 1 | 1 | 0 | 0 |
| `ADMN-PROD-004_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-005_baseline.html` | 0 | 1 | 1 | 0 | 0 |
| `ADMN-PROD-006_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-007_baseline.html` | 0 | 3 | 3 | 0 | 0 |
| `ADMN-PROM-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROM-002_baseline.html` | 1 | 0 | 1 | 0 | 0 |
| `ADMN-RFD-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-SETT-001_baseline.html` | 0 | 27 | 27 | 0 | 0 |
| `ADMN-SETT-002_baseline.html` | 6 | 62 | 52 | 14 | 2 |
| `ADMN-SETT-004_baseline.html` | 0 | 6 | 6 | 0 | 0 |
| `ADMN-SETT-005_baseline.html` | 1 | 14 | 15 | 0 | 0 |
| `ADMN-SETT-006_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-SETT-007_baseline.html` | 8 | 21 | 24 | 4 | 1 |
| `ADMN-SETT-008_baseline.html` | 1 | 10 | 11 | 0 | 0 |
| `ADMN-SETT-009_baseline.html` | 5 | 15 | 17 | 0 | 3 |
| `ADMN-SETT-011_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-USER-001_baseline.html` | 1 | 0 | 1 | 0 | 0 |
| `ADMN-USER-007_baseline.html` | 3 | 8 | 11 | 0 | 0 |
| `patch_all_snb_v3.html` | 0 | 0 | 0 | 0 | 0 |

## 3. [A] DOM 가시 텍스트 상세 (우선 정비 대상)

### `00_WORKFLOW_GUIDE_baseline.html` — 2건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 708 | text | 내부암호 | CHAPTER | `제14장` | 제14장 정산 기준 |
| 824 | text | 내부암호 | SECTION | `8.3절` | SSOT: 02권 정산 기준 8.3절 |

### `ADMN-BOOK-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 762 | text | 내부암호 | CHAPTER | `제6장` | 제6장 정산 기준 · v4.0.0 SSOT |

### `ADMN-CONF-010_baseline.html` — 2건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 344 | text | 내부암호 | CODE_D | `D-12` | D-12 · 17장 · 6장 |
| 349 | text | 내부암호 | SECTION | `3.5절` | USER-007 · 3.5절 |

### `ADMN-DASH-001_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 546 | text | 내부암호 | CODE_D | `D-3` | D-3 |
| 606 | text | 금지어 | BAN_80PCT | `80%` | CDN 트래픽 80% 초과 시 주의 배지가 점등되며, 수동 점검 시 a… |
| 629 | text | 금지어 | BAN_80PCT | `80%` | · 80% 임계치 초과 · 응답 118ms |

### `ADMN-INST-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 2858 | text | 내부암호 | SECTION | `3.2.2절` | …권 정산 기준 · 정산 기준 · 통합 상세 설계서 3.2.2절 |

### `ADMN-ORD-001_baseline.html` — 2건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 621 | text | 내부암호 | SECTION | `8.2절` | 8.2절 · 24시간 기한 |
| 627 | text | 내부암호 | SECTION | `5.5절` | 5.5절 우편번호 판정 |

### `ADMN-PROM-002_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 932 | text | 내부암호 | SECTION | `8.1절` | 8.1절 연동 |

### `ADMN-SETT-002_baseline.html` — 6건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1057 | text | 번역중복 | DUP_PAREN | `개발지원금(개발지원금)` | 2. 개발지원금(개발지원금) 소진 원장 (확정·한도소진·실지급 3분리 · 정산… |
| 1078 | text | 번역중복 | DUP_PAREN | `개발지원금 (개발지원금)` | 매출연동 개발지원금 (개발지원금) |
| 1307 | text | 내부암호 | SECTION | `16.1절` | 16.1절 · 정산 기준 필수 규격 |
| 1372 | text | 내부암호 | SECTION | `7.4절` | 7.4절 carryover_ledger |
| 1972 | text | 내부암호 | SECTION | `7.4절` | 7.4절 연속성 등식: [1] + [2] + [3] = [… |
| 2093 | text | 내부암호 | CHAPTER | `제9장` | 제9장 · 정산 기준 매트릭스 |

### `ADMN-SETT-005_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 635 | text | 내부암호 | SECTION | `10.4절` | 10.4절 도서 공급형태 오등록 규칙: 기지급·신고 없으므로… |

### `ADMN-SETT-007_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 333 | text | 내부암호 | CODE_D | `D-1` | 16.1절 · D-1 |
| 333 | text | 내부암호 | SECTION | `16.1절` | 16.1절 · D-1 |
| 338 | text | 내부암호 | SECTION | `5.3절` | 5.3절 하드락 |
| 425 | text | 내부암호 | CODE_D | `D-2` | Case 7 / 검증규칙 / D-2 |
| 428 | text | 번역중복 | DUP_PAREN | `개발지원금 (개발지원금)` | 5단계 확정 매출연동 개발지원금 (개발지원금) 및 7단계 비정기 가산금 |
| 431 | text | 내부암호 | SECTION | `4.1절` | 4.1절 / 13.1절 |
| 431 | text | 내부암호 | SECTION | `13.1절` | 4.1절 / 13.1절 |
| 437 | text | 내부암호 | SECTION | `5.3절` | 5.3절 상호 차단 |

### `ADMN-SETT-008_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1220 | text | 내부암호 | SECTION | `17.5절` | 17.5절 하드락 |

### `ADMN-SETT-009_baseline.html` — 5건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 341 | text | 번역중복 | DUP_PAREN | `개발지원금(개발지원금)` | 2. 자사 지분 내 개발지원금(개발지원금) 차감 검증 (정산 기준 · 검증규칙·16) |
| 356 | text | 번역중복 | DUP_PAREN | `개발지원금 (개발지원금)` | 매출연동 개발지원금 (개발지원금) |
| 370 | text | 내부암호 | PIPELINE | `Pipeline` | 정산 입력 구분 (Pipeline) |
| 390 | text | 번역중복 | DUP_PAREN | `개발지원금(개발지원금)` | 🛡️ 개발지원금(개발지원금) 자사 지분('RH-INTERNAL') 내 차감 및… |
| 492 | text | 내부암호 | CHAPTER | `제18장` | 제18장 정산 기준 · Case 11 · Case 12 정… |

### `ADMN-USER-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1415 | text | 내부암호 | SNAKE_ID | `cafe_member_id` | users.cafe_member_id IS NOT NULL |

### `ADMN-USER-007_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 306 | text | 내부암호 | CHAPTER | `제3장` | 제3장 3.2절 |
| 306 | text | 내부암호 | SECTION | `3.2절` | 제3장 3.2절 |
| 610 | text | 내부암호 | SNAKE_ID | `settlement_recipient_id` | settlement_recipient_id |

## 4. [B] JS 동적 렌더링 후보 상세

### `ADMN-CONF-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 460 | js-string | 내부암호 | CODE_D | `D-15` | 2026 제3회 실기 시험 D-15 파이널 모의고사 특강 |

### `ADMN-CONF-010_baseline.html` — 15건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 549 | js-string | 내부암호 | CODE_D | `D-12` | …LETED → ACTIVE) 및 한도 복원 (부록 D-12) |
| 571 | js-string | 내부암호 | CODE_D | `D-12` | ACTIVE (유효 복귀 · 부록 D-12) |
| 582 | js-string | 내부암호 | SECTION | `7.3절` | …POST_TAX) 이월 계정 간 대체 2차 승인 (7.3절) |
| 611 | js-string | 내부암호 | SECTION | `3.4절` | 민감 정보(주민번호·계좌번호) 마스킹 해제 열람 (3.4절 · TTL 30초) |
| 638 | js-string | 내부암호 | SECTION | `4.3절` | …lecture_instructors) 변경 저장 (4.3절) |
| 666 | js-string | 내부암호 | SECTION | `4.1절` | …취인 분할 지분율(payee_splits) 등록 (4.1절 · Case 7) |
| 696 | js-string | 내부암호 | SECTION | `7.2절` | …금 수기 소명(MANUAL_NOTE) 검수 승인 (7.2절) |
| 724 | js-string | 내부암호 | SECTION | `17.5절` | …과세유형 전환 감지 승인 및 신규 버전 행 추가 (17.5절) |
| 755 | js-string | 내부암호 | SECTION | `5.2절` | … 이행률 정산(PRO_RATA) 수동 조정 승인 (5.2절) |
| 785 | js-string | 내부암호 | SECTION | `3.5절` | …드 분리 파기 및 계층 2 정산원장 비식별 보존 (3.5절) |
| 835 | js-string | 내부암호 | SECTION | `16.1절` | …저작자 지위(payee_is_author) 전환 (16.1절) |
| 858 | js-string | 내부암호 | SECTION | `3.3절` | …resigned URL 발급 열람 (5분 만료 · 3.3절) |
| 877 | js-string | 내부암호 | SECTION | `6.2절` | …= true) 신규 SKU 등록 및 가채번 매칭 (6.2절) |
| 877 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 저작권 도서(own_copyright_yn = true) 신규 SKU 등록 및 가채번 매칭 … |
| 879 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …결 및 자사 저작권 100% + 정종대 개발지원금(Pipeline 5.1) 모수 설정 |

### `ADMN-INST-001_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1316 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [자사저작권] 정종대 산업안전 필기 빈출문제집 (own_copyright_yn=true) |
| 2607 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [v4.0.0 대표 사례] 자사저작권 도서(own_copyright_yn=true) 매출연동 지원금 15% + 선급금 상계… |
| 2746 | js-string | 내부암호 | PIPELINE | `Pipeline` | … 만료 D-Day 적용 정산 조항 (Pipeline) 세무 판정 · 국세청 … |

### `ADMN-INST-002_baseline.html` — 13건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 727 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …권 도서+강좌] 정종대 산업안전 필기 개발지원금 (Pipeline 5.1) |
| 984 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …roved.toLocaleString()}원 + Pipeline 5.1 매출연동 약정 활성화 ${rsApprovedCo… |
| 1025 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 (R/S 1회) ${item.rateText} |
| 1085 | js-string | 내부암호 | SECTION | `6.4절` | ⚖️ [6.4절 · TX-03 매절(권리 양도) 세무 근거 통제]… |
| 1093 | js-string | 내부암호 | SECTION | `5.2절` | …SHARE) 지원금 약정 체결 1회 필수값 검증 (5.2절 · 7.2절) ${item.t… |
| 1093 | js-string | 내부암호 | SECTION | `7.2절` | …지원금 약정 체결 1회 필수값 검증 (5.2절 · 7.2절) ${item.targetCo… |
| 1130 | js-string | 내부암호 | SECTION | `7.2절` | … 🔒 [7.2절] 마일스톤 검수 승인 3대 필수 게이트 판정 … |
| 1156 | js-string | 내부암호 | SECTION | `7.2절` | … 이원화 검수 방식 선택 (7.2절) … |
| 1291 | js-string | 내부암호 | CHAPTER | `제17장` | 국세청 API 연동(제17장) |
| 1319 | js-string | 내부암호 | SECTION | `7.0절` | [7.0절 마감 상태별 인입 통제]\n선택하신 '${tMon… |
| 1339 | js-string | 내부암호 | SECTION | `7.0절` | [7.0절 마감 상태별 인입 통제]\n선택하신 '${tMon… |
| 1351 | js-string | 내부암호 | SECTION | `7.2절` | [7.2절 담당자 수기 소명형 검수 규칙]\n수기 검수(내부… |
| 1372 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동(Pipeline 5.1) 지원금 약정 1회 검수 승인 (${item.ta… |

### `ADMN-PROD-003_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1913 | js-string | 내부암호 | SECTION | `4.2절` | 기획서 4.2절 정책에 따라 ADMN-SETT-001의 1계층 지… |

### `ADMN-PROD-005_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1883 | js-string | 내부암호 | SECTION | `4.2절` | 기획서 4.2절에 따라 패키지에 포함된 모든 단과 강좌의 ADMN… |

### `ADMN-PROD-007_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 867 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …Badge} TX-13 · Pipeline 2.3 ${stBadge} … |
| 933 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …스터 (공급 형태 · 재고 · 일반 상품 판매매출 Pipeline 2.3) |
| 1046 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …. (자사 권리자 100% 매핑 · TX-13 · Pipeline 2.3) |

### `ADMN-SETT-001_baseline.html` — 27건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 458 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 470 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 480 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 493 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 505 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 515 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …_copyright_yn=true) → 개발지원금(Pipeline 5.1) |
| 515 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 도서(own_copyright_yn=true) → 개발지원금(Pipeline 5.1) |
| 535 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 604 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 저작권 보유 도서(own_copyright_yn=true) 자사 100% 자동 매핑 |
| 612 | js-string | 내부암호 | SECTION | `4.2절` | 1계층 권리자 매핑 미완료 상태로 신규 결제 차단(4.2절) |
| 657 | js-string | 내부암호 | CHAPTER | `제6장` | …되며 별도 1계층 인세 지분 매핑 대상이 아닙니다(제6장 6.1절). |
| 657 | js-string | 내부암호 | SECTION | `6.1절` | …도 1계층 인세 지분 매핑 대상이 아닙니다(제6장 6.1절). |
| 660 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …MENT)는 1계층 인세 지분 매핑 대상이 아니며 Pipeline 2.2로 별도 정산합니다. |
| 674 | js-string | 내부암호 | SNAKE_ID | `contract_id` | ${idx+1}행: 유효 계약(contract_id) 바인딩이 필요합니다. |
| 715 | js-string | 내부암호 | SECTION | `5.2절` | … 지분 0% 구간: 지원금 0원 미발생 예외 적용(5.2절). |
| 739 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁정산 분리(Pipeline 2.2) |
| 832 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | … 현재 매핑된 권리자 개발지원금(Pipeline 5.1) 판매 게이트 작업 … |
| 943 | js-string | 내부암호 | CODE_D | `D-15` | …ypass되지 않고 지원금 모수로 정상 인입됩니다(D-15·D-16). |
| 943 | js-string | 내부암호 | CODE_D | `D-16` | …되지 않고 지원금 모수로 정상 인입됩니다(D-15·D-16). |
| 943 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | … 수취인( 정종대 강사 )의 매출연동 개발지원금( Pipeline 5.1 , 요율 15%, 상계 허용 CONDITIONA… |
| 943 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [v4.0.0 자사 저작권 보유 도서 (own_copyright_yn = true)] 저작권이 당사(엘캠퍼스)에 있으… |
| 948 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …도서는 1계층 지분 매핑 대상이 아니며 위탁 정산(Pipeline 2.2)으로 직접 처리됩니다. |
| 955 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | [연결된 매출연동 개발지원금(Pipeline 5.1)] ${p.supportAgreements.ma… |
| 955 | js-string | 내부암호 | SECTION | `5.2절` | …침해하지 않고 자사 귀속 지분 내에서만 차감됩니다(5.2절). |
| 961 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …ternalShare)} 개발지원금(Pipeline 5.1) 요율 ${pct(lastSlice.suppor… |
| 968 | js-string | 내부암호 | SNAKE_ID | `contract_id` | … 상태 권리자 (1계층) 바인딩 계약 (contract_id) 1계층 지분율 적용 시작일 종… |
| 1076 | js-string | 내부암호 | SNAKE_ID | `contract_id` | … 바인딩 계약 선택 (contract_id NOT NULL) … |

### `ADMN-SETT-002_baseline.html` — 62건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1445 | js-string | 내부암호 | SECTION | `6.5절` | …기 이월액(+45,000원) 합산]에 기인합니다 (6.5절). |
| 1487 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2 · 수수료 차감지급) |
| 1510 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금(Pipeline 2.2)은 원천징수 비대상이며, 수수료 차감 후 지급(N… |
| 1510 | js-string | 내부암호 | SECTION | `6.6절` | …100,000원)를 차감한 실정산액을 지급합니다 (6.6절 · 8.3절 9단계). |
| 1510 | js-string | 내부암호 | SECTION | `8.3절` | …원)를 차감한 실정산액을 지급합니다 (6.6절 · 8.3절 9단계). |
| 1520 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 단독 (Pipeline 5.1 · 무한도형) |
| 1542 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …금액(72,000원)을 세전 계정(PRE_TAX, Pipeline 5.1 전용 구분)으로 차월 이월합니다 (7.3~7.4절… |
| 1542 | js-string | 내부암호 | SECTION | `7.4절` | … 5.1 전용 구분)으로 차월 이월합니다 (7.3~7.4절). |
| 1550 | js-string | 내부암호 | CODE_D | `D-11` | … 청구 트리거 발동 (10단계 CLAIM · QA D-11) |
| 1574 | js-string | 내부암호 | CODE_D | `D-11` | …과 무관하게 소액 미상계 선급금(-50,000원, D-11) 및 전속계약금 세후 일할 반환액(-4,768,7… |
| 1622 | js-string | 내부암호 | PIPELINE | `pipeline` | … ${s.pipelineText} ${s.step8T… |
| 1665 | js-string | 내부암호 | SECTION | `6.5절` | … 💡 [6.5절 과세표준 ↔ 실지급액 차액 사유 자동 명시] … |
| 1665 | js-string | 내부암호 | SECTION | `8.3절` | …📊 1단계 ~ 11단계 순방향 단방향 연산 명세 (8.3절 SSOT 정본) … |
| 1747 | js-string | 내부암호 | PIPELINE | `pipeline` | … ${s.payeeName} ${s.pipelineText} ${s.bankInf… |
| 1852 | js-string | 내부암호 | CODE_D | `D-13` | 🧪 [QA D-13 검증 완료] 펌뱅킹 실패 시 마감 원장(Locke… |
| 2261 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 80%) |
| 2264 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌 수익배분) |
| 2282 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 80%) |
| 2285 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 (자사 발행 도서 인세) |
| 2306 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 (위탁 도서 판매대금) |
| 2327 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (일시 특강·콘텐츠 용역) |
| 2330 | js-string | 내부암호 | CODE_D | `D-13` | …완료 후 수취인 계좌번호 오기재로 송금 실패(QA D-13) → 이중 과세 방지를 위해 세후(POST_TAX… |
| 2348 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (선급금 해지 강제청구) |
| 2351 | js-string | 내부암호 | CODE_C | `C-03` | … 환수 청구 전환하여 선급금 원장 잔액 0원 종결(C-03·C-04) |
| 2351 | js-string | 내부암호 | CODE_C | `C-04` | …구 전환하여 선급금 원장 잔액 0원 종결(C-03·C-04) |
| 2375 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 · 2계층 지분 80%) |
| 2376 | js-string | 금지어 | BAN_80PCT | `80%` | 개인 면세사업자 (수취인 분할 80% · 원천징수 3.3% + 계산서 역발행) |
| 2383 | js-string | 금지어 | BAN_80PCT | `80%` | …001 \| 1계층 단독 100% → 2계층 정종대 80% / (주)산준교육 20% |
| 2384 | js-string | 금지어 | BAN_80PCT | `80%` | … 전체 당월 상계 -1,500,000원 중 정종대(80%) 귀속분 -1,200,000원 (기말 잔액 2,0… |
| 2396 | js-string | 금지어 | BAN_80PCT | `80%` | 8단계 수취인 분할(80%) 후 과세표준 5,915,000원(계산서 역발행 … |
| 2396 | js-string | 금지어 | BAN_80PCT | `80%` | …5,000원(계산서 역발행 금액) − 선급금 상계(80% 귀속분) 1,200,000원 − 원천징수세액(3.… |
| 2398 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (강좌 수익배분) |
| 2405 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | OWN_PUBLISHED (자사발행 인세 · Pipeline 2.1) |
| 2408 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 (Pipeline 5.1) |
| 2411 | js-string | 금지어 | BAN_80PCT | `80%` | …상계 -1,500,000원 → 8단계 수취인 분할(80%) 적용 시 정종대 귀속 상계액 -1,200,000… |
| 2414 | js-string | 금지어 | BAN_80PCT | `80%` | 본인 귀속 80% (과세표준 5,915,000원 / 선급금상계 -1… |
| 2425 | js-string | 금지어 | BAN_80PCT | `80%` | 과세표준 7,393,750×80%=5,915,000원 / 상계 후 잔액 5,893,… |
| 2425 | js-string | 금지어 | BAN_80PCT | `80%` | …15,000원 / 상계 후 잔액 5,893,750×80%=4,715,000원 |
| 2432 | js-string | 금지어 | BAN_80PCT | `80%` | …6-10-31 19:05] 재무팀 김회계: 정종대(80%) / 산준교육(20%) 2계층 분할 및 선급금 1… |
| 2469 | js-string | 금지어 | BAN_80PCT | `80%` | 주권리자 80% 귀속 |
| 2492 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | CON-2026-014 \| 위탁 도서(Pipeline 2.2) 수수료 차감지급(NET_DEDUCT, 수수료율 … |
| 2505 | js-string | 내부암호 | SECTION | `6.6절` | …) = 위탁 순정산 실지급액 1,820,000원 (6.6절 품목별 구성요소 등식 100% 일치) |
| 2509 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | CONSIGNMENT (위탁도서 · Pipeline 2.2 · NET_DEDUCT) |
| 2515 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 출고 기준 위탁 순액 산출 (Pipeline 2.2) |
| 2522 | js-string | 내부암호 | SECTION | `6.6절` | [2026-10-31 19:18] 재무팀 이검수: 6.6절 품목별 배분 등식(판매대금 260만 − 위탁순액 … |
| 2550 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (일시 용역) |
| 2581 | js-string | 내부암호 | CODE_C | `C-02` | C-02·C-03 가드레일: 3단계 MMG 보전금(800,… |
| 2581 | js-string | 내부암호 | CODE_C | `C-03` | C-02·C-03 가드레일: 3단계 MMG 보전금(800,000원)… |
| 2599 | js-string | 내부암호 | CODE_C | `C-02` | NON_OFFSET (선급금 상계 절대 금지 · C-02/C-03) |
| 2599 | js-string | 내부암호 | CODE_C | `C-03` | …OFFSET (선급금 상계 절대 금지 · C-02/C-03) |
| 2611 | js-string | 내부암호 | CODE_C | `C-03` | 중도해지 미상계 선급금 강제 환수청구 분리 발행 (C-03·C-04) |
| 2611 | js-string | 내부암호 | CODE_C | `C-04` | …미상계 선급금 강제 환수청구 분리 발행 (C-03·C-04) |
| 2616 | js-string | 내부암호 | CODE_C | `C-02` | …1 19:30] 법무·재무 합동검토: v4.0.0 C-02/C-03 가드레일에 따라 비상계 MMG(80만원)… |
| 2616 | js-string | 내부암호 | CODE_C | `C-03` | …30] 법무·재무 합동검토: v4.0.0 C-02/C-03 가드레일에 따라 비상계 MMG(80만원)는 선급금… |
| 2731 | js-string | 내부암호 | PIPELINE | `pipeline` | …ntLabel} ${r.pipeline} … |
| 2768 | js-string | 내부암호 | PIPELINE | `pipeline` | …riginMonth} ${r.pipeline.replace(/Pipeline [0-9.]+ /… |
| 2768 | js-string | 내부암호 | PIPELINE | `Pipeline` | … ${r.pipeline.replace(/Pipeline [0-9.]+ /g, '')} … |
| 2887 | js-string | 내부암호 | SECTION | `6.5절` | 📐 [6.5절 과세표준 vs 실지급액 차액 검증 등식] ${c… |
| 2939 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | … [테이블 B] 온라인 강좌 수익배분 산출 명세 (Pipeline 1.1) 정산기준금 DECIMA… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | … 📚 [테이블 C] 교재 저작권 인세(Pipeline 2.1) · 위탁 도서 판매대금(Pipeline 2.2)… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …(Pipeline 2.1) · 위탁 도서 판매대금(Pipeline 2.2) 산출 명세 3PL 출고… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline` | …재명 공급 형태 (Pipeline) 출고 / 반품 … |

### `ADMN-SETT-004_baseline.html` — 6건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 873 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 (위탁 도서) |
| 892 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌) |
| 911 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 (자사발행 도서) |
| 930 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌) |
| 1171 | js-string | 내부암호 | PIPELINE | `pipeline` | … 연결 파이프라인 ${r.pipeline} 3계층 과·면세 구성 … |
| 1171 | js-string | 내부암호 | SECTION | `8.2절` | … 차이 원인 코드 분류 (8.2절 표준 코드) … |

### `ADMN-SETT-005_baseline.html` — 14건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 881 | js-string | 내부암호 | SECTION | `7.3절` | [7.3절 · 10.3절] 세전·세후 계정 간 대체 전표는 … |
| 881 | js-string | 내부암호 | SECTION | `10.3절` | [7.3절 · 10.3절] 세전·세후 계정 간 대체 전표는 금액 크기와 무… |
| 908 | js-string | 내부암호 | SECTION | `10.4절` | [10.4절 도서 오등록 특칙] 전월에 인세가 지급·신고된 바… |
| 931 | js-string | 내부암호 | SECTION | `5.2절` | [5.2절 · 10.3절] 계약 해지 시 지원금 이행률 정산… |
| 931 | js-string | 내부암호 | SECTION | `10.3절` | [5.2절 · 10.3절] 계약 해지 시 지원금 이행률 정산(PRO_RAT… |
| 951 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 정산금 (Pipeline 2.2) |
| 1082 | js-string | 내부암호 | SECTION | `10.3절` | … 승인 통제 규칙 (10.3절) ${item.requireRe… |
| 1082 | js-string | 내부암호 | SECTION | `10.4절` | … 🔗 [10.4절] 자동 분기된 증빙 · 원천세 정정 채널 (1:N… |
| 1219 | js-string | 내부암호 | SECTION | `10.4절` | [10.4절 도서 오등록 특칙] 기지급·신고 이력 없을 시 당… |
| 1225 | js-string | 내부암호 | SECTION | `10.3절` | • 승인 경로 판정 (10.3절): ${approvalText} … |
| 1225 | js-string | 내부암호 | SECTION | `10.4절` | … • 자동 연결 증빙 정정 채널 (10.4절): ${channelText} |
| 1238 | js-string | 내부암호 | SECTION | `10.2절` | [10.2절 필수 입력 통제]\n수동 조정 소명 내용(adj_… |
| 1292 | js-string | 내부암호 | SECTION | `10.4절` | 10.4절 기준 세무 매트릭스 정정 채널 자동 연결됨 |
| 1329 | js-string | 내부암호 | SECTION | `10.2절` | [10.2절 필수 입력 통제]\n수동 조정 소명 내용(adj_… |

### `ADMN-SETT-007_baseline.html` — 21건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 549 | js-string | 금지어 | BAN_80PCT | `80%` | 2026 산업안전기사 정종대 통합계약 — 주권리자 80% : (주)산준교육 에이전시 20% (SETT-00… |
| 565 | js-string | 금지어 | BAN_80PCT | `80%` | 주권리자 정종대 80% 귀속 (2026-10 과세표준 5,915,000원… |
| 568 | js-string | 금지어 | BAN_80PCT | `80%` | …계약 체결 시 주권리자 정종대(PY-0025-A, 80%) 및 공동서명 에이전시 (주)산준교육(PY-002… |
| 596 | js-string | 내부암호 | SECTION | `16.1절` | …기사 기본서 저작권 및 강의 계약 (상속 승계 · 16.1절) |
| 613 | js-string | 내부암호 | CODE_D | `D-1` | …분할협의서 기준 자녀 40% (이전 원거래 환불은 D-1 스냅샷 적용) |
| 670 | js-string | 내부암호 | SECTION | `5.3절` | …3,500,000원 존재 (선급금 원장 미종결 — 5.3절 상호 차단) |
| 681 | js-string | 내부암호 | SECTION | `5.3절` | 선급금 미종결 계약으로 원 권리자 100% 고정 (5.3절) |
| 870 | js-string | 내부암호 | SECTION | `4.1절` | … • 계약서 등록 공동 서명인 풀(4.1절): ${c.coSigners.map(cs => |
| 906 | js-string | 내부암호 | SECTION | `4.1절` | ✅ [4.1절 정합성 통과] 공동 서명 수취인 분할 비율 합계가… |
| 915 | js-string | 내부암호 | SECTION | `4.1절` | … 수취인 (공동 서명인 그룹 · 4.1절) 사업자/소득 구분 및 … |
| 915 | js-string | 내부암호 | SECTION | `16.1절` | … 저작자 본인 여부 / 승계 확정일 (16.1절) 2계층 분할 비율 (%… |
| 915 | js-string | 금지어 | BAN_80PCT | `80%` | …30% (강사:소속사 표준) 80% : 20% 60% : 40%… |
| 970 | js-string | 내부암호 | CODE_D | `D-1` | …ccessionDate} (이전 환불은 원 스냅샷 D-1) |
| 991 | js-string | 내부암호 | SECTION | `13.3절` | …무 독립 판정 미리보기 (Case 7 · 13.2~13.3절) … |
| 991 | js-string | 내부암호 | SECTION | `13.3절` | … 배분 순번 (13.3절 정렬) 수취인 … |
| 991 | js-string | 내부암호 | SECTION | `13.2절` | …할 비율 산출 공식 (13.2절 총액 역산) 8단계 … |
| 991 | js-string | 내부암호 | SNAKE_ID | `payee_id` | …split_ratio) 내림차순 → 수취인 식별자(payee_id) 오름차순 · 선행 수취인 내림(Floor) … |
| 1060 | js-string | 내부암호 | SECTION | `5.3절` | 저장 하드락 (5.3절) 선택 계약( ${c.id} )… |
| 1072 | js-string | 내부암호 | SECTION | `4.1절` | …계약( ${c.id} ): 공동 서명 당사자 일치(4.1절) · 선급금 미보유(5.3절) · 분할 합계 10… |
| 1072 | js-string | 내부암호 | SECTION | `5.3절` | …동 서명 당사자 일치(4.1절) · 선급금 미보유(5.3절) · 분할 합계 100.00% 검증 통과 … |
| 1254 | js-string | 내부암호 | SECTION | `5.3절` | [5.3절 차단] 선급금 미종결 계약에는 수취인 분할을 저장… |

### `ADMN-SETT-008_baseline.html` — 10건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 801 | js-string | 내부암호 | SECTION | `17.5절` | 2026-09-28 폐업 확인됨. 17.5절에 따라 미승인 증빙 리마인더를 즉시 중단하고, 미… |
| 801 | js-string | 내부암호 | SECTION | `7.3절` | …즉시 중단하고, 미지급 정산금은 강제 정산 트리거(7.3절) 대상으로 선정함. 수취 계산서 확보 불가 시 채… |
| 834 | js-string | 내부암호 | SECTION | `17.3절` | 국세청 과세유형 코드 05(비영리법인) 응답. 17.3절 규칙에 따라 인세 라인은 후보 TX-09, 강의 … |
| 896 | js-string | 내부암호 | SECTION | `17.3절` | 17.3절 공급 성격 우선 규칙: 매입처의 과세유형은 일반과… |
| 1018 | js-string | 내부암호 | SECTION | `17.5절` | … 🔄 [17.5절] 과세유형 전환 확인 및 신규 유효일자 버전 행 … |
| 1038 | js-string | 내부암호 | SECTION | `17.3절` | … 🟣 [17.3절] 비영리법인·고유번호 단체(05·06) 세무 판정… |
| 1058 | js-string | 내부암호 | SECTION | `17.5절` | 🚨 [17.5절 폐업 사업자 후속 통제 작동 중] … |
| 1058 | js-string | 내부암호 | SECTION | `7.3절` | … 2) 미지급 정산금 잔액은 강제 정산 트리거(7.3절) 에 의해 최소 지급 하한(100,000원)과 무… |
| 1110 | js-string | 내부암호 | SECTION | `17.5절` | [17.5절 효력일 통제]\n전환 효력 시작일자가 비어 있습니… |
| 1149 | js-string | 내부암호 | SECTION | `17.5절` | ✔ [17.5절 행분할 승인] [${r.partnerName}] … |

### `ADMN-SETT-009_baseline.html` — 15건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 661 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 680 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 682 | js-string | 내부암호 | CODE_D | `D-16` | 2026 위험물산업기사 실기 시뮬레이션 특강 (D-16) |
| 691 | js-string | 내부암호 | CODE_P | `P5.1` | 최그래픽 P5.1 지원금 (5% · 자사몫 차감) |
| 699 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 718 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 737 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사저작권 도서 + 개발지원금 (Pipeline 2.1 / 5.1) |
| 739 | js-string | 내부암호 | CODE_D | `D-15` | [자사저작권] 정종대 산업안전 실기 빈출문제집 (D-15) |
| 748 | js-string | 내부암호 | CODE_P | `P5.1` | 정종대 P5.1 지원금 15% (CONDITIONAL) |
| 756 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 767 | js-string | 내부암호 | SECTION | `5.2절` | 지원금 모수 제외 (5.2절) |
| 794 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출 (Pipeline 2.3 · 소비재) |
| 805 | js-string | 내부암호 | SECTION | `18.3절` | 지원금 모수 제외 (18.3절) |
| 934 | js-string | 내부암호 | CHAPTER | `제14장` | [제14장 14.1절 산출물] '${filename}' 파일… |
| 934 | js-string | 내부암호 | SECTION | `14.1절` | [제14장 14.1절 산출물] '${filename}' 파일을 생성하여… |

### `ADMN-USER-007_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 700 | js-string | 내부암호 | SECTION | `3.1절` | 3.1절 최소 수집 원칙 — 법인은 주민등록번호 미수집 |
| 702 | js-string | 내부암호 | SECTION | `3.1절` | 미수집 (법인사업자 필드 미노출 · 3.1절) |
| 703 | js-string | 내부암호 | SECTION | `3.1절` | 미수집 (법인사업자 필드 미노출 · 3.1절) |
| 976 | js-string | 내부암호 | SECTION | `3.4절` | [3.4절 감사 통제] 열람 사유를 최소 10자 이상 구체적… |
| 1014 | js-string | 내부암호 | SECTION | `3.3절` | ✅ [3.3절 임시 서명 URL(Presigned URL) 발급… |
| 1052 | js-string | 내부암호 | SECTION | `3.4절` | [3.4절 자동 재마스킹] 30초(pii_unmask_ttl… |
| 1113 | js-string | 내부암호 | SECTION | `3.5절` | 3.5절 계층 1 개인정보 필드 분리 파기 승인 실행 |
| 1120 | js-string | 내부암호 | SECTION | `3.5절` | [3.5절 분리 파기 완료] ${item.id}의 개인식별 … |

## 5. 무결 화면 (탐지 0건)

- `ADMN-BRD-001_baseline.html`
- `ADMN-BRD-002_baseline.html`
- `ADMN-BRD-005_baseline.html`
- `ADMN-CONF-002_baseline.html`
- `ADMN-CONF-003_baseline.html`
- `ADMN-CONF-004_baseline.html`
- `ADMN-CONF-005_baseline.html`
- `ADMN-LOGIN-001_baseline.html`
- `ADMN-PROD-001_baseline.html`
- `ADMN-PROD-002_baseline.html`
- `ADMN-PROD-004_baseline.html`
- `ADMN-PROD-006_baseline.html`
- `ADMN-PROM-001_baseline.html`
- `ADMN-RFD-002_baseline.html`
- `ADMN-SETT-006_baseline.html`
- `ADMN-SETT-011_baseline.html`
- `patch_all_snb_v3.html`

