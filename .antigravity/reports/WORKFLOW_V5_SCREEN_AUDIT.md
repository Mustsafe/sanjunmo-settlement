# 00_WORKFLOW_GUIDE v5 렌더링 및 디렉터리 검증 리포트

> 생성일시: 2026-10-21  
> 대상 파일: `prototype_clean/00_WORKFLOW_GUIDE_baseline.html`  
> 검증 도구: Playwright Chromium (1440px 뷰포트)

---

## 1. 캡처 결과물 안내

1. **기본 접힘 상태 전체 페이지:** [`.antigravity/reports/screens/workflow_v5_full_collapsed.png`](screens/workflow_v5_full_collapsed.png)
2. **전체 펼침 상태 (예외 상황 및 계산 순서 포함):** [`.antigravity/reports/screens/workflow_v5_full_expanded.png`](screens/workflow_v5_full_expanded.png)
   - 전수 펼침 대상: `details` 태그 총 5건

---

## 2. #wf-dir-grid 디렉터리 카드 분석 (총 9개 카드)

| No | 카드 분류명 (`h4`) | 비고 |
| :-: | :--- | :--- |
| 1 | **대시보드 · 통계** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 2 | **회원 · 수강 관리** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 3 | **주문 · 환불 · CS · 프로모션** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 4 | **상품 · 강좌 · 교재 관리** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 5 | **권리자 계약 · 지분 매핑** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 6 | **정산 마감 전 사전 대사** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 7 | **월간 정산 · 지급 · 조회** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 8 | **개인정보 · 보안 감사** | 좌측 SNB 그룹 미러링 정상 바인딩 |
| 9 | **사이트 · 약관 · 메시지 설정** | 좌측 SNB 그룹 미러링 정상 바인딩 |

---

## 3. 검증 결론

- **레이아웃:** 1440px 폭 기준 `#wf-root` 최대 1280px 중앙 정렬, 상단 진입 카드 2열 그리드, 운영 3개 레인, 정산 3개 스테이지, 전체 화면 디렉터리가 시각적 결함 없이 정상 렌더링됨.
- **디렉터리 런타임 미러링:** 좌측 SNB의 9대 메뉴 그룹 타이틀이 `#wf-dir-grid`의 9개 카드로 100% 정상 동적 파싱·배치됨.
- **상호작용:** `details` 접힘/펼침 트랜지션 및 화면 내 앵커 이동(`href="#wf-ops"`, `#wf-sett`), 외부 화면 바로가기 링크(`ADMN-*`) 연결 정상 확인.