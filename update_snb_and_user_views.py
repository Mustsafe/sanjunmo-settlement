import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# 1. prototype/common-snb.js 업데이트
# ==============================================================================
snb_path = os.path.join("prototype", "common-snb.js")
with open(snb_path, "r", encoding="utf-8") as f:
    snb_content = f.read()

# 1-1. SNB_GROUPS 내 회원관리 그룹 독립 또는 메뉴 구성
# 기존 ORD/RFD/BRD 그룹에서 USER-001 항목 제거하고,
# 상단에 "회원 · 수강 · 태그 관리 (USER)" 전용 그룹 추가
old_ord_group = """    {
      title: "주문 · 배송 · 환불 · CS 관리 (ORD/RFD/BRD)",
      items: [
        { code: "USER-001", label: "일반 회원 · 수강 · 태그 관리", href: "ADMN-USER-001_baseline.html", screenCode: "ADMN-USER-001" },
        { code: "ORD-001", label: "주문 · 배송 · 3PL 관리", href: "ADMN-ORD-001_baseline.html" },
        { code: "RFD-002", label: "환불 요청 · 심사 관리", href: "ADMN-RFD-002_baseline.html" },
        { code: "BRD-002", label: "1:1 문의 관리 (문의 분기 허브)", href: "ADMN-BRD-002_baseline.html", screenCode: "ADMN-BRD-002" },
        { code: "PROM-002", label: "쿠폰 마스터 · 포인트 혜택 관리", href: "ADMN-PROM-002_baseline.html", screenCode: "ADMN-PROM-002" }
      ]
    },"""

new_user_and_ord_groups = """    {
      title: "회원 · 수강 · 태그 관리 (USER)",
      items: [
        { code: "USER-001", label: "일반 회원 관리 (목록·상세)", href: "ADMN-USER-001_baseline.html?view=list", screenCode: "ADMN-USER-001" },
        { code: "USER-003", label: "회원 수강 · 기간 · 기기 제어", href: "ADMN-USER-001_baseline.html?view=course", screenCode: "ADMN-USER-003" },
        { code: "USER-006", label: "회원 그룹 · 태그 관리", href: "ADMN-USER-001_baseline.html?view=tags", screenCode: "ADMN-USER-006" }
      ]
    },
    {
      title: "주문 · 배송 · 환불 · CS 관리 (ORD/RFD/BRD)",
      items: [
        { code: "ORD-001", label: "주문 · 배송 · 3PL 관리", href: "ADMN-ORD-001_baseline.html" },
        { code: "RFD-002", label: "환불 요청 · 심사 관리", href: "ADMN-RFD-002_baseline.html" },
        { code: "BRD-002", label: "1:1 문의 관리 (문의 분기 허브)", href: "ADMN-BRD-002_baseline.html", screenCode: "ADMN-BRD-002" },
        { code: "PROM-002", label: "쿠폰 마스터 · 포인트 혜택 관리", href: "ADMN-PROM-002_baseline.html", screenCode: "ADMN-PROM-002" }
      ]
    },"""

if old_ord_group in snb_content:
    snb_content = snb_content.replace(old_ord_group, new_user_and_ord_groups, 1)
    print("[OK] Replaced ORD group with USER and ORD groups in common-snb.js")
else:
    print("[WARN] old_ord_group not found in common-snb.js")

# 1-2. 현재 페이지 매칭 로직 보완 (URL 쿼리스트링 포함 매칭 우선)
old_matching_logic = """  function buildSnbHtml(currentFile) {
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
    }).join("");"""

new_matching_logic = """  function buildSnbHtml(currentFileWithQuery, currentFileOnly) {
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
        <div class="snb-group-title">${group.title}</div>
        <div class="snb-item-list">${itemsHtml}</div>
      </div>`;
    }).join("");"""

old_init_snb = """  function initMasterSnb() {
    const pathParts = window.location.pathname.replace(/\\\\/g, "/").split("/");
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
  }"""

new_init_snb = """  function initMasterSnb() {
    const pathParts = window.location.pathname.replace(/\\\\/g, "/").split("/");
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
  }"""

if old_matching_logic in snb_content:
    snb_content = snb_content.replace(old_matching_logic, new_matching_logic, 1)
    print("[OK] Updated matching logic in common-snb.js")
else:
    print("[WARN] old_matching_logic not found in common-snb.js")

if old_init_snb in snb_content:
    snb_content = snb_content.replace(old_init_snb, new_init_snb, 1)
    print("[OK] Updated initMasterSnb in common-snb.js")
else:
    print("[WARN] old_init_snb not found in common-snb.js")

with open(snb_path, "w", encoding="utf-8") as f:
    f.write(snb_content)


# ==============================================================================
# 2. prototype/ADMN-USER-001_baseline.html 업데이트
# ==============================================================================
user_path = os.path.join("prototype", "ADMN-USER-001_baseline.html")
with open(user_path, "r", encoding="utf-8") as f:
    user_content = f.read()

# 2-1. 가짜 탭 바 제거
# <div class="subview-bar"> ... </div> 제거
subview_bar_pattern = re.compile(r'    <div class="subview-bar">[\s\S]*?    </div>\s*\n', re.MULTILINE)
if subview_bar_pattern.search(user_content):
    user_content = subview_bar_pattern.sub("", user_content)
    print("[OK] Removed .subview-bar from ADMN-USER-001_baseline.html")
else:
    print("[WARN] subview-bar not found in ADMN-USER-001_baseline.html")

# 2-2. header.top-bar.v4-gen3-topbar 내부 Breadcrumb 에 id 부여 (동적 변경용)
old_crumb = """    <header class="top-bar v4-gen3-topbar">
      <div class="crumb">
        <span class="crumb-code">ADMN-USER-001 ~ 006</span>
        <span>회원관리 &gt; 일반 회원 관리 &gt;</span>
        <strong style="color:var(--text-main);">회원 목록 · CS 원스톱 상세 · 수강/기기 제어 · 그룹/태그 관리</strong>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="badge badge-blue">개인정보 기본 마스킹 (해제 시 10분 후 자동 재마스킹)</span>
        <span class="badge badge-purple">유상 P(LIFO 부활) / 무상 P(환불 회수) 분리</span>
        <a href="ADMN-CONF-010_baseline.html" class="btn btn-sm btn-outline">감사·보안 로그 (ADMN-CONF-006/010) ↗</a>
      </div>
    </header>"""

new_crumb = """    <header class="top-bar v4-gen3-topbar">
      <div class="crumb">
        <span class="crumb-code" id="top-crumb-code">ADMN-USER-001</span>
        <span>회원관리 &gt; 일반 회원 관리 &gt;</span>
        <strong style="color:var(--text-main);" id="top-crumb-title">회원 목록 조회</strong>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <button type="button" class="btn btn-sm btn-outline" id="top-btn-point" onclick="openPointModal()">＋ 수동 무상 포인트 지급/차감 (002-P1)</button>
        <button type="button" class="btn btn-sm btn-dark" id="top-btn-excel" onclick="openExcelModal()">🔒 엑셀 다운로드 (001-P1)</button>
        <span class="badge badge-blue">개인정보 기본 마스킹 (10분 후 자동 재마스킹)</span>
        <a href="ADMN-CONF-010_baseline.html" class="btn btn-sm btn-outline">감사·보안 로그 ↗</a>
      </div>
    </header>"""

if old_crumb in user_content:
    user_content = user_content.replace(old_crumb, new_crumb, 1)
    print("[OK] Updated top-bar header in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_crumb not found in ADMN-USER-001_baseline.html")

# 2-3. 회원 상세(view-detail) 카드 헤더 좌측 및 하단에 [← 회원 목록으로 (ADMN-USER-001)] 배치
old_dt_header = """        <div class="card">
          <div class="card-header">
            <div class="card-title">
              <span>회원 상세 정보 (ADMN-USER-002)</span>
              <span id="dt-header-sub" style="font-size:12.5px; font-weight:500; color:var(--text-muted);">회원번호 100482 · 홍*동 · 가입 2026.08.19</span>
            </div>
            <div style="display:flex; gap:8px;">
              <button type="button" class="btn btn-sm btn-outline" id="btn-unmask" onclick="unmaskMemberDetail()">🔓 마스킹 해제 (10분 후 자동 재마스킹)</button>
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('course')">수강 · 기기 제어 (ADMN-USER-003) →</button>
              <button type="button" class="btn btn-sm btn-danger" onclick="openStatusModal('BLOCKED')">블랙리스트 · 정지 등재 (ADMN-USER-005)</button>
            </div>
          </div>"""

new_dt_header = """        <div class="card">
          <div class="card-header">
            <div class="card-title">
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('list')" style="font-weight:700;">← 회원 목록으로 (ADMN-USER-001)</button>
              <span>회원 상세 정보 (ADMN-USER-002)</span>
              <span id="dt-header-sub" style="font-size:12.5px; font-weight:500; color:var(--text-muted);">회원번호 100482 · 홍*동 · 가입 2026.08.19</span>
            </div>
            <div style="display:flex; gap:8px;">
              <button type="button" class="btn btn-sm btn-outline" id="btn-unmask" onclick="unmaskMemberDetail()">🔓 마스킹 해제 (10분 후 자동 재마스킹)</button>
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('course')">수강 · 기기 제어 (ADMN-USER-003) →</button>
              <button type="button" class="btn btn-sm btn-danger" onclick="openStatusModal('BLOCKED')">블랙리스트 · 정지 등재 (ADMN-USER-005)</button>
            </div>
          </div>"""

if old_dt_header in user_content:
    user_content = user_content.replace(old_dt_header, new_dt_header, 1)
    print("[OK] Updated view-detail card-header with back button in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_dt_header not found in ADMN-USER-001_baseline.html")

# 회원 상세(view-detail) 하단에도 [← 회원 목록으로 (ADMN-USER-001)] 바 추가
old_dt_end = """              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================================================================= -->
      <!-- VIEW 3: ADMN-USER-003 / 004 회원 수강 · 기간 · 기기 제어           -->"""

new_dt_end = """              </div>
            </div>

            <!-- 상세 하단 액션 바 -->
            <div style="margin-top:20px; padding-top:16px; border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
              <button type="button" class="btn btn-outline" onclick="switchView('list')">← 회원 목록으로 (ADMN-USER-001)</button>
              <div style="display:flex; gap:8px;">
                <button type="button" class="btn btn-outline" onclick="switchView('course')">이 회원의 수강 · 기기 제어 (ADMN-USER-003) 이동 →</button>
                <a href="ADMN-PROM-002_baseline.html" class="btn btn-outline">쿠폰 마스터 · 포인트 전역 설정 (PROM-002) ↗</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================================================================= -->
      <!-- VIEW 3: ADMN-USER-003 / 004 회원 수강 · 기간 · 기기 제어           -->"""

if old_dt_end in user_content:
    user_content = user_content.replace(old_dt_end, new_dt_end, 1)
    print("[OK] Added bottom action bar to view-detail in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_dt_end not found in ADMN-USER-001_baseline.html")

# view-course 헤더에도 뒤로가기 버튼 추가
old_course_head = """      <section id="view-course" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">회원 수강 계약 · 기간 강제 조정 · 동시접속/기기 제어 (ADMN-USER-003 / 004)</div>"""

new_course_head = """      <section id="view-course" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('list')" style="font-weight:700;">← 회원 목록</button>
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('detail')" style="font-weight:700;">← 회원 상세</button>
              <span>회원 수강 계약 · 기간 강제 조정 · 동시접속/기기 제어 (ADMN-USER-003 / 004)</span>
            </div>"""

if old_course_head in user_content:
    user_content = user_content.replace(old_course_head, new_course_head, 1)
    print("[OK] Updated view-course header with back buttons in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_course_head not found in ADMN-USER-001_baseline.html")

# view-tags 헤더에도 뒤로가기 버튼 추가
old_tags_head = """      <section id="view-tags" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">수평적 다중 태그(N:M) 그룹 관리 (ADMN-USER-006 — ADMN-PROM-002 쿠폰 대량 발급 타겟 연동)</div>"""

new_tags_head = """      <section id="view-tags" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">
              <button type="button" class="btn btn-sm btn-outline" onclick="switchView('list')" style="font-weight:700;">← 회원 목록</button>
              <span>수평적 다중 태그(N:M) 그룹 관리 (ADMN-USER-006 — ADMN-PROM-002 쿠폰 대량 발급 타겟 연동)</span>
            </div>"""

if old_tags_head in user_content:
    user_content = user_content.replace(old_tags_head, new_tags_head, 1)
    print("[OK] Updated view-tags header with back button in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_tags_head not found in ADMN-USER-001_baseline.html")

# 2-4. switchView(view) 함수 수정: Breadcrumb 동적 업데이트 및 pushState URL 파라미터 연동
old_switch_view = """    function switchView(view) {
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.subview-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('view-' + view).classList.add('active');
      document.getElementById('tab-btn-' + view).classList.add('active');
    }"""

new_switch_view = """    const VIEW_META = {
      'list': {
        code: 'ADMN-USER-001',
        title: '회원 목록 조회',
        crumb: '회원 목록 조회'
      },
      'detail': {
        code: 'ADMN-USER-002',
        title: '회원 상세 정보 (CS 원스톱 창구)',
        crumb: '회원 상세 정보 (CS 원스톱 창구)'
      },
      'course': {
        code: 'ADMN-USER-003 / 004',
        title: '회원 수강 · 기간 · 기기 제어',
        crumb: '회원 수강 · 기간 · 기기 제어'
      },
      'tags': {
        code: 'ADMN-USER-006',
        title: '회원 그룹 · 다중 태그 관리',
        crumb: '회원 그룹 · 다중 태그 관리'
      }
    };

    function switchView(view, pushState = true) {
      if (!VIEW_META[view]) view = 'list';
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      const targetPanel = document.getElementById('view-' + view);
      if (targetPanel) targetPanel.classList.add('active');

      const meta = VIEW_META[view];
      const crumbCode = document.getElementById('top-crumb-code');
      const crumbTitle = document.getElementById('top-crumb-title');
      if (crumbCode) crumbCode.textContent = meta.code;
      if (crumbTitle) crumbTitle.textContent = meta.title;

      document.title = `[${meta.code}] ${meta.title} — 산준모닷컴 백오피스 v8.4 Final`;

      if (pushState && window.history && window.history.replaceState) {
        const newUrl = window.location.pathname + '?view=' + view;
        window.history.replaceState({ view: view }, '', newUrl);
      }

      // SNB 활성 메뉴 동기화
      if (window.location.search) {
        document.querySelectorAll('#v4-master-snb .snb-item').forEach(item => {
          const href = item.getAttribute('href') || '';
          if (href.indexOf('view=' + view) !== -1) {
            item.classList.add('active');
          } else if (href.indexOf('ADMN-USER-001_baseline.html') !== -1) {
            item.classList.remove('active');
          }
        });
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    window.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(window.location.search);
      const initialView = params.get('view') || 'list';
      switchView(initialView, false);
    });"""

if old_switch_view in user_content:
    user_content = user_content.replace(old_switch_view, new_switch_view, 1)
    print("[OK] Updated switchView and added DOMContentLoaded in ADMN-USER-001_baseline.html")
else:
    print("[WARN] old_switch_view not found in ADMN-USER-001_baseline.html")

with open(user_path, "w", encoding="utf-8") as f:
    f.write(user_content)

print("[COMPLETE] Successfully processed common-snb.js and ADMN-USER-001_baseline.html")
