# 프로젝트 아카이브 (_archive)

본 폴더는 정합성 정비 및 테스트 과정에서 완료된 과거 일회성 패치 스크립트, 구 감사 리포트, 단위 테스트 잔재를 영구 보존용으로 격리 보관하는 디렉토리입니다.

---

## 1. 폴더 구조 및 보관 내역

### 📁 `scripts/` (완료된 일회성 패치/빌더 스크립트 13종)
- `phase1_clean_and_audit.py`: Phase 1 감사 및 정제
- `phase2_to_5_full_clean.py`: Phase 2~5 전 도메인 일괄 클린업
- `phase6_deep_polish_and_audit.py`: Phase 6 심층 2차 정제 및 잔재 스캔
- `fix_tax_exempt_lectures.py` / `fix_tax_exempt_all.py`: 교육용역 인강 면세(0%) 세무 정합성 교정
- `apply_modal_and_tax_patch.py`: 공통 모달 및 세무 교정
- `fix_six_defects.py`: 6대 잔여 결함 일괄 패치
- `builder_patch.py`: 태그 속성 보존형 빌더 스크립트
- `audit_functional_e2e.py` / `e2e_functional_audit.py`: E2E 브라우저 기능 검수기
- `patch_pass_refund_requirements.py`: 합격환급반 4대 제출자료 정합화
- `patch_operator_friendly_terms.py`: ADMN-SETT-006 내부 기획코드 제거 및 실무 운영자 용어화
- `patch_rfd001_s1_and_sett006.py`: ADMN-RFD-001-S1 심사 모달 스펙 정합화 (명의 3중 대조 하드락)

> **※ 현행 마스터 검증 엔진:** 루트 디렉토리의 [`master_fix_and_verify.py`](../master_fix_and_verify.py)에서 위 패치들이 영구 반영된 `prototype/`을 바탕으로 `prototype_clean/` 빌드 및 38개 전 화면 Playwright 헤드리스 검증을 단일 스크립트로 일괄 수행합니다.

---

### 📁 `reports/` (과거 임시 감사 리포트)
- `CLEANUP_AUDIT_REPORT.md`: Phase 6 완료 직후 37개 파일 정합성 스캔 결과 리포트
- `PLAYWRIGHT_UI_AUDIT_REPORT.md`: 10-19 수행된 초기 Playwright UI 감사 결과 리포트

> **※ 현행 최신 리포트:** 38개 전 화면 기능 검증 최종 통과 리포트는 [`docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md`](../docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md)에 보존됩니다.

---

### 📁 `tests/` (구 단독 테스트 잔재)
- `test_inst001_playwright.py`: ADMN-INST-001 단독 Playwright 검증 스크립트
- `output/`: 과거 실행 시 캡처된 스크린샷 4종
