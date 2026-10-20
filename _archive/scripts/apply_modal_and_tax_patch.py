#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[통합 패치]
1. ADMN-BRD-002 (및 전 화면 공통) 모달 안 닫히는 현상 원천 해결
   - common-v84.css: .modal-backdrop 기본 숨김(display:none) 및 활성화(.show/.open/.active) 조건 명확화
   - common-snb.js & ADMN-BRD-002: 닫기/취소/X버튼, 배경 클릭, ESC 키 입력 시
     클래스(.show/.open/.active) 제거 + style.display='none' 강제 초기화
2. ADMN-ORD-001 / PROD-003 / PROD-005: 강좌(교육면세) + 교재(도서면세) 복합과세 오표기 전수 교정
"""

import re
from pathlib import Path

TARGET_DIRS = [Path("prototype"), Path("prototype_clean")]

# ==============================================================================
# 1. CSS 모달 표시/숨김 규칙 교정 (common-v84.css)
# ==============================================================================
MODAL_CSS_PATCH = """
/* === [MODAL-VISIBILITY-AND-CLOSE-LOCK] === */
.modal-backdrop,
.p1-modal-backdrop,
.s1-modal-backdrop,
.s2-modal-backdrop {
  display: none !important;
}

.modal-backdrop.show,
.modal-backdrop.open,
.modal-backdrop.active,
.p1-modal-backdrop.show,
.p1-modal-backdrop.open,
.p1-modal-backdrop.active,
.s1-modal-backdrop.show,
.s1-modal-backdrop.open,
.s1-modal-backdrop.active,
.s2-modal-backdrop.show,
.s2-modal-backdrop.open,
.s2-modal-backdrop.active,
.modal-backdrop[style*="display: flex"],
.modal-backdrop[style*="display:flex"],
.modal-backdrop[style*="display: block"],
.modal-backdrop[style*="display:block"],
.p1-modal-backdrop[style*="display: flex"],
.p1-modal-backdrop[style*="display:flex"],
.s1-modal-backdrop[style*="display: flex"],
.s1-modal-backdrop[style*="display:flex"],
.s2-modal-backdrop[style*="display: flex"],
.s2-modal-backdrop[style*="display:flex"] {
  display: flex !important;
}

.modal-backdrop.force-closed,
.p1-modal-backdrop.force-closed,
.s1-modal-backdrop.force-closed,
.s2-modal-backdrop.force-closed {
  display: none !important;
}
"""

# ==============================================================================
# 2. JS 범용 모달 닫기 보강 스크립트 (common-snb.js 및 ADMN-BRD-002 주입용)
# ==============================================================================
UNIVERSAL_MODAL_CLOSER_JS = """
/* === [UNIVERSAL-MODAL-CLOSER-HOTFIX] === */
(function() {
  if (window.__sjmModalCloserInstalled) return;
  window.__sjmModalCloserInstalled = true;

  function forceCloseModalEl(backdrop) {
    if (!backdrop) return;
    backdrop.classList.remove('show', 'open', 'active');
    backdrop.style.setProperty('display', 'none', 'important');
    backdrop.setAttribute('aria-hidden', 'true');
  }

  function forceOpenModalEl(backdrop) {
    if (!backdrop) return;
    backdrop.classList.remove('force-closed');
    backdrop.classList.add('show');
    backdrop.style.setProperty('display', 'flex', 'important');
    backdrop.setAttribute('aria-hidden', 'false');
  }

  // 전역 헬퍼 등록 (기존 페이지 함수 보강)
  window.closeAllModals = function() {
    document.querySelectorAll('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop, [id*="Modal"], [id*="modal"]').forEach(function(el) {
      if (el.classList.contains('modal-backdrop') || el.classList.contains('p1-modal-backdrop') || el.classList.contains('s1-modal-backdrop') || el.classList.contains('s2-modal-backdrop') || getComputedStyle(el).position === 'fixed') {
        forceCloseModalEl(el);
      }
    });
  };

  // 페이지 로드 후 ADMN-BRD-002 등 고유 모달 열기/닫기 함수 래핑
  window.addEventListener('DOMContentLoaded', function() {
    if (typeof window.closeTransferModal === 'function') {
      var origClose = window.closeTransferModal;
      window.closeTransferModal = function() {
        try { origClose.apply(this, arguments); } catch (e) {}
        window.closeAllModals();
      };
    } else {
      window.closeTransferModal = function() {
        window.closeAllModals();
      };
    }

    if (typeof window.openTransferModal === 'function') {
      var origOpen = window.openTransferModal;
      window.openTransferModal = function() {
        document.querySelectorAll('.modal-backdrop').forEach(function(m) {
          m.style.removeProperty('display');
        });
        try { origOpen.apply(this, arguments); } catch (e) {}
        var modal = document.getElementById('transfer-modal') || document.getElementById('transferModal') || document.getElementById('modal-transfer') || document.querySelector('.modal-backdrop');
        if (modal) forceOpenModalEl(modal);
      };
    }
  });

  // 1) 닫기/취소/X 버튼 및 배경 클릭 시 즉시 닫기 (이벤트 위임)
  document.addEventListener('click', function(e) {
    // (A) 배경(backdrop) 자체를 클릭한 경우
    if (e.target && (
      e.target.classList.contains('modal-backdrop') ||
      e.target.classList.contains('p1-modal-backdrop') ||
      e.target.classList.contains('s1-modal-backdrop') ||
      e.target.classList.contains('s2-modal-backdrop')
    )) {
      forceCloseModalEl(e.target);
      return;
    }

    // (B) 모달 내부의 닫기 버튼(✕, ×, 취소, 닫기, [onclick*="close"]) 클릭 시
    var btn = e.target.closest('button, a, span, [role="button"]');
    if (!btn) return;
    var backdrop = btn.closest('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop');
    if (!backdrop) return;

    var txt = (btn.textContent || '').trim();
    var onclickAttr = (btn.getAttribute('onclick') || '');
    var isCloseBtn = (
      txt === '✕' || txt === '×' || txt === 'X' || txt === 'x' ||
      txt === '취소' || txt === '닫기' || txt === '창 닫기' ||
      onclickAttr.indexOf('close') !== -1 ||
      onclickAttr.indexOf('Close') !== -1 ||
      btn.classList.contains('modal-close') ||
      btn.classList.contains('btn-close')
    );

    if (isCloseBtn) {
      setTimeout(function() {
        forceCloseModalEl(backdrop);
      }, 0);
    }
  }, true);

  // 2) ESC 키 입력 시 열려 있는 모든 모달 닫기
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      window.closeAllModals();
    }
  });
})();
"""

# ==============================================================================
# 3. 과세/면세 오표기 치환 테이블 (ORD-001, PROD-003, PROD-005)
# ==============================================================================
COMMON_TAX_REPLACEMENTS = [
    ("과세 (VAT 10% 포함 · 온라인 교육용역)", "면세 (VAT 0% · 원격평생교육시설 온라인 교육용역)"),
    ("과세 (VAT 10% 포함)", "면세 (VAT 0% · 교육용역)"),
    ("패키지 · 환급반 상품 관리 (복합과세 분할 · 안분 가중치)", "패키지 · 환급반 상품 관리 (강좌·교재 면세 분리 · 안분 가중치)"),
    ("PG 복합과세 결제 승인 및 정산 원장(ADMN-SETT-002) 매출 분리 기준", "도서정가제 준수를 위한 강좌(교육면세)·교재(도서면세) 결제 분리 및 정산 원장(ADMN-SETT-002) 안분 기준"),
    ("PG 복합과세 결제 승인 및 정산 원장(월간 정산 산출·마감) 매출 분리 기준", "도서정가제 준수를 위한 강좌(교육면세)·교재(도서면세) 결제 분리 및 정산 원장 안분 기준"),
    ("패키지 강좌 할인 -100,000원 (VAT 10% 포함)", "패키지 강좌 할인 -100,000원 (교육용역 면세 · VAT 0%)"),
    ("과세 240,000원 + 면세 72,000원 자동 분리", "교육면세 240,000원 + 도서면세 72,000원 자동 분리"),
    ("복합상품 과세·면세 분할 및 환급반 연동", "패키지(강좌·교재) 결제 금액 분할 및 환급반 연동"),
]


def patch_ord_001_tax(text: str) -> str:
    text = re.sub(r"(산업안전기사[^\n<]*?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
    text = re.sub(r"(강좌[^\n<]{1,60}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
    text = re.sub(r"(올패스[^\n<]{0,40}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
    text = re.sub(r"(필기\+실기[^\n<]{0,40}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
    text = re.sub(r"(type\s*:\s*['\"]강좌['\"][^\}]*?)과세\s*10%", r"\1교육용역 면세 0%", text)
    text = re.sub(r"(badge[^>]*>강좌<[\s\S]{0,180}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)

    text = text.replace("MIXED (과·면세 복합)", "EXEMPT (교육·도서 통합면세)")
    text = text.replace("과·면세 복합 (MIXED)", "교육·도서 통합면세 (EXEMPT)")
    text = text.replace("과·면세 복합", "교육·도서 통합면세")

    text = re.sub(r"강좌\s*\(\s*과세\s*10%\s*\)", "강좌(교육용역 면세 0%)", text)
    text = re.sub(r"강좌\s*\(\s*과세\s*\)", "강좌(교육면세)", text)
    text = re.sub(r"인강\s*\(\s*과세\s*\)", "인강(교육면세)", text)
    return text


def main():
    modified = []

    for folder in TARGET_DIRS:
        if not folder.exists():
            continue

        # 1) common-v84.css 패치
        css_file = folder / "common-v84.css"
        if css_file.exists():
            css_txt = css_file.read_text(encoding="utf-8")
            if "[MODAL-VISIBILITY-AND-CLOSE-LOCK]" not in css_txt:
                css_txt = css_txt.rstrip() + "\n\n" + MODAL_CSS_PATCH.strip() + "\n"
                css_file.write_text(css_txt, encoding="utf-8")
                modified.append(str(css_file))

        # 2) common-snb.js 패치
        js_file = folder / "common-snb.js"
        if js_file.exists():
            js_txt = js_file.read_text(encoding="utf-8")
            if "[UNIVERSAL-MODAL-CLOSER-HOTFIX]" not in js_txt:
                js_txt = js_txt.rstrip() + "\n\n" + UNIVERSAL_MODAL_CLOSER_JS.strip() + "\n"
                js_file.write_text(js_txt, encoding="utf-8")
                modified.append(str(js_file))

        # 3) HTML 파일 패치 (ADMN-BRD-002 모달 직접 보강 + 과세/면세 교정)
        for html_file in sorted(folder.glob("*.html")):
            orig = html_file.read_text(encoding="utf-8")
            txt = orig

            for old, new in COMMON_TAX_REPLACEMENTS:
                txt = txt.replace(old, new)

            if "ADMN-ORD-001" in html_file.name:
                txt = patch_ord_001_tax(txt)

            if "ADMN-PROD-003" in html_file.name or "ADMN-PROD-005" in html_file.name:
                txt = re.sub(
                    r"과세\s*\$\{([^}]+)\}\s*원\s*\+\s*면세\s*\$\{([^}]+)\}\s*원\s*자동\s*분리",
                    r"교육면세 ${\1}원 + 도서면세 ${\2}원 자동 분리",
                    txt
                )

            # ADMN-BRD-002에 인라인으로도 모달 클로저 보장
            if "ADMN-BRD-002" in html_file.name and "[UNIVERSAL-MODAL-CLOSER-HOTFIX]" not in txt:
                txt = txt.replace("</body>", f"<script>{UNIVERSAL_MODAL_CLOSER_JS}</script>\n</body>")

            if txt != orig:
                html_file.write_text(txt, encoding="utf-8")
                modified.append(str(html_file))

    print(f"[패치 완료] 총 {len(modified)}개 파일 업데이트됨:")
    for f in modified:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
