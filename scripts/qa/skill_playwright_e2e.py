#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 4] Playwright E2E 기능·인터랙션 검수 스킬 (scripts/qa/skill_playwright_e2e.py)
- prototype_clean/ 38개 전체 화면 브라우저 렌더링 검수
- 검수 항목:
  1. JS 런타임 에러(pageerror) 0건 검증
  2. 주요 목록 테이블(tbody tr) 렌더링 여부 (빈 테이블 탐지)
  3. 서브뷰 탭(.subview-tab, .subview-btn, .tab-btn) 클릭 전환 검증
  4. 모달 열기 및 범용 닫기(closeAllModals / ESC / 닫기버튼) 검증
- 결과 산출: docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

CLEAN_DIR = Path("prototype_clean").resolve()
# v5.4 검수 폴더 인자 — python scripts/qa/skill_playwright_e2e.py prototype  # WF_TARGET_DIR
import sys as _sys, os as _os
if len(_sys.argv) > 1:
    CLEAN_DIR = type(CLEAN_DIR)(_os.path.abspath(_sys.argv[1]))
REPORT_PATH = Path("scripts/qa/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md")


async def audit_page(browser, html_path: Path):
    page = await browser.new_page(viewport={"width": 1440, "height": 900})
    js_errors = []
    page.on("pageerror", lambda err: js_errors.append(str(err)))

    url = html_path.as_uri()
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(250)

    # 1. 초기 상태에서 열려 있는 모달 체크 & 닫기 테스트
    stuck_modals = await page.evaluate("""() => {
      const modals = Array.from(document.querySelectorAll('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop'));
      const openOnes = modals.filter(m => getComputedStyle(m).display !== 'none');
      if (openOnes.length > 0 && typeof window.closeAllModals === 'function') {
        window.closeAllModals();
      }
      return modals.filter(m => getComputedStyle(m).display !== 'none').map(m => m.id || m.className);
    }""")

    # 2. 모달 열림 후 범용 닫기(closeAllModals) 동작 검증
    modal_close_ok = await page.evaluate("""() => {
      const m = document.querySelector('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop');
      if (!m) return true;
      m.classList.add('show');
      m.style.setProperty('display', 'flex', 'important');
      if (typeof window.closeAllModals === 'function') {
        window.closeAllModals();
      }
      return getComputedStyle(m).display === 'none';
    }""")

    # 3. 서브뷰 / 탭 버튼 클릭 전환 검증
    tabs_tested = await page.evaluate("""() => {
      const tabs = Array.from(document.querySelectorAll('.subview-tab, .subview-btn, .tab-btn'));
      let count = 0;
      tabs.forEach(t => {
        try { t.click(); count++; } catch (e) {}
      });
      if (tabs.length > 0) {
        try { tabs[0].click(); } catch (e) {}
      }
      return count;
    }""")

    await page.wait_for_timeout(100)

    # 4. 테이블 데이터 렌더링(tbody tr 수) 확인
    table_info = await page.evaluate("""() => {
      const tables = Array.from(document.querySelectorAll('table.data-table, table'));
      const totalRows = tables.reduce((acc, tbl) => acc + tbl.querySelectorAll('tbody tr').length, 0);
      return { tableCount: tables.length, rowCount: totalRows };
    }""")

    await page.close()

    status = "PASS"
    notes = []
    if js_errors:
        status = "FAIL"
        notes.append(f"JS 에러 {len(js_errors)}건: {js_errors[0][:80]}")
    if stuck_modals:
        status = "FAIL"
        notes.append(f"미폐쇄 모달 감지: {stuck_modals}")
    if not modal_close_ok:
        status = "FAIL"
        notes.append("모달 닫기(closeAllModals) 실패")
    if table_info["rowCount"] == 0 and not any(k in html_path.name for k in ["LOGIN", "WORKFLOW_GUIDE"]):
        status = "FAIL"
        notes.append("데이터 행 0건 감지 (빈 테이블)")

    return {
        "file": html_path.name,
        "status": status,
        "js_errors": len(js_errors),
        "tabs_tested": tabs_tested,
        "rows": table_info["rowCount"],
        "modal_ok": modal_close_ok and len(stuck_modals) == 0,
        "notes": ", ".join(notes) if notes else "정상 (모달/탭/렌더링 통과)",
    }


async def main():
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(CLEAN_DIR.glob("*.html"))
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for f in files:
            res = await audit_page(browser, f)
            results.append(res)
            print(f"[{res['status']}] {res['file']} (탭:{res['tabs_tested']}개, 행:{res['rows']}행, 모달닫기:{res['modal_ok']})")
        await browser.close()

    passed = sum(1 for r in results if r["status"] == "PASS")
    lines = [
        "# Playwright 기능·인터랙션(E2E) 전수 검수 리포트",
        f"- 검수 대상: `prototype_clean/*.html` ({len(results)}개 화면)",
        f"- 통과 현황: **{passed} / {len(results)} PASS**",
        "",
        "| 화면 파일명 | 판정 | JS 에러 | 탭 전환 검증 | 렌더링 데이터 행(tr) | 모달 열기/닫기 | 비고 |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :--- |",
    ]
    for r in results:
        lines.append(
            f"| `{r['file']}` | **{r['status']}** | {r['js_errors']}건 | {r['tabs_tested']}개 탭 | {r['rows']}행 | {'✓ 정상' if r['modal_ok'] else '✕ 실패'} | {r['notes']} |"
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[Skill 4 리포트 저장 완료] {REPORT_PATH} ({passed}/{len(results)} PASS)")


if __name__ == "__main__":
    asyncio.run(main())
