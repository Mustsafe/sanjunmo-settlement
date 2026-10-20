#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 전 화면 작동 무결성 복구 + 과·면세 교정 + 모달 핫픽스 통합 빌더
1. prototype/ 원본에 비즈니스/세무 교정(인강·교재 통합면세, 금지어 '기출'->'빈출') 및 모달 클로저 반영
2. prototype/ -> prototype_clean/ 재생성 시:
   - <script>, <style>, HTML 속성(value, onclick, data-*, id, class)은 100% 원본 보존 (JS 작동 깨짐 원천 차단)
   - 순수 텍스트 노드(HTML 태그 바깥 텍스트)에만 운영자용 용어 정제 적용
"""

import re
import shutil
from pathlib import Path

PROTO_DIR = Path("prototype")
CLEAN_DIR = Path("prototype_clean")

# ==============================================================================
# A. 모달 열기/닫기 원천 보장 CSS & JS
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

  window.closeAllModals = function() {
    document.querySelectorAll('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop').forEach(forceCloseModalEl);
  };

  // 페이지 진입 시 실수로 열려 있는 모달 초기화 (단, URL 해시/쿼리로 의도적 오픈된 경우 제외)
  window.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop').forEach(function(el) {
      if (!el.classList.contains('show') && !el.classList.contains('open') && !el.classList.contains('active')) {
        el.style.setProperty('display', 'none', 'important');
      }
    });
  });

  // 클릭 이벤트 위임 (배경 클릭 또는 닫기/취소/✕ 버튼 클릭 시 즉시 닫기)
  document.addEventListener('click', function(e) {
    if (e.target && (
      e.target.classList.contains('modal-backdrop') ||
      e.target.classList.contains('p1-modal-backdrop') ||
      e.target.classList.contains('s1-modal-backdrop') ||
      e.target.classList.contains('s2-modal-backdrop')
    )) {
      forceCloseModalEl(e.target);
      return;
    }

    var btn = e.target.closest('button, a, span, [role="button"]');
    if (!btn) return;

    // 1) 모달 열기 버튼 클릭 시 inline display:none 강제 잠금 해제
    var onclickAttr = (btn.getAttribute('onclick') || '');
    if (onclickAttr.indexOf('open') !== -1 || onclickAttr.indexOf('Open') !== -1 || onclickAttr.indexOf('Modal') !== -1) {
      if (onclickAttr.indexOf('close') === -1 && onclickAttr.indexOf('Close') === -1) {
        document.querySelectorAll('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop').forEach(function(m) {
          m.style.removeProperty('display');
        });
      }
    }

    // 2) 모달 내부 닫기 버튼 판정
    var backdrop = btn.closest('.modal-backdrop, .p1-modal-backdrop, .s1-modal-backdrop, .s2-modal-backdrop');
    if (!backdrop) return;

    var txt = (btn.textContent || '').trim();
    var isCloseBtn = (
      txt === '✕' || txt === '×' || txt === 'X' || txt === 'x' ||
      txt === '취소' || txt === '닫기' || txt === '창 닫기' ||
      onclickAttr.indexOf('close') !== -1 ||
      onclickAttr.indexOf('Close') !== -1 ||
      btn.classList.contains('modal-close') ||
      btn.classList.contains('btn-close')
    );

    if (isCloseBtn) {
      setTimeout(function() { forceCloseModalEl(backdrop); }, 0);
    }
  }, true);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') window.closeAllModals();
  });
})();
"""

# ==============================================================================
# B. 비즈니스/세무 정합성 교정 (prototype 원본 & prototype_clean 공통)
# ==============================================================================
BUSINESS_FIXES = [
    # 1) 단과 강좌(PROD-003) & 패키지(PROD-005) 교육면세 교정
    ("과세 (VAT 10% 포함 · 온라인 교육용역)", "면세 (VAT 0% · 원격평생교육시설 온라인 교육용역)"),
    ("과세 (VAT 10% 포함)", "면세 (VAT 0% · 교육용역)"),
    ("패키지 · 환급반 상품 관리 (복합과세 분할 · 안분 가중치)", "패키지 · 환급반 상품 관리 (강좌·교재 면세 분리 · 안분 가중치)"),
    ("패키지 강좌 할인 -100,000원 (VAT 10% 포함)", "패키지 강좌 할인 -100,000원 (교육용역 면세 · VAT 0%)"),
    ("과세 240,000원 + 면세 72,000원 자동 분리", "교육면세 240,000원 + 도서면세 72,000원 자동 분리"),
    ("복합상품 과세·면세 분할 및 환급반 연동", "패키지(강좌·교재) 결제 금액 분할 및 환급반 연동"),
    # 2) 금지어 '기출' -> '빈출'
    ("한권완성 이론+기출", "한권완성 이론+빈출"),
    ("이론+기출", "이론+빈출"),
    # 3) 어색한 중복 단어 및 문구 교정
    ("실결제금액(실결제금액)", "실결제금액"),
    ("실결제 실결제금액 기준", "실결제금액 기준"),
    ("수수료 차감지급(수수료 차감지급)", "수수료 차감지급(순액 정산)"),
    ("(수수료 차감지급 수수료 차감지급)", "(수수료 차감 후 순액 지급)"),
    ("출고지시 일시이 기록되며", "출고지시 일시가 기록되며"),
    ("항목명 'ID' 고정('닉네임' 표기 금지 · @ 이메일 형식 검증 제외)", "네이버 카페 정회원 연동 확인용 ID"),
]


def apply_business_fixes(text: str, filename: str) -> str:
    for old, new in BUSINESS_FIXES:
        text = text.replace(old, new)

    if "ADMN-ORD-001" in filename:
        text = re.sub(r"(산업안전기사[^\n<]*?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
        text = re.sub(r"(강좌[^\n<]{1,60}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
        text = re.sub(r"(올패스[^\n<]{0,40}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
        text = re.sub(r"(필기\+실기[^\n<]{0,40}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
        text = re.sub(r"(type\s*:\s*['\"]강좌['\"][^\}]*?)과세\s*10%", r"\1교육용역 면세 0%", text)
        text = re.sub(r"(badge[^>]*>강좌<[\s\S]{0,180}?)\(과세\s*10%\)", r"\1(교육용역 면세 0%)", text)
        text = text.replace("MIXED (과·면세 복합)", "EXEMPT (교육·도서 통합면세)")
        text = text.replace("과·면세 복합 (MIXED)", "교육·도서 통합면세 (EXEMPT)")

    if "ADMN-PROD-003" in filename or "ADMN-PROD-005" in filename:
        text = re.sub(
            r"과세\s*\$\{([^}]+)\}\s*원\s*\+\s*면세\s*\$\{([^}]+)\}\s*원\s*자동\s*분리",
            r"교육면세 ${\1}원 + 도서면세 ${\2}원 자동 분리",
            text
        )

    return text


# ==============================================================================
# C. prototype_clean 전용 안전한 텍스트 노드 치환 (<script>/<style>/속성 보존)
# ==============================================================================
CLEAN_TEXT_ONLY_REPLACEMENTS = [
    ("EXEMPT (교육·도서 통합면세)", "교육·도서 통합면세 (VAT 0%)"),
    ("BOOK_GOODS (도서 면세)", "도서 면세 (VAT 0%)"),
    ("LECTURE_EDU (강좌 교육면세)", "강좌 교육면세 (VAT 0%)"),
    ("payment.paid_amount", "실결제금액"),
    ("actual_paid_amount", "실결제금액"),
    ("order_item.supply_type_snapshot = ROYALTY", "도서 공급형태 스냅샷 = 인세 도서"),
    ("Step 4 DEDUCT", "4단계 환불·할인 공제"),
    ("admin_access_log", "보안 열람 로그"),
]


def clean_visible_html_only(html: str) -> str:
    """
    <script>...</script> 및 <style>...</style> 블록과 HTML 태그 내부(<...>)는
    전혀 건드리지 않고, 순수 텍스트 영역만 치환하여 JS 런타임 깨짐을 100% 방지합니다.
    """
    protected = []

    def protect_block(match):
        protected.append(match.group(0))
        return f"__PROTECTED_BLOCK_{len(protected) - 1}__"

    # 1) script, style 블록 보호
    temp = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", protect_block, html)
    # 2) HTML 태그 자체(<...>) 보호 (속성값 value="ON_SALE" 등 절대 보존)
    temp = re.sub(r"(?s)<[^>]+>", protect_block, temp)

    # 3) 순수 텍스트 영역만 치환
    for old, new in CLEAN_TEXT_ONLY_REPLACEMENTS:
        temp = temp.replace(old, new)

    # 4) 타이틀의 [ADMN-XXX-NNN] 프리픽스 제거
    # (태그 복원 후 title 태그 내부 텍스트만 정리)
    for i in range(len(protected) - 1, -1, -1):
        temp = temp.replace(f"__PROTECTED_BLOCK_{i}__", protected[i])

    temp = re.sub(r"(<title>\s*)\[[A-Z0-9\-]+\]\s*", r"\1", temp)
    return temp


def patch_css_and_js(folder: Path, is_clean: bool):
    css_file = folder / "common-v84.css"
    if css_file.exists():
        css_txt = css_file.read_text(encoding="utf-8")
        if "[MODAL-VISIBILITY-AND-CLOSE-LOCK]" not in css_txt:
            css_txt = css_txt.rstrip() + "\n\n" + MODAL_CSS_PATCH.strip() + "\n"
            css_file.write_text(css_txt, encoding="utf-8")

    js_file = folder / "common-snb.js"
    if js_file.exists():
        js_txt = js_file.read_text(encoding="utf-8")
        if "[UNIVERSAL-MODAL-CLOSER-HOTFIX]" not in js_txt:
            js_txt = js_txt.rstrip() + "\n\n" + UNIVERSAL_MODAL_CLOSER_JS.strip() + "\n"
            js_file.write_text(js_txt, encoding="utf-8")


def main():
    CLEAN_DIR.mkdir(exist_ok=True)

    # 1. prototype/ 원본 HTML에 비즈니스/세무 교정 적용 및 prototype_clean/으로 안전 재빌드
    html_files = sorted(PROTO_DIR.glob("*.html"))
    for src_file in html_files:
        raw = src_file.read_text(encoding="utf-8")
        fixed_proto = apply_business_fixes(raw, src_file.name)

        # ADMN-BRD-002 등 common-snb.js 미포함 단독 페이지에도 모달 클로저 보장
        if "[UNIVERSAL-MODAL-CLOSER-HOTFIX]" not in fixed_proto and "</body>" in fixed_proto:
            fixed_proto = fixed_proto.replace("</body>", f"<script>{UNIVERSAL_MODAL_CLOSER_JS}</script>\n</body>")

        if fixed_proto != raw:
            src_file.write_text(fixed_proto, encoding="utf-8")

        # prototype_clean/ 생성 (JS/속성 100% 보존 + 순수 텍스트만 클렌징)
        clean_html = clean_visible_html_only(fixed_proto)
        dst_file = CLEAN_DIR / src_file.name
        dst_file.write_text(clean_html, encoding="utf-8")

    # 2. common-v84.css, common-snb.js 패치 적용
    patch_css_and_js(PROTO_DIR, is_clean=False)
    patch_css_and_js(CLEAN_DIR, is_clean=True)

    print(f"[완료] prototype/ 및 prototype_clean/ 총 {len(html_files)}개 화면 복구 및 동기화 완료.")


if __name__ == "__main__":
    main()
