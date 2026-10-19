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


/* === [PROTOTYPE-CLEAN: DOM TEXT-NODE ONLY TRANSLATOR (ZERO CODE MUTATION)] === */
(function () {
  // 1) 긴 구문부터 먼저 치환하여 동어반복("권리자 계약 원장 ([권리자 계약 원장])") 원천 방지
  const TEXT_REPLACEMENTS = [
    // 동어반복 방지를 위한 복합 문구 우선 치환
    ["권리자 계약 원장 (ADMN-INST-001)", "권리자 계약 원장"],
    ["권리자 계약 원장(ADMN-INST-001)", "권리자 계약 원장"],
    ["도서 공급 원장 (ADMN-BOOK-001)", "도서 공급 원장"],
    ["도서 공급 원장(ADMN-BOOK-001)", "도서 공급 원장"],
    ["상품별 권리자 매핑 (ADMN-SETT-001)", "상품별 권리자 매핑"],
    ["상품별 권리자 매핑(ADMN-SETT-001)", "상품별 권리자 매핑"],
    ["월간 정산(ADMN-SETT-002)", "월간 정산"],
    ["정산 원장(ADMN-SETT-002)", "월간 정산 원장"],
    ["정산 원장(SETT-002)", "월간 정산 원장"],
    ["감사 로그(ADMN-CONF-010)", "정산 감사 로그"],
    ["감사·보안 로그 (ADMN-CONF-006/010)", "감사 · 보안 로그"],
    ["수동 무상 포인트 지급/차감 (002-P1)", "수동 포인트 지급 · 차감"],
    ["엑셀 다운로드 (001-P1)", "엑셀 다운로드"],
    ["이월 발생 내역 원장 (ADMN-SETT-002-P1)", "이월 발생 내역 원장"],
    ["통합 정산서 상세·마감 (S1)", "통합 정산서 상세 · 마감"],
    ["상세·마감 워크스페이스 (S1)", "통합 정산서 상세"],
    ["권리자 제공 정산서 (S2)", "권리자 제공 정산서"],
    ["권리자 정산서 (S2)", "권리자 정산서"],
    ["합격 심사 (S1)", "합격 증빙 심사"],
    ["1. 환불 요청 목록 (RFD-004)", "환불 요청 목록"],
    ["2. 합격환급반 심사 (RFD-001)", "합격환급반 심사"],
    ["3. 환불 처리 상세 (RFD-002)", "환불 처리 상세"],
    ["4. 환불 완료 내역 (RFD-003)", "환불 완료 내역"],
    ["1. 주문 내역 관리 (ORD-001)", "주문 내역 관리"],
    ["2. 3PL 배송·출고·반품검수 (ORD-002)", "3PL 배송 · 출고 · 반품검수"],
    ["3. 주문 상세 · 배송지 Lock (ORD-001-S1)", "주문 상세 · 배송지 관리"],
    ["수강권 직권 부여 (0원 주문 · 구 ORD-003)", "수강권 직권 부여 (0원 주문)"],
    ["3PL 물류 격리 (ROLE_PARTNER_3PL)", "3PL 물류 파트너 뷰"],
    ["빈출특강 (FREQ_EXAM)", "빈출특강"],
    ["무료특강 영상 (FREE_LECTURE)", "무료특강 영상"],
    ["빈출문제 해설 (FREQ_EXAM)", "빈출문제 해설"],
    ["교재 정답지 및 상세 해설 (ANSWER_SHEET)", "교재 정답지 및 상세 해설"],
    ["정산 매핑 (SETT-001)", "정산 지분 매핑"],
    ["권리자 지분 매핑 (SETT-001)", "권리자 지분 매핑"],
    ["공급원가(BOOK-001)", "공급원가"],
    ["합격수기 검수 (BRD-005)", "합격수기 검수"],
    ["BRD-005 검수완료 (우수)", "검수 완료 (우수)"],
    ["옵션 B (강사 50% 분담 · SETT-006 C-01)", "강사 50% 분담 약정"],
    ["차월 전기오류수정 대기 (SETT-005)", "차월 정산 반영 대기"],
    ["재무 권한(FIN_MANAGER) 시뮬레이션 (사입원가 열람)", "재무 담당자 원가 표시"],
    ["재무/정산책임자 (FIN_MANAGER)", "재무/정산 책임자"],
    ["매입 재판매 (PURCHASED_RESALE)", "매입 재판매"],
    ["자사 직접 판매 (DIRECT_SALE)", "자사 직접 제작·판매"],
    ["OWN_PUBLISHED (자사발행 인세 · Pipeline 2.1)", "자사발행 도서 (인세)"],
    ["OWN_PUBLISHED (자사발행)", "자사 발행 도서"],
    ["OWN_PUBLISHED (자사저작권)", "자사 저작권 도서"],
    ["CONSIGNMENT (위탁 판매 · Pipeline 2.2)", "위탁 판매 도서"],
    ["CONSIGNMENT (위탁판매)", "위탁 판매 도서"],
    ["PURCHASED_RESALE (사입)", "매입 재판매 도서"],
    ["BUNDLED (강좌포함 비매품)", "강좌 포함 비매품"],
    ["CONDITIONAL (상계 허용 · v4.0.0)", "상계 허용"],
    ["NON_OFFSET (비상계 보장)", "비상계 보장 (MMG)"],
    ["원인 미분류 불일치 (UNKNOWN_MISMATCH)", "원인 미분류 불일치"],
    ["UNKNOWN_MISMATCH (미분류)", "원인 미분류 불일치"],
    ["TIMING_GAP (기간 귀속차)", "기간 귀속 차이 (월말·월초)"],
    ["PARTIAL_CANCEL_PENDING (부분취소 대기)", "부분취소 처리 대기"],
    ["PG_FEE_DIFF (PG 수수료 차감차)", "PG 수수료 차액"],
    ["REFUND_TIMING_DIFF (환불 처리 시차)", "환불 처리 시차"],
    ["계약 중 (ACTIVE)", "계약 중"],
    ["작성 중 (DRAFT)", "작성 중"],
    ["만료 / 해지 (EXPIRED · TERMINATED)", "만료 / 해지"],
    ["정상 (ACTIVE)", "정상"],
    ["정상 활성 (ACTIVE)", "정상 활성"],
    ["잠김/중지 (LOCKED)", "잠김 / 중지"],
    ["[내부] 최고관리자 (ROLE_SUPER_ADMIN)", "[내부] 최고관리자"],
    ["[내부] 정산/재무 담당 (ROLE_FINANCE_ADMIN)", "[내부] 정산 · 재무 담당자"],
    ["[내부] 정산/재무 관리자 (ROLE_FINANCE_ADMIN)", "[내부] 정산 · 재무 관리자"],
    ["[내부] 서비스/콘텐츠 운영 (ROLE_OPS_ADMIN)", "[내부] 서비스 · 콘텐츠 운영자"],
    ["[내부] 서비스/콘텐츠 운영자 (ROLE_OPS_ADMIN)", "[내부] 서비스 · 콘텐츠 운영자"],
    ["[내부] 고객센터 CS 전담 (ROLE_CS_ADMIN)", "[내부] 고객센터(CS) 담당자"],
    ["[파트너] 강사 전용 (ROLE_PARTNER_INST)", "[파트너] 강사 전용 계정"],
    ["[파트너] 교재 저작권자 (ROLE_PARTNER_COPYRIGHT)", "[파트너] 교재 저작권자 계정"],
    ["[파트너] 외부 물류 3PL (ROLE_PARTNER_3PL)", "[파트너] 외부 물류(3PL) 계정"],
    ["시연 권한", "열람 권한"],
    ["국세청 진위 확인 · 모의", "국세청 진위 확인"],
    ["휴업자 저장 예외 승인 · 모의", "휴업자 예외 승인"],
    ["세무 판정 상태 · 시연", "세무 판정 상태"],
    ["🧪 QA D-13 시연: 은행 계좌오류 송금 실패 시뮬레이션", "⚠️ 이체 실패(계좌오류) 재처리 테스트"],
    ["[P1 시연] 정액 250,000원 초과 입력", "한도 초과 입력 테스트 (250,000원)"],
    ["[P1 시연] 정률 45% 초과 입력", "한도 초과 입력 테스트 (45%)"],
    // 단독 코드 치환
    ["USER-PROM-001", "프론트 이벤트/기획전"],
    ["USER-CS-001", "프론트 공지사항"],
    ["USER-CS-002", "프론트 FAQ"],
    ["USER-LECT-002-S1", "프론트 강좌상세"],
    ["USER-LECT-002", "프론트 강좌상세"],
    ["USER-CRS-002", "프론트 강좌상세"],
    ["USER-MY-003", "내 강의실"],
    ["USER-MY-007", "내 쿠폰함"],
    ["USER-PAY-001", "주문/결제서"],
    ["USER-FREE-001", "무료특강/빈출문제"],
    ["USER-INST-001", "강사 소개"],
    ["USER-JOIN-002", "회원가입 화면"],
    ["USER-INFO-001", "하단 푸터"],
    ["ADMN-SETT-001", "상품별 권리자 매핑"],
    ["ADMN-SETT-002-S1", "통합 정산서 원장"],
    ["ADMN-SETT-002-S2", "권리자 정산내역서"],
    ["ADMN-SETT-002-P1", "이월 내역 원장"],
    ["ADMN-SETT-002", "월간 정산 관리"],
    ["ADMN-SETT-004", "PG 정산 대사"],
    ["ADMN-SETT-005", "정산 수동 조정"],
    ["ADMN-SETT-006", "합격환급반 정산"],
    ["ADMN-SETT-007", "수취인 분할 관리"],
    ["ADMN-SETT-008", "사업자 과세유형 확인"],
    ["ADMN-SETT-009", "내부 정산 조회"],
    ["ADMN-SETT-011", "택배 운임 대사"],
    ["ADMN-INST-001", "권리자 계약 원장"],
    ["ADMN-INST-002", "약정금 마일스톤 검수"],
    ["ADMN-BOOK-001", "도서 공급 원장"],
    ["ADMN-ORD-001", "통합 주문 관리"],
    ["ADMN-ORD-002", "배송·3PL 관리"],
    ["ADMN-RFD-002", "환불 심사 관리"],
    ["ADMN-USER-001", "회원 목록"],
    ["ADMN-USER-002", "회원 상세"],
    ["ADMN-USER-003", "수강·기기 제어"],
    ["ADMN-USER-005", "블랙리스트 관리"],
    ["ADMN-USER-006", "그룹·태그 관리"],
    ["ADMN-USER-007", "민감정보 열람통제"],
    ["ADMN-PROM-001", "이벤트·기획전 관리"],
    ["ADMN-PROM-002", "쿠폰 마스터 관리"],
    ["ADMN-PROM-003", "포인트 원장 관리"],
    ["ADMN-BRD-001", "공지사항 관리"],
    ["ADMN-BRD-002", "1:1 문의 허브"],
    ["ADMN-BRD-005", "후기·무료특강·정답지"],
    ["ADMN-BRD-009", "교재 정답지 관리"],
    ["ADMN-BRD-010", "당첨자 발표 관리"],
    ["ADMN-CONF-004-S1", "타겟 메시지 발송"],
    ["ADMN-CONF-004", "메시지 템플릿 관리"],
    ["ADMN-CONF-006", "보안 감사로그"],
    ["ADMN-CONF-010", "정산 감사로그"],
    ["Pipeline 1.1", "강좌 수익배분"],
    ["Pipeline 2.1", "자사발행 도서 인세"],
    ["Pipeline 2.2", "위탁 도서 판매대금"],
    ["Pipeline 2.3", "일반상품 매출"],
    ["Pipeline 5.1", "매출연동 개발지원금"],
    ["— 산준모 백오피스 v4.0.0", "— 산준모 관리자 센터"],
    ["— 산준모닷컴 백오피스 v8.4 Final", "— 산준모 관리자 센터"],
    ["— 산준모닷컴 백오피스 v8.4 FINAL", "— 산준모 관리자 센터"],
    ["— 산준모닷컴 백오피스", "— 산준모 관리자 센터"],
    // 권한(ROLE) 코드 번역
    ["ROLE_SUPER_ADMIN", "최고 관리자"],
    ["ROLE_MASTER_ADMIN", "최고 관리자"],
    ["ROLE_FINANCE_DIRECTOR", "재무 총괄 책임자"],
    ["ROLE_FINANCE_ADMIN", "재무/정산 담당자"],
    ["ROLE_SETT_ADMIN", "정산 관리자"],
    ["ROLE_OPS_ADMIN", "서비스 운영자"],
    ["ROLE_CS_ADMIN", "고객센터 담당자"],
    ["ROLE_PARTNER_INST", "강사/학원 파트너"],
    ["ROLE_PARTNER_COPYRIGHT", "저작권 파트너"],
    ["ROLE_PARTNER_3PL", "물류(3PL) 파트너"],
    ["ROLE_STUDENT", "일반 회원"],
    // 미등록 화면 코드 번역
    ["ADMN-SETT-003", "정산 마감 확정"],
    ["ADMN-STAT-001", "매출·정산 통계"],
    ["ADMN-DASH-001", "대시보드"],
    ["ADMN-CONF-001-S1", "약관 개정 이력"],
    ["ADMN-CONF-001-S2", "신규 약관 등록"],
    ["ADMN-CONF-001", "배너/팝업 관리"],
    ["ADMN-CONF-002", "약관/개인정보 관리"],
    ["ADMN-CONF-003", "시스템 환경설정"],
    ["ADMN-CONF-005", "관리자 권한 관리"],
    ["ADMN-CONF-008", "환경설정 연동"],
    ["ADMN-LOGIN-001-P1", "2차 인증 OTP"],
    ["ADMN-LOGIN-001", "관리자 로그인"],
    ["ADMN-LOGIN-002", "비밀번호 재설정"],
    ["ADMN-LOGIN-003", "계정 잠금 해제"],
    ["ADMN-BRD-004", "수험 자료실"],
    ["ADMN-BRD-006", "무료특강·빈출문제"],
    // 기술 파라미터 및 DB 컬럼명
    ["tax_type", "과세유형"],
    ["utcc_yn", "확인여부"],
    ["origin_settlement_id", "참조 정산서 ID"],
    ["origin_month", "원 발생 귀속월"],
    ["applied_month", "반영 기준월"],
    ["adj_reason_code", "조정 사유 구분"],
    ["adj_account_type", "이월/반영 계정"],
    ["adj_tax_type", "과·면세 구분"],
    ["adj_explanation", "조정 소명 내용"]
  ];

  const REGEX_CLEANERS = [
    // [ADMN-...] 또는 [Term-...] 또는 [테이블 A~G] 또는 [8.3절...] 대괄호 태그 제거
    /\[\s*(?:ADMN-[A-Z]+-\d+[^\]]*|Term-[A-Z]+|테이블\s*[A-G]|(?:제?\d+장|\d+(?:\.\d+)?절|부록)[^\]]*)\]\s*/g,
    // (ADMN-...), (SETT-001), (001-P1), (S1), (P2) 등 화면코드 괄호 제거
    /\s*\(\s*(?:ADMN-|USER-)?(?:SETT|INST|BOOK|PROD|ORD|RFD|USER|PROM|BRD|CONF|DASH|STAT|CRS|MY|FREE|LECT)-\d+(?:-[A-Z0-9]+)?[^)]*\)/g,
    /\s*\(\s*(?:\d{3}-[SP]\d+|[SP]\d+)\s*\)/g,
    // (6.5절 · 8.3절), (제15장 15.2절), (Case 7), (부록 D-15) 등 기획서 장/절/케이스 괄호 제거
    /\s*\(\s*(?:합의서\s*)?(?:제?\d+장\s*)?\d+(?:\.\d+)?절[^)]*\)/g,
    /\s*·\s*\d+(?:\.\d+)?절/g,
    /\s*\(\s*(?:Case\s*\d+[^)]*|부록\s*[A-Z][^)]*|QA\s*D-\d+[^)]*)\)/gi,
    // (member_status), (goods_stock_log), (own_copyright_yn) 등 영문 snake_case DB 컬럼 괄호 제거
    /\s*\(\s*[a-z]+_[a-z0-9_]+(?:\s*=\s*[^)]+)?\s*\)/g,
    // Table: xxx 배지 텍스트 제거
    /^\s*Table:\s*[a-z0-9_]+\s*$/i,
    // 잔여 화면코드 접두사 및 기술 코드 제거
    /\b(?:ADMN|USER)-[A-Z]+-\d+(?:-[A-Z0-9]+)?\b/g,
    /\bROLE_[A-Z0-9_]+\b/g,
    /\b[a-z]+_(?:yn|type|status|mode|limit|flag|scope)\b/g
  ];

  function transformText(str) {
    if (!str || typeof str !== "string" || !str.trim()) return str;
    let out = str;
    for (let i = 0; i < TEXT_REPLACEMENTS.length; i++) {
      const target = TEXT_REPLACEMENTS[i][0];
      if (out.indexOf(target) !== -1) {
        out = out.split(target).join(TEXT_REPLACEMENTS[i][1]);
      }
    }
    for (let j = 0; j < REGEX_CLEANERS.length; j++) {
      out = out.replace(REGEX_CLEANERS[j], "");
    }
    return out;
  }

  function walkAndClean(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) {
      const p = node.parentNode;
      if (!p) continue;
      const tag = p.tagName;
      // 코드/스타일/입력창 내부 텍스트는 절대 건드리지 않음
      if (tag === "SCRIPT" || tag === "STYLE" || tag === "TEXTAREA" || tag === "CODE" && p.classList.contains("raw-keep")) continue;
      textNodes.push(node);
    }
    for (let i = 0; i < textNodes.length; i++) {
      const orig = textNodes[i].nodeValue;
      const cleaned = transformText(orig);
      if (cleaned !== orig) {
        textNodes[i].nodeValue = cleaned;
      }
    }
    if (document.title) {
      const ct = transformText(document.title);
      if (ct !== document.title) document.title = ct;
    }
  }

  function startSafeCleaner() {
    walkAndClean(document.body);
    let pending = false;
    const obs = new MutationObserver(function () {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () {
        pending = false;
        walkAndClean(document.body);
      });
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startSafeCleaner);
  } else {
    startSafeCleaner();
  }
})();
