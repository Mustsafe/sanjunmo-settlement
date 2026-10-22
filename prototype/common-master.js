/**
 * SANJUNMO BACKOFFICE — 공통 기준정보 (common-master.js)
 *
 * 역할 그룹 · 1:1 문의 분류는 고정값이 아니라 운영 중 관리 화면에서 바뀌는 변수 데이터다.
 *   - 역할 그룹(권한 묶음)      : 운영자 권한 관리 (ADMN-CONF-005)
 *   - 1:1 문의 분류(라우팅)     : 1:1 문의 분류 관리 (ADMN-BRD-007)
 *   - 거래처 · 거래처 유형      : 거래처 관리 (ADMN-VEND-001)
 *   - 권리자 원장 요약(읽기 전용): 원천은 권리자 계약 원장 (ADMN-INST-001)
 * 아래 SEED는 최초 기본값일 뿐이다. 다른 화면은 이름을 직접 적지 말고 이 목록을 읽는다.
 * 프로토타입에서는 관리 화면에서 바꾼 값을 브라우저 localStorage에 저장해 다른 화면이 같은 값을 읽게 한다
 * (실서비스에서는 서버 기준정보 API가 이 역할을 한다).
 */
(function () {
  if (window.SJM_MASTER) return;

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  function store(key, seed) {
    var data = null;
    try {
      var s = window.localStorage.getItem(key);
      if (s) data = JSON.parse(s);
    } catch (e) {}
    if (!data) data = clone(seed);
    return {
      get: function () { return data; },
      set: function (v) {
        data = v;
        try { window.localStorage.setItem(key, JSON.stringify(v)); } catch (e) {}
      },
      reset: function () {
        data = clone(seed);
        try { window.localStorage.removeItem(key); } catch (e) {}
      }
    };
  }

  // 권한 매트릭스의 메뉴 축 — 메뉴(화면) 구성은 시스템이 정하고, 역할 그룹별 읽기(R) · 쓰기(W) · 엑셀(X) 값만 운영에서 바꾼다
  var MENUS = [
    { key: "dash", label: "운영 현황 대시보드", screens: "DASH-001" },
    { key: "stat", label: "매출 · 상품 통계", screens: "STAT-001 · 002" },
    { key: "user", label: "회원 · 수강 관리", screens: "USER-001~006" },
    { key: "order", label: "주문 · 배송 관리", screens: "ORD-001" },
    { key: "shipout", label: "출고 지시 · 송장 업로드", screens: "ORD-002" },
    { key: "refund", label: "환불 요청 · 심사", screens: "RFD-002" },
    { key: "inquiry", label: "1:1 문의 · 공지 · FAQ · 후기", screens: "BRD-001 · 002 · 005" },
    { key: "pqna", label: "상품 Q&A", screens: "BRD-003" },
    { key: "lqna", label: "학습 Q&A", screens: "BRD-004" },
    { key: "promo", label: "이벤트 · 쿠폰 · 포인트", screens: "PROM-001 · 002" },
    { key: "product", label: "상품 · 강좌 · 교재", screens: "PROD-001~007 · BOOK-001" },
    { key: "contract", label: "권리자 계약 · 지분 매핑", screens: "INST-001 · SETT-001 · 007" },
    { key: "vendor", label: "거래처 관리", screens: "VEND-001" },
    { key: "presettle", label: "정산 마감 전 사전 대사", screens: "SETT-004 · 006 · 008 · INST-002" },
    { key: "settle", label: "월간 정산 · 지급 · 조회", screens: "SETT-002 · 005 · 009 · 011" },
    { key: "statement", label: "본인 정산서 확인 · 역발행 승인", screens: "SETT-002-S2" },
    { key: "privacy", label: "민감 정보 · 시스템 감사 로그", screens: "USER-007 · CONF-010" },
    { key: "site", label: "사이트 · 약관 · 메시지 설정", screens: "CONF-001~004" },
    { key: "inqcat", label: "1:1 문의 분류", screens: "BRD-007" },
    { key: "rbac", label: "운영자 권한 관리", screens: "CONF-005" }
  ];

  var ALL = {};
  MENUS.forEach(function (m) { ALL[m.key] = "RWX"; });

  // 역할 그룹 최초값 — 화면설계서 v12 예시 6종 + README 외부 파트너 2종(2026-10-22). 이름 · 구성 · 권한은 운영 중 바뀐다
  // side: INTERNAL 내부 관리자 / EXTERNAL 외부 계정, queue: 1:1 문의 담당 부서 큐로 선택 가능 여부
  var ROLE_SEED = [
    { id: "RG-01", name: "최고 관리자", side: "INTERNAL", queue: false, on: true, order: 1,
      desc: "전 메뉴 · 권한 · 감사 관리", perms: ALL },
    { id: "RG-02", name: "CS담당자", side: "INTERNAL", queue: true, on: true, order: 2,
      desc: "회원 응대 · 1:1 문의 · 환불 접수",
      perms: { dash: "R", user: "RW", order: "RW", refund: "RW", inquiry: "RW", pqna: "RW", lqna: "R", promo: "R", product: "R" } },
    { id: "RG-03", name: "물류팀", side: "INTERNAL", queue: true, on: true, order: 3,
      desc: "출고 지시 · 송장 · 반품 검수",
      perms: { dash: "R", order: "RW", shipout: "RWX", refund: "R", inquiry: "R", pqna: "RW", product: "R" } },
    { id: "RG-04", name: "재무팀", side: "INTERNAL", queue: true, on: true, order: 4,
      desc: "환불 승인 · 지급 · 정산 · 세무",
      perms: { dash: "R", stat: "RX", user: "R", order: "R", refund: "RWX", product: "R", contract: "RWX", vendor: "RWX", presettle: "RWX", settle: "RWX", privacy: "R" } },
    { id: "RG-05", name: "강사", side: "EXTERNAL", queue: true, on: true, order: 5,
      desc: "본인 강좌 학습 Q&A 답변 · 본인 정산서 확인",
      perms: { lqna: "RW", statement: "RW" } },
    { id: "RG-06", name: "조교", side: "EXTERNAL", queue: true, on: true, order: 6,
      desc: "소속 강사 강좌 학습 Q&A · 상품 Q&A 내용 오류 답변",
      perms: { lqna: "RW", pqna: "RW" } },
    { id: "RG-07", name: "저작권자", side: "EXTERNAL", queue: false, on: true, order: 7,
      desc: "본인 도서 인세 정산서 확인 · 역발행 승인",
      perms: { statement: "RW" } },
    { id: "RG-08", name: "외부 3PL", side: "EXTERNAL", queue: false, on: true, order: 8,
      desc: "출고 대상 조회 · 송장 업로드 (금액 비노출)",
      perms: { shipout: "RW" } }
  ];

  // 1:1 문의 분류 최초값 — 담당 부서 큐(depts)는 역할 그룹 ID로 가리킨다(그룹 이름이 바뀌어도 연결 유지)
  var MAJOR_SEED = [
    { prefix: "PAY", name: "결제 · 환불", on: true },
    { prefix: "SHIP", name: "배송 · 교재", on: true },
    { prefix: "LECT", name: "수강 · 기기", on: true },
    { prefix: "PASS", name: "합격환급 · 혜택", on: true },
    { prefix: "STUDY", name: "학습 · 자료", on: true },
    { prefix: "ETC", name: "회원 · 기타", on: true }
  ];
  var CAT_SEED = [
    { code: "VOC-PAY-01", major: "PAY", name: "카드 · 간편결제 취소", screen: "ADMN-RFD-002-S1", depts: ["RG-04"], on: true, order: 1 },
    { code: "VOC-PAY-02", major: "PAY", name: "가상계좌 · 무통장 입금 확인", screen: "ADMN-RFD-002-S1", depts: ["RG-02", "RG-04"], on: true, order: 2 },
    { code: "VOC-PAY-03", major: "PAY", name: "휴대폰 결제 환불", screen: "ADMN-RFD-002-S1", depts: ["RG-04"], on: true, order: 3 },
    { code: "VOC-PAY-04", major: "PAY", name: "영수증 · 증빙 발급", screen: "ADMN-BRD-002", depts: ["RG-02"], on: true, order: 4 },
    { code: "VOC-PAY-05", major: "PAY", name: "상담 필요 (관리자 판단)", screen: "ADMN-BRD-002", depts: ["RG-02"], on: true, order: 5 },
    { code: "VOC-SHIP-01", major: "SHIP", name: "배송지 변경", screen: "ADMN-ORD-001-S1", depts: ["RG-03"], on: true, order: 1 },
    { code: "VOC-SHIP-02", major: "SHIP", name: "배송 지연 · 배송 조회", screen: "ADMN-ORD-002", depts: ["RG-03", "RG-02"], on: true, order: 2 },
    { code: "VOC-SHIP-03", major: "SHIP", name: "파손 · 오배송 교환", screen: "ADMN-ORD-002", depts: ["RG-03"], on: true, order: 3 },
    { code: "VOC-SHIP-04", major: "SHIP", name: "교재 낙장 · 인쇄 불량", screen: "ADMN-ORD-002", depts: ["RG-03"], on: true, order: 4 },
    { code: "VOC-LECT-01", major: "LECT", name: "동시접속 · 세션 차단", screen: "ADMN-USER-003", depts: ["RG-02"], on: true, order: 1 },
    { code: "VOC-LECT-02", major: "LECT", name: "수강 기간 연장", screen: "ADMN-USER-003", depts: ["RG-02"], on: true, order: 2 },
    { code: "VOC-LECT-03", major: "LECT", name: "진도율 누락 · 플레이어 오류", screen: "ADMN-USER-004", depts: ["RG-02"], on: true, order: 3 },
    { code: "VOC-LECT-04", major: "LECT", name: "기기 등록 초기화 (2차 고도화)", screen: "ADMN-USER-003", depts: ["RG-02"], on: false, order: 4 },
    { code: "VOC-PASS-01", major: "PASS", name: "합격환급 서류 보완", screen: "ADMN-SETT-006", depts: ["RG-02", "RG-04"], on: true, order: 1 },
    { code: "VOC-PASS-02", major: "PASS", name: "포인트 · 쿠폰 누락", screen: "ADMN-USER-002", depts: ["RG-02"], on: true, order: 2 },
    { code: "VOC-PASS-03", major: "PASS", name: "이벤트 경품 미수령", screen: "ADMN-USER-002", depts: ["RG-02"], on: true, order: 3 },
    { code: "VOC-STUDY-01", major: "STUDY", name: "강의 내용 질문", screen: "ADMN-BRD-004", depts: ["RG-05", "RG-06"], on: true, order: 1 },
    { code: "VOC-STUDY-02", major: "STUDY", name: "교재 정답지 요청", screen: "ADMN-BRD-010", depts: ["RG-06", "RG-02"], on: true, order: 2 },
    { code: "VOC-ETC-01", major: "ETC", name: "회원정보 변경", screen: "ADMN-BRD-002", depts: ["RG-02"], on: true, order: 1 },
    { code: "VOC-ETC-02", major: "ETC", name: "탈퇴 · 개인정보 처리", screen: "ADMN-BRD-002", depts: ["RG-02"], on: true, order: 2 },
    { code: "VOC-ETC-03", major: "ETC", name: "기타 문의", screen: "ADMN-BRD-002", depts: ["RG-02"], on: false, order: 3 }
  ];

  // 거래처 유형 최초값 — 권리자(계약 원장의 계약 당사자)가 아닌 거래 상대방의 분류. 공급 파트너가 늘면 거래처 관리에서 유형을 추가한다
  // form: 거래 조건 입력 양식 — PURCHASE 매입(공급률 · 결제 조건) / LOGISTICS 물류 대행(건당 단가 · 회수 · 보관) / GENERAL 일반
  var VENDOR_TYPE_SEED = [
    { id: "VT-01", name: "도서 매입처", form: "PURCHASE", evidence: "전자계산서(면세)", on: true, order: 1 },
    { id: "VT-02", name: "상품 매입처", form: "PURCHASE", evidence: "전자세금계산서(과세)", on: true, order: 2 },
    { id: "VT-03", name: "물류 대행사(3PL)", form: "LOGISTICS", evidence: "전자세금계산서(과세)", on: true, order: 3 }
  ];

  // 거래처 최초값 — 화면들에 흩어져 있던 매입처 · 3PL을 한 원장으로 모은 것(코드 SUP-NNNN은 기존 화면 표기를 따름)
  var VENDOR_SEED = [
    { id: "SUP-0003", type: "VT-01", name: "한국자격교재총판", bizNo: "214-81-33201", ceo: "권총판", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "65", pay: "월말 마감 · 익월 10일 지급" }, contact: "02-555-1203", since: "2024-03-01" },
    { id: "SUP-0004", type: "VT-01", name: "예문사", bizNo: "105-81-12345", ceo: "정예문", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "70", pay: "월말 마감 · 익월 10일 지급" }, contact: "02-701-4410", since: "2023-01-10" },
    { id: "SUP-0005", type: "VT-01", name: "구민사", bizNo: "101-81-22987", ceo: "조구민", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "68", pay: "월말 마감 · 익월 15일 지급" }, contact: "02-333-1200", since: "2023-06-01" },
    { id: "SUP-0006", type: "VT-01", name: "성안당", bizNo: "110-81-40018", ceo: "이성안", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "70", pay: "월말 마감 · 익월 10일 지급" }, contact: "031-950-6300", since: "2024-01-15" },
    { id: "SUP-0008", type: "VT-01", name: "(주)한빛도서유통", bizNo: "124-86-77120", ceo: "한빛남", taxType: "일반과세", status: "폐업", checkedAt: "2026-06-01", on: false,
      terms: { rate: "66", pay: "월말 마감 · 익월 10일 지급" }, contact: "031-221-0090", since: "2022-09-01" },
    { id: "SUP-0007", type: "VT-02", name: "(주)세이프기프트", bizNo: "220-87-10293", ceo: "안세이", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "55", pay: "입고 후 30일" }, contact: "02-6010-7788", since: "2025-04-01" },
    { id: "SUP-0012", type: "VT-02", name: "카시오코리아 공식총판", bizNo: "211-88-55031", ceo: "김카시", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { rate: "72", pay: "입고 후 45일" }, contact: "02-2222-3456", since: "2025-07-01" },
    { id: "SUP-0020", type: "VT-03", name: "CJ대한통운 파주 물류센터", bizNo: "110-81-05034", ceo: "신물류", taxType: "일반과세", status: "계속", checkedAt: "2026-10-02", on: true,
      terms: { outFee: "2000", returnFee: "4000", storage: "300000", cycle: "월 1회 (익월 초 명세서)" }, contact: "031-940-1100", since: "2025-11-01" }
  ];

  // 권리자 원장 요약 — 원천은 권리자 계약 원장(ADMN-INST-001)의 현행 계약(해지 · 종료 계약 제외). 외부 계정의 소속(본인 데이터 범위) 지정에 쓴다.
  // 강사 · 저자 · 위탁사 같은 구분은 고정 분류가 아니라 계약 유형(정산 입력 구분)에서 나온다
  var RIGHTS_HOLDER_SEED = [
    { id: "RH-0012", name: "산준교육 콘텐츠 주식회사", contracts: [{ no: "CT-2026-0412", types: ["강의 수익배분", "교재 인세", "개발지원금"] }] },
    { id: "RH-0018", name: "고(故) 박위생 (상속 승계)", contracts: [{ no: "CT-2025-1102", types: ["교재 인세", "강의 수익배분"] }] },
    { id: "RH-0019", name: "김안전 강사", contracts: [{ no: "CT-2026-0715", types: ["강의 수익배분", "월 최저보장", "문항 매절"] }] },
    { id: "RH-0025", name: "정종대 강사 (정종대 안전연구소)", contracts: [{ no: "CT-2026-0501", types: ["강의 수익배분", "교재 인세", "개발지원금"] }] },
    { id: "RH-0031", name: "이안전 저자", contracts: [{ no: "CT-2026-0610", types: ["교재 인세"] }] },
    { id: "RH-0046", name: "이건설 강사", contracts: [{ no: "CT-2026-0712", types: ["강의 수익배분", "교재 인세"] }] },
    { id: "RH-0047", name: "박보건 강사", contracts: [{ no: "CT-2024-1101", types: ["강의 수익배분"] }] },
    { id: "RH-0048", name: "최지도 강사 · 저자", contracts: [{ no: "CT-2026-0405", types: ["교재 인세", "강의 수익배분"] }] },
    { id: "RH-0042", name: "최그래픽 (기여자)", contracts: [{ no: "CT-2026-0702", types: ["개발지원금", "공동제작"] }] },
    { id: "RH-0044", name: "안전기술출판 (위탁사)", contracts: [{ no: "CT-2026-0705", types: ["도서 위탁"] }] },
    { id: "RH-0051", name: "사단법인 한국소방학회", contracts: [{ no: "CT-2026-0801", types: ["도서 위탁"] }] },
    { id: "RH-0063", name: "한도해 작가", contracts: [{ no: "CT-2026-0919", types: ["일시 용역 (삽화 · 자문)"] }] },
    { id: "RH-0088", name: "최신규 강사 (신규 영입)", contracts: [{ no: "CT-2026-NEW", types: ["강의 수익배분", "개발지원금"] }] }
  ];

  var roleStore = store("sjm.master.roleGroups.v1", ROLE_SEED);
  var vendorTypeStore = store("sjm.master.vendorTypes.v1", VENDOR_TYPE_SEED);
  var vendorStore = store("sjm.master.vendors.v1", VENDOR_SEED);
  var majorStore = store("sjm.master.inquiryMajors.v1", MAJOR_SEED);
  var catStore = store("sjm.master.inquiryCats.v1", CAT_SEED);

  function byOrder(a, b) { return (a.order || 0) - (b.order || 0); }

  var roles = {
    list: function () { return roleStore.get().slice().sort(byOrder); },
    active: function () { return roles.list().filter(function (g) { return g.on; }); },
    queues: function () { return roles.active().filter(function (g) { return g.queue; }); },
    get: function (id) {
      var all = roleStore.get();
      for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i];
      return null;
    },
    name: function (id) { var g = roles.get(id); return g ? g.name : id; },
    perm: function (id, menu) { var g = roles.get(id); return (g && g.perms && g.perms[menu]) || ""; },
    has: function (id, menu, flag) { return roles.perm(id, menu).indexOf(flag) !== -1; },
    save: function (list) { roleStore.set(clone(list)); },
    reset: function () { roleStore.reset(); },
    nextId: function () {
      var max = 0;
      roleStore.get().forEach(function (g) { var n = parseInt(String(g.id).split("-")[1], 10); if (n > max) max = n; });
      return "RG-" + (max + 1 < 10 ? "0" : "") + (max + 1);
    }
  };

  var inquiry = {
    majors: function () { return majorStore.get(); },
    cats: function () { return catStore.get(); },
    save: function (majors, cats) { majorStore.set(clone(majors)); catStore.set(clone(cats)); },
    reset: function () { majorStore.reset(); catStore.reset(); },
    // 역할 그룹을 담당 부서 큐로 쓰는 사용 중 분류 — 그룹 변경 · 미사용 전환의 영향 확인에 쓴다
    catsUsingRole: function (roleId) {
      return catStore.get().filter(function (c) { return c.on && c.depts.indexOf(roleId) !== -1; });
    },
    // 대분류에 속한 사용 중 분류의 담당 부서 큐 합집합 — 1:1 문의 허브에서 접수 건이 올라가는 큐
    queuesForMajor: function (prefix) {
      var seen = {};
      var out = [];
      catStore.get().forEach(function (c) {
        if (!c.on || c.major !== prefix) return;
        c.depts.forEach(function (d) { if (!seen[d]) { seen[d] = true; out.push(d); } });
      });
      return out;
    }
  };

  var vendors = {
    types: function () { return vendorTypeStore.get().slice().sort(byOrder); },
    activeTypes: function () { return vendors.types().filter(function (t) { return t.on; }); },
    type: function (id) {
      var all = vendorTypeStore.get();
      for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i];
      return null;
    },
    list: function () { return vendorStore.get().slice(); },
    get: function (id) {
      var all = vendorStore.get();
      for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i];
      return null;
    },
    name: function (id) { var v = vendors.get(id); return v ? v.name : id; },
    // 양식(form)으로 고른다 — 유형 이름이 바뀌거나 늘어도 '물류 대행' 거래처를 찾을 수 있게
    byForm: function (form) {
      return vendorStore.get().filter(function (v) { var t = vendors.type(v.type); return t && t.form === form; });
    },
    byType: function (typeId) { return vendorStore.get().filter(function (v) { return v.type === typeId; }); },
    save: function (list) { vendorStore.set(clone(list)); },
    saveTypes: function (list) { vendorTypeStore.set(clone(list)); },
    reset: function () { vendorStore.reset(); vendorTypeStore.reset(); },
    nextId: function () {
      var max = 0;
      vendorStore.get().forEach(function (v) { var n = parseInt(String(v.id).split("-")[1], 10); if (n > max) max = n; });
      var s = String(max + 1);
      while (s.length < 4) s = "0" + s;
      return "SUP-" + s;
    },
    nextTypeId: function () {
      var max = 0;
      vendorTypeStore.get().forEach(function (t) { var n = parseInt(String(t.id).split("-")[1], 10); if (n > max) max = n; });
      return "VT-" + (max + 1 < 10 ? "0" : "") + (max + 1);
    }
  };

  // 2계층 사업자 수취인 — 원천은 수취인 2계층 분할(ADMN-SETT-007). 현재 분할 몫이 있고 세금계산서 · 계산서 역발행 승인이 필요한
  // 사업자 수취인만 둔다(원천징수 대상 개인 수취인은 계정 없이 정산서 PDF 발송). 소속은 권리자이며 데이터 범위는 본인 수취 몫
  var PAYEE_SEED = [
    { id: "PY-9001", name: "(주)스타에듀매니지먼트", entity: "법인 일반과세자", bizNo: "106-81-55210", contract: "CT-2026-0715", holderId: "RH-0019", holderName: "김안전", ratio: 30, evidence: "세금계산서 역발행" }
  ];

  var rightsHolders = {
    list: function () { return clone(RIGHTS_HOLDER_SEED); },
    get: function (id) {
      for (var i = 0; i < RIGHTS_HOLDER_SEED.length; i++) if (RIGHTS_HOLDER_SEED[i].id === id) return clone(RIGHTS_HOLDER_SEED[i]);
      return null;
    },
    // 계약 유형 합집합 — 이 권리자가 어떤 성격의 파트너인지는 계약 유형으로 판단한다
    types: function (id) {
      var h = rightsHolders.get(id);
      var seen = {};
      var out = [];
      if (!h) return out;
      h.contracts.forEach(function (c) { c.types.forEach(function (t) { if (!seen[t]) { seen[t] = true; out.push(t); } }); });
      return out;
    },
    payees: function () { return clone(PAYEE_SEED); },
    payee: function (id) {
      for (var i = 0; i < PAYEE_SEED.length; i++) if (PAYEE_SEED[i].id === id) return clone(PAYEE_SEED[i]);
      return null;
    }
  };

  window.SJM_MASTER = { menus: MENUS, roles: roles, inquiry: inquiry, vendors: vendors, rightsHolders: rightsHolders };
})();
