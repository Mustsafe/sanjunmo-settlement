# 업무플로우 마크업 기초 추출

> update_plan_v1_1_and_extract_markup_base.py 자동 생성 · 읽기 전용

## 1. common-v84.css

경로: prototype_clean\common-v84.css

### CSS 변수

- `--navy-950: #0B1120`
- `--navy-900: #0F172A`
- `--navy-800: #1E293B`
- `--navy-700: #334155`
- `--slate-600: #475569`
- `--slate-500: #64748B`
- `--slate-400: #94A3B8`
- `--slate-300: #CBD5E1`
- `--slate-200: #E2E8F0`
- `--slate-100: #F1F5F9`
- `--slate-50: #F8FAFC`
- `--white: #FFFFFF`
- `--primary: #2563EB`
- `--primary-hover: #1D4ED8`
- `--primary-soft: #EFF6FF`
- `--primary-light: #EFF6FF`
- `--primary-border: #BFDBFE`
- `--emerald: #059669`
- `--emerald-soft: #ECFDF5`
- `--emerald-border: #A7F3D0`
- `--amber: #D97706`
- `--amber-soft: #FFFBEB`
- `--amber-border: #FDE68A`
- `--rose: #E11D48`
- `--rose-soft: #FFF1F2`
- `--rose-border: #FECDD3`
- `--violet: #7C3AED`
- `--violet-soft: #F5F3FF`
- `--violet-border: #DDD6FE`
- `--snb-width: 260px`
- `--topbar-height: 60px`
- `--font: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--mono: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--font-sans: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--font-mono: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--font: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--mono: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--font-sans: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`
- `--font-mono: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSy`

### 클래스 (91개)

active, app-layout, app-shell, badge, book-pipeline-stepper, btn, chip, code, code-badge, code-pill, code-tag, content, crumb-code, crumb-group, crumb-sep, crumb-title, current-screen, field-hint, footer-bar, force-closed, help-txt, info-callout, k-num, k-sub, k-title, kpi-card, kpi-grid, layout, legacy-top-banner, main, main-container, modal-backdrop, mono, nav-code, neg, num, open, p1-modal-backdrop, page-container, page-top-banner, partner-isolated-mode, policy-banner, policy-note, pos, role-sim-box, routing-architecture-card, rule-banner, s1-modal-backdrop, s2-modal-backdrop, savebar, screen-id-badge, screen-id-pill, select, show, sidebar, snb, snb-brand, snb-brand-dot, snb-brand-logo, snb-brand-sub, snb-brand-title, snb-brand-top, snb-code, snb-footer, snb-group, snb-group-title, snb-item, snb-item-list, snb-label, snb-link, snb-scroll-area, snb-version-pill, step-banner-grid, step-desc, step-light, step-node, step-node-top, step-num, subview-btn, subview-switcher, subview-tab, top-bar, top-bar-left, top-bar-right, topbar, topbar-left, topbar-title, v4-gen3-topbar, v4-master-snb, wb-header, wireframe-banner

## 2. 현재 페이지 <head>

### 외부 에셋
- <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
- <link id="v4-common-css" rel="stylesheet" href="common-v84.css">
- <script id="v4-common-snb" src="common-snb.js" defer>

### 인라인 스타일 클래스 (49개)

b-bad, b-dark, b-gray, b-ok, b-pri, b-pur, b-teal, b-warn, badge, btn, btn-pri, btn-sm, code, code-badge, code-pill, code-tag, content, crumb-code, engine-grid, engine-group, engine-step, flow-arrow, flow-node, flow-track, hero, k-num, layout, main, mono, nav-code, num, screen-card, screen-code, screen-go, screen-id-badge, screen-name, screen-role, screen-rules, screen-top, section-bd, section-card, section-hd, snb-code, stage-col, stage-col-hd, stage-desc, stage-grid, stage-num, stage-title

### 인라인 스타일 변수 (33개)

--bg, --card, --ink, --muted, --sub, --line, --line-strong, --pri, --pri-soft, --ok, --ok-soft, --ok-line, --warn, --warn-soft, --warn-line, --bad, --bad-soft, --bad-line, --purple, --purple-soft, --teal, --teal-soft, --snb-bg, --snb-ink, --snb-active, --shadow, --radius, --font, --mono, --font, --mono, --font-sans, --font-mono

## 3. 현재 페이지 body 뼈대 (depth 6)

```
  body
    aside#v4-master-snb
    div#v4-root-shell
      header#v4-gen3-topbar.top-bar.v4-gen3-topbar
        div.top-bar-left
          span.crumb-group
          span.crumb-sep
          span#header-screen-code.crumb-code
          h1#header-screen-title.crumb-title
        div#v4-topbar-right-slot.top-bar-right
          span
      div#v4-page-body
        main.main
          section#set1-4-e2e-workflows.section
            div.sec-head
            div
          section.hero
            div  ×2
          div.content
            div.section-card  ×5
```

## 4. 참고 화면 ADMN-SETT-002 <head> 에셋

- <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
- <link id="v4-common-css" rel="stylesheet" href="common-v84.css">
- <script id="v4-common-snb" src="common-snb.js" defer>

## 5. 참고 화면 ADMN-SETT-002 body 뼈대 (depth 5)

```
  body
    aside#v4-master-snb
    div#v4-root-shell
      header#v4-gen3-topbar.top-bar.v4-gen3-topbar
        div.top-bar-left
          span.crumb-group
          span.crumb-sep
          span#header-screen-code.crumb-code
          h1#header-screen-title.crumb-title
        div#v4-topbar-right-slot.top-bar-right
          select#monthSelect.select
          button#btnRunEngine.btn
          button#btnOpenStatementS1.btn.btn-primary  [onclick=openStatementModalS1(getSelectedPayeeKey())]
          button#btnOpenStatementS2.btn  [onclick=openStatementModalS2(getSelectedPayeeKey())]
          button#btnOpenCarryModal.btn
          button#btnLockSettlement.btn.btn-primary
      div#v4-page-body
        div.app-layout
          div.main
        div#modal-sett-gate.modal-backdrop.hidden
          div.modal-card
        div#toastContainer.toast-container
    div#modalCarryoverP1.p1-modal-backdrop  [onclick=if(event.target===this) closeCarryoverModalP1()]
      div.p1-modal-dialog
        div.p1-modal-header
          div  ×2
        div.p1-modal-body
          div
          div.p1-eq-grid
          div
        div.p1-modal-footer
          div  ×2
    div#modalStatementS1.s1-modal-backdrop  [onclick=if(event.target===this) closeStatementModalS1()]
      div.s1-modal-dialog
        div.s1-modal-header
          div  ×2
        div.s1-modal-body
          div.s1-card  ×2
          div#s1DynamicTablesContainer
          div.s1-card
          div
        div.s1-modal-footer
          div  ×2
    div#modalStatementS2.s2-modal-backdrop  [onclick=if(event.target===this && !window.isPartnerIsolate]
      div.s2-modal-dialog
        div.s2-modal-header
          div  ×2
        div.s2-modal-body
          div#s2PrintableSheet.s2-paper-sheet
        div.s2-modal-footer
          div  ×2
```

## 6. 현재 페이지 인라인 스크립트

### script 1 (84자)
```js
function goScreen(filename) {
            window.location.href = filename;
        }
```

### script 2 (2,828자)
```js
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
      onclickAttr.indexOf('Close') !==
... (생략)
```
