/**
 * SANJUNMO BACKOFFICE v8.4 FINAL — MASTER SNB INJECTOR (common-snb.js)
 */
(function () {
  const SNB_GROUPS = [
    {
      title: "0단계 · 전체 업무 플로우 안내",
      items: [
        { code: "GUIDE", label: "전체 업무 플로우 가이드", href: "00_WORKFLOW_GUIDE_baseline.html", screenCode: "WORKFLOW-GUIDE" }
      ]
    },
    {
      title: "주문 · 배송 · 환불 · CS 관리 (ORD/RFD/BRD)",
      items: [
        { code: "ORD-001", label: "주문 · 배송 · 3PL 관리", href: "ADMN-ORD-001_baseline.html" },
        { code: "RFD-002", label: "환불 요청 · 심사 관리", href: "ADMN-RFD-002_baseline.html" },
        { code: "BRD-002", label: "1:1 문의 관리 (문의 분기 허브)", href: "ADMN-BRD-002_baseline.html", screenCode: "ADMN-BRD-002" },
        { code: "MKT-001", label: "쿠폰 · 포인트 혜택 관리", href: "ADMN-MKT-001_baseline.html", screenCode: "ADMN-MKT-001" }
      ]
    },
    {
      title: "상품 · 강좌 · 교재 관리 (PROD)",
      items: [
        { code: "PROD-001", label: "카테고리 관리", href: "ADMN-PROD-001_baseline.html", screenCode: "ADMN-PROD-001" },
        { code: "PROD-002", label: "강의 관리 (영상 단품)", href: "ADMN-PROD-002_baseline.html", screenCode: "ADMN-PROD-002" },
        { code: "PROD-003", label: "단과 강좌 관리", href: "ADMN-PROD-003_baseline.html", screenCode: "ADMN-PROD-003" },
        { code: "PROD-004", label: "교재 관리", href: "ADMN-PROD-004_baseline.html", screenCode: "ADMN-PROD-004" },
        { code: "PROD-005", label: "패키지 · 환급반 상품 관리", href: "ADMN-PROD-005_baseline.html", screenCode: "ADMN-PROD-005" },
        { code: "PROD-006", label: "강사 노출 정보 관리", href: "ADMN-PROD-006_baseline.html", screenCode: "ADMN-PROD-006" },
        { code: "PROD-007", label: "일반상품 관리", href: "ADMN-PROD-007_baseline.html", screenCode: "ADMN-PROD-007" }
      ]
    },
    {
      title: "1단계 · 계약 · 상품 · 매핑 설정",
      items: [
        { code: "INST-001", label: "권리자 계약 원장", href: "ADMN-INST-001_baseline.html", screenCode: "ADMN-INST-001" },
        { code: "SETT-007", label: "수취인 분할 관리", href: "ADMN-SETT-007_baseline.html", screenCode: "ADMN-SETT-007" },
        { code: "BOOK-001", label: "도서 공급 원장", href: "ADMN-BOOK-001_baseline.html", screenCode: "ADMN-BOOK-001" },
        { code: "SETT-001", label: "상품별 권리자 매핑", href: "ADMN-SETT-001_baseline.html", screenCode: "ADMN-SETT-001" }
      ]
    },
    {
      title: "2단계 · 월마감 전 검증 (Gate)",
      items: [
        { code: "SETT-004", label: "PG 정산 원장 대사", href: "ADMN-SETT-004_baseline.html", screenCode: "ADMN-SETT-004" },
        { code: "INST-002", label: "약정금 마일스톤 검수", href: "ADMN-INST-002_baseline.html", screenCode: "ADMN-INST-002" },
        { code: "SETT-006", label: "합격 환급반 관리", href: "ADMN-SETT-006_baseline.html", screenCode: "ADMN-SETT-006" },
        { code: "SETT-008", label: "사업자등록 확인 이력", href: "ADMN-SETT-008_baseline.html", screenCode: "ADMN-SETT-008" }
      ]
    },
    {
      title: "3단계 · 월간 정산 · 집행 · 조회",
      items: [
        { code: "SETT-002", label: "월간 정산 및 집행", href: "ADMN-SETT-002_baseline.html", screenCode: "ADMN-SETT-002" },
        { code: "SETT-005", label: "정산 수동 조정", href: "ADMN-SETT-005_baseline.html", screenCode: "ADMN-SETT-005" },
        { code: "SETT-009", label: "내부 정산 조회 - 조회 전용", href: "ADMN-SETT-009_baseline.html", screenCode: "ADMN-SETT-009" }
      ]
    },
    {
      title: "4단계 · 보안 및 감사 통제",
      items: [
        { code: "USER-007", label: "민감 정보 열람 통제", href: "ADMN-USER-007_baseline.html", screenCode: "ADMN-USER-007" },
        { code: "CONF-010", label: "정산 감사 로그", href: "ADMN-CONF-010_baseline.html", screenCode: "ADMN-CONF-010" }
      ]
    }
  ];

  function buildSnbHtml(currentFile) {
    const groupsHtml = SNB_GROUPS.map(group => {
      const itemsHtml = group.items.map(item => {
        const isActive = currentFile === item.href || currentFile.indexOf(item.screenCode) !== -1;
        return `
        <a href="${item.href}" class="snb-item${isActive ? ' active' : ''}" data-screen-code="${item.screenCode}">
          <span class="snb-code">${item.code}</span>
          <span class="snb-label">${item.label}</span>
        </a>`;
      }).join("");
      return `
      <div class="snb-group">
        <div class="snb-group-title">${group.title}</div>
        <div class="snb-item-list">${itemsHtml}</div>
      </div>`;
    }).join("");

    return `
    <div class="snb-brand" onclick="window.location.href='00_WORKFLOW_GUIDE_baseline.html'">
      <div class="snb-brand-top">
        <div class="snb-brand-title">
          <img class="snb-brand-logo" src="img/sjm_logo-horizontal-white.png" alt="산준모">
          <span>백오피스</span>
        </div>
        <span class="snb-version-pill">v4.0.0</span>
      </div>
      <div class="snb-brand-sub">상품 · 권리자 · 정산 통합 어드민</div>
    </div>
    <div class="snb-scroll-area">${groupsHtml}</div>
    <div class="snb-footer">
      <span>PROD &amp; SETTLEMENT</span>
      <span>SSOT Verified</span>
    </div>`;
  }

  function initMasterSnb() {
    const pathParts = window.location.pathname.replace(/\\/g, "/").split("/");
    const currentFile = decodeURIComponent(pathParts[pathParts.length - 1] || "");

    let snbEl = document.getElementById("v4-master-snb");
    if (!snbEl) {
      snbEl = document.createElement("aside");
      snbEl.id = "v4-master-snb";
      snbEl.setAttribute("role", "navigation");
      snbEl.setAttribute("aria-label", "산준모 마스터 사이드바");
      document.body.insertBefore(snbEl, document.body.firstChild);
    }
    snbEl.innerHTML = buildSnbHtml(currentFile);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMasterSnb);
  } else {
    initMasterSnb();
  }
})();
