/**
 * SANJUNMO BACKOFFICE v8.4 FINAL — MASTER SNB INJECTOR (common-snb.js)
 */
(function () {
  const SNB_GROUPS = [
    {
      title: "대시보드 · 통계",
      items: [
        { code: "GUIDE", label: "전체 업무 플로우 가이드", href: "00_WORKFLOW_GUIDE_baseline.html", screenCode: "WORKFLOW-GUIDE" },
        { code: "DASH-001", label: "통합 대시보드 홈 (현황·큐·연동)", href: "ADMN-DASH-001_baseline.html?view=dash", screenCode: "ADMN-DASH-001" },
        { code: "STAT-001", label: "매출 · 상품 통계 (결제·환불·순위)", href: "ADMN-DASH-001_baseline.html?view=stat-sales", screenCode: "ADMN-STAT-001" },
        { code: "LOGIN-001", label: "관리자 · 파트너 로그인 게이트", href: "ADMN-LOGIN-001_baseline.html", screenCode: "ADMN-LOGIN-001" }
      ]
    },
    {
      title: "회원 · 수강 관리",
      items: [
        { code: "USER-001", label: "일반 회원 관리 (목록·상세)", href: "ADMN-USER-001_baseline.html?view=list", screenCode: "ADMN-USER-001" },
        { code: "USER-003", label: "회원 수강 · 기간 · 기기 제어", href: "ADMN-USER-001_baseline.html?view=course", screenCode: "ADMN-USER-003" },
        { code: "USER-006", label: "회원 그룹 · 다중 태그 관리", href: "ADMN-USER-001_baseline.html?view=tags", screenCode: "ADMN-USER-006" },
        { code: "USER-005", label: "블랙리스트 · 부정사용 제재 관리", href: "ADMN-USER-001_baseline.html?view=blacklist", screenCode: "ADMN-USER-005" },
        { code: "USER-007", label: "민감 정보 열람 · 파기 통제", href: "ADMN-USER-007_baseline.html", screenCode: "ADMN-USER-007" }
      ]
    },
    {
      title: "주문 · 환불 · CS · 프로모션",
      items: [
        { code: "ORD-001", label: "주문 · 배송 · 3PL 관리", href: "ADMN-ORD-001_baseline.html" },
        { code: "RFD-002", label: "환불 요청 · 심사 관리", href: "ADMN-RFD-002_baseline.html" },
        { code: "BRD-002", label: "1:1 문의 관리 (문의 분기 허브)", href: "ADMN-BRD-002_baseline.html", screenCode: "ADMN-BRD-002" },
        { code: "BRD-001", label: "공지사항 · FAQ · 당첨자 발표", href: "ADMN-BRD-001_baseline.html?view=notice", screenCode: "ADMN-BRD-001" },
        { code: "BRD-005", label: "수강·합격수기 · 무료특강(빈출)·정답지", href: "ADMN-BRD-005_baseline.html?view=review", screenCode: "ADMN-BRD-005" },
        { code: "PROM-001", label: "이벤트 · 기획전 관리 (Slug·특가)", href: "ADMN-PROM-001_baseline.html", screenCode: "ADMN-PROM-001" },
        { code: "PROM-002", label: "쿠폰 마스터 등록 · 발급 관리", href: "ADMN-PROM-002_baseline.html?view=list", screenCode: "ADMN-PROM-002" },
        { code: "PROM-003", label: "포인트 적립 정책 및 원장 관리", href: "ADMN-PROM-002_baseline.html?view=point", screenCode: "ADMN-PROM-003" }
      ]
    },
    {
      title: "상품 · 강좌 · 교재 관리",
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
      title: "권리자 계약 · 지분 매핑",
      items: [
        { code: "INST-001", label: "권리자 계약 원장", href: "ADMN-INST-001_baseline.html", screenCode: "ADMN-INST-001" },
        { code: "SETT-007", label: "수취인 분할 관리", href: "ADMN-SETT-007_baseline.html", screenCode: "ADMN-SETT-007" },
        { code: "BOOK-001", label: "도서 공급 원장", href: "ADMN-BOOK-001_baseline.html", screenCode: "ADMN-BOOK-001" },
        { code: "SETT-001", label: "상품별 권리자 매핑", href: "ADMN-SETT-001_baseline.html", screenCode: "ADMN-SETT-001" }
      ]
    },
    {
      title: "정산 마감 전 사전 대사",
      items: [
        { code: "SETT-004", label: "PG 정산 원장 대사", href: "ADMN-SETT-004_baseline.html", screenCode: "ADMN-SETT-004" },
        { code: "INST-002", label: "약정금 마일스톤 검수", href: "ADMN-INST-002_baseline.html", screenCode: "ADMN-INST-002" },
        { code: "SETT-006", label: "합격 환급반 관리", href: "ADMN-SETT-006_baseline.html", screenCode: "ADMN-SETT-006" },
        { code: "SETT-008", label: "사업자등록 확인 이력", href: "ADMN-SETT-008_baseline.html", screenCode: "ADMN-SETT-008" }
      ]
    },
    {
      title: "월간 정산 · 지급 · 조회",
      items: [
        { code: "SETT-002", label: "월간 정산 및 집행", href: "ADMN-SETT-002_baseline.html", screenCode: "ADMN-SETT-002" },
        { code: "SETT-005", label: "정산 수동 조정", href: "ADMN-SETT-005_baseline.html", screenCode: "ADMN-SETT-005" },
        { code: "SETT-009", label: "내부 정산 조회 - 조회 전용", href: "ADMN-SETT-009_baseline.html", screenCode: "ADMN-SETT-009" },
        { code: "SETT-010", label: "원천세 · 지급명세서 신고 산출물", href: "ADMN-SETT-009_baseline.html?view=tax-report", screenCode: "ADMN-SETT-010" },
        { code: "SETT-011", label: "택배 대리점 운임 · 배송비 대사", href: "ADMN-SETT-011_baseline.html", screenCode: "ADMN-SETT-011" }
      ]
    },
    {
      title: "개인정보 · 보안 감사",
      items: [
        { code: "USER-007", label: "민감 정보 열람 통제", href: "ADMN-USER-007_baseline.html", screenCode: "ADMN-USER-007" },
        { code: "CONF-010", label: "정산 감사 로그", href: "ADMN-CONF-010_baseline.html", screenCode: "ADMN-CONF-010" },
        { code: "CONF-006", label: "운영 · 보안 통합 감사 로그", href: "ADMN-CONF-005_baseline.html?view=ADMN-CONF-006", screenCode: "ADMN-CONF-006" }
      ]
    },
    {
      title: "사이트 · 약관 · 메시지 설정",
      items: [
        { code: "CONF-001", label: "전시 배너 · 띠배너 · 팝업 관리", href: "ADMN-CONF-001_baseline.html?view=banner", screenCode: "ADMN-CONF-001" },
        { code: "CONF-002", label: "약관 · 개인정보처리방침 관리", href: "ADMN-CONF-002_baseline.html", screenCode: "ADMN-CONF-002" },
        { code: "CONF-003", label: "플레이어 · 동시접속 · 인증 설정", href: "ADMN-CONF-003_baseline.html?view=player", screenCode: "ADMN-CONF-003" },
        { code: "CONF-004", label: "메시지 템플릿 관리 (알림톡·문자·메일)", href: "ADMN-CONF-004_baseline.html?view=template", screenCode: "ADMN-CONF-004" },
        { code: "CONF-004-S1", label: "타겟 메시지 발송 · 내역 (알림톡·문자·메일)", href: "ADMN-CONF-004_baseline.html?view=send", screenCode: "ADMN-CONF-004-S1" },
        { code: "CONF-005", label: "운영자 계정 · 역할 권한(RBAC)", href: "ADMN-CONF-005_baseline.html", screenCode: "ADMN-CONF-005" }
      ]
    }
  ];

  function buildSnbHtml(currentFileWithQuery, currentFileOnly) {
    const groupsHtml = SNB_GROUPS.map(group => {
      const itemsHtml = group.items.map(item => {
        // 1순위: 파일명 + 쿼리스트링 완전 일치 (?view=course 등)
        // 2순위: 쿼리가 없는 일반 페이지의 경우 파일명 일치
        // 3순위: screenCode 부분 일치
        let isActive = false;
        if (item.href.indexOf("?") !== -1) {
          isActive = (currentFileWithQuery === item.href);
          // 쿼리 없이 들어온 경우 list 기본 매칭
          if (!isActive && currentFileWithQuery === item.href.split("?")[0] && item.href.indexOf("view=list") !== -1) {
            isActive = true;
          }
        } else {
          isActive = (currentFileOnly === item.href || (currentFileOnly && currentFileOnly.indexOf(item.screenCode) !== -1));
        }

        return `
        <a href="${item.href}" class="snb-item${isActive ? ' active' : ''}" data-screen-code="${item.screenCode}">
          <span class="snb-code">${item.code}</span>
          <span class="snb-label">${item.label}</span>
        </a>`;
      }).join("");
      return `
      <div class="snb-group">
        <div class="snb-group-title">${group.title || group.groupTitle}</div>
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
      <div class="snb-brand-sub">산준모닷컴 통합 관리자 센터</div>
    </div>
    <div class="snb-scroll-area">${groupsHtml}</div>
    <div class="snb-footer">
      <span>PROD &amp; SETTLEMENT</span>
      <span>SSOT Verified</span>
    </div>`;
  }

  function initMasterSnb() {
    const pathParts = window.location.pathname.replace(/\\/g, "/").split("/");
    const currentFileOnly = decodeURIComponent(pathParts[pathParts.length - 1] || "");
    const currentFileWithQuery = currentFileOnly + window.location.search;

    let snbEl = document.getElementById("v4-master-snb");
    if (!snbEl) {
      snbEl = document.createElement("aside");
      snbEl.id = "v4-master-snb";
      snbEl.setAttribute("role", "navigation");
      snbEl.setAttribute("aria-label", "산준모 마스터 사이드바");
      document.body.insertBefore(snbEl, document.body.firstChild);
    }
    snbEl.innerHTML = buildSnbHtml(currentFileWithQuery, currentFileOnly);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMasterSnb);
  } else {
    initMasterSnb();
  }
})();


/* === [PROTOTYPE-CLEAN: RUNTIME TEXT SANITIZER] === */
(function () {
  const PATTERNS = [
    // [ADMN-XXX-000] 또는 (ADMN-XXX-000-P1 · ...) 형태 제거
    /\[\s*ADMN-[A-Z]+-\d+(?:-[A-Z0-9]+)?[^\]]*\]\s*/g,
    /\(\s*ADMN-[A-Z]+-\d+(?:-[A-Z0-9]+)?[^)]*\)/g,
    // (001-P1), (002-P1), (003-S1), (S1), (S2), (P1), (P2) 등 화면설계서 서브코드 꼬리표 제거
    /\s*\(\s*(?:\d{3}-[SP]\d+|[SP]\d+)\s*\)/g,
    // [테이블 A] ~ [테이블 G], [8.3절 SSOT] 등 기획서 마커 제거
    /\[\s*테이블\s*[A-G]\s*\]\s*/g,
    /\[\s*\d+(?:\.\d+)?절[^\]]*\]\s*/g,
    // (6.5절 · 8.3절), (제15장 15.2절), (합의서 제18장 18.1절), (4.3절) 등 장/절 참조 괄호 제거
    /\s*\(\s*(?:합의서\s*)?(?:제?\d+장\s*)?\d+(?:\.\d+)?절[^)]*\)/g,
    /\s*·\s*\d+(?:\.\d+)?절/g,
    // (Pipeline 1.1) 등 괄호형 파이프라인 코드 제거
    /\s*\(\s*Pipeline\s*\d+\.\d+[^)]*\)/gi,
    // DB 컬럼명 괄호 표기 제거: (member_status), (users.is_marketing_agreed...), (goods_stock_log) 등
    /\s*\(\s*[a-z]+_[a-z0-9_]+\s*\)/g,
    /\s*\(\s*(?:Case\s*\d+[^)]*|부록\s*[A-Z][^)]*|QA\s*D-\d+[^)]*)\)/gi,
    /\[\s*(?:제?\d+장|\d+\.\d+절|부록)[^\]]*\]\s*/g
  ];

  function cleanString(str) {
    if (!str || typeof str !== "string") return str;
    let out = str;
    for (let i = 0; i < PATTERNS.length; i++) {
      out = out.replace(PATTERNS[i], "");
    }
    return out.replace(/\s{2,}/g, " ");
  }

  function cleanTextNodes(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) {
      const parentTag = n.parentNode && n.parentNode.tagName;
      if (parentTag === "SCRIPT" || parentTag === "STYLE" || parentTag === "TEXTAREA") continue;
      nodes.push(n);
    }
    for (let i = 0; i < nodes.length; i++) {
      const orig = nodes[i].nodeValue;
      const cleaned = cleanString(orig);
      if (cleaned !== orig) {
        nodes[i].nodeValue = cleaned;
      }
    }
    // option 텍스트 및 문서 타이틀 정리
    if (document.title) {
      const ct = cleanString(document.title);
      if (ct !== document.title) document.title = ct;
    }
  }

  function initCleaner() {
    cleanTextNodes(document.body);
    let scheduled = false;
    const observer = new MutationObserver(function () {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(function () {
        scheduled = false;
        cleanTextNodes(document.body);
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCleaner);
  } else {
    initCleaner();
  }
})();
