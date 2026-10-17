import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

html_content = r'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[ADMN-USER-001~006] 일반 회원 · 상세 CS · 수강 · 태그 통합 관리 — 산준모닷컴 백오피스 v8.4 Final</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <link id="v4-common-css" rel="stylesheet" href="common-v84.css" />
  <script id="v4-common-snb" src="common-snb.js" defer></script>
  <style>
    :root {
      --bg-main: #F3F5F9;
      --bg-card: #FFFFFF;
      --bg-subtle: #F8FAFC;
      --text-main: #0F172A;
      --text-sub: #475569;
      --text-muted: #64748B;
      --border: #E2E8F0;
      --border-strong: #CBD5E1;
      --primary: #2563EB;
      --primary-hover: #1D4ED8;
      --primary-soft: #EFF6FF;
      --primary-border: #BFDBFE;
      --success: #059669;
      --success-soft: #ECFDF5;
      --success-border: #A7F3D0;
      --warning: #D97706;
      --warning-soft: #FFFBEB;
      --warning-border: #FDE68A;
      --danger: #DC2626;
      --danger-soft: #FEF2F2;
      --danger-border: #FECACA;
      --purple: #7C3AED;
      --purple-soft: #F5F3FF;
      --purple-border: #DDD6FE;
      --radius-md: 10px;
      --radius-lg: 14px;
      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      font-size: 13px;
      line-height: 1.5;
    }

    #v4-root-shell {
      margin-left: 260px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header.top-bar.v4-gen3-topbar {
      height: 60px;
      background: #FFFFFF;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 28px;
      position: sticky;
      top: 0;
      z-index: 900;
    }
    .crumb { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-sub); }
    .crumb-code {
      background: #1E293B;
      color: #F8FAFC;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 5px;
    }

    .subview-bar {
      background: #FFFFFF;
      border-bottom: 1px solid var(--border);
      padding: 12px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .subview-switcher {
      display: inline-flex;
      background: #F1F5F9;
      padding: 4px;
      border-radius: 10px;
      border: 1px solid var(--border);
      gap: 4px;
    }
    .subview-btn {
      border: none;
      background: transparent;
      padding: 8px 16px;
      border-radius: 7px;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-sub);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
    }
    .subview-btn.active {
      background: #FFFFFF;
      color: var(--primary);
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
    }

    .main-container {
      padding: 22px 28px 60px;
      max-width: 1640px;
      width: 100%;
      margin: 0 auto;
    }
    .view-panel { display: none; }
    .view-panel.active { display: block; }

    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
      margin-bottom: 18px;
    }
    .kpi-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: border-color 0.15s;
    }
    .kpi-card:hover { border-color: var(--primary); }
    .kpi-card .k-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
    .kpi-card .k-title { font-size: 12px; font-weight: 700; color: var(--text-sub); }
    .kpi-card .k-num { font-size: 22px; font-weight: 800; color: var(--text-main); margin: 2px 0 4px; }
    .kpi-card .k-sub { font-size: 11.5px; color: var(--text-muted); }

    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      margin-bottom: 18px;
      overflow: hidden;
    }
    .card-header {
      padding: 13px 18px;
      background: #FAFBFD;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
    }
    .card-title { font-size: 14px; font-weight: 800; color: var(--text-main); display: flex; align-items: center; gap: 8px; }
    .card-body { padding: 18px; }

    /* Search Table */
    .search-tbl { width: 100%; border-collapse: collapse; }
    .search-tbl th {
      width: 120px;
      background: #F8FAFC;
      border: 1px solid var(--border);
      padding: 9px 14px;
      text-align: left;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-sub);
    }
    .search-tbl td {
      border: 1px solid var(--border);
      padding: 9px 14px;
      background: #FFFFFF;
    }

    .chip-group { display: inline-flex; gap: 4px; flex-wrap: wrap; vertical-align: middle; }
    .chip {
      padding: 4px 10px;
      border: 1px solid var(--border-strong);
      border-radius: 6px;
      background: #FFFFFF;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-sub);
      cursor: pointer;
    }
    .chip.active {
      background: var(--primary-soft);
      color: var(--primary);
      border-color: var(--primary-border);
      font-weight: 700;
    }

    .f-input, .f-select, .f-textarea {
      height: 32px;
      padding: 0 10px;
      border: 1px solid var(--border-strong);
      border-radius: 6px;
      font-size: 12.5px;
      font-family: inherit;
      color: var(--text-main);
      background: #FFFFFF;
    }
    .f-textarea { height: auto; padding: 8px 10px; width: 100%; }

    .btn {
      height: 32px;
      padding: 0 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      border: 1px solid transparent;
      font-family: inherit;
      text-decoration: none;
      white-space: nowrap;
    }
    .btn-sm { height: 27px; padding: 0 9px; font-size: 11.5px; }
    .btn-primary { background: var(--primary); color: #FFFFFF; }
    .btn-primary:hover { background: var(--primary-hover); }
    .btn-dark { background: #0F172A; color: #FFFFFF; }
    .btn-outline { background: #FFFFFF; border-color: var(--border-strong); color: var(--text-main); }
    .btn-outline:hover { background: #F8FAFC; }
    .btn-danger { background: var(--danger-soft); border-color: var(--danger-border); color: var(--danger); }
    .btn-warning { background: var(--warning-soft); border-color: var(--warning-border); color: #B45309; }
    .btn:disabled, .btn-off {
      background: #E2E8F0 !important;
      color: #94A3B8 !important;
      border-color: #CBD5E1 !important;
      cursor: not-allowed !important;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 11px;
      font-weight: 700;
      white-space: nowrap;
    }
    .badge-green { background: var(--success-soft); color: var(--success); border: 1px solid var(--success-border); }
    .badge-blue { background: var(--primary-soft); color: var(--primary); border: 1px solid var(--primary-border); }
    .badge-amber { background: var(--warning-soft); color: #B45309; border: 1px solid var(--warning-border); }
    .badge-red { background: var(--danger-soft); color: var(--danger); border: 1px solid var(--danger-border); }
    .badge-purple { background: var(--purple-soft); color: var(--purple); border: 1px solid var(--purple-border); }
    .badge-gray { background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }

    .data-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    .data-table th {
      background: #F8FAFC;
      color: var(--text-sub);
      font-weight: 700;
      font-size: 11.5px;
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    .data-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    .data-table tbody tr:hover { background: #F8FAFC; }
    .data-table tbody tr.selected-row { background: #EFF6FF; }
    .tr-right { text-align: right !important; }

    .kv-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    .kv-table th {
      width: 140px;
      background: #F8FAFC;
      padding: 10px 14px;
      text-align: left;
      font-weight: 700;
      color: var(--text-sub);
      border: 1px solid var(--border);
    }
    .kv-table td {
      padding: 10px 14px;
      border: 1px solid var(--border);
      background: #FFFFFF;
    }

    /* Summary Strip in Detail View */
    .sum-strip {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FFFFFF;
      overflow: hidden;
    }
    .sum-cell {
      padding: 12px 14px;
      border-right: 1px solid var(--border);
    }
    .sum-cell:last-child { border-right: none; }
    .sum-lbl { font-size: 11.5px; color: var(--text-muted); font-weight: 600; display: block; }
    .sum-val { font-size: 18px; font-weight: 800; color: var(--text-main); margin-top: 2px; display: block; }

    /* CS 6 Tabs */
    .cs-tabs {
      display: flex;
      border-bottom: 2px solid var(--border);
      gap: 2px;
      margin-bottom: 14px;
    }
    .cs-tab {
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-sub);
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-bottom: none;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .cs-tab.active {
      background: #FFFFFF;
      color: var(--primary);
      border-bottom: 2px solid #FFFFFF;
      margin-bottom: -2px;
    }
    .cs-pane { display: none; }
    .cs-pane.active { display: block; }

    .policy-banner {
      background: #FFFBEB;
      border: 1px solid #FDE68A;
      border-left: 4px solid #D97706;
      border-radius: 8px;
      padding: 11px 15px;
      font-size: 12px;
      color: #78350F;
    }

    /* Modals */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(2px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-backdrop.show { display: flex; }
    .modal-box {
      background: #FFFFFF;
      border-radius: 12px;
      width: 100%;
      max-width: 560px;
      box-shadow: 0 20px 45px rgba(15, 23, 42, 0.25);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    .modal-head {
      padding: 15px 20px;
      background: #0F172A;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 14px;
      font-weight: 800;
    }
    .modal-body { padding: 18px 20px; max-height: 78vh; overflow-y: auto; }
    .modal-foot {
      padding: 13px 20px;
      background: #F8FAFC;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }

    .pair-box {
      display: grid;
      grid-template-columns: 1fr 30px 1fr;
      align-items: center;
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      margin-top: 10px;
    }

    .toast-msg {
      position: fixed;
      bottom: 26px;
      right: 26px;
      background: #0F172A;
      color: #FFFFFF;
      padding: 13px 20px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.25);
      z-index: 3000;
      display: none;
    }
  </style>
</head>
<body>
  <aside id="v4-master-snb"></aside>

  <div id="v4-root-shell">
    <header class="top-bar v4-gen3-topbar">
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
    </header>

    <div class="subview-bar">
      <div class="subview-switcher">
        <button type="button" class="subview-btn active" id="tab-btn-list" onclick="switchView('list')">
          1. 회원 목록 조회 (ADMN-USER-001)
        </button>
        <button type="button" class="subview-btn" id="tab-btn-detail" onclick="switchView('detail')">
          2. 회원 상세 · CS 6대 원스톱 탭 (ADMN-USER-002)
        </button>
        <button type="button" class="subview-btn" id="tab-btn-course" onclick="switchView('course')">
          3. 회원 수강 · 기간 · 기기 제어 (ADMN-USER-003/004)
        </button>
        <button type="button" class="subview-btn" id="tab-btn-tags" onclick="switchView('tags')">
          4. 그룹 · 다중 태그 관리 (ADMN-USER-006)
        </button>
      </div>
      <div style="display:flex; gap:8px;">
        <button type="button" class="btn btn-sm btn-outline" onclick="openPointModal()">＋ 수동 무상 포인트 지급/차감 (002-P1)</button>
        <button type="button" class="btn btn-sm btn-dark" onclick="openExcelModal()">🔒 엑셀 다운로드 (001-P1)</button>
      </div>
    </div>

    <div id="v4-page-body" class="main-container content-wrap">

      <!-- ================================================================= -->
      <!-- VIEW 1: ADMN-USER-001 회원 목록 조회                               -->
      <!-- ================================================================= -->
      <section id="view-list" class="view-panel active">

        <!-- 상태 스코어카드 (5칸) -->
        <div class="kpi-grid">
          <div class="kpi-card" onclick="filterByStatus('ALL')">
            <div class="k-top"><span class="k-title">전체 회원</span><span class="badge badge-blue">ALL</span></div>
            <div class="k-num">12,480</div>
            <div class="k-sub">산준모 카페 전환 회원 포함</div>
          </div>
          <div class="kpi-card" onclick="filterByStatus('ACTIVE')">
            <div class="k-top"><span class="k-title">정상 회원</span><span class="badge badge-green">ACTIVE</span></div>
            <div class="k-num">11,902</div>
            <div class="k-sub">활성 수강 · 정상 로그인</div>
          </div>
          <div class="kpi-card" onclick="filterByStatus('DORMANT')">
            <div class="k-top"><span class="k-title">휴면 (1년 미접속)</span><span class="badge badge-amber">DORMANT</span></div>
            <div class="k-num">521</div>
            <div class="k-sub">전환 30일·14일 전 사전 통지 메일</div>
          </div>
          <div class="kpi-card" onclick="filterByStatus('BLOCKED')">
            <div class="k-top"><span class="k-title">정지 · 블랙리스트</span><span class="badge badge-red">ADMN-USER-005</span></div>
            <div class="k-num" style="color:var(--danger);">57</div>
            <div class="k-sub">마이너스 포인트 · 부정공유 정지</div>
          </div>
          <div class="kpi-card" onclick="filterByStatus('TODAY')">
            <div class="k-top"><span class="k-title">오늘 신규 가입</span><span class="badge badge-purple">TODAY</span></div>
            <div class="k-num">38</div>
            <div class="k-sub">웰컴 5,000P + 10% 쿠폰(D+21)</div>
          </div>
        </div>

        <!-- 다중 조건 검색 -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">다중 조건 검색 (원본 DB 조회 후 응답만 마스킹 · 2자 미만 검색 거부)</div>
            <span style="font-size:11.5px; color:var(--text-muted);">조회 조건은 GET 파라미터로 유지되어 상세 진입 후 뒤로가기 시 복원됩니다.</span>
          </div>
          <div class="card-body" style="padding:14px 18px;">
            <table class="search-tbl">
              <tbody>
                <tr>
                  <th>가입일</th>
                  <td>
                    <input type="date" class="f-input" value="2026-07-17" /> ~
                    <input type="date" class="f-input" value="2026-10-17" />
                    <div class="chip-group" style="margin-left:6px;">
                      <span class="chip">오늘</span>
                      <span class="chip">7일</span>
                      <span class="chip active">3개월</span>
                      <span class="chip">1년</span>
                      <span class="chip">전체</span>
                    </div>
                  </td>
                  <th>회원 상태</th>
                  <td>
                    <div class="chip-group" id="status-chips">
                      <span class="chip active" onclick="filterByStatus('ALL')">전체</span>
                      <span class="chip" onclick="filterByStatus('ACTIVE')">정상</span>
                      <span class="chip" onclick="filterByStatus('DORMANT')">휴면</span>
                      <span class="chip" onclick="filterByStatus('BLOCKED')">정지·BL</span>
                      <span class="chip" onclick="filterByStatus('LOCK5')">비밀번호 5회 잠금</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <th>검색어</th>
                  <td>
                    <select class="f-select" style="width:130px;">
                      <option>이름</option>
                      <option>이메일(ID)</option>
                      <option>휴대폰 뒤 4자리</option>
                      <option>회원번호</option>
                      <option>산준모 카페 ID</option>
                    </select>
                    <input type="text" id="kw-input" class="f-input" style="width:240px;" placeholder="이름 / 이메일 / 휴대폰 뒤 4자리 / 회원번호" />
                  </td>
                  <th>가입 방식</th>
                  <td>
                    <div class="chip-group">
                      <span class="chip active">전체</span>
                      <span class="chip">email</span>
                      <span class="chip">naver</span>
                      <span class="chip">kakao</span>
                      <span class="chip">google</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <th>보유 포인트</th>
                  <td>
                    <input type="number" class="f-input" style="width:90px;" value="0" /> ~
                    <input type="text" class="f-input" style="width:100px;" placeholder="제한없음" /> P
                    <label style="margin-left:10px; font-size:12px; font-weight:700; color:var(--danger); cursor:pointer;">
                      <input type="checkbox" id="chk-minus-only" onchange="toggleMinusFilter(this.checked)" /> 마이너스 포인트 보유자만 (환불 회수 부채)
                    </label>
                  </td>
                  <th>태그 · 그룹</th>
                  <td>
                    <select class="f-select" style="width:220px;">
                      <option value="">전체 (ADMN-USER-006 태그 연동)</option>
                      <option value="TAG-FREE-30D">무료회원 × 최근 30일 로그인 (4,208명)</option>
                      <option value="TAG-CAFE-AUTH">산준모 카페 정회원 인증 (8,940명)</option>
                      <option value="TAG-PASS-CLASS">2026 산업안전기사 환급반 (1,450명)</option>
                    </select>
                  </td>
                </tr>
                <tr>
                  <th>최종 접속</th>
                  <td>
                    <select class="f-select" style="width:170px;">
                      <option>전체</option>
                      <option>30일 이상 미접속</option>
                      <option>90일 이상 미접속</option>
                      <option>1년 경과 (휴면 전환 대상)</option>
                    </select>
                  </td>
                  <th>배송 주소</th>
                  <td>
                    <label style="font-size:12px; margin-right:14px; cursor:pointer;">
                      <input type="checkbox" /> 기본 배송지 등록자
                    </label>
                    <label style="font-size:12px; font-weight:700; color:#B45309; cursor:pointer;">
                      <input type="checkbox" /> 주소 미등록 (교재 주문 건 발송 불가 CS 추출용)
                    </label>
                  </td>
                </tr>
              </tbody>
            </table>
            <div style="display:flex; justify-content:center; gap:8px; margin-top:12px;">
              <button type="button" class="btn btn-outline" onclick="resetFilters()">조건 초기화</button>
              <button type="button" class="btn btn-dark" onclick="showToast('검색 조건 원문이 admin_access_log에 기록되었습니다.')">조회</button>
            </div>
          </div>
        </div>

        <!-- 툴바 & 목록 그리드 -->
        <div class="card">
          <div class="card-header">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:13px;">전체 <strong id="grid-total-cnt">12,480</strong>건 · 선택 <strong id="sel-cnt">0</strong>건</span>
              <span class="badge badge-gray">개인정보 마스킹 ON (목록 해제 불가)</span>
              <span class="badge badge-blue">포인트 실시간 합산 정상</span>
            </div>
            <div style="display:flex; gap:6px;">
              <button type="button" class="btn btn-sm btn-outline" onclick="openBulkTagModal()">선택 회원 그룹·태그 부여 (ADMN-USER-006)</button>
              <button type="button" class="btn btn-sm btn-outline" onclick="sendBulkMsg()">선택 회원 메시지 발송 (ADMN-CONF-004)</button>
              <button type="button" class="btn btn-sm btn-dark" onclick="openExcelModal()">🔒 엑셀 다운로드</button>
            </div>
          </div>
          <div style="overflow-x:auto;">
            <table class="data-table" id="member-grid">
              <thead>
                <tr>
                  <th style="width:36px;"><input type="checkbox" onchange="toggleAllRows(this.checked)" /></th>
                  <th>가입일 ▾</th>
                  <th>회원번호 / 이름</th>
                  <th>이메일(ID) · 가입방식</th>
                  <th>산준모 카페 ID</th>
                  <th>휴대폰</th>
                  <th class="tr-right">누적 결제 ▾</th>
                  <th class="tr-right">누적 환불 ▾</th>
                  <th class="tr-right">유상 P ▾</th>
                  <th class="tr-right">무상 P ▾</th>
                  <th>상태 / 잠금</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr class="selected-row" data-status="ACTIVE" data-minus="false" onclick="selectMember('100482', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.08.19</td>
                  <td><strong>100482</strong> · 홍*동</td>
                  <td>hon***@naver.com <span class="badge badge-gray">email</span></td>
                  <td><code>sanjun_hong88</code></td>
                  <td>010-****-5678</td>
                  <td class="tr-right" style="font-weight:700;">1,248,000</td>
                  <td class="tr-right">0</td>
                  <td class="tr-right" style="font-weight:700; color:var(--primary);">1,890</td>
                  <td class="tr-right" style="font-weight:700;">5,000</td>
                  <td><span class="badge badge-green">정상</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100482'); switchView('detail');">상세</button></td>
                </tr>
                <tr data-status="ACTIVE" data-minus="false" onclick="selectMember('100479', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.08.18</td>
                  <td><strong>100479</strong> · 김*연</td>
                  <td>soo***@gmail.com <span class="badge badge-gray">google</span></td>
                  <td><code>safety_kim26</code></td>
                  <td>010-****-2211</td>
                  <td class="tr-right" style="font-weight:700;">396,000</td>
                  <td class="tr-right">0</td>
                  <td class="tr-right" style="font-weight:700; color:var(--primary);">2,191</td>
                  <td class="tr-right">0</td>
                  <td><span class="badge badge-green">정상</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100479'); switchView('detail');">상세</button></td>
                </tr>
                <tr data-status="LOCK5" data-minus="false" onclick="selectMember('100451', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.08.14</td>
                  <td><strong>100451</strong> · 박*우</td>
                  <td>jw**@hanmail.net <span class="badge badge-gray">email</span></td>
                  <td><code>park_jw90</code></td>
                  <td>010-****-9043</td>
                  <td class="tr-right" style="font-weight:700;">780,000</td>
                  <td class="tr-right">156,000</td>
                  <td class="tr-right">0</td>
                  <td class="tr-right" style="font-weight:700;">5,000</td>
                  <td>
                    <span class="badge badge-green">정상</span>
                    <span class="badge badge-amber" title="is_locked=true (auto_5fail)">🔒 PW 5회 잠금</span>
                  </td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100451'); switchView('detail');">상세</button></td>
                </tr>
                <tr data-status="DORMANT" data-minus="false" onclick="selectMember('100390', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.07.30</td>
                  <td><strong>100390</strong> · 이*준</td>
                  <td>seo***@naver.com <span class="badge badge-green">naver</span></td>
                  <td><code>lee_sjm77</code></td>
                  <td>010-****-1177</td>
                  <td class="tr-right" style="font-weight:700;">2,140,000</td>
                  <td class="tr-right">0</td>
                  <td class="tr-right" style="font-weight:700; color:var(--primary);">3,440</td>
                  <td class="tr-right">0</td>
                  <td><span class="badge badge-amber">휴면</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100390'); switchView('detail');">상세</button></td>
                </tr>
                <tr data-status="BLOCKED" data-minus="true" onclick="selectMember('100215', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.06.11</td>
                  <td><strong>100215</strong> · 최*아</td>
                  <td>min****@daum.net <span class="badge badge-gray">email</span></td>
                  <td><code>choi_min33</code></td>
                  <td>010-****-3388</td>
                  <td class="tr-right" style="font-weight:700;">324,000</td>
                  <td class="tr-right" style="color:var(--danger); font-weight:700;">324,000</td>
                  <td class="tr-right"><strong style="color:var(--danger);">-2,400</strong></td>
                  <td class="tr-right">0</td>
                  <td>
                    <span class="badge badge-red">정지</span>
                    <span class="badge badge-purple" title="2026-08-09 환불 회수 마이너스 포인트 미납 · 블랙리스트 등재">BL</span>
                  </td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100215'); switchView('detail');">상세</button></td>
                </tr>
                <tr data-status="ACTIVE" data-minus="false" onclick="selectMember('100188', this)">
                  <td onclick="event.stopPropagation()"><input type="checkbox" class="row-chk" onchange="updateSelCount()" /></td>
                  <td>2026.05.28</td>
                  <td><strong>100188</strong> · 정*늘</td>
                  <td>han***@nate.com <span class="badge badge-amber">kakao</span></td>
                  <td><code>jung_sky20</code></td>
                  <td>010-****-6620</td>
                  <td class="tr-right" style="font-weight:700;">468,000</td>
                  <td class="tr-right">0</td>
                  <td class="tr-right" style="font-weight:700; color:var(--primary);">780</td>
                  <td class="tr-right" style="font-weight:700;">5,000</td>
                  <td><span class="badge badge-green">정상</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="event.stopPropagation(); selectMember('100188'); switchView('detail');">상세</button></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style="padding:12px 18px; border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
            <div class="policy-banner" style="flex:1; margin-right:16px;">
              <strong>개인정보 보호 및 포인트 분리 원칙:</strong> 목록의 이름·이메일·휴대폰·주소는 <strong>항상 마스킹</strong>되며 목록에는 해제 버튼이 없습니다(회원 상세 <code>ADMN-USER-002</code>에서 건별 해제 · 10분 후 자동 재마스킹). 포인트는 환불 시 <strong>무상 P 회수 → 유상 P 차감(LIFO 부활)</strong> 처리가 다르므로 반드시 분리 노출합니다.
            </div>
            <div class="chip-group">
              <span class="chip">‹</span>
              <span class="chip active">1</span>
              <span class="chip">2</span>
              <span class="chip">3</span>
              <span class="chip">4</span>
              <span class="chip">5</span>
              <span class="chip">›</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ================================================================= -->
      <!-- VIEW 2: ADMN-USER-002 회원 상세 정보 (CS 원스톱 창구)              -->
      <!-- ================================================================= -->
      <section id="view-detail" class="view-panel">
        <div class="card">
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
          </div>
          <div class="card-body">
            <table class="kv-table">
              <tbody>
                <tr>
                  <th>이름 / 회원번호</th>
                  <td>
                    <strong id="dt-name" style="font-size:14px;">홍*동</strong> (<code id="dt-no">100482</code>)
                    <span id="unmask-timer-badge" class="badge badge-amber" style="display:none; margin-left:6px;">열람 중 · 09:59 후 자동 재마스킹</span>
                    <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">클릭 즉시 <code>admin_access_log</code>에 계정·일시·IP·대상 회원번호가 기록됩니다.</div>
                  </td>
                  <th>회원 상태 · 잠금 분리</th>
                  <td>
                    <span id="dt-status-badge" class="badge badge-green">정상 (ACTIVE)</span>
                    <select id="dt-status-sel" class="f-select" style="width:120px; margin-left:6px;">
                      <option value="ACTIVE">정상</option>
                      <option value="DORMANT">휴면</option>
                      <option value="BLOCKED">정지(BL)</option>
                    </select>
                    <button type="button" class="btn btn-sm btn-outline" onclick="openStatusModal(document.getElementById('dt-status-sel').value)">상태 변경</button>
                    <span id="dt-lock-area" style="margin-left:8px;">
                      <span class="badge badge-gray">로그인 실패 0회 (is_locked=false)</span>
                    </span>
                  </td>
                </tr>
                <tr>
                  <th>이메일(ID)</th>
                  <td id="dt-email">hon***@naver.com</td>
                  <th>가입 방식 · 연동 소셜</th>
                  <td>
                    <span class="badge badge-gray">email 직접 가입</span> · 연동 소셜:
                    <span class="badge badge-green" id="soc-naver">naver <a href="javascript:void(0)" onclick="unlinkSocial('naver')" style="color:inherit; margin-left:4px;">✕</a></span>
                    <span class="badge badge-amber" id="soc-kakao">kakao <a href="javascript:void(0)" onclick="unlinkSocial('kakao')" style="color:inherit; margin-left:4px;">✕</a></span>
                    <span style="font-size:11px; color:var(--text-muted); margin-left:4px;">(마지막 로그인 수단은 해제 불가)</span>
                  </td>
                </tr>
                <tr>
                  <th>휴대폰 / SMS 인증</th>
                  <td>
                    <span id="dt-phone">010-****-5678</span>
                    <span class="badge badge-green">본인인증 완료</span>
                    <span class="badge badge-gray">24h SMS 인증 1/5회 (CONF-008)</span>
                  </td>
                  <th>최종 접속</th>
                  <td>2026.10.17 09:41 · 접속 IP <code>121.***.7.90</code></td>
                </tr>
                <tr>
                  <th>산준모 네이버 카페 ID</th>
                  <td>
                    <input type="text" id="dt-cafe" class="f-input" style="width:190px;" value="sanjun_hong88" />
                    <span style="font-size:11px; color:var(--text-muted); margin-left:6px;">항목명 'ID' 고정('닉네임' 표기 금지 · @ 이메일 형식 검증 제외)</span>
                  </td>
                  <th>마케팅 수신 동의</th>
                  <td>
                    <label style="margin-right:10px;"><input type="checkbox" checked /> SMS/알림톡 동의</label>
                    <label><input type="checkbox" /> 이메일 동의</label>
                    <span style="font-size:11px; color:var(--text-muted); margin-left:6px;">(<code>users.is_marketing_agreed</code> · 2026.08.19 동의)</span>
                  </td>
                </tr>
                <tr>
                  <th>기본 배송지</th>
                  <td id="dt-addr">(07803) 서울 강서구 마곡중앙*로 *** ***동 ***호</td>
                  <th>DI (중복가입 · 웰컴혜택)</th>
                  <td id="dt-di">
                    <code>DI-8842-****-9910</code>
                    <span class="badge badge-green">최초 가입 · 웰컴 혜택(5,000P + 10% 쿠폰 D+21) 지급 완료</span>
                  </td>
                </tr>
                <tr>
                  <th>비밀번호 · 계정 통제</th>
                  <td>
                    최종 변경 2026.08.19 ·
                    <button type="button" class="btn btn-sm btn-outline" onclick="showToast('가입 이메일로 8자리 임시 비밀번호(24시간 유효)를 발송했습니다. 화면에는 비밀번호를 노출하지 않습니다.')">임시 비밀번호 메일 발송</button>
                    <button type="button" class="btn btn-sm btn-warning" onclick="openPwResetModal()">비밀번호 수동 초기화 (SUPER_ADMIN)</button>
                  </td>
                  <th>관리자 내부 메모</th>
                  <td>
                    <div style="display:flex; gap:6px;">
                      <input type="text" class="f-input" style="flex:1;" placeholder="내부 메모 — 고객 화면·알림톡에 노출되지 않으며 수정 이력이 보존됩니다." value="산업안전기사 필기+실기 올패스 수강생. 교재 배송지 확인 완료." />
                      <button type="button" class="btn btn-sm btn-dark" onclick="showToast('관리자 내부 메모 및 수정 가능 필드가 저장되었습니다.')">저장</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- 보유 포인트 · 쿠폰 · 누적 거래 요약 -->
            <div style="margin-top:18px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="font-size:13px; font-weight:800;">보유 포인트 · 쿠폰 · 누적 거래 요약 <span style="font-size:11.5px; font-weight:500; color:var(--text-muted);">(유상 P: 강좌 실결제 1% 올림·LIFO 부활 / 무상 P: 웰컴·이벤트·CS 보상·환불 시 우선 회수)</span></div>
                <div style="display:flex; gap:6px;">
                  <button type="button" class="btn btn-sm btn-outline" onclick="switchCsTab('points')">포인트 원장 탭 보기</button>
                  <button type="button" class="btn btn-sm btn-primary" onclick="openPointModal()">＋ 포인트 수동 지급/차감 (ADMN-USER-002-P1)</button>
                </div>
              </div>
              <div class="sum-strip">
                <div class="sum-cell">
                  <span class="sum-lbl">유상 포인트 (PAID)</span>
                  <span class="sum-val" id="dt-paid-p" style="color:var(--primary);">1,890 P</span>
                </div>
                <div class="sum-cell">
                  <span class="sum-lbl">무상 포인트 (FREE · 20만 Cap)</span>
                  <span class="sum-val" id="dt-free-p">5,000 P</span>
                </div>
                <div class="sum-cell">
                  <span class="sum-lbl">합계 사용 가능 (1회 5만 한도)</span>
                  <span class="sum-val" id="dt-total-p" style="color:var(--success);">6,890 P</span>
                </div>
                <div class="sum-cell">
                  <span class="sum-lbl">보유 쿠폰</span>
                  <span class="sum-val">2 매</span>
                </div>
                <div class="sum-cell">
                  <span class="sum-lbl">누적 확정 결제액</span>
                  <span class="sum-val" id="dt-paid-amt">1,248,000 원</span>
                </div>
                <div class="sum-cell">
                  <span class="sum-lbl">누적 확정 환불액</span>
                  <span class="sum-val" id="dt-rfd-amt" style="color:var(--danger);">0 원</span>
                </div>
              </div>
              <div class="policy-banner" style="margin-top:8px;">
                <strong>가장 임박한 만료 안내:</strong> 무상 <strong>5,000P</strong> — <strong>2026.11.09 23:59:59 자정</strong> 만료 (웰컴 D+21) · 유상 <strong>1,890P</strong> — 2027.08.19 만료 (만료된 유상 포인트는 환불 부활 시 <strong>D+7 유예 연장</strong> 자동 적용)
              </div>
            </div>

            <!-- CS 원스톱 6대 이력 탭 -->
            <div style="margin-top:22px;">
              <div class="cs-tabs">
                <button type="button" class="cs-tab active" data-tab="orders" onclick="switchCsTab('orders')">주문 내역 <span class="badge badge-gray">4</span></button>
                <button type="button" class="cs-tab" data-tab="refunds" onclick="switchCsTab('refunds')">환불 내역 <span class="badge badge-gray">1</span></button>
                <button type="button" class="cs-tab" data-tab="inquiries" onclick="switchCsTab('inquiries')">1:1 문의 <span class="badge badge-red">2 · 미답변 1</span></button>
                <button type="button" class="cs-tab" data-tab="courses" onclick="switchCsTab('courses')">수강 현황 <span class="badge badge-blue">3</span></button>
                <button type="button" class="cs-tab" data-tab="points" onclick="switchCsTab('points')">포인트 원장</button>
                <button type="button" class="cs-tab" data-tab="logs" onclick="switchCsTab('logs')">관리 이력 (감사 타임라인)</button>
              </div>

              <!-- 탭 1: 주문 내역 (최근 5건) -->
              <div id="cs-pane-orders" class="cs-pane active">
                <table class="data-table">
                  <thead>
                    <tr><th>주문일</th><th>주문번호</th><th>상품명</th><th class="tr-right">실결제액</th><th>결제수단</th><th>상태</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026.08.19</td>
                      <td><a href="ADMN-ORD-001_baseline.html" style="color:var(--primary); font-weight:700;">SJM-20260819-004821 ↗</a></td>
                      <td>2026 산업안전기사 필기+실기 올패스 (강좌+교재 복합)</td>
                      <td class="tr-right" style="font-weight:700;">344,000원</td>
                      <td>신용카드</td>
                      <td><span class="badge badge-green">결제완료</span></td>
                    </tr>
                    <tr>
                      <td>2026.08.25</td>
                      <td><a href="ADMN-ORD-001_baseline.html" style="color:var(--primary); font-weight:700;">SJM-20260825-005104 ↗</a></td>
                      <td>산업안전기사 실기 핵심요약집 (교재 단독 · 면세)</td>
                      <td class="tr-right" style="font-weight:700;">28,000원</td>
                      <td>신용카드</td>
                      <td><span class="badge badge-gray">배송완료</span></td>
                    </tr>
                    <tr>
                      <td>2026.09.02</td>
                      <td><a href="ADMN-ORD-001_baseline.html" style="color:var(--primary); font-weight:700;">SJM-20260902-005933 ↗</a></td>
                      <td>전기기사 필기 이론 단과</td>
                      <td class="tr-right" style="font-weight:700;">89,000원</td>
                      <td>카카오페이</td>
                      <td><span class="badge badge-red">환불</span></td>
                    </tr>
                    <tr>
                      <td>2026.10.05</td>
                      <td><a href="ADMN-ORD-001_baseline.html" style="color:var(--primary); font-weight:700;">SJM-20261005-006471 ↗</a></td>
                      <td>산업안전기사 실기 작업형 특강</td>
                      <td class="tr-right" style="font-weight:700;">69,000원</td>
                      <td>토스페이</td>
                      <td><span class="badge badge-green">결제완료</span></td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>최근 <strong>5</strong>건만 표시 · 전체 4건</span>
                  <a href="ADMN-ORD-001_baseline.html" class="btn btn-sm btn-outline">전체 주문 보기 (ADMN-ORD-001) ↗</a>
                </div>
              </div>

              <!-- 탭 2: 환불 내역 (최근 5건) -->
              <div id="cs-pane-refunds" class="cs-pane">
                <table class="data-table">
                  <thead>
                    <tr><th>신청일</th><th>주문번호</th><th>상품명</th><th>귀책 구분</th><th class="tr-right">공제액</th><th class="tr-right">환급액</th><th>상태</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026.09.04</td>
                      <td><a href="ADMN-RFD-002_baseline.html" style="color:var(--primary); font-weight:700;">SJM-20260902-005933 ↗</a></td>
                      <td>전기기사 필기 이론 단과</td>
                      <td>고객 변심 (반품배송비 왕복 6,000원은 교재 반품 시 고객 귀책만 공제)</td>
                      <td class="tr-right">0원</td>
                      <td class="tr-right" style="font-weight:700; color:var(--danger);">89,000원</td>
                      <td><span class="badge badge-gray">환급완료</span></td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>최근 <strong>5</strong>건만 표시 · 전체 1건</span>
                  <a href="ADMN-RFD-002_baseline.html" class="btn btn-sm btn-outline">전체 환불 보기 (ADMN-RFD-002) ↗</a>
                </div>
              </div>

              <!-- 탭 3: 1:1 문의 (최근 5건) -->
              <div id="cs-pane-inquiries" class="cs-pane">
                <table class="data-table">
                  <thead>
                    <tr><th>접수일</th><th>문의 분류</th><th>제목</th><th>담당자</th><th>상태</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026.10.16</td>
                      <td><span class="badge badge-blue">수강·동시접속</span></td>
                      <td><a href="ADMN-BRD-002_baseline.html" style="color:var(--primary); font-weight:700;">실기 3강 재생 시 동시접속 제한 알림이 뜹니다 ↗</a></td>
                      <td>CS 김상담</td>
                      <td><span class="badge badge-amber">답변 대기</span></td>
                    </tr>
                    <tr>
                      <td>2026.08.28</td>
                      <td><span class="badge badge-gray">배송·교재</span></td>
                      <td><a href="ADMN-BRD-002_baseline.html" style="color:var(--text-main);">교재 배송 송장번호 문의드립니다 ↗</a></td>
                      <td>물류 박출고</td>
                      <td><span class="badge badge-green">답변 완료</span></td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>최근 <strong>5</strong>건만 표시 · 전체 2건 · 미답변 <strong style="color:var(--danger);">1</strong>건</span>
                  <a href="ADMN-BRD-002_baseline.html" class="btn btn-sm btn-outline">전체 문의 보기 (ADMN-BRD-002) ↗</a>
                </div>
              </div>

              <!-- 탭 4: 수강 현황 (계약 전체) -->
              <div id="cs-pane-courses" class="cs-pane">
                <table class="data-table">
                  <thead>
                    <tr><th>강좌명</th><th>시작일</th><th>종료일</th><th>가중평균 진도율</th><th>환급 인정 진도율 (90%)</th><th>동시접속/기기</th><th>상태</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>2026 산업안전기사 필기+실기 올패스</strong> <span class="badge badge-purple">환급반 패키지</span></td>
                      <td>2026.08.19</td>
                      <td>2027.02.18</td>
                      <td><strong>62.4%</strong></td>
                      <td>90% 기준 <span class="badge badge-amber">미달</span></td>
                      <td>1세션 정상 (모바일 2/2)</td>
                      <td><span class="badge badge-green">수강중</span></td>
                    </tr>
                    <tr>
                      <td><strong>산업안전기사 실기 작업형 특강</strong></td>
                      <td>2026.10.05</td>
                      <td>2026.12.04</td>
                      <td><strong>18.0%</strong></td>
                      <td>— (비환급 단과)</td>
                      <td>1세션 정상</td>
                      <td><span class="badge badge-green">수강중</span></td>
                    </tr>
                    <tr>
                      <td><strong>전기기사 필기 이론 단과</strong></td>
                      <td>2026.09.02</td>
                      <td>2026.09.04</td>
                      <td>0.0%</td>
                      <td>—</td>
                      <td>—</td>
                      <td><span class="badge badge-red">환불 종료 (연장불가)</span></td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>수강 계약 전체 3건 표시</span>
                  <button type="button" class="btn btn-sm btn-primary" onclick="switchView('course')">수강 기간 · 기기/세션 제어 (ADMN-USER-003) →</button>
                </div>
              </div>

              <!-- 탭 5: 포인트 원장 (최근 10건) -->
              <div id="cs-pane-points" class="cs-pane">
                <table class="data-table" id="dt-point-ledger">
                  <thead>
                    <tr><th>일시</th><th>구분</th><th>사유 · 근거 번호</th><th class="tr-right">유상 P (PAID)</th><th class="tr-right">무상 P (FREE)</th><th>만료일</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026.10.05 14:02</td>
                      <td><span class="badge badge-green">적립</span></td>
                      <td>SJM-20261005-006471 강좌 실결제액 1% 올림 (교재·배송비 제외)</td>
                      <td class="tr-right" style="color:var(--primary); font-weight:700;">+690</td>
                      <td class="tr-right">—</td>
                      <td>2027.10.05</td>
                    </tr>
                    <tr>
                      <td>2026.09.04 11:30</td>
                      <td><span class="badge badge-red">회수</span></td>
                      <td>환불 RFD-2609-0113 · 기적립 포인트 환불 회수 (무상 우선 차감 → 부족 시 유상 차감)</td>
                      <td class="tr-right" style="color:var(--danger); font-weight:700;">-890</td>
                      <td class="tr-right">—</td>
                      <td>—</td>
                    </tr>
                    <tr>
                      <td>2026.08.19 09:15</td>
                      <td><span class="badge badge-green">적립</span></td>
                      <td>SJM-20260819-004821 올패스 강좌 라인 실결제액 1% 적립</td>
                      <td class="tr-right" style="color:var(--primary); font-weight:700;">+2,090</td>
                      <td class="tr-right">—</td>
                      <td>2027.08.19</td>
                    </tr>
                    <tr>
                      <td>2026.08.19 09:12</td>
                      <td><span class="badge badge-blue">웰컴</span></td>
                      <td>신규 가입 웰컴 혜택 (DI 생애 1회 · D+21 자정 만료)</td>
                      <td class="tr-right">—</td>
                      <td class="tr-right" style="font-weight:700;">+5,000</td>
                      <td>2026.09.09</td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>최근 <strong>10</strong>건만 표시 · 결제 차감은 FIFO(만료 임박 무상→유상), 환불 복원은 LIFO(유상→무상), 기적립 회수는 무상 0P 소진 후 유상 마이너스(-) 처리</span>
                  <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">전체 포인트 원장 보기 (ADMN-PROM-002) ↗</a>
                </div>
              </div>

              <!-- 탭 6: 관리 이력 (최근 10건 · 단일 감사 타임라인) -->
              <div id="cs-pane-logs" class="cs-pane">
                <table class="data-table" id="dt-audit-timeline">
                  <thead>
                    <tr><th>일시</th><th>관리자</th><th>행위 구분</th><th>사유 · 상세 내역</th><th>접속 IP</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>2026.10.17 10:41</td>
                      <td>CS 김상담 (admin_kim)</td>
                      <td><span class="badge badge-amber">마스킹 해제</span></td>
                      <td>회원 상세 본인확인 열람 (10분 후 자동 재마스킹 예약)</td>
                      <td><code>121.***.7.90</code></td>
                    </tr>
                    <tr>
                      <td>2026.09.04 11:30</td>
                      <td>재무 이정산 (admin_lee)</td>
                      <td><span class="badge badge-blue">환불 승인</span></td>
                      <td>RFD-2609-0113 · 전기기사 단과 환불 승인 및 기적립 890P 회수</td>
                      <td><code>121.***.7.12</code></td>
                    </tr>
                    <tr>
                      <td>2026.08.19 09:12</td>
                      <td>SYSTEM</td>
                      <td><span class="badge badge-green">웰컴 혜택 발급</span></td>
                      <td>생애 1회 DI 검증 통과 · 무상 5,000P + 10% 쿠폰 자동 발급</td>
                      <td>—</td>
                    </tr>
                  </tbody>
                </table>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:var(--text-muted);">
                  <span>최근 <strong>10</strong>건만 표시 · 수정/삭제 불가(Append-only, 5년 보존)</span>
                  <a href="ADMN-CONF-010_baseline.html" class="btn btn-sm btn-outline">보안 감사 로그 전체 보기 (ADMN-CONF-006/010) ↗</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================================================================= -->
      <!-- VIEW 3: ADMN-USER-003 / 004 회원 수강 · 기간 · 기기 제어           -->
      <!-- ================================================================= -->
      <section id="view-course" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">회원 수강 계약 · 기간 강제 조정 · 동시접속/기기 제어 (ADMN-USER-003 / 004)</div>
            <div style="display:flex; gap:8px;">
              <input type="text" class="f-input" style="width:240px;" value="hon***@naver.com (100482)" placeholder="이메일(ID) / 회원번호 / 휴대폰 뒤 4자리" />
              <button type="button" class="btn btn-sm btn-dark" onclick="showToast('해당 회원의 수강 계약 및 세션 현황을 조회했습니다.')">조회</button>
            </div>
          </div>
          <div class="card-body">
            <!-- 3번 영역: 수강 중인 강좌 계약 목록 -->
            <div style="font-size:13px; font-weight:800; margin-bottom:8px;">1. 수강 중인 강좌 계약 목록 (잔여일 30일 이하 D-N 배지 · 환불 종료 계약은 연장 불가)</div>
            <table class="data-table" style="margin-bottom:20px;">
              <thead>
                <tr>
                  <th style="width:36px;"><input type="radio" name="crs_sel" checked /></th>
                  <th>계약번호</th>
                  <th>강좌명</th>
                  <th>수강 시작일</th>
                  <th>수강 종료일</th>
                  <th>잔여일</th>
                  <th>가중평균 진도율 (ADMN-USER-004)</th>
                  <th>상태</th>
                </tr>
              </thead>
              <tbody>
                <tr class="selected-row">
                  <td><input type="radio" name="crs_sel" checked /></td>
                  <td><code>CRS-2026-8841</code></td>
                  <td><strong>2026 산업안전기사 필기+실기 올패스</strong></td>
                  <td>2026.08.19</td>
                  <td id="crs-end-1"><strong>2027.02.18</strong></td>
                  <td><span class="badge badge-blue">D-124</span></td>
                  <td><strong>62.4%</strong> (재생시간 가중평균 · 24/38강 완료)</td>
                  <td><span class="badge badge-green">수강중</span></td>
                </tr>
                <tr>
                  <td><input type="radio" name="crs_sel" /></td>
                  <td><code>CRS-2026-9102</code></td>
                  <td><strong>산업안전기사 실기 작업형 특강</strong></td>
                  <td>2026.10.05</td>
                  <td><strong>2026.11.04</strong></td>
                  <td><span class="badge badge-amber">D-18</span></td>
                  <td><strong>18.0%</strong> (3/15강 완료)</td>
                  <td><span class="badge badge-green">수강중</span></td>
                </tr>
                <tr style="background:#F8FAFC; color:var(--text-muted);">
                  <td><input type="radio" name="crs_sel" disabled /></td>
                  <td><code>CRS-2026-7901</code></td>
                  <td>전기기사 필기 이론 단과 (환불 완료)</td>
                  <td>2026.09.02</td>
                  <td>2026.09.04</td>
                  <td>—</td>
                  <td>0.0%</td>
                  <td><span class="badge badge-red">환불 종료 (연장 불가)</span></td>
                </tr>
              </tbody>
            </table>

            <!-- 4번 & 5번 영역: 좌우 2단 (기간 강제 조정 + 동시접속/기기 제어) -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:18px;">
              <div class="card" style="margin-bottom:0;">
                <div class="card-header">
                  <div class="card-title">2. 수강 기간 강제 조정 (원 수강기간의 최대 1배수 상한 · 단축 불가)</div>
                  <span class="badge badge-blue">StarPlayer+ DRM 만료일 실시간 동기화</span>
                </div>
                <div class="card-body">
                  <div style="margin-bottom:10px;">
                    <label style="font-weight:700; margin-right:14px;"><input type="radio" name="adj_type" checked /> 종료일 연장 (+N일)</label>
                    <label style="font-weight:700;"><input type="radio" name="adj_type" /> 일시정지 부여 (정지 일수만큼 종료일 자동 순연)</label>
                  </div>
                  <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                    <span style="font-size:12px; font-weight:700;">빠른 프리셋:</span>
                    <button type="button" class="chip" onclick="setExtendDays(7)">+7일</button>
                    <button type="button" class="chip active" onclick="setExtendDays(15)">+15일</button>
                    <button type="button" class="chip" onclick="setExtendDays(30)">+30일</button>
                    <button type="button" class="chip" onclick="setExtendDays(60)">+60일</button>
                    <button type="button" class="chip" onclick="setExtendDays(90)">+90일</button>
                    <input type="number" id="ext-days-input" class="f-input" style="width:80px;" value="15" /> 일
                  </div>
                  <div style="margin-bottom:10px;">
                    <label style="display:block; font-size:12px; font-weight:700; margin-bottom:4px;">조정 사유 (필수 · 최소 10자 · 감사 타임라인 기록)</label>
                    <input type="text" id="ext-reason-input" class="f-input" style="width:100%;" placeholder="예) 병가 입원 증빙 확인에 따른 수강기간 15일 예외 연장 (CS-20261017-09)" />
                  </div>
                  <button type="button" class="btn btn-primary" style="width:100%;" onclick="applyCourseExtend()">수강 기간 조정 확정 및 DRM 만료일 동기화</button>
                </div>
              </div>

              <div class="card" style="margin-bottom:0;">
                <div class="card-header">
                  <div class="card-title">3. 동시 접속 IP/세션 제어 및 등록 기기 리셋</div>
                  <span class="badge badge-amber">11/16 오픈: 동시접속 1세션 통제 우선</span>
                </div>
                <div class="card-body">
                  <table class="data-table" style="margin-bottom:10px;">
                    <thead>
                      <tr><th>구분</th><th>접속 IP / 기기 식별 정보</th><th>최근 재생 시각</th><th>상태 / 제어</th></tr>
                    </thead>
                    <tbody id="session-list-body">
                      <tr>
                        <td><span class="badge badge-blue">PC 웹 세션</span></td>
                        <td><code>211.36.***.104</code> (Chrome · Windows 11)</td>
                        <td>2026.10.17 10:38 (재생중)</td>
                        <td><button type="button" class="btn btn-sm btn-danger" onclick="killSession(this)">세션 강제 로그아웃</button></td>
                      </tr>
                      <tr>
                        <td><span class="badge badge-purple">모바일 1/2</span></td>
                        <td>Galaxy S24 Ultra (<code>UUID-9981-A</code>)</td>
                        <td>2026.10.16 22:14</td>
                        <td><button type="button" class="btn btn-sm btn-outline" onclick="resetDevice(this)">기기 리셋 (당월 1/3회)</button></td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="policy-banner">
                    <strong>통제 정책:</strong> PC는 대수 제한 없이 <strong>동시 재생 1세션</strong>만 허용되며, 중복 접속 시 기존 세션을 강제 종료합니다. (모바일 기기 UUID 등록제도는 2차 고도화 슬롯 · 월 3회 초과 리셋 시 상급자 승인)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================================================================= -->
      <!-- VIEW 4: ADMN-USER-006 그룹 · 다중 태그 관리                        -->
      <!-- ================================================================= -->
      <section id="view-tags" class="view-panel">
        <div class="card">
          <div class="card-header">
            <div class="card-title">수평적 다중 태그(N:M) 그룹 관리 (ADMN-USER-006 — ADMN-PROM-002 쿠폰 대량 발급 타겟 연동)</div>
            <button type="button" class="btn btn-sm btn-primary" onclick="showToast('신규 커스텀 태그가 생성되었습니다.')">＋ 신규 태그 생성</button>
          </div>
          <div class="card-body">
            <table class="data-table">
              <thead>
                <tr><th>태그 코드</th><th>태그명</th><th>조합 조건 (N:M)</th><th class="tr-right">소속 회원 수</th><th>연동 프로모션 (ADMN-PROM-002)</th><th>관리</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>TAG-FREE-30D</code></td>
                  <td><strong>무료회원 × 최근 30일 로그인</strong></td>
                  <td>결제 이력 0건 AND 최종 접속 ≤ 30일</td>
                  <td class="tr-right" style="font-weight:800; color:var(--primary);">4,208 명</td>
                  <td>가을 얼리버드 15% 할인 쿠폰 대량 발급 타겟</td>
                  <td><a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급 이동 ↗</a></td>
                </tr>
                <tr>
                  <td><code>TAG-CAFE-AUTH</code></td>
                  <td><strong>산준모 네이버 카페 인증 회원</strong></td>
                  <td><code>users.cafe_member_id IS NOT NULL</code></td>
                  <td class="tr-right" style="font-weight:800;">8,940 명</td>
                  <td>카페 회원 전용 시크릿 특강 안내</td>
                  <td><a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급 이동 ↗</a></td>
                </tr>
                <tr>
                  <td><code>TAG-PASS-2026</code></td>
                  <td><strong>2026 산업안전기사 환급반 수강생</strong></td>
                  <td>환급반 패키지 결제 완료 (진도율 90% 심사 대상)</td>
                  <td class="tr-right" style="font-weight:800;">1,450 명</td>
                  <td>ADMN-SETT-006 합격 환급 심사 대상 풀</td>
                  <td><a href="ADMN-SETT-006_baseline.html" class="btn btn-sm btn-outline">환급반 관리 ↗</a></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- MODAL 1: ADMN-USER-001-P1 개인정보 엑셀 다운로드 사유 입력 팝업        -->
  <!-- ===================================================================== -->
  <div class="modal-backdrop" id="modal-excel-p1">
    <div class="modal-box">
      <div class="modal-head">
        <span>🔒 개인정보 포함 파일 다운로드 (ADMN-USER-001-P1)</span>
        <button type="button" class="btn btn-sm btn-outline" onclick="closeModal('modal-excel-p1')">✕</button>
      </div>
      <div class="modal-body">
        <div style="background:#FEF2F2; border:1px solid #FECACA; border-left:4px solid #DC2626; border-radius:8px; padding:12px 14px; margin-bottom:14px; font-size:12px; color:#991B1B;">
          <div style="font-weight:800; margin-bottom:4px;">⚠️ 대량 추출 경고 (1,000건 초과) — 이 다운로드는 영구 보안 로그에 기록됩니다</div>
          요청 관리자: <strong>admin_kim (김운영 · 회원관리팀)</strong><br/>
          요청 일시: <strong>2026.10.17 14:07:22</strong> · 접속 IP: <strong>210.***.44.18</strong> (로그에는 원본 IP 적재)<br/>
          추출 대상: <strong id="excel-target-cnt">12,480건</strong> (5,000건 초과 상급자 승인은 2차 오픈 이관 · 1차는 워터마크 + 사유 10자 통제)
        </div>

        <div style="margin-bottom:14px;">
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">
            다운로드 사유 <span style="color:var(--danger);">*</span> <span style="font-weight:500; color:var(--text-muted);">— 최소 10자 필수 (공백·동일문자 반복 거부)</span>
          </label>
          <textarea id="excel-reason" class="f-textarea" rows="3" oninput="validateExcelModal()" placeholder="예) 2026년 4분기 산업안전기사 실기 교재 발송 대상자 주소 확인 요청 (CS-2026-1017-14)"></textarea>
          <div id="excel-reason-help" style="font-size:11.5px; color:var(--danger); margin-top:4px;">10자 이상 입력해 주세요. (현재 0자 / 최소 10자)</div>
        </div>

        <div style="margin-bottom:14px;">
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:6px;">추출 항목 선택 (휴대폰 · 배송 주소는 민감정보로 기본 해제)</label>
          <div style="display:flex; gap:10px; flex-wrap:wrap; font-size:12px;">
            <label><input type="checkbox" class="ex-col-chk" checked onchange="validateExcelModal()" /> 가입일</label>
            <label><input type="checkbox" class="ex-col-chk" checked onchange="validateExcelModal()" /> 이름</label>
            <label><input type="checkbox" class="ex-col-chk" checked onchange="validateExcelModal()" /> 이메일(ID)</label>
            <label style="color:var(--danger); font-weight:700;"><input type="checkbox" class="ex-col-chk" onchange="validateExcelModal()" /> 휴대폰 (민감)</label>
            <label style="color:var(--danger); font-weight:700;"><input type="checkbox" class="ex-col-chk" onchange="validateExcelModal()" /> 배송 주소 (민감)</label>
            <label><input type="checkbox" class="ex-col-chk" checked onchange="validateExcelModal()" /> 보유 포인트(유/무상)</label>
            <label><input type="checkbox" class="ex-col-chk" checked onchange="validateExcelModal()" /> 회원 상태</label>
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">선택한 항목 조합이 그대로 <code>admin_access_log</code>에 기록됩니다.</div>
        </div>

        <div style="background:#F8FAFC; border:1px solid var(--border); border-radius:8px; padding:10px 12px; font-size:12px;">
          <label style="display:block; margin-bottom:6px; cursor:pointer;">
            <input type="checkbox" id="ex-pledge-1" onchange="validateExcelModal()" /> 본 파일을 <strong>업무 목적 외로 사용·전달하지 않겠습니다.</strong>
          </label>
          <label style="display:block; cursor:pointer;">
            <input type="checkbox" id="ex-pledge-2" onchange="validateExcelModal()" /> 다운로드 후 <strong>7일 이내 파기</strong>하겠습니다.
          </label>
        </div>
      </div>
      <div class="modal-foot">
        <button type="button" class="btn btn-outline" onclick="closeModal('modal-excel-p1')">취소 (로그 미기록)</button>
        <button type="button" id="btn-excel-submit" class="btn btn-dark" disabled onclick="submitExcelDownload()">다운로드 실행 (1행 워터마크 삽입)</button>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- MODAL 2: ADMN-USER-002-P1 포인트 수동 지급 / 차감 팝업                 -->
  <!-- ===================================================================== -->
  <div class="modal-backdrop" id="modal-point-p1">
    <div class="modal-box">
      <div class="modal-head">
        <span>＋ 수동 무상 포인트 지급 · 차감 (ADMN-USER-002-P1)</span>
        <button type="button" class="btn btn-sm btn-outline" onclick="closeModal('modal-point-p1')">✕</button>
      </div>
      <div class="modal-body">
        <div style="background:#F8FAFC; border:1px solid var(--border); border-radius:8px; padding:10px 14px; margin-bottom:12px; font-size:12px;">
          대상 회원: <strong id="pt-target-name">홍*동 (100482 · hon***@naver.com)</strong><br/>
          현재 잔액: 유상 <strong id="pt-cur-paid">1,890P</strong> · 무상 <strong id="pt-cur-free">5,000P</strong> (무상 보유 상한 200,000P Cap)
        </div>

        <div style="margin-bottom:12px;">
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">조작 유형 (유상 원장은 실결제 1% 전용이므로 수동 조작 불가 · 무상 원장만 허용)</label>
          <div style="display:flex; gap:16px; font-size:12.5px;">
            <label style="font-weight:700; color:var(--primary); cursor:pointer;">
              <input type="radio" name="pt_mode" value="PLUS" checked onchange="updatePointPreview()" /> 무상 지급 (+)
            </label>
            <label style="font-weight:700; color:var(--danger); cursor:pointer;">
              <input type="radio" name="pt_mode" value="MINUS" onchange="updatePointPreview()" /> 무상 차감 (-) (오지급 정정 · 부정취득 회수)
            </label>
          </div>
        </div>

        <div style="grid-template-columns: 1fr 1fr; display:grid; gap:12px; margin-bottom:12px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">포인트 수량 (1회 상한 30,000P)</label>
            <input type="number" id="pt-amount" class="f-input" style="width:100%;" value="3000" min="1" max="30000" oninput="updatePointPreview()" />
          </div>
          <div>
            <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">유효기간 (무기한 불가 · 기본 +90일)</label>
            <select id="pt-exp" class="f-select" style="width:100%;">
              <option value="30">지급일 +30일 (23:59:59 만료)</option>
              <option value="90" selected>지급일 +90일 (기본값)</option>
              <option value="180">지급일 +180일</option>
            </select>
          </div>
        </div>

        <div style="margin-bottom:12px;">
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">지급/차감 사유 (정형 사유 + 상세 10자 이상 · point.memo 내부 저장)</label>
          <select id="pt-reason-cat" class="f-select" style="width:100%; margin-bottom:6px;">
            <option>CS 장애/불편 보상</option>
            <option>이벤트 당첨 수동 지급</option>
            <option>오지급 포인트 회수 차감</option>
            <option>기타 관리자 직권 조정</option>
          </select>
          <input type="text" id="pt-reason-txt" class="f-input" style="width:100%;" oninput="updatePointPreview()" placeholder="최소 10자 이상 상세 사유 입력 (회원 화면에는 노출되지 않습니다)" value="실기 3강 일시 스트리밍 지연에 따른 CS 보상 지급" />
        </div>

        <div style="margin-bottom:12px; font-size:12px;">
          <label style="cursor:pointer; font-weight:700;">
            <input type="checkbox" id="pt-alimtalk" checked /> 카카오 알림톡 안내 발송 (차감 선택 시 기본 해제)
          </label>
        </div>

        <!-- 지급 전/후 비교 박스 -->
        <div class="pair-box">
          <div>
            <div style="font-size:11px; color:var(--text-muted); font-weight:700;">조작 전 잔액</div>
            <div style="font-size:13px; font-weight:800; margin-top:2px;">유상 1,890P / 무상 5,000P</div>
            <div style="font-size:11.5px; color:var(--text-sub);">합계 6,890P</div>
          </div>
          <div style="text-align:center; font-weight:800; color:var(--primary);">→</div>
          <div>
            <div style="font-size:11px; color:var(--primary); font-weight:700;">조작 후 예상 잔액</div>
            <div id="pt-after-detail" style="font-size:13px; font-weight:800; margin-top:2px; color:var(--primary);">유상 1,890P / 무상 8,000P</div>
            <div id="pt-after-sum" style="font-size:11.5px; font-weight:700; color:var(--success);">합계 9,890P</div>
          </div>
        </div>
        <div style="font-size:11px; color:var(--text-muted); margin-top:6px;">※ 되돌리기(Undo) 기능은 없으며, 오지급 시 반대 방향 차감 건으로 상계하여 두 건 모두 원장에 보존합니다.</div>
      </div>
      <div class="modal-foot">
        <button type="button" class="btn btn-outline" onclick="closeModal('modal-point-p1')">취소</button>
        <button type="button" id="btn-pt-submit" class="btn btn-primary" onclick="submitManualPoint()">지급 확정</button>
      </div>
    </div>
  </div>

  <!-- ===================================================================== -->
  <!-- MODAL 3: 회원 상태 변경 / 블랙리스트 등재 (ADMN-USER-005)              -->
  <!-- ===================================================================== -->
  <div class="modal-backdrop" id="modal-status">
    <div class="modal-box" style="max-width:480px;">
      <div class="modal-head">
        <span>회원 상태 변경 · 블랙리스트 통제 (ADMN-USER-005)</span>
        <button type="button" class="btn btn-sm btn-outline" onclick="closeModal('modal-status')">✕</button>
      </div>
      <div class="modal-body">
        <div class="policy-banner" style="margin-bottom:12px;">
          <strong>정지(BLOCKED) 전환 시 즉시 효력:</strong> 로그인이 즉시 차단되며 진행 중인 VOD 수강 재생도 차단됩니다. 진행 중인 환불 건이 있으면 사전 확인이 필요합니다.
        </div>
        <div style="margin-bottom:10px;">
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">변경할 상태</label>
          <select id="modal-st-val" class="f-select" style="width:100%;">
            <option value="ACTIVE">정상 (ACTIVE)</option>
            <option value="DORMANT">휴면 (DORMANT)</option>
            <option value="BLOCKED">정지 · 블랙리스트 등재 (BLOCKED)</option>
          </select>
        </div>
        <div>
          <label style="display:block; font-size:12px; font-weight:800; margin-bottom:4px;">상태 변경 사유 (필수 · 최소 10자)</label>
          <textarea id="modal-st-reason" class="f-textarea" rows="3" placeholder="예) 환불 후 마이너스 포인트(-2,400P) 미납 및 계정 불법 공유 적발에 따른 정지 처리"></textarea>
        </div>
      </div>
      <div class="modal-foot">
        <button type="button" class="btn btn-outline" onclick="closeModal('modal-status')">취소</button>
        <button type="button" class="btn btn-danger" onclick="confirmStatusChange()">상태 변경 확정</button>
      </div>
    </div>
  </div>

  <div class="toast-msg" id="toast-box"></div>

  <script>
    const MEMBERS = {
      '100482': {
        no: '100482', maskedName: '홍*동', realName: '홍길동',
        maskedEmail: 'hon***@naver.com', realEmail: 'hong88@naver.com',
        maskedPhone: '010-****-5678', realPhone: '010-3921-5678',
        maskedAddr: '(07803) 서울 강서구 마곡중앙*로 *** ***동 ***호',
        realAddr: '(07803) 서울 강서구 마곡중앙6로 42 사이언스파크 102동 1104호',
        cafeId: 'sanjun_hong88', joinDate: '2026.08.19', status: 'ACTIVE',
        lockHtml: '<span class="badge badge-gray">로그인 실패 0회 (is_locked=false)</span>',
        paidP: 1890, freeP: 5000, paidAmt: '1,248,000 원', rfdAmt: '0 원',
        diHtml: '<code>DI-8842-****-9910</code> <span class="badge badge-green">최초 가입 · 웰컴 혜택(5,000P + 10% 쿠폰 D+21) 지급 완료</span>'
      },
      '100479': {
        no: '100479', maskedName: '김*연', realName: '김수연',
        maskedEmail: 'soo***@gmail.com', realEmail: 'sooyeon26@gmail.com',
        maskedPhone: '010-****-2211', realPhone: '010-8421-2211',
        maskedAddr: '(06234) 서울 강남구 테헤란*로 ***',
        realAddr: '(06234) 서울 강남구 테헤란로 212 8층',
        cafeId: 'safety_kim26', joinDate: '2026.08.18', status: 'ACTIVE',
        lockHtml: '<span class="badge badge-gray">로그인 실패 0회 (is_locked=false)</span>',
        paidP: 2191, freeP: 0, paidAmt: '396,000 원', rfdAmt: '0 원',
        diHtml: '<code>DI-7712-****-3301</code> <span class="badge badge-green">최초 가입</span>'
      },
      '100451': {
        no: '100451', maskedName: '박*우', realName: '박진우',
        maskedEmail: 'jw**@hanmail.net', realEmail: 'jw90@hanmail.net',
        maskedPhone: '010-****-9043', realPhone: '010-5512-9043',
        maskedAddr: '(48058) 부산 해운대구 센텀*로 ***',
        realAddr: '(48058) 부산 해운대구 센텀중앙로 90 301호',
        cafeId: 'park_jw90', joinDate: '2026.08.14', status: 'ACTIVE',
        lockHtml: '<span class="badge badge-amber">🔒 비밀번호 5회 오류 자동 잠금 (is_locked=true · auto_5fail)</span> <button type="button" class="btn btn-sm btn-outline" onclick="unlockPw5()">잠금 즉시 해제</button>',
        paidP: 0, freeP: 5000, paidAmt: '780,000 원', rfdAmt: '156,000 원',
        diHtml: '<code>DI-5501-****-1120</code> <span class="badge badge-amber">재가입 1회 · 웰컴 혜택 지급 불가 (동일 DI 2025.11.14 수령 이력)</span>'
      },
      '100390': {
        no: '100390', maskedName: '이*준', realName: '이서준',
        maskedEmail: 'seo***@naver.com', realEmail: 'seojun77@naver.com',
        maskedPhone: '010-****-1177', realPhone: '010-7120-1177',
        maskedAddr: '(13529) 경기 성남시 분당구 판교*로 ***',
        realAddr: '(13529) 경기 성남시 분당구 판교역로 166',
        cafeId: 'lee_sjm77', joinDate: '2026.07.30', status: 'DORMANT',
        lockHtml: '<span class="badge badge-gray">1년 미접속 휴면 분리</span>',
        paidP: 3440, freeP: 0, paidAmt: '2,140,000 원', rfdAmt: '0 원',
        diHtml: '<code>DI-3190-****-7741</code> <span class="badge badge-green">최초 가입</span>'
      },
      '100215': {
        no: '100215', maskedName: '최*아', realName: '최민아',
        maskedEmail: 'min****@daum.net', realEmail: 'mina3388@daum.net',
        maskedPhone: '010-****-3388', realPhone: '010-6320-3388',
        maskedAddr: '주소 미등록 (교재 발송 불가)',
        realAddr: '주소 미등록 (교재 발송 불가)',
        cafeId: 'choi_min33', joinDate: '2026.06.11', status: 'BLOCKED',
        lockHtml: '<span class="badge badge-red">관리자 강제 정지 (admin_block) · 블랙리스트(BL)</span>',
        paidP: -2400, freeP: 0, paidAmt: '324,000 원', rfdAmt: '324,000 원',
        diHtml: '<code>DI-9012-****-4412</code> <span class="badge badge-red">unpaid_points_blacklist 등재 (환불 회수 마이너스 유상 -2,400P · 탈퇴 Lock 및 재가입 시 부채 승계)</span>'
      },
      '100188': {
        no: '100188', maskedName: '정*늘', realName: '정하늘',
        maskedEmail: 'han***@nate.com', realEmail: 'haneul20@nate.com',
        maskedPhone: '010-****-6620', realPhone: '010-2910-6620',
        maskedAddr: '(34141) 대전 유성구 대학*로 ***',
        realAddr: '(34141) 대전 유성구 대학로 99',
        cafeId: 'jung_sky20', joinDate: '2026.05.28', status: 'ACTIVE',
        lockHtml: '<span class="badge badge-gray">로그인 실패 0회</span>',
        paidP: 780, freeP: 5000, paidAmt: '468,000 원', rfdAmt: '0 원',
        diHtml: '<code>DI-6610-****-8821</code> <span class="badge badge-green">최초 가입</span>'
      }
    };

    let currentMemberId = '100482';
    let isUnmasked = false;

    function switchView(view) {
      document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.subview-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('view-' + view).classList.add('active');
      document.getElementById('tab-btn-' + view).classList.add('active');
    }

    function selectMember(id, trEl) {
      currentMemberId = id;
      isUnmasked = false;
      document.getElementById('unmask-timer-badge').style.display = 'none';
      document.getElementById('btn-unmask').textContent = '🔓 마스킹 해제 (10분 후 자동 재마스킹)';

      if (trEl) {
        document.querySelectorAll('#member-grid tbody tr').forEach(r => r.classList.remove('selected-row'));
        trEl.classList.add('selected-row');
      }
      renderMemberDetail();
    }

    function renderMemberDetail() {
      const m = MEMBERS[currentMemberId];
      if (!m) return;
      const nameStr = isUnmasked ? m.realName : m.maskedName;
      const emailStr = isUnmasked ? m.realEmail : m.maskedEmail;
      const phoneStr = isUnmasked ? m.realPhone : m.maskedPhone;
      const addrStr = isUnmasked ? m.realAddr : m.maskedAddr;

      document.getElementById('dt-header-sub').textContent = `회원번호 ${m.no} · ${nameStr} · 가입 ${m.joinDate}`;
      document.getElementById('dt-name').textContent = nameStr;
      document.getElementById('dt-no').textContent = m.no;
      document.getElementById('dt-email').textContent = emailStr;
      document.getElementById('dt-phone').textContent = phoneStr;
      document.getElementById('dt-addr').textContent = addrStr;
      document.getElementById('dt-cafe').value = m.cafeId;
      document.getElementById('dt-lock-area').innerHTML = m.lockHtml;
      document.getElementById('dt-di').innerHTML = m.diHtml;

      const stBadge = document.getElementById('dt-status-badge');
      document.getElementById('dt-status-sel').value = m.status;
      if (m.status === 'ACTIVE') { stBadge.className = 'badge badge-green'; stBadge.textContent = '정상 (ACTIVE)'; }
      else if (m.status === 'DORMANT') { stBadge.className = 'badge badge-amber'; stBadge.textContent = '휴면 (DORMANT)'; }
      else { stBadge.className = 'badge badge-red'; stBadge.textContent = '정지 · BL (BLOCKED)'; }

      const paidEl = document.getElementById('dt-paid-p');
      paidEl.textContent = m.paidP.toLocaleString() + ' P';
      paidEl.style.color = m.paidP < 0 ? 'var(--danger)' : 'var(--primary)';

      document.getElementById('dt-free-p').textContent = m.freeP.toLocaleString() + ' P';
      const total = m.paidP + m.freeP;
      const totalEl = document.getElementById('dt-total-p');
      totalEl.textContent = total.toLocaleString() + ' P';
      totalEl.style.color = total < 0 ? 'var(--danger)' : 'var(--success)';

      document.getElementById('dt-paid-amt').textContent = m.paidAmt;
      document.getElementById('dt-rfd-amt').textContent = m.rfdAmt;
    }

    function unmaskMemberDetail() {
      isUnmasked = !isUnmasked;
      renderMemberDetail();
      if (isUnmasked) {
        document.getElementById('unmask-timer-badge').style.display = 'inline-flex';
        document.getElementById('btn-unmask').textContent = '🔒 즉시 재마스킹';
        showToast(`회원번호 ${currentMemberId}의 개인정보 마스킹이 해제되었습니다. (admin_access_log 적재 완료 · 10분 후 자동 재마스킹)`);
      } else {
        document.getElementById('unmask-timer-badge').style.display = 'none';
        document.getElementById('btn-unmask').textContent = '🔓 마스킹 해제 (10분 후 자동 재마스킹)';
        showToast('개인정보가 재마스킹 처리되었습니다.');
      }
    }

    function unlockPw5() {
      MEMBERS[currentMemberId].lockHtml = '<span class="badge badge-green">잠금 해제 완료 (is_locked=false)</span>';
      renderMemberDetail();
      showToast('비밀번호 5회 오류 잠금(auto_5fail)이 즉시 해제되었습니다.');
    }

    function unlinkSocial(provider) {
      const el = document.getElementById('soc-' + provider);
      if (el) el.remove();
      showToast(`${provider.toUpperCase()} 소셜 계정 연동이 해제되었습니다. (마지막 로그인 수단은 해제 불가)`);
    }

    function switchCsTab(tabKey) {
      document.querySelectorAll('.cs-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabKey));
      document.querySelectorAll('.cs-pane').forEach(p => p.classList.remove('active'));
      document.getElementById('cs-pane-' + tabKey).classList.add('active');
    }

    function filterByStatus(st) {
      const rows = document.querySelectorAll('#member-grid tbody tr');
      let cnt = 0;
      rows.forEach(r => {
        const show = (st === 'ALL' || st === 'TODAY' || r.dataset.status === st);
        r.style.display = show ? '' : 'none';
        if (show) cnt++;
      });
      document.getElementById('grid-total-cnt').textContent = st === 'ALL' ? '12,480' : cnt.toLocaleString();
    }

    function toggleMinusFilter(checked) {
      const rows = document.querySelectorAll('#member-grid tbody tr');
      rows.forEach(r => {
        r.style.display = (!checked || r.dataset.minus === 'true') ? '' : 'none';
      });
      if (checked) showToast('환불 회수로 유상 포인트 잔액이 음수(-)가 된 블랙리스트 검토 대상 회원만 필터링했습니다.');
    }

    function resetFilters() {
      document.getElementById('kw-input').value = '';
      document.getElementById('chk-minus-only').checked = false;
      filterByStatus('ALL');
      showToast('검색 조건이 기본값(최근 3개월 · 전체)으로 초기화되었습니다.');
    }

    function toggleAllRows(checked) {
      document.querySelectorAll('.row-chk').forEach(c => c.checked = checked);
      updateSelCount();
    }

    function updateSelCount() {
      const cnt = document.querySelectorAll('.row-chk:checked').length;
      document.getElementById('sel-cnt').textContent = cnt;
    }

    function openBulkTagModal() {
      const cnt = document.querySelectorAll('.row-chk:checked').length;
      showToast(cnt > 0 ? `선택한 ${cnt}명의 회원에게 태그 일괄 부여 레이어를 호출합니다.` : '현재 검색 조건 전체(12,480건) 또는 선택 행 중 대상을 지정하여 태그를 부여합니다.');
    }

    function sendBulkMsg() {
      showToast('단체 메시지 발송(ADMN-CONF-004)으로 이동합니다. (marketing_agree 미동의자는 자동 제외 후 사전 고지)');
    }

    /* ADMN-USER-001-P1 Excel Modal */
    function openExcelModal() {
      document.getElementById('excel-reason').value = '';
      document.getElementById('ex-pledge-1').checked = false;
      document.getElementById('ex-pledge-2').checked = false;
      validateExcelModal();
      document.getElementById('modal-excel-p1').classList.add('show');
    }

    function validateExcelModal() {
      const reason = document.getElementById('excel-reason').value.trim();
      const cols = document.querySelectorAll('.ex-col-chk:checked').length;
      const p1 = document.getElementById('ex-pledge-1').checked;
      const p2 = document.getElementById('ex-pledge-2').checked;
      const help = document.getElementById('excel-reason-help');

      if (reason.length < 10) {
        help.textContent = `10자 이상 입력해 주세요. (현재 ${reason.length}자 / 최소 10자)`;
        help.style.color = 'var(--danger)';
      } else {
        help.textContent = `입력 완료 (${reason.length}자) — admin_access_log.reason에 원문 적재됩니다.`;
        help.style.color = 'var(--success)';
      }

      const valid = (reason.length >= 10 && cols >= 1 && p1 && p2);
      document.getElementById('btn-excel-submit').disabled = !valid;
    }

    function submitExcelDownload() {
      closeModal('modal-excel-p1');
      showToast('admin_access_log 적재 완료 → 1행 워터마크 삽입 파일(members_20261017_1407_adminkim.xlsx) 다운로드가 시작되었습니다.');
    }

    /* ADMN-USER-002-P1 Manual Point Modal */
    function openPointModal() {
      const m = MEMBERS[currentMemberId];
      document.getElementById('pt-target-name').textContent = `${m.maskedName} (${m.no} · ${m.maskedEmail})`;
      document.getElementById('pt-cur-paid').textContent = m.paidP.toLocaleString() + 'P';
      document.getElementById('pt-cur-free').textContent = m.freeP.toLocaleString() + 'P';
      updatePointPreview();
      document.getElementById('modal-point-p1').classList.add('show');
    }

    function updatePointPreview() {
      const m = MEMBERS[currentMemberId];
      const mode = document.querySelector('input[name="pt_mode"]:checked').value;
      const amt = parseInt(document.getElementById('pt-amount').value || '0', 10);
      const reason = document.getElementById('pt-reason-txt').value.trim();

      document.getElementById('pt-alimtalk').checked = (mode === 'PLUS');
      const nextFree = mode === 'PLUS' ? (m.freeP + amt) : (m.freeP - amt);
      const nextSum = m.paidP + nextFree;

      document.getElementById('pt-after-detail').textContent = `유상 ${m.paidP.toLocaleString()}P / 무상 ${nextFree.toLocaleString()}P`;
      document.getElementById('pt-after-sum').textContent = `합계 ${nextSum.toLocaleString()}P` + (nextFree > 200000 ? ' (⚠️ 무상 20만P Cap 초과!)' : '');

      const btn = document.getElementById('btn-pt-submit');
      btn.textContent = mode === 'PLUS' ? '무상 지급 확정' : '무상 차감 확정';
      btn.disabled = (amt < 1 || amt > 30000 || reason.length < 10 || nextFree > 200000);
    }

    function submitManualPoint() {
      const m = MEMBERS[currentMemberId];
      const mode = document.querySelector('input[name="pt_mode"]:checked').value;
      const amt = parseInt(document.getElementById('pt-amount').value || '0', 10);
      const reason = document.getElementById('pt-reason-txt').value.trim();

      m.freeP = mode === 'PLUS' ? (m.freeP + amt) : (m.freeP - amt);
      renderMemberDetail();

      const tbody = document.querySelector('#dt-point-ledger tbody');
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>2026.10.17 14:15</td>
        <td><span class="badge ${mode === 'PLUS' ? 'badge-blue' : 'badge-red'}">${mode === 'PLUS' ? '수동지급' : '수동차감'}</span></td>
        <td>[ADMN-USER-002-P1] ${reason}</td>
        <td class="tr-right">—</td>
        <td class="tr-right" style="font-weight:700; color:${mode === 'PLUS' ? 'var(--primary)' : 'var(--danger)'};">${mode === 'PLUS' ? '+' : '-'}${amt.toLocaleString()}</td>
        <td>2027.01.15</td>
      `;
      tbody.prepend(tr);
      closeModal('modal-point-p1');
      showToast(`무상 포인트 ${mode === 'PLUS' ? '+' : '-'}${amt.toLocaleString()}P 처리가 원장 및 관리 이력에 기록되었습니다.`);
    }

    /* Status Modal */
    function openStatusModal(targetSt) {
      document.getElementById('modal-st-val').value = targetSt || 'BLOCKED';
      document.getElementById('modal-st-reason').value = '';
      document.getElementById('modal-status').classList.add('show');
    }

    function confirmStatusChange() {
      const reason = document.getElementById('modal-st-reason').value.trim();
      if (reason.length < 10) {
        showToast('상태 변경 사유를 최소 10자 이상 입력해 주세요.');
        return;
      }
      const st = document.getElementById('modal-st-val').value;
      MEMBERS[currentMemberId].status = st;
      renderMemberDetail();
      closeModal('modal-status');
      showToast(`회원 상태가 [${st}]로 변경되고 관리 이력 타임라인에 영구 기록되었습니다.`);
    }

    function openPwResetModal() {
      showToast('SUPER_ADMIN 전용 수동 비밀번호 초기화: 유선 본인확인 후 임시값을 설정하고 감사 로그에 사유를 적재합니다.');
    }

    /* Course & Device Control (ADMN-USER-003) */
    function setExtendDays(d) {
      document.getElementById('ext-days-input').value = d;
    }

    function applyCourseExtend() {
      const days = document.getElementById('ext-days-input').value;
      const reason = document.getElementById('ext-reason-input').value.trim();
      if (reason.length < 10) {
        showToast('수강 기간 조정 사유를 최소 10자 이상 입력해 주세요.');
        return;
      }
      document.getElementById('crs-end-1').innerHTML = `<strong style="color:var(--primary);">2027.03.05 (+${days}일 연장됨)</strong>`;
      showToast(`수강 종료일이 +${days}일 연장되고 StarPlayer+ DRM 만료일과 실시간 동기화되었습니다.`);
    }

    function killSession(btn) {
      btn.closest('tr').remove();
      showToast('기존 활성 웹 세션을 강제 로그아웃(초기화)했습니다.');
    }

    function resetDevice(btn) {
      btn.closest('tr').innerHTML = '<td colspan="4" style="color:var(--success); font-weight:700;">모바일 등록 기기 리셋 완료 (DRM 서버 트랜잭션 동기화 완료 · 당월 잔여 리셋 2회)</td>';
      showToast('등록 기기 UUID가 리셋되었습니다.');
    }

    function closeModal(id) {
      document.getElementById(id).classList.remove('show');
    }

    function showToast(msg) {
      const box = document.getElementById('toast-box');
      box.textContent = msg;
      box.style.display = 'block';
      clearTimeout(window.__toastTimer);
      window.__toastTimer = setTimeout(() => { box.style.display = 'none'; }, 3500);
    }
  </script>
</body>
</html>
'''

out_path = os.path.join('prototype', 'ADMN-USER-001_baseline.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[OK] Updated {out_path} ({len(html_content)} bytes)")
