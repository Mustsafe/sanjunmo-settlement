import os
import sys
import time

# UTF-8 출력 보장
sys.stdout.reconfigure(encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright

def run_inst001_playwright_test():
    print("=" * 70)
    print("🚀 [ADMN-INST-001] 권리자 계약 원장 Playwright E2E 자동화 테스트 시작")
    print("=" * 70)

    # 출력 디렉토리 준비
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    # 타겟 파일 경로
    html_path = os.path.abspath(os.path.join("..", "prototype", "ADMN-INST-001_baseline.html"))
    file_url = f"file:///{html_path}".replace("\\", "/")
    print(f"[*] 테스트 대상 HTML: {file_url}")

    results = []

    def log_step(name, status, detail=""):
        res = "[PASS]" if status else "[FAIL]"
        color = "\033[92m" if status else "\033[91m"
        reset = "\033[0m"
        results.append((name, status, detail))
        print(f"  {color}{res}{reset} {name} {f'({detail})' if detail else ''}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        try:
            # -------------------------------------------------------------
            # STEP 1. 페이지 로드 및 기본 메타데이터 검증
            # -------------------------------------------------------------
            page.goto(file_url, wait_until="load")
            time.sleep(0.5)

            title = page.title()
            is_title_ok = "[ADMN-INST-001] 권리자 계약 원장" in title
            log_step("1.1 페이지 타이틀 및 메타데이터 검증", is_title_ok, f"Title: {title}")

            header_code = page.locator("#header-screen-code").inner_text().strip()
            is_code_ok = header_code == "ADMN-INST-001"
            log_step("1.2 화면 식별 코드 검증", is_code_ok, f"Header Code: {header_code}")

            snb_nav = page.locator("#v4-master-snb")
            snb_ok = snb_nav.is_visible() and len(snb_nav.inner_text().strip()) > 50
            log_step("1.3 공통 마스터 SNB 렌더링 검증", snb_ok, f"SNB Text Length: {len(snb_nav.inner_text().strip())} chars")

            # 스크린샷 1: 목록 전체 뷰
            sc1 = os.path.join(out_dir, "01_contract_list_full.png")
            page.screenshot(path=sc1, full_page=False)
            print(f"      📸 스크린샷 저장: {sc1}")

            # -------------------------------------------------------------
            # STEP 2. 계약 목록 KPI 스코어카드 검증 및 인터랙션
            # -------------------------------------------------------------
            kpi_cards = page.locator("#contractKpiGrid .kpi-card")
            kpi_count = kpi_cards.count()
            log_step("2.1 KPI 4칸 스코어카드 렌더링 확인", kpi_count == 4, f"카드 개수: {kpi_count}")

            # '만료 임박 / 세무 보류 / 미확정' KPI 필터 카드 클릭
            alert_kpi = page.locator('[data-kpi-filter="ALERT"]')
            alert_kpi.click()
            time.sleep(0.3)
            
            # 행 수 확인 (ALERT 상태인 행만 표시되는지)
            rows = page.locator("#contractListTableWrap tbody tr")
            alert_row_count = rows.count()
            log_step("2.2 ALERT KPI 카드 클릭 필터링 동작", alert_row_count > 0, f"필터된 행 수: {alert_row_count}")

            # 전체 필터 복구
            page.locator('[data-kpi-filter="ALL"]').click()
            time.sleep(0.3)

            # -------------------------------------------------------------
            # STEP 3. 실시간 검색 및 권리자 구분 필터 검증
            # -------------------------------------------------------------
            search_input = page.locator("#clSearch")
            search_input.fill("정종대")
            time.sleep(0.3)

            filtered_rows = page.locator("#contractListTableWrap tbody tr")
            f_count = filtered_rows.count()
            first_row_text = filtered_rows.first.inner_text() if f_count > 0 else ""
            has_jongdae = "정종대" in first_row_text and "CT-2026-0501" in first_row_text
            log_step("3.1 키워드 검색 ('정종대') 필터링 검증", has_jongdae, f"검색 결과 행 수: {f_count}")

            # 스크린샷 2: 검색 필터링 뷰
            sc2 = os.path.join(out_dir, "02_contract_search_filtered.png")
            page.screenshot(path=sc2)
            print(f"      📸 스크린샷 저장: {sc2}")

            # -------------------------------------------------------------
            # STEP 4. 계약 원장 상세 화면 전환 및 폼 바인딩 검증
            # -------------------------------------------------------------
            # '계약 상세/편집 →' 버튼 클릭
            filtered_rows.first.locator("button[data-open-contract]").click()
            time.sleep(0.5)

            # 탭 전환 확인
            tab_contract = page.locator("#tab-contract")
            is_tab_active = tab_contract.get_attribute("aria-selected") == "true"
            log_step("4.1 계약 상세 탭 활성화 확인", is_tab_active, "tab-contract aria-selected=true")

            page_contract_visible = page.locator("#page-contract").is_visible()
            log_step("4.2 계약 상세 본문 영역 노출 확인", page_contract_visible, "page-contract visible")

            # 바인딩된 계약 식별자 및 대표명 확인
            chip_code = page.locator("#activeContractChip").inner_text().strip()
            banner_title = page.locator("#currentContractBannerTitle").inner_text().strip()
            holder_name_val = page.locator("#holderName").input_value()
            is_holder_ok = (chip_code == "CT-2026-0501" and "정종대" in banner_title and "정종대" in holder_name_val)
            log_step("4.3 정종대(CT-2026-0501) 데이터 폼 바인딩 검증", is_holder_ok, f"홀더명: {holder_name_val}, 칩: {chip_code}")

            # 스크린샷 3: 계약 상세 폼 뷰
            sc3 = os.path.join(out_dir, "03_contract_detail_view.png")
            page.screenshot(path=sc3)
            print(f"      📸 스크린샷 저장: {sc3}")

            # -------------------------------------------------------------
            # STEP 5. 빠른 계약 셀렉트 전환 인터랙션
            # -------------------------------------------------------------
            switch_select = page.locator("#quickContractSwitch")
            switch_select.select_option("CT-2026-0412")
            time.sleep(0.5)

            new_chip_code = page.locator("#activeContractChip").inner_text().strip()
            new_holder_val = page.locator("#holderName").input_value()
            is_switched_ok = (new_chip_code == "CT-2026-0412" and "산준교육" in new_holder_val)
            log_step("5.1 셀렉트박스를 통한 빠른 계약 전환", is_switched_ok, f"전환된 계약: {new_chip_code} ({new_holder_val})")

            # -------------------------------------------------------------
            # STEP 6. 하위 탭(국세청 확인 이력 / 변경·열람 이력) 전환
            # -------------------------------------------------------------
            page.locator("#tab-nts").click()
            time.sleep(0.3)
            is_nts_visible = page.locator("#page-nts").is_visible()
            log_step("6.1 국세청 확인 이력 탭 전환", is_nts_visible, "page-nts visible")

            page.locator("#tab-audit").click()
            time.sleep(0.3)
            is_audit_visible = page.locator("#page-audit").is_visible()
            log_step("6.2 변경·열람 감사 이력 탭 전환", is_audit_visible, "page-audit visible")

            # 스크린샷 4: 감사 이력 뷰
            sc4 = os.path.join(out_dir, "04_audit_history_view.png")
            page.screenshot(path=sc4)
            print(f"      📸 스크린샷 저장: {sc4}")

            # -------------------------------------------------------------
            # STEP 7. 다시 계약 목록 복귀
            # -------------------------------------------------------------
            page.locator("#tab-list").click()
            time.sleep(0.3)
            is_list_back = page.locator("#page-list").is_visible()
            log_step("7.1 계약 목록으로 원복 확인", is_list_back, "page-list visible")

            # 콘솔 에러 검증 (외부 Cloudflare 비콘 원격 측정 에러는 프로토타입 로직과 무관하므로 제외)
            telemetry_keywords = ["cloudflare", "cdn-cgi", "net::err_failed"]
            real_errors = [e for e in console_errors if not any(k in e.lower() for k in telemetry_keywords)]
            if real_errors:
                print(f"      [DEBUG] 감지된 애플리케이션 콘솔 에러 목록: {real_errors}")
            log_step("7.2 애플리케이션 콘솔 에러 없음 검증", len(real_errors) == 0, f"에러 수: {len(real_errors)}")

        finally:
            browser.close()

    print("=" * 70)
    passed_count = sum(1 for _, ok, _ in results if ok)
    total_count = len(results)
    print(f"📊 최종 테스트 결과: {passed_count}/{total_count} 항목 통과 ({'ALL PASS' if passed_count == total_count else 'FAILURES DETECTED'})")
    print("=" * 70)
    return passed_count == total_count

if __name__ == "__main__":
    success = run_inst001_playwright_test()
    sys.exit(0 if success else 1)
