#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] ADMN-SETT-006 (및 연관 화면) 기획서 내부 암호(C-01, P5.1, MMG 중복 플래그, 장절 번호) 제거 및
실무 운영자 친화적 용어 전환 + 4대 제출 증빙(합격증 사본·카페 수기 링크·통장사본·1금융 실명계좌) 완벽 반영 스크립트
"""

import re
from pathlib import Path

PROTO_DIR = Path("prototype")
CLEAN_DIR = Path("prototype_clean")

# ==============================================================================
# 1. ADMN-SETT-006 전용: 운영자 친화적 스크립트 및 UI 문구
# ==============================================================================
SETT_006_OPERATOR_SCRIPT = """<script>
  const BURDEN_LABELS = {
    OPTION_A: "옵션 A (플랫폼 100% 부담 · 강사 차감 없음)",
    OPTION_B: "옵션 B (강사·플랫폼 비율 공동 분담)",
    OPTION_C: "옵션 C (환급금 전액 매출 취소 차감)"
  };

  const state = {
    selectedId: "HRF-202610-01",
    kpiFilter: "ALL",
    items: [
      {
        id: "HRF-202610-01",
        rfdApproveId: "PASS-2026-0041",
        orderId: "ORD-202603-112",
        originPaidMonth: "2026-03",
        studentName: "홍길동",
        studentUid: "hong88 (수험번호: 26-01-09821)",
        courseName: "[환급반] 2026 산업안전기사 100% 환급반 (총결제 450,000원 / 교재 40,000원 제외)",
        rightsHolderId: "RH-0025",
        rightsHolderName: "정종대 (산업안전)",
        contractId: "CT-2026-0501",
        burdenType: "OPTION_B",
        totalPaidAmount: 450000,
        excludedBookAmount: 40000,
        studentRefundAmount: 410000,
        withholdingTax22: 90200,
        netPayoutToStudent: 319800,
        snapshotRsRate: 50,
        snapshotSupportRate: 15,
        deductBasicRs: 102500,
        deductSupport: 15000,
        capRestoreYn: true,
        mmgOverlapFlag: false,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "92.4% (기준 90% 충족)",
        certImageFile: "합격증사본_국가기술자격_홍길동_2026.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/984120",
        reviewPlatformId: "플랫폼·산준모 카페 수기 등록 확인",
        bankbookCopyFile: "통장사본_KB국민은행_홍길동.png",
        bankNameTier1: "KB국민은행 (시중 1금융권)",
        bankAccountRealName: "123-45-****-890 (예금주: 홍길동 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "PENDING",
        memo: "올패스 환급 심사에서 4대 제출자료(합격증 사본·산준모 카페 합격수기 아웃링크·통장사본·1금융권 실명계좌) 확인 완료. 당월 정산 공제 반영 대기 중"
      },
      {
        id: "HRF-202610-02",
        rfdApproveId: "PASS-2026-0039",
        orderId: "ORD-202604-309",
        originPaidMonth: "2026-04",
        studentName: "최안전",
        studentUid: "safe_choi (수험번호: 26-01-44120)",
        courseName: "[환급반] 김안전 산업안전 핵심이론 패스 (강좌 실결제 400,000원)",
        rightsHolderId: "RH-0019",
        rightsHolderName: "김안전 (산업안전 · 월 최저보장 150만원 약정)",
        contractId: "CT-2026-0610",
        burdenType: "OPTION_C",
        totalPaidAmount: 438000,
        excludedBookAmount: 38000,
        studentRefundAmount: 400000,
        withholdingTax22: 88000,
        netPayoutToStudent: 312000,
        snapshotRsRate: 50,
        snapshotSupportRate: 0,
        deductBasicRs: 200000,
        deductSupport: 0,
        capRestoreYn: false,
        mmgOverlapFlag: true,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "100.0% (기준 90% 충족)",
        certImageFile: "합격증사본_큐넷확인서_최안전.png",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/983910",
        reviewPlatformId: "플랫폼·산준모 카페 수기 등록 확인",
        bankbookCopyFile: "통장사본_신한은행_최안전.jpg",
        bankNameTier1: "신한은행 (시중 1금융권)",
        bankAccountRealName: "110-382-****91 (예금주: 최안전 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "월 최저보장금(150만원)을 먼저 산정한 뒤 합격환급 분담금(200,000원)을 별도 차감 완료 (최저보장 약정 강사 동시 발생 건)",
        approvedBy: "재무팀장 (조정식)",
        approvedAt: "2026-10-13 16:40:00"
      },
      {
        id: "HRF-202610-03",
        rfdApproveId: "PASS-2026-0035",
        orderId: "ORD-202602-055",
        originPaidMonth: "2026-02",
        studentName: "이수석",
        studentUid: "top_lee (수험번호: 26-01-10294)",
        courseName: "[초단기환급] 산업안전 필기+실기 올인원 (강좌 실결제 240,000원 / 교재 72,000원 제외)",
        rightsHolderId: "RH-0025",
        rightsHolderName: "정종대 (산업안전)",
        contractId: "CT-2026-0501",
        burdenType: "OPTION_B",
        totalPaidAmount: 312000,
        excludedBookAmount: 72000,
        studentRefundAmount: 240000,
        withholdingTax22: 52800,
        netPayoutToStudent: 187200,
        snapshotRsRate: 50,
        snapshotSupportRate: 15,
        deductBasicRs: 60000,
        deductSupport: 18000,
        capRestoreYn: true,
        mmgOverlapFlag: false,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "95.2% (기준 90% 충족)",
        certImageFile: "합격증사본_산업안전기사_이수석.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/983102",
        reviewPlatformId: "플랫폼·산준모 카페 수기 등록 확인",
        bankbookCopyFile: "통장사본_우리은행_이수석.png",
        bankNameTier1: "우리은행 (시중 1금융권)",
        bankAccountRealName: "1002-841-****12 (예금주: 이수석 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "원 결제월(2026-02) 정산율을 적용하여 당월(2026-10) 강사료 차감(-60,000원) 및 개발지원금 차감·잔여한도 복원(+18,000원) 완료",
        approvedBy: "재무팀장 (조정식)",
        approvedAt: "2026-10-12 11:20:00"
      },
      {
        id: "HRF-202610-04",
        rfdApproveId: "PASS-2026-0029",
        orderId: "ORD-202605-210",
        originPaidMonth: "2026-05",
        studentName: "최유진",
        studentUid: "yj_choi (수험번호: 26-01-07119)",
        courseName: "[환급반] 건설안전기사 필기+실기 패스 (강좌 실결제 300,000원)",
        rightsHolderId: "RH-0031",
        rightsHolderName: "이건설 (건설안전)",
        contractId: "CT-2026-0712",
        burdenType: "OPTION_A",
        totalPaidAmount: 338000,
        excludedBookAmount: 38000,
        studentRefundAmount: 300000,
        withholdingTax22: 66000,
        netPayoutToStudent: 234000,
        snapshotRsRate: 40,
        snapshotSupportRate: 0,
        deductBasicRs: 0,
        deductSupport: 0,
        capRestoreYn: false,
        mmgOverlapFlag: false,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "91.8% (기준 90% 충족)",
        certImageFile: "합격증사본_건설안전기사_최유진.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/982400",
        reviewPlatformId: "플랫폼·산준모 카페 수기 등록 확인",
        bankbookCopyFile: "통장사본_하나은행_최유진.jpg",
        bankNameTier1: "하나은행 (시중 1금융권)",
        bankAccountRealName: "391-910***-**107 (예금주: 최유진 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "계약 옵션 A(플랫폼 100% 부담 · 마케팅비 처리) 적용 — 강사 정산 차감 0원 확정",
        approvedBy: "운영팀장 (김검수)",
        approvedAt: "2026-10-10 14:15:00"
      },
      {
        id: "HRF-202610-05",
        rfdApproveId: "PASS-2026-0044",
        orderId: "ORD-202606-088",
        originPaidMonth: "2026-06",
        studentName: "정하늘",
        studentUid: "sky_jung (수험번호: 26-01-55210)",
        courseName: "[환급반] 산업안전기사 실기 단기완성 환급패스 (강좌 실결제 180,000원)",
        rightsHolderId: "RH-0025",
        rightsHolderName: "정종대 (산업안전)",
        contractId: "CT-2026-0501",
        burdenType: "OPTION_A",
        totalPaidAmount: 212000,
        excludedBookAmount: 32000,
        studentRefundAmount: 180000,
        withholdingTax22: 39600,
        netPayoutToStudent: 140400,
        snapshotRsRate: 50,
        snapshotSupportRate: 0,
        deductBasicRs: 0,
        deductSupport: 0,
        capRestoreYn: false,
        mmgOverlapFlag: false,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "96.0% (기준 90% 충족)",
        certImageFile: "합격증사본_산업안전기사_정하늘.png",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/984511",
        reviewPlatformId: "플랫폼·산준모 카페 수기 등록 확인",
        bankbookCopyFile: "통장사본_IBK기업은행_정하늘.png",
        bankNameTier1: "IBK기업은행 (시중 1금융권)",
        bankAccountRealName: "221-08****-01-011 (예금주: 정하늘 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "PENDING",
        memo: "특강 프로모션 옵션 A(플랫폼 부담) 적용 대상 — 4대 제출 증빙 확인 완료, 정산 반영 승인 대기"
      }
    ],
    auditLogs: [
      {
        time: "2026-10-13 16:40:00",
        actor: "재무팀장 (조정식)",
        targetId: "HRF-202610-02",
        burden: "옵션 C / 김안전",
        action: "합격환급 강사료 차감 확정 (-200,000원) · 최저보장(MMG) 보전금 산정 후 별도 차감",
        basis: "합격증 사본·산준모 카페 수기 링크·신한은행 통장사본·실명계좌 4종 대조 완료"
      },
      {
        time: "2026-10-12 11:20:00",
        actor: "재무팀장 (조정식)",
        targetId: "HRF-202610-03",
        burden: "옵션 B / 정종대",
        action: "강사료 차감(-60,000원) 및 개발지원금 차감(-18,000원) · 잔여 지원금 한도 복원(+18,000원) 확정",
        basis: "합격증 사본·카페 합격수기 링크·우리은행 통장사본·실명계좌 4종 검증 완료 (원결제 2026-02 기준)"
      },
      {
        time: "2026-10-10 14:15:00",
        actor: "운영팀장 (김검수)",
        targetId: "HRF-202610-04",
        burden: "옵션 A / 이건설",
        action: "플랫폼 전액 부담(옵션 A) 확정 — 강사 정산 차감 0원 처리",
        basis: "합격증 사본·카페 수기 링크·하나은행 통장사본·실명계좌 검증 완료 (제세공과금 22% 공제 후 234,000원 지급)"
      }
    ]
  };

  function fmt(n) {
    return Number(n || 0).toLocaleString("ko-KR") + "원";
  }

  function renderTable() {
    const tbody = document.getElementById("refundTableBody");
    if (!tbody) return;
    const q = (document.getElementById("searchInput")?.value || "").trim().toLowerCase();
    const bFilter = document.getElementById("burdenFilter")?.value || "ALL";

    const filtered = state.items.filter(item => {
      if (state.kpiFilter === "PENDING" && item.status !== "PENDING") return false;
      if (state.kpiFilter === "OPT_BC" && !(item.burdenType === "OPTION_B" || item.burdenType === "OPTION_C")) return false;
      if (state.kpiFilter === "OPT_A" && item.burdenType !== "OPTION_A") return false;
      if (state.kpiFilter === "MMG_OVERLAP" && !item.mmgOverlapFlag) return false;
      if (bFilter !== "ALL" && item.burdenType !== bFilter) return false;
      if (q) {
        const hay = `${item.id} ${item.rfdApproveId} ${item.orderId} ${item.studentName} ${item.rightsHolderName} ${item.courseName}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    tbody.innerHTML = filtered.map(item => {
      const isSel = item.id === state.selectedId;
      const burdenBadge = item.burdenType === "OPTION_A"
        ? `<span class="badge badge-primary">옵션 A (플랫폼 100%)</span>`
        : item.burdenType === "OPTION_B"
          ? `<span class="badge badge-warn">옵션 B (강사·플랫폼 공동분담)</span>`
          : `<span class="badge badge-danger">옵션 C (매출 취소차감)</span>`;

      const statusBadge = item.status === "APPROVED"
        ? `<span class="badge badge-success">✔ 정산반영 확정</span>`
        : `<span class="badge badge-warn">⏳ 공제검수 대기</span>`;

      const overlapTag = item.mmgOverlapFlag
        ? `<div style="margin-top:3px;"><span class="badge badge-purple">최저보장(MMG) 적용 강사</span></div>`
        : "";

      return `
        <tr class="${isSel ? "selected" : ""}" style="cursor:pointer;" onclick="selectItem('${item.id}')">
          <td>
            <strong>${item.id}</strong> <span class="badge badge-neutral">${item.rfdApproveId}</span>
            <div class="mono" style="color:var(--text-muted); margin-top:2px;">원주문: ${item.orderId} (${item.originPaidMonth})</div>
          </td>
          <td>
            <strong>${item.studentName}</strong> <span style="font-size:11.5px; color:var(--text-muted);">${item.studentUid}</span>
            <div style="font-size:11.5px; color:var(--text-sub); margin-top:2px;">${item.courseName}</div>
            <div style="font-size:11px; color:var(--primary); margin-top:2px;">📎 합격증사본 O · 카페수기링크 O · 통장사본 O · 1금융실명계좌 O</div>
          </td>
          <td>
            <strong>${item.rightsHolderName}</strong>
            <div style="margin-top:3px;">${burdenBadge}</div>
            ${overlapTag}
          </td>
          <td class="num">
            <strong>${fmt(item.studentRefundAmount)}</strong>
            <div style="font-size:11px; color:var(--text-muted);">세후 실지급: ${fmt(item.netPayoutToStudent)} (22% 공제)</div>
          </td>
          <td class="num" style="color:${item.deductBasicRs > 0 ? "var(--danger)" : "var(--text-muted)"}; font-weight:700;">
            ${item.deductBasicRs > 0 ? "-" + fmt(item.deductBasicRs) : "0원 (차감없음)"}
          </td>
          <td class="num" style="color:${item.deductSupport > 0 ? "var(--danger)" : "var(--text-muted)"}; font-weight:700;">
            ${item.deductSupport > 0 ? "-" + fmt(item.deductSupport) : "0원"}
            ${item.capRestoreYn ? `<div style="font-size:10.5px; color:var(--primary);">+잔여한도 복원 ${fmt(item.deductSupport)}</div>` : ""}
          </td>
          <td>${statusBadge}</td>
        </tr>
      `;
    }).join("");

    updateFooterSummary();
  }

  function renderDetail() {
    const box = document.getElementById("detailBody");
    const badge = document.getElementById("detailBadge");
    if (!box) return;
    const item = state.items.find(x => x.id === state.selectedId) || state.items[0];
    if (!item) return;

    if (badge) {
      badge.className = "badge " + (item.status === "APPROVED" ? "badge-success" : "badge-warn");
      badge.textContent = item.status === "APPROVED" ? "당월 정산 반영 완료" : "검수 · 정산반영 대기";
    }

    box.innerHTML = `
      <div class="kv-grid">
        <div class="kv-label">환급정산 번호 / 심사번호</div>
        <div><strong>${item.id}</strong> (환불심사 번호: <code>${item.rfdApproveId}</code>)</div>
        <div class="kv-label">수강생 / 인정 진도율</div>
        <div><strong>${item.studentName}</strong> (${item.studentUid}) · <span class="badge badge-success">${item.progressRate}</span></div>
        <div class="kv-label">원 주문번호 / 결제월</div>
        <div><code>${item.orderId}</code> (원 결제월: <strong>${item.originPaidMonth}</strong> → 정산 반영월: <strong>${item.appliedMonth}</strong>)</div>
        <div class="kv-label">귀속 강사(권리자)</div>
        <div><strong>${item.rightsHolderName}</strong> (계약번호: <code>${item.contractId}</code>)</div>
        <div class="kv-label">계약상 환급 분담 방식</div>
        <div><strong style="color:var(--primary);">${BURDEN_LABELS[item.burdenType]}</strong></div>
      </div>

      <div class="calc-box" style="background:#EFF6FF; border-color:#BFDBFE;">
        <div style="font-weight:800; font-size:12.5px; color:#1E3A8A; margin-bottom:4px;">
          📋 수강생 제출 4대 필수 자료 및 1금융권 실명 계좌 확인 내역
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">① 합격증 사본 이미지</span>
          <span>📎 <code>${item.certImageFile}</code> <button type="button" class="btn btn-sm" style="padding:2px 7px; font-size:11px;" onclick="showToast('합격증 사본 이미지 원본을 열람합니다: ' + '${item.certImageFile}')">이미지 보기</button></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">② 플랫폼 및 산준모 카페 합격수기 아웃링크</span>
          <span>🔗 <a href="${item.reviewOutlinkUrl}" target="_blank" rel="noopener" style="color:var(--primary); font-weight:700; text-decoration:underline;">${item.reviewOutlinkUrl} ↗</a> <span class="badge badge-purple">${item.reviewPlatformId}</span></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">③ 환급금 입금용 통장 사본</span>
          <span>📎 <code>${item.bankbookCopyFile}</code> <button type="button" class="btn btn-sm" style="padding:2px 7px; font-size:11px;" onclick="showToast('통장 사본 이미지를 열람합니다: ' + '${item.bankbookCopyFile}')">사본 보기</button></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">④ 시중 1금융권 은행명 · 실명 계좌번호</span>
          <span>🏦 <strong>${item.bankNameTier1}</strong> · <code>${item.bankAccountRealName}</code></span>
        </div>
      </div>

      <div class="calc-box">
        <div style="font-weight:800; font-size:12.5px; color:var(--text); margin-bottom:2px;">
          💰 수강생 환급금(제세공과금 22% 제외) 및 강사 정산 차감액 계산 내역
        </div>
        <div class="calc-row">
          <span>패키지 총 실결제액 (교재 정가 ${fmt(item.excludedBookAmount)} 포함)</span>
          <strong class="mono">${fmt(item.totalPaidAmount)}</strong>
        </div>
        <div class="calc-row">
          <span>환급 대상 금액 (도서정가제 교재비 제외 순수 강좌 결제액)</span>
          <strong class="mono" style="color:var(--primary);">${fmt(item.studentRefundAmount)}</strong>
        </div>
        <div class="calc-row">
          <span>수강생 실입금 환급액 (기타소득 제세공과금 22% = -${fmt(item.withholdingTax22)} 원천징수 차감)</span>
          <strong class="mono" style="color:var(--success);">${fmt(item.netPayoutToStudent)}</strong>
        </div>
        <hr style="border:none; border-top:1px dashed var(--border-strong); margin:4px 0;">
        <div class="calc-row">
          <span>강사료(R/S) 환급분 차감액 (원 결제 시점 정산율 ${item.snapshotRsRate}% 적용)</span>
          <strong class="mono" style="color:var(--danger);">${item.deductBasicRs > 0 ? "-" + fmt(item.deductBasicRs) : "0원 (플랫폼 부담)"}</strong>
        </div>
        <div class="calc-row">
          <span>개발지원금 환급분 차감 및 잔여 한도 복원액</span>
          <strong class="mono" style="color:var(--danger);">${item.deductSupport > 0 ? "-" + fmt(item.deductSupport) + " (잔여 한도 +" + fmt(item.deductSupport) + " 복원)" : "0원"}</strong>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">정산 검수 메모</label>
        <textarea id="detailMemo" class="input">${item.memo || ""}</textarea>
      </div>

      <div style="display:flex; gap:8px; justify-content:flex-end;">
        <button type="button" class="btn" onclick="location.href='ADMN-RFD-002_baseline.html'">⇄ 올패스 환급 심사 목록 열기</button>
        <button type="button" class="btn btn-primary" onclick="approveSettlementDeduct('${item.id}')" ${item.status === "APPROVED" ? "disabled" : ""}>
          ${item.status === "APPROVED" ? "✔ 당월 정산 차감 반영됨" : "✔ 당월 정산 차감 승인"}
        </button>
      </div>
    `;
  }

  function renderAuditLogs() {
    const tbody = document.getElementById("auditTableBody");
    if (!tbody) return;
    tbody.innerHTML = state.auditLogs.map(log => `
      <tr>
        <td class="mono">${log.time}</td>
        <td><strong>${log.actor}</strong></td>
        <td class="mono"><strong>${log.targetId}</strong></td>
        <td><span class="badge badge-neutral">${log.burden}</span></td>
        <td>${log.action}</td>
        <td style="color:var(--text-sub);">${log.basis}</td>
      </tr>
    `).join("");
  }

  function updateFooterSummary() {
    const el = document.getElementById("footerSummary");
    if (!el) return;
    const totalBasic = state.items.reduce((acc, x) => acc + x.deductBasicRs, 0);
    const totalSup = state.items.reduce((acc, x) => acc + x.deductSupport, 0);
    const pendingCnt = state.items.filter(x => x.status === "PENDING").length;
    el.innerHTML = `당월 환급 <strong>${state.items.length}건</strong> (승인 대기 <strong>${pendingCnt}건</strong>) · 강사료 총 차감액: <strong style="color:#fca5a5;">-${fmt(totalBasic)}</strong> · 개발지원금 차감(잔여한도 복원): <strong style="color:#93c5fd;">-${fmt(totalSup)}</strong>`;
  }

  function selectItem(id) {
    state.selectedId = id;
    renderTable();
    renderDetail();
  }

  function approveSettlementDeduct(id) {
    const item = state.items.find(x => x.id === id);
    if (!item) return;
    const memoVal = document.getElementById("detailMemo")?.value || item.memo;
    item.memo = memoVal;
    item.status = "APPROVED";
    state.auditLogs.unshift({
      time: "2026-10-18 15:10:22",
      actor: "재무팀장 (조정식)",
      targetId: item.id,
      burden: `${item.burdenType} / ${item.rightsHolderName}`,
      action: `강사료 차감(-${fmt(item.deductBasicRs)}) 및 개발지원금 차감(-${fmt(item.deductSupport)}) 정산 반영 승인`,
      basis: "4대 수집 증빙(합격증 사본·산준모 카페 합격수기 아웃링크·통장 사본·1금융권 실명계좌) 확인 완료"
    });
    renderTable();
    renderDetail();
    renderAuditLogs();
    showToast(`[${item.id}] 합격환급 정산 차감 내역이 확정되었습니다.`);
  }

  function showToast(msg) {
    const wrap = document.getElementById("toastContainer");
    if (!wrap) return;
    const div = document.createElement("div");
    div.className = "toast";
    div.textContent = msg;
    wrap.appendChild(div);
    setTimeout(() => div.remove(), 3200);
  }

  window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".kpi-card[data-filter]").forEach(card => {
      card.addEventListener("click", () => {
        document.querySelectorAll(".kpi-card[data-filter]").forEach(c => c.classList.remove("active"));
        card.classList.add("active");
        state.kpiFilter = card.getAttribute("data-filter") || "ALL";
        renderTable();
      });
    });

    document.querySelectorAll(".tab-btn[data-tab]").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn[data-tab]").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        const target = btn.getAttribute("data-tab");
        document.querySelectorAll(".tab-panel").forEach(p => {
          p.classList.toggle("hidden", p.id !== target);
        });
      });
    });

    document.getElementById("searchInput")?.addEventListener("input", renderTable);
    document.getElementById("burdenFilter")?.addEventListener("change", renderTable);

    renderTable();
    renderDetail();
    renderAuditLogs();
  });
</script>"""


SETT_006_UI_REPLACEMENTS = [
    # 상단 타이틀 및 탭 이름(C-01, MMG 이중 부담 회피 등) 운영자 용어화
    ("합격 환급반 관리 (출석 · 진도율 · 환급 차감 검증)", "합격 환급반 정산 관리"),
    ("합격 환급반 관리 (4대 증빙 · 진도율 90% · 환급 정산 차감 검증)", "합격 환급반 정산 관리"),
    ("1. 합격 환급 검수 및 계약별 부담 옵션(A/B/C) 워크스페이스", "1. 합격 환급 정산 반영 목록 (부담 옵션 A/B/C)"),
    ("2. MMG 이중 부담 회피 & 지원금(Pipeline 5.1) C-01 캡 흡수 방지 검증", "2. 최저보장금(MMG) · 개발지원금 차감 및 한도 복원 기준"),
    ("2. MMG 이중 부담 회피 & 지원금(매출연동 개발지원금) C-01 캡 흡수 방지 검증", "2. 최저보장금(MMG) · 개발지원금 차감 및 한도 복원 기준"),
    ("3. 정산 4·5단계 반영 감사 로그 (ADMN-CONF-010)", "3. 환급 정산 차감 처리 이력"),
    ("3. 정산 4·5단계 반영 감사 로그", "3. 환급 정산 차감 처리 이력"),
    # KPI 카드 내부 암호 제거
    ("⏳ 자격 검수 대기 (합격증 확인)", "⏳ 정산 차감 승인 대기"),
    ("큐넷 합격증 · 출석률 · 수강기한 검수", "4대 증빙(합격증·수기링크·통장·실명계좌) 확인됨"),
    ("4단계(DEDUCT) 스냅샷 역참조 공제", "원 결제 시점 정산율 기준 차감"),
    ("4단계 스냅샷 역참조 공제", "원 결제 시점 정산율 기준 차감"),
    ("🚨 MMG · 환급반 중복 플래그", "최저보장(MMG) 적용 강사 건"),
    ("mmg_promo_overlap_flag = true", "최저보장 보전금 산정 후 별도 차감"),
    ("최저보장·환급반 중복 발생 감지", "최저보장 보전금 산정 후 별도 차감"),
    # 테이블 헤더 암호(BASIC, P5.1) 제거
    ("4단계 R/S 공제(BASIC)", "강사료(R/S) 차감액"),
    ("4·5단계 지원금 공제(P5.1)", "개발지원금 차감 (한도복원)"),
    # 탭 2 내부의 기획서용 문구('C-01', '15.2절', '8.3절') 운영자 용어화
    ("재무 영향 판정 (15.2절)", "정산 적용 결과"),
    ("수식 및 스냅샷 역참조 규칙 (8.3절 4·5단계 정본)", "개발지원금 차감 및 잔여 한도 복원 계산 방식"),
    ("수식 및 스냅샷 역참조 규칙 (4·5단계 정본)", "개발지원금 차감 및 잔여 한도 복원 계산 방식"),
    ("✅ 당사 정본 규칙 적용 (3단계 선행 → 4단계 차감)", "✅ 적용 기준 (최저보장금 우선 산정 후 환급 분담금 차감)"),
    ("❌ 잘못된 설계 (차감액을 MMG 모수에 선반영 시)", "⚠️ 비교 참고 (환급 차감액을 최저보장 기준매출에서 먼저 뺄 경우 — 미적용)"),
]


def main():
    modified = []
    for folder in [PROTO_DIR, CLEAN_DIR]:
        if not folder.exists():
            continue

        # 1) ADMN-SETT-006 패치
        f_sett = folder / "ADMN-SETT-006_baseline.html"
        if f_sett.exists():
            orig = f_sett.read_text(encoding="utf-8")
            txt = orig
            for old, new in SETT_006_UI_REPLACEMENTS:
                txt = txt.replace(old, new)

            # <script> 블록을 운영자 친화적 완성본으로 교체
            txt = re.sub(
                r"<script>\s*const BURDEN_LABELS =[\s\S]*?</script>",
                SETT_006_OPERATOR_SCRIPT,
                txt
            )
            # 만약 이전 스크립트에서 </body></html>까지 붙어 있었다면 안전하게 매칭
            if "합격증사본_국가기술자격_홍길동_2026.jpg" not in txt:
                txt = re.sub(
                    r"<script>\s*const BURDEN_LABELS =[\s\S]*$",
                    SETT_006_OPERATOR_SCRIPT + "\n</body></html>",
                    txt
                )

            if txt != orig:
                f_sett.write_text(txt, encoding="utf-8")
                modified.append(str(f_sett))

        # 2) ADMN-RFD-002 (올패스 환급 심사 탭 내 'SETT-006 C-01' 등 내부 코드 제거)
        f_rfd = folder / "ADMN-RFD-002_baseline.html"
        if f_rfd.exists():
            orig = f_rfd.read_text(encoding="utf-8")
            txt = orig.replace("옵션 B (강사 50% 분담 · SETT-006 C-01)", "옵션 B (강사 50% 공동 분담)")
            txt = txt.replace("(`ADMN-SETT-006 C-01`)", "(`합격 환급반 정산 관리`)")
            txt = txt.replace("(ADMN-SETT-006 C-01)", "(합격 환급반 정산 관리)")
            if txt != orig:
                f_rfd.write_text(txt, encoding="utf-8")
                modified.append(str(f_rfd))

        # 3) ADMN-SETT-007 (KPI 카드의 'D-1' 같은 부록 번호 제거)
        f_s007 = folder / "ADMN-SETT-007_baseline.html"
        if f_s007.exists():
            orig = f_s007.read_text(encoding="utf-8")
            txt = orig.replace(">D-1<", ">권리 승계<")
            if txt != orig:
                f_s007.write_text(txt, encoding="utf-8")
                modified.append(str(f_s007))

    print(f"[패치 완료] 총 {len(modified)}개 파일에서 내부 이슈 코드(C-01, D-1, P5.1 등) 제거 및 4대 증빙 반영 완료:")
    for m in modified:
        print(f"  - {m}")


if __name__ == "__main__":
    main()
