#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 합격환급반(USER-MY-011-S1 / ADMN-RFD-001 / ADMN-SETT-006 / ADMN-PROD-005)
제출 자료 4종 정합화 및 ADMN-SETT-006 잘린 JS 렌더링 엔진 완벽 복구 스크립트

반영 기준 (통합 상세 설계서 & screen_spec):
  1) 합격증 사본 이미지 (Image)
  2) 플랫폼 및 산준모 카페 등록 합격 수기 아웃링크 작성 (URL)
  3) 환급금 입금용 통장 사본 이미지 (Image)
  4) 시중 1금융권 은행명 및 실명 계좌번호 입력 수집 (1금융권 검증 & 실명 대조)
  5) 인정 진도율 90% 이상 (출석률/출석일수 조건 제거)
"""

import re
from pathlib import Path

PROTO_DIR = Path("prototype")
CLEAN_DIR = Path("prototype_clean")

# ==============================================================================
# 1. ADMN-SETT-006 완벽 복구용 전체 <script> 블록 (잘린 JS 복원 + 4대 수집자료 완비)
# ==============================================================================
SETT_006_COMPLETE_SCRIPT = """<script>
  const BURDEN_LABELS = {
    OPTION_A: "옵션 A (플랫폼 전액 부담 · 기본값)",
    OPTION_B: "옵션 B (비율 공동 부담 · 4단계 공제)",
    OPTION_C: "옵션 C (매출 취소 처리 · 4단계 차감)"
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
        studentRefundAmount: 410000, // 교재비 제외한 순수 강좌 실결제 환급 모수
        withholdingTax22: 90200,     // 기타소득 제세공과금 22% (소득세 20% + 지방세 2%)
        netPayoutToStudent: 319800,  // 수강생 실입금액
        snapshotRsRate: 50,
        snapshotSupportRate: 15,
        deductBasicRs: 102500,       // 원거래 강사 R/S(205,000원) × 50%(옵션B 분담) = 102,500원 공제
        deductSupport: 15000,        // 원거래 지원금 확정액(30,000원) × 50%(옵션B) = 15,000원 공제 및 한도복원
        capRestoreYn: true,
        mmgOverlapFlag: false,
        originSettlementStatus: "PAID_POST_TAX",
        progressRate: "92.4% (기준 90% 충족 · 가중평균)",
        // 통합 상세 설계서 & USER-MY-011-S1 4대 필수 수집 자료
        certImageFile: "합격증사본_국가기술자격_홍길동_2026.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/984120",
        reviewPlatformId: "BRD-005-REV-0412 (플랫폼·카페 동시 등록 확인)",
        bankbookCopyFile: "통장사본_KB국민은행_홍길동.png",
        bankNameTier1: "KB국민은행 (시중 1금융권 검증 통과)",
        bankAccountRealName: "123-45-****-890 (예금주: 홍길동 · 회원 실명 100% 일치)",
        appliedMonth: "2026-10",
        status: "PENDING",
        memo: "ADMN-RFD-001(올패스 환급 심사) 4대 제출자료(합격증 사본·카페 합격수기 아웃링크·통장사본·1금융권 실명계좌) 검수 완료 후 정산 4단계(DEDUCT) 공제 확정 대기"
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
        rightsHolderName: "김안전 (강사 · RH-0019 · MMG 150만 특약)",
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
        progressRate: "100.0% (기준 90% 충족 · 가중평균)",
        certImageFile: "합격증사본_큐넷확인서_최안전.png",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/983910",
        reviewPlatformId: "BRD-005-REV-0398 (플랫폼·카페 동시 등록 확인)",
        bankbookCopyFile: "통장사본_신한은행_최안전.jpg",
        bankNameTier1: "신한은행 (시중 1금융권 검증 통과)",
        bankAccountRealName: "110-382-****91 (예금주: 최안전 · 회원 실명 100% 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "15.2절 규칙에 따라 3단계 MMG(150만, 보전금 120만) 판정 후 4단계(DEDUCT)에서 200,000원 차감 확정 (mmg_promo_overlap_flag=true)",
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
        progressRate: "95.2% (기준 90% 충족 · 가중평균)",
        certImageFile: "합격증사본_산업안전기사_이수석.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/983102",
        reviewPlatformId: "BRD-005-REV-0351 (플랫폼·카페 동시 등록 확인)",
        bankbookCopyFile: "통장사본_우리은행_이수석.png",
        bankNameTier1: "우리은행 (시중 1금융권 검증 통과)",
        bankAccountRealName: "1002-841-****12 (예금주: 이수석 · 회원 실명 100% 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "원 결제(2026-02) 스냅샷 역참조하여 2026-10 귀속 4단계 공제 및 5단계 지원금 한도(+18,000원) 복원 완료",
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
        progressRate: "91.8% (기준 90% 충족 · 가중평균)",
        certImageFile: "합격증사본_건설안전기사_최유진.jpg",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/982400",
        reviewPlatformId: "BRD-005-REV-0319 (플랫폼·카페 동시 등록 확인)",
        bankbookCopyFile: "통장사본_하나은행_최유진.jpg",
        bankNameTier1: "하나은행 (시중 1금융권 검증 통과)",
        bankAccountRealName: "391-910***-**107 (예금주: 최유진 · 회원 실명 100% 일치)",
        appliedMonth: "2026-10",
        status: "APPROVED",
        memo: "계약 옵션 A(플랫폼 100% 부담 · 마케팅 판촉비 처리) 적용 — 권리자 정산 차감 0원 확정",
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
        progressRate: "96.0% (기준 90% 충족 · 가중평균)",
        certImageFile: "합격증사본_산업안전기사_정하늘.png",
        reviewOutlinkUrl: "https://cafe.naver.com/sanjunmo/984511",
        reviewPlatformId: "BRD-005-REV-0429 (플랫폼·카페 동시 등록 확인)",
        bankbookCopyFile: "통장사본_IBK기업은행_정하늘.png",
        bankNameTier1: "IBK기업은행 (시중 1금융권 검증 통과)",
        bankAccountRealName: "010-****-6620 평생계좌 / 221-08****-01-011 (예금주: 정하늘 · 실명 일치)",
        appliedMonth: "2026-10",
        status: "PENDING",
        memo: "특강 프로모션 옵션 A 적용 대상 — 4대 제출 증빙 검수 완료, 최종 정산 이관 승인 대기"
      }
    ],
    auditLogs: [
      {
        time: "2026-10-13 16:40:00",
        actor: "재무팀장 (조정식)",
        targetId: "HRF-202610-02",
        burden: "OPTION_C / 김안전 (RH-0019)",
        action: "합격환급 정산 차감 확정 (-200,000원) · MMG 중복 플래그(mmg_promo_overlap_flag=true) 기록",
        basis: "합격증 사본·산준모 카페 수기 아웃링크·신한은행 통장사본·실명계좌 4종 대조 완료 (15.2절 3단계 MMG 선행 후 4단계 차감)"
      },
      {
        time: "2026-10-12 11:20:00",
        actor: "재무팀장 (조정식)",
        targetId: "HRF-202610-03",
        burden: "OPTION_B / 정종대 (RH-0025)",
        action: "4단계 R/S 공제(-60,000원) 및 개발지원금 공제(-18,000원) · 5단계 한도 복원(+18,000원) 확정",
        basis: "합격증 사본·카페 합격수기 아웃링크·우리은행 통장사본·실명계좌 4종 검증 완료 (원결제 2026-02 스냅샷 역참조)"
      },
      {
        time: "2026-10-10 14:15:00",
        actor: "운영팀장 (김검수)",
        targetId: "HRF-202610-04",
        burden: "OPTION_A / 이건설 (RH-0031)",
        action: "플랫폼 전액 부담(옵션 A) 확정 — 권리자 정산 차감 0원 처리",
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
          ? `<span class="badge badge-warn">옵션 B (비율 공동분담)</span>`
          : `<span class="badge badge-danger">옵션 C (매출 취소차감)</span>`;

      const statusBadge = item.status === "APPROVED"
        ? `<span class="badge badge-success">✔ 정산반영 확정</span>`
        : `<span class="badge badge-warn">⏳ 공제검수 대기</span>`;

      const overlapTag = item.mmgOverlapFlag
        ? `<div style="margin-top:3px;"><span class="badge badge-purple">🚨 MMG 중복 발생</span></div>`
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
            <strong>${item.rightsHolderName}</strong> <span class="mono" style="color:var(--text-muted);">(${item.rightsHolderId})</span>
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
            ${item.capRestoreYn ? `<div style="font-size:10.5px; color:var(--primary);">+한도복원 ${fmt(item.deductSupport)}</div>` : ""}
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
      badge.textContent = item.status === "APPROVED" ? "정산 4단계 반영 완료" : "검수 · 정산반영 대기";
    }

    box.innerHTML = `
      <div class="kv-grid">
        <div class="kv-label">환급정산 ID / 심사번호</div>
        <div><strong>${item.id}</strong> (환불심사 연동: <code>${item.rfdApproveId}</code>)</div>
        <div class="kv-label">수강생 / 인정 진도율</div>
        <div><strong>${item.studentName}</strong> (${item.studentUid}) · <span class="badge badge-success">${item.progressRate}</span></div>
        <div class="kv-label">원 주문번호 / 결제월</div>
        <div><code>${item.orderId}</code> (원 결제월: <strong>${item.originPaidMonth}</strong> → 환급 귀속월: <strong>${item.appliedMonth}</strong>)</div>
        <div class="kv-label">귀속 권리자 / 계약</div>
        <div><strong>${item.rightsHolderName}</strong> (<code>${item.rightsHolderId}</code> · 계약 <code>${item.contractId}</code>)</div>
        <div class="kv-label">계약 환급 부담 옵션</div>
        <div><strong style="color:var(--primary);">${BURDEN_LABELS[item.burdenType]}</strong></div>
      </div>

      <!-- 통합 상세 설계서 & USER-MY-011-S1 4대 필수 수집 증빙 박스 -->
      <div class="calc-box" style="background:#EFF6FF; border-color:#BFDBFE;">
        <div style="font-weight:800; font-size:12.5px; color:#1E3A8A; margin-bottom:4px;">
          📋 [USER-MY-011-S1 ➔ ADMN-RFD-001-S1] 수강생 제출 4대 필수 증빙 및 계좌 검증 내역
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">① 합격증 사본 이미지</span>
          <span>📎 <code>${item.certImageFile}</code> <button type="button" class="btn btn-sm" style="padding:2px 7px; font-size:11px;" onclick="showToast('합격증 사본 이미지 원본 뷰어를 호출합니다: ' + '${item.certImageFile}')">이미지 열람</button></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">② 플랫폼 및 산준모 카페 합격수기 아웃링크</span>
          <span>🔗 <a href="${item.reviewOutlinkUrl}" target="_blank" rel="noopener" style="color:var(--primary); font-weight:700; text-decoration:underline;">${item.reviewOutlinkUrl} ↗</a> <span class="badge badge-purple">${item.reviewPlatformId}</span></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">③ 환급금 입금용 통장 사본</span>
          <span>📎 <code>${item.bankbookCopyFile}</code> <button type="button" class="btn btn-sm" style="padding:2px 7px; font-size:11px;" onclick="showToast('통장 사본 이미지 원본 뷰어를 호출합니다: ' + '${item.bankbookCopyFile}')">사본 열람</button></span>
        </div>
        <div class="calc-row">
          <span style="color:#1E40AF; font-weight:600;">④ 시중 1금융권 은행명 · 실명 계좌번호</span>
          <span>🏦 <strong>${item.bankNameTier1}</strong> · <code>${item.bankAccountRealName}</code></span>
        </div>
      </div>

      <!-- 수강생 환급금(제세공과금 22%) 및 권리자 4·5단계 역참조 공제 산출 박스 -->
      <div class="calc-box">
        <div style="font-weight:800; font-size:12.5px; color:var(--text); margin-bottom:2px;">
          💰 수강생 환급금(제세공과금 22% 공제) 및 권리자 4·5단계 스냅샷 역참조 산출
        </div>
        <div class="calc-row">
          <span>패키지 총 실결제액 (교재 정가 ${fmt(item.excludedBookAmount)} 포함)</span>
          <strong class="mono">${fmt(item.totalPaidAmount)}</strong>
        </div>
        <div class="calc-row">
          <span>환급 기준 모수 (도서정가제 교재비 제외 순수 강좌 실결제액)</span>
          <strong class="mono" style="color:var(--primary);">${fmt(item.studentRefundAmount)}</strong>
        </div>
        <div class="calc-row">
          <span>수강생 실입금 환급액 (기타소득 제세공과금 22% = -${fmt(item.withholdingTax22)} 원천징수)</span>
          <strong class="mono" style="color:var(--success);">${fmt(item.netPayoutToStudent)}</strong>
        </div>
        <hr style="border:none; border-top:1px dashed var(--border-strong); margin:4px 0;">
        <div class="calc-row">
          <span>[4단계 DEDUCT] 기본 R/S(Pipeline 1.1) 스냅샷 공제액 (원요율 ${item.snapshotRsRate}%)</span>
          <strong class="mono" style="color:var(--danger);">${item.deductBasicRs > 0 ? "-" + fmt(item.deductBasicRs) : "0원 (옵션 A 면제)"}</strong>
        </div>
        <div class="calc-row">
          <span>[4·5단계 C-01] 매출연동 개발지원금(Pipeline 5.1) 공제 및 한도 복원액</span>
          <strong class="mono" style="color:var(--danger);">${item.deductSupport > 0 ? "-" + fmt(item.deductSupport) + " (한도 +" + fmt(item.deductSupport) + " 복원)" : "0원"}</strong>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">정산 검수 메모 및 스냅샷 역참조 근거</label>
        <textarea id="detailMemo" class="input">${item.memo || ""}</textarea>
      </div>

      <div style="display:flex; gap:8px; justify-content:flex-end;">
        <button type="button" class="btn" onclick="location.href='ADMN-RFD-002_baseline.html'">⇄ 올패스 환급 심사원장(RFD-001) 열기</button>
        <button type="button" class="btn btn-primary" onclick="approveSettlementDeduct('${item.id}')" ${item.status === "APPROVED" ? "disabled" : ""}>
          ${item.status === "APPROVED" ? "✔ 당월 4단계(DEDUCT) 반영 확정됨" : "✔ 4단계(DEDUCT) 정산 공제 확정 승인"}
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
    el.innerHTML = `당월 환급 <strong>${state.items.length}건</strong> (공제대기 <strong>${pendingCnt}건</strong>) · 4단계 R/S 총 공제액: <strong style="color:#fca5a5;">-${fmt(totalBasic)}</strong> · 4·5단계 지원금 공제(한도복원): <strong style="color:#93c5fd;">-${fmt(totalSup)}</strong>`;
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
      action: `4단계 R/S 공제(-${fmt(item.deductBasicRs)}) 및 지원금 공제(-${fmt(item.deductSupport)}) 정산 반영 승인`,
      basis: "4대 수집 증빙(합격증 사본·산준모 카페 합격수기 아웃링크·통장 사본·1금융권 실명계좌) 및 원거래 스냅샷 검증 완료"
    });
    renderTable();
    renderDetail();
    renderAuditLogs();
    showToast(`[${item.id}] 합격환급 정산 4단계(DEDUCT) 공제 반영이 확정되었습니다.`);
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
    // KPI 카드 필터 바인딩
    document.querySelectorAll(".kpi-card[data-filter]").forEach(card => {
      card.addEventListener("click", () => {
        document.querySelectorAll(".kpi-card[data-filter]").forEach(c => c.classList.remove("active"));
        card.classList.add("active");
        state.kpiFilter = card.getAttribute("data-filter") || "ALL";
        renderTable();
      });
    });

    // 탭 전환 바인딩
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


def patch_sett_006(html: str, is_clean: bool) -> str:
    # 1) 상단 타이틀 및 KPI의 '출석률' -> '4대 증빙 · 진도율 90% · 환급 차감 검증'으로 교정
    html = html.replace(
        "합격 환급반 관리 (출석 · 진도율 · 환급 차감 검증)",
        "합격 환급반 관리 (4대 증빙 · 진도율 90% · 환급 정산 차감 검증)"
    )
    html = html.replace(
        "큐넷 합격증 · 출석률 · 수강기한 검수",
        "합격증·카페수기링크·통장사본·1금융실명계좌"
    )
    html = html.replace(
        "⏳ 자격 검수 대기 (합격증 확인)",
        "⏳ 정산 공제 검수 대기 (4종 증빙 완비)"
    )

    # 2) 잘려 있던 마지막 <script> 블록을 완전한 SETT_006_COMPLETE_SCRIPT로 교체
    html = re.sub(
        r"<script>\s*const BURDEN_LABELS =[\s\S]*$",
        SETT_006_COMPLETE_SCRIPT + "\n</body></html>",
        html
    )

    if is_clean:
        html = re.sub(r"(<title>\s*)\[[A-Z0-9\-]+\]\s*", r"\1", html)
    return html


def patch_prod_005(html: str) -> str:
    # 패키지·환급반 관리에서 스펙 외 '출석일수 60일 이상'을 4대 제출 자료 기준으로 교정
    html = html.replace(
        "환급조건 (진도/출석)",
        "환급조건 (진도율 90% · 4대 증빙)"
    )
    html = html.replace(
        "<strong>출석일수 60일 이상</strong> + 시험 최종합격 수기/자격증 인증 시",
        "<strong>합격증 사본 · 플랫폼/산준모 카페 합격수기 아웃링크 · 통장 사본 · 시중 1금융권 실명계좌</strong> 제출 승인 시"
    )
    html = html.replace(
        "ADMN-SETT-006 환급 심사 및 진도/출석율 연동",
        "ADMN-RFD-001 / SETT-006 환급 4대 증빙 심사 및 진도율(90%) 연동"
    )
    return html


def patch_rfd_002(html: str) -> str:
    # ADMN-RFD-002 내 합격환급반(RFD-001) 안내 배너 및 테이블에 4대 수집 항목 명시 보강
    old_banner_line = "• <b>환급 모수:</b> 전체 결제액(450,000원) 중 도서정가제 대상인 실물 교재 정가(40,000원)를 제외한 순수 교습비(410,000원)만 환급 대상입니다.<br>"
    new_banner_line = (
        "• <b>수강생 필수 제출 4대 자료 (USER-MY-011-S1):</b> ① 합격증 사본 이미지, ② 플랫폼 및 산준모 카페 등록 합격수기 아웃링크 작성, ③ 환급금 입금용 통장 사본, ④ 시중 1금융권 은행명 및 실명 계좌번호 입력 수집 (명의 3중 대조 필수)<br>"
        + old_banner_line
    )
    if "수강생 필수 제출 4대 자료" not in html:
        html = html.replace(old_banner_line, new_banner_line)

    html = html.replace(
        "<th>합격수기 검수 (BRD-005)</th>",
        "<th>합격수기 아웃링크 · 통장사본 · 1금융 계좌</th>"
    )
    html = html.replace(
        "<th>합격수기 검수</th>",
        "<th>합격수기 아웃링크 · 통장사본 · 1금융 계좌</th>"
    )
    html = html.replace(
        '<span class="badge badge-purple">BRD-005 검수완료 (우수)</span>',
        '<span class="badge badge-purple">카페·플랫폼 수기링크 O</span> <span class="badge badge-green">통장사본·KB국민 실명계좌 O</span>'
    )
    html = html.replace(
        '<span class="badge badge-amber">수기 분량 미달 (보완요청)</span>',
        '<span class="badge badge-amber">카페 수기 아웃링크 미등록 (보완요청)</span>'
    )
    html = html.replace(
        '<span class="badge badge-green">BRD-005 승인완료</span>',
        '<span class="badge badge-purple">카페·플랫폼 수기링크 O</span> <span class="badge badge-green">통장사본·우리 실명계좌 O</span>'
    )
    return html


def main():
    modified = []
    for folder in [PROTO_DIR, CLEAN_DIR]:
        if not folder.exists():
            continue
        is_clean = (folder == CLEAN_DIR)

        # 1) ADMN-SETT-006 패치
        f_sett = folder / "ADMN-SETT-006_baseline.html"
        if f_sett.exists():
            orig = f_sett.read_text(encoding="utf-8")
            updated = patch_sett_006(orig, is_clean)
            if updated != orig:
                f_sett.write_text(updated, encoding="utf-8")
                modified.append(str(f_sett))

        # 2) ADMN-PROD-005 패치
        f_prod = folder / "ADMN-PROD-005_baseline.html"
        if f_prod.exists():
            orig = f_prod.read_text(encoding="utf-8")
            updated = patch_prod_005(orig)
            if updated != orig:
                f_prod.write_text(updated, encoding="utf-8")
                modified.append(str(f_prod))

        # 3) ADMN-RFD-002 패치
        f_rfd = folder / "ADMN-RFD-002_baseline.html"
        if f_rfd.exists():
            orig = f_rfd.read_text(encoding="utf-8")
            updated = patch_rfd_002(orig)
            if updated != orig:
                f_rfd.write_text(updated, encoding="utf-8")
                modified.append(str(f_rfd))

    print(f"[패치 완료] 총 {len(modified)}개 파일 업데이트됨:")
    for m in modified:
        print(f"  - {m}")


if __name__ == "__main__":
    main()
