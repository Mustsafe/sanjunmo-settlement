#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 누락 3대 기능 추가 패치 (patch_missing_3_features.py)

대상 (prototype/ · prototype_clean/ 양쪽, 총 4개 파일)
  - ADMN-USER-001_baseline.html
      작업 1) ?view=course  : 차시별 진도율 · 진도율 보정 이력 원장 + 진도율 수동 보정 모달 (ADMN-USER-004 / 004-P1)
      작업 2) ?view=tags    : 신규 태그 생성 모달(S1) + 그룹 생성 · 다중 태그 연결(S2) + 그룹 저장 모달
  - ADMN-RFD-002_baseline.html
      작업 3) ?view=done    : 환불 완료 원장 [사후 보정] 컬럼 + 별도 보정 거래 원장 + 보정 거래 등록 모달 (ADMN-RFD-003-S2)

안전장치
  - 모든 삽입 지점은 '정확히 1회' 매칭되는 앵커 문자열로 검증하며, 하나라도 어긋나면 해당 파일은 저장하지 않음
  - 파일별 마커([M3F-PATCH-v1])로 멱등성 보장: 이미 패치된 파일은 건너뜀
  - 기존 함수·ID와 충돌하지 않도록 신규 JS는 IIFE + 고유 접두사(m3f)로 격리
  - 저장 후 필수 ID 존재 여부 및 신규 <script> 블록을 node 로 문법 검사 (node 미설치 시 생략)

사용법 (프로젝트 루트에서)
  python patch_missing_3_features.py            # 4개 파일 패치 + 자체 검증
  python patch_missing_3_features.py --dry-run  # 저장 없이 앵커·검증만 수행
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

MARKER = "[M3F-PATCH-v1]"
TARGET_DIRS = ["prototype", "prototype_clean"]


# =============================================================================
# 공통 유틸
# =============================================================================
class PatchError(Exception):
    pass


def replace_once(src, anchor, new, label):
    cnt = src.count(anchor)
    if cnt != 1:
        raise PatchError(f"앵커 매칭 실패 [{label}] — 기대 1회, 실제 {cnt}회")
    return src.replace(anchor, new, 1)


def insert_before(src, anchor, block, label):
    return replace_once(src, anchor, block + anchor, label)


def insert_after(src, anchor, block, label):
    return replace_once(src, anchor, anchor + block, label)


def js_syntax_check(js_code):
    """node 로 신규 스크립트 문법 검사. (ok, message) 반환. node 없으면 (None, msg)."""
    node = shutil.which("node")
    if not node:
        return None, "node 미설치 — JS 문법 검사 생략"
    checker = (
        "let s='';process.stdin.setEncoding('utf8');"
        "process.stdin.on('data',d=>s+=d).on('end',()=>{"
        "try{new Function(s);console.log('OK');}"
        "catch(e){console.error(e.message);process.exit(1);}});"
    )
    p = subprocess.run([node, "-e", checker], input=js_code.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        return True, "OK"
    return False, p.stderr.decode("utf-8", "replace").strip()


def extract_m3f_scripts(html):
    return re.findall(r"<script data-m3f=\"[^\"]+\">(.*?)</script>", html, re.S)


# =============================================================================
# [ADMN-USER-001] 작업 1 · 작업 2
# =============================================================================
USER_CSS = r'''
    /* === [M3F-PATCH-v1] USER-004 진도율 보정 · USER-006 태그/그룹 연결 추가 스타일 === */
    .m3f-summary { display:flex; flex-wrap:wrap; align-items:center; gap:14px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px; padding:11px 14px; margin-bottom:12px; }
    .m3f-summary .m3f-cap { font-size:11px; color:#1E40AF; font-weight:700; margin-bottom:2px; }
    .m3f-summary .m3f-big { font-size:20px; font-weight:800; color:#1E3A8A; }
    .m3f-spacer { flex:1; }
    .m3f-info { background:#F8FAFC; border:1px solid var(--border); border-left:4px solid #2563EB; border-radius:8px; padding:10px 14px; font-size:12px; color:#334155; margin-bottom:12px; line-height:1.6; }
    .m3f-field { margin-bottom:12px; }
    .m3f-field > label, .m3f-label { display:block; font-size:12px; font-weight:700; margin-bottom:4px; color:#0F172A; }
    .m3f-req { color:#DC2626; }
    .m3f-hint { font-size:11.5px; color:var(--text-muted); margin-top:4px; }
    .m3f-readonly { background:#F1F5F9; border:1px solid #CBD5E1; border-radius:6px; padding:8px 10px; font-size:12.5px; }
    .m3f-preview { background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:10px 14px; font-size:12.5px; color:#065F46; line-height:1.55; }
    .m3f-preview.warn { background:#FEF2F2; border-color:#FECACA; color:#991B1B; }
    .m3f-row-adjusted td { background:#FFFBEB; }
    .m3f-flash td { animation: m3fFlash 2.6s ease-out; }
    @keyframes m3fFlash { 0% { background:#DCFCE7; } 100% { background:transparent; } }
    .m3f-builder { border:1px solid var(--border); border-radius:10px; padding:14px 16px; background:#F8FAFC; margin-bottom:16px; }
    .m3f-builder-grid { display:grid; grid-template-columns: minmax(0,1fr) 240px; gap:16px; align-items:start; }
    .m3f-chip { display:inline-flex; align-items:center; gap:4px; padding:5px 11px; margin:0 6px 6px 0; border:1px solid #CBD5E1; border-radius:999px; background:#FFFFFF; font-size:12px; font-weight:700; color:#475569; cursor:pointer; }
    .m3f-chip.on { background:#EFF6FF; border-color:#2563EB; color:#1D4ED8; }
    .m3f-radio-row { display:flex; flex-wrap:wrap; gap:16px; font-size:12.5px; font-weight:700; }
    .m3f-radio-row label { display:inline-flex; align-items:center; gap:5px; cursor:pointer; }
    .m3f-target-badge { display:block; background:#0F172A; color:#FFFFFF; border-radius:8px; padding:10px 12px; font-size:12.5px; font-weight:700; line-height:1.5; margin-bottom:10px; }
    .m3f-tagpill { display:inline-block; padding:2px 7px; margin:2px 1px; border-radius:6px; background:#EEF2FF; color:#3730A3; font-size:11.5px; font-weight:700; border:1px solid #C7D2FE; }
    .m3f-op { display:inline-block; font-size:11px; font-weight:800; color:#B45309; margin:0 3px; }
    .m3f-actions { display:flex; flex-wrap:wrap; gap:4px; }
    .m3f-rule-box { border:1px dashed #94A3B8; border-radius:8px; padding:12px; background:#F8FAFC; }
    .m3f-grid2 { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .m3f-sum-table { width:100%; border-collapse:collapse; font-size:12.5px; }
    .m3f-sum-table th { text-align:left; width:130px; background:#F8FAFC; color:#475569; padding:7px 10px; border:1px solid #E2E8F0; }
    .m3f-sum-table td { padding:7px 10px; border:1px solid #E2E8F0; }
'''

USER_COURSE_SECTIONS = r'''
        <!-- [M3F-PATCH-v1] 작업 1-A(카드 4): ADMN-USER-004 차시별 진도율 · 이어보기 지점 조회 및 수동 보정 -->
        <div class="card" id="m3f-progress-card">
          <div class="card-header">
            <div class="card-title">4. 강의 차시별 진도율 · 이어보기 지점 조회 및 수동 보정 (ADMN-USER-004)</div>
            <span class="badge badge-blue">합격환급 심사 기준 진도율 실시간 연동</span>
          </div>
          <div class="card-body">
            <div class="m3f-summary">
              <div>
                <div class="m3f-cap">선택 강좌</div>
                <strong id="m3f-course-name">2026 산업안전기사 필기+실기 올패스</strong>
              </div>
              <div>
                <div class="m3f-cap">재생시간 가중평균 진도율</div>
                <span class="m3f-big" id="m3f-overall-rate">92.4%</span>
                <span id="m3f-overall-sub" style="font-size:12px; color:#1E40AF; font-weight:700; margin-left:4px;">(111 / 120강 완료 · 환급 인정 기준 90% 충족)</span>
              </div>
              <span class="badge badge-amber" id="m3f-adj-count-badge">보정 포함 1건</span>
              <div class="m3f-spacer"></div>
              <button type="button" class="btn btn-sm btn-outline" onclick="m3fRecalcProgress()">🔄 진도율 실시간 재집계</button>
              <button type="button" class="btn btn-sm btn-primary" onclick="openProgressAdjustModal()">+ 진도율 수동 보정 등록</button>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>차시</th>
                  <th>강의명</th>
                  <th>러닝타임</th>
                  <th>누적 시청시간</th>
                  <th>차시 진도율</th>
                  <th>최종 이어보기 지점(초)</th>
                  <th>최근 학습일시</th>
                  <th>보정 상태</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody id="m3f-unit-body">
                <tr><td colspan="9" style="text-align:center; color:var(--text-muted);">차시별 진도 데이터를 불러오는 중입니다…</td></tr>
              </tbody>
            </table>
            <div class="m3f-hint">• 최근 집계 시각: <strong id="m3f-recalc-at">2026.10.18 06:00</strong> · 가중평균 진도율 = Σ(차시 진도율 × 차시 러닝타임) ÷ 전체 러닝타임 · 표시 차시는 최근 학습 구간(31~34강)입니다.</div>
          </div>
        </div>

        <!-- [M3F-PATCH-v1] 작업 1-B(카드 5): 진도율 수동 보정 이력 원장 -->
        <div class="card" id="m3f-adjlog-card">
          <div class="card-header">
            <div class="card-title">5. 진도율 수동 보정 이력 원장 (환급 심사 ADMN-RFD-001 자동 연동)</div>
            <a href="ADMN-RFD-002_baseline.html?view=pass" class="btn btn-sm btn-outline">합격환급 심사 화면 ↗</a>
          </div>
          <div class="card-body">
            <div class="m3f-info">
              진도율 수동 보정은 별도 상급자 승인 없이 사유 및 증빙 입력 즉시 반영되며, 보정된 차시가 1건이라도 포함된 수강생은 올패스 합격환급 심사 시 <strong>[진도율 보정 포함]</strong> 수동 확인 대상으로 자동 분류됩니다.
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>보정번호 / 처리일시</th>
                  <th>대상 강좌 · 차시</th>
                  <th>보정 전 ➔ 보정 후</th>
                  <th>가중평균 진도율 변동</th>
                  <th>보정 사유 구분</th>
                  <th>상세 보정 사유 및 근거 증빙</th>
                  <th>처리 관리자</th>
                </tr>
              </thead>
              <tbody id="m3f-adjlog-body">
                <tr><td colspan="7" style="text-align:center; color:var(--text-muted);">보정 이력을 불러오는 중입니다…</td></tr>
              </tbody>
            </table>
          </div>
        </div>
'''

USER_TAG_EXTRA_ROWS = r'''
                <tr>
                  <td><code>TAG-LOW-PROG</code></td>
                  <td><strong>수강 진도율 30% 미만 정체 회원</strong></td>
                  <td>수강 시작 후 30일 경과 AND 가중평균 진도율 &lt; 30%</td>
                  <td class="tr-right" style="font-weight:800;">1,872 명</td>
                  <td>학습 독려 알림톡 · 이탈방지 집중케어 그룹 타겟</td>
                  <td><a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급 이동 ↗</a></td>
                </tr>
                <tr>
                  <td><code>TAG-INACTIVE-14D</code></td>
                  <td><strong>최근 14일 미접속 회원</strong></td>
                  <td>최종 접속일 기준 14일 이상 경과 (수강중 계약 보유)</td>
                  <td class="tr-right" style="font-weight:800;">3,315 명</td>
                  <td>복귀 유도 메시지 · 이탈방지 집중케어 그룹 타겟</td>
                  <td><a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급 이동 ↗</a></td>
                </tr>'''

USER_TAG_SECTION = r'''
        <!-- [M3F-PATCH-v1] 작업 2: ADMN-USER-006-S2 다중 태그 조합 타겟팅 & 회원 그룹 생성 · 태그 연결 -->
        <div class="card" id="m3f-group-card">
          <div class="card-header">
            <div class="card-title">2. 다중 태그 조합 타겟팅 &amp; 회원 그룹 생성 · 태그 연결 (ADMN-USER-006-S2)</div>
            <span class="badge badge-purple">쿠폰 대량 발급(ADMN-PROM-002) · 단체 메시지(ADMN-CONF-004) 연동</span>
          </div>
          <div class="card-body">
            <div class="m3f-builder">
              <div class="m3f-builder-grid">
                <div>
                  <div class="m3f-field">
                    <label for="m3f-grp-name">그룹명 <span class="m3f-req">*</span> <span id="m3f-grp-edit-badge" class="badge badge-amber" style="display:none; margin-left:6px;"></span></label>
                    <input type="text" id="m3f-grp-name" class="f-input" style="width:100%;" placeholder="예: 2026 3회차 실기 대비 이탈방지 집중케어 그룹" />
                  </div>
                  <div class="m3f-field">
                    <span class="m3f-label">연결할 태그 (다중 선택) <span class="m3f-req">*</span></span>
                    <div id="m3f-chip-wrap"></div>
                  </div>
                  <div class="m3f-field">
                    <span class="m3f-label">결합 연산자</span>
                    <div class="m3f-radio-row">
                      <label><input type="radio" name="m3f-grp-op" value="AND" checked onchange="m3fSetGroupOp(this.value)" /> AND (모든 태그 동시 충족)</label>
                      <label><input type="radio" name="m3f-grp-op" value="OR" onchange="m3fSetGroupOp(this.value)" /> OR (하나라도 충족)</label>
                    </div>
                  </div>
                  <div class="m3f-field" style="margin-bottom:0;">
                    <span class="m3f-label">그룹 갱신 방식</span>
                    <div class="m3f-radio-row">
                      <label><input type="radio" name="m3f-grp-mode" value="DYNAMIC" checked onchange="m3fSetGroupMode(this.value)" /> 동적 그룹 (Dynamic · 매일 06:00 조건 매칭 회원 자동 편입/이탈)</label>
                      <label><input type="radio" name="m3f-grp-mode" value="STATIC" onchange="m3fSetGroupMode(this.value)" /> 정적 그룹 (Static · 생성 시점 대상자 명단 고정)</label>
                    </div>
                  </div>
                </div>
                <div>
                  <span class="m3f-target-badge" id="m3f-grp-preview">예상 매칭 회원: 412명 — 마케팅 수신동의 388명 / 거부 24명</span>
                  <button type="button" class="btn btn-primary" id="m3f-grp-save-btn" style="width:100%; margin-bottom:6px;" onclick="m3fSaveGroup(false)">+ 그룹 생성 및 태그 연결 저장</button>
                  <button type="button" class="btn btn-outline" style="width:100%; margin-bottom:6px;" onclick="openGroupSaveModal()">조건 그룹 저장 모달로 열기</button>
                  <button type="button" class="btn btn-sm btn-outline" id="m3f-grp-cancel-edit" style="width:100%; display:none;" onclick="m3fCancelGroupEdit()">수정 모드 해제</button>
                  <div class="m3f-hint">• 메시지 발송 시 마케팅 수신 거부 회원은 광고성 발송 대상에서 자동 제외됩니다.</div>
                </div>
              </div>
            </div>

            <div style="font-size:13px; font-weight:800; margin-bottom:8px;">생성된 회원 타겟 그룹 및 연결 태그 현황</div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>그룹 코드</th>
                  <th>그룹명</th>
                  <th>연결된 태그 조합 (AND / OR)</th>
                  <th>갱신 방식</th>
                  <th class="tr-right">소속 회원 수 (수신동의)</th>
                  <th>최근 갱신일시</th>
                  <th>연동 액션 (쿠폰·메시지·해제)</th>
                </tr>
              </thead>
              <tbody id="m3f-group-body">
                <tr><td colspan="7" style="text-align:center; color:var(--text-muted);">회원 그룹 현황을 불러오는 중입니다…</td></tr>
              </tbody>
            </table>
          </div>
        </div>
'''

USER_MODALS_AND_JS = r'''
<!-- ==================== [M3F-PATCH-v1] ADMN-USER-001 추가 모달 3종 ==================== -->
<!-- 모달: 진도율 수동 보정 등록 (ADMN-USER-004-P1) -->
<div class="modal-backdrop" id="modalProgressAdjust" aria-hidden="true">
  <div class="modal-box" style="max-width:660px; width:94%;">
    <div class="modal-head">
      <span>🛠 진도율 수동 보정 등록 (ADMN-USER-004-P1)</span>
      <button type="button" class="btn btn-sm btn-outline" onclick="closeProgressAdjustModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="m3f-field">
        <span class="m3f-label">대상 회원 / 강좌</span>
        <div class="m3f-readonly"><strong>hon***@naver.com</strong> (회원번호 100482) · <strong>2026 산업안전기사 필기+실기 올패스</strong> (CRS-2026-8841)</div>
      </div>
      <div class="m3f-field">
        <label for="m3f-pa-unit">보정 대상 차시 <span class="m3f-req">*</span></label>
        <select id="m3f-pa-unit" class="f-select" style="width:100%;" onchange="m3fUpdateAdjustPreview()"></select>
        <div class="m3f-hint">• 이미 수동 보정이 반영된 차시는 목록에서 제외됩니다 (이력 원장에서 확인).</div>
      </div>
      <div class="m3f-field">
        <label for="m3f-pa-rate">보정 후 진도율 (0 ~ 100%) <span class="m3f-req">*</span></label>
        <div style="display:flex; align-items:center; gap:8px;">
          <input type="number" id="m3f-pa-rate" class="f-input" style="width:120px;" min="0" max="100" step="0.1" value="100" oninput="m3fUpdateAdjustPreview()" /> %
          <button type="button" class="btn btn-sm btn-outline" onclick="m3fSetRatePreset(100)">100% 수강완료 프리셋</button>
        </div>
      </div>
      <div class="m3f-field">
        <label for="m3f-pa-type">보정 사유 구분 <span class="m3f-req">*</span></label>
        <select id="m3f-pa-type" class="f-select" style="width:100%;">
          <option>플레이어·네트워크 장애</option>
          <option>모바일 앱 동기화 오류</option>
          <option>구 버전 강좌 개편 승계</option>
          <option>기타 CS 예외 인정</option>
        </select>
      </div>
      <div class="m3f-field">
        <label for="m3f-pa-reason">상세 보정 사유 <span class="m3f-req">*</span> <span style="font-weight:500; color:var(--text-muted);">(최소 10자 · 감사 로그 기록)</span></label>
        <textarea id="m3f-pa-reason" class="f-textarea" rows="3" style="width:100%;" placeholder="예) 10/17 오후 CDN 일시 순단으로 시청 완료 로그가 유실된 것을 서버 로그로 확인하여 보정함" oninput="m3fUpdateReasonCount()"></textarea>
        <div class="m3f-hint" id="m3f-pa-reason-count">현재 0자 / 최소 10자</div>
      </div>
      <div class="m3f-field">
        <span class="m3f-label">근거 자료 첨부 <span class="m3f-req">*</span></span>
        <input type="file" id="m3f-pa-file" style="display:none;" onchange="m3fOnEvidenceSelected(this)" />
        <div style="display:flex; align-items:center; gap:8px;">
          <button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('m3f-pa-file').click()">📎 파일 선택</button>
          <span class="m3f-readonly" style="padding:4px 10px;" id="m3f-pa-filename">cs_evidence_capture.png</span>
          <button type="button" class="btn btn-sm btn-outline" onclick="m3fRemoveEvidence()">첨부 삭제</button>
        </div>
      </div>
      <div class="m3f-preview" id="m3f-pa-preview">보정 반영 시 전체 가중평균 진도율: 92.4% ➔ 93.2% (환급 인정 기준 90% 충족 · 환급 심사 화면에 [보정 포함] 배지 자동 노출)</div>
    </div>
    <div class="modal-foot">
      <button type="button" class="btn btn-outline" onclick="closeProgressAdjustModal()">취소</button>
      <button type="button" class="btn btn-primary" onclick="submitProgressAdjustLedger()">보정 즉시 반영</button>
    </div>
  </div>
</div>

<!-- 모달: 신규 태그 생성 · 규칙 설정 (ADMN-USER-006-S1) -->
<div class="modal-backdrop" id="modalTagCreate" aria-hidden="true">
  <div class="modal-box" style="max-width:680px; width:94%;">
    <div class="modal-head">
      <span>🏷 신규 태그 생성 · 규칙 설정 (ADMN-USER-006-S1)</span>
      <button type="button" class="btn btn-sm btn-outline" onclick="closeTagCreateModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="m3f-grid2">
        <div class="m3f-field">
          <label for="m3f-tc-name">태그명 <span class="m3f-req">*</span></label>
          <input type="text" id="m3f-tc-name" class="f-input" style="width:100%;" placeholder="예: 수강 진도율 30% 미만 정체 회원" />
        </div>
        <div class="m3f-field">
          <label for="m3f-tc-code">태그 코드 <span class="m3f-req">*</span> <span style="font-weight:500; color:var(--text-muted);">(자동/수동 입력)</span></label>
          <div style="display:flex; gap:6px;">
            <input type="text" id="m3f-tc-code" class="f-input" style="flex:1;" placeholder="예: TAG-LOW-PROG-30" oninput="this.value=this.value.toUpperCase()" />
            <button type="button" class="btn btn-sm btn-outline" onclick="m3fAutoTagCode()">자동 생성</button>
          </div>
        </div>
      </div>
      <div class="m3f-field">
        <span class="m3f-label">부여 유형</span>
        <div class="m3f-radio-row">
          <label><input type="radio" name="m3f-tc-type" value="AUTO" checked onchange="m3fToggleTagRule()" /> 자동 규칙 태그 (조건 충족 시 시스템 자동 부여)</label>
          <label><input type="radio" name="m3f-tc-type" value="MANUAL" onchange="m3fToggleTagRule()" /> 수동 부여 태그 (관리자가 회원 선택 후 직접 부여)</label>
        </div>
      </div>
      <div class="m3f-field m3f-rule-box" id="m3f-tc-rule">
        <div style="font-size:12.5px; font-weight:800; margin-bottom:8px;">자동 규칙 조건 빌더</div>
        <div class="m3f-grid2">
          <div class="m3f-field">
            <label for="m3f-tc-domain">조건 도메인</label>
            <select id="m3f-tc-domain" class="f-select" style="width:100%;">
              <option>수강/진도율</option>
              <option>결제/주문 이력</option>
              <option>접속/로그인</option>
              <option>산준모 카페 인증</option>
              <option>마케팅 수신 동의</option>
            </select>
          </div>
          <div class="m3f-field">
            <label for="m3f-tc-cycle">평가 주기</label>
            <select id="m3f-tc-cycle" class="f-select" style="width:100%;">
              <option value="DAILY">매일 06:00 정기 배치</option>
              <option value="REALTIME">이벤트 발생 시 실시간</option>
            </select>
          </div>
        </div>
        <div class="m3f-field">
          <label for="m3f-tc-expr">상세 조건식 <span class="m3f-req">*</span></label>
          <input type="text" id="m3f-tc-expr" class="f-input" style="width:100%;" placeholder="예: 수강 시작 후 30일 경과 AND 가중평균 진도율 < 30%" />
        </div>
        <div class="m3f-field" style="margin-bottom:0;">
          <label for="m3f-tc-exit">조건 이탈 시 처리</label>
          <select id="m3f-tc-exit" class="f-select" style="width:100%;">
            <option>조건 미충족 전환 시 태그 자동 해제</option>
            <option>한 번 부여되면 영구 유지</option>
          </select>
        </div>
      </div>
      <div class="m3f-field" style="margin-bottom:0;">
        <label for="m3f-tc-memo">연동 대상 프로모션 / 설명 메모</label>
        <input type="text" id="m3f-tc-memo" class="f-input" style="width:100%;" placeholder="예: 실기 대비 학습 독려 알림톡 + 10% 재수강 쿠폰 타겟" />
      </div>
    </div>
    <div class="modal-foot">
      <button type="button" class="btn btn-outline" onclick="closeTagCreateModal()">취소</button>
      <button type="button" class="btn btn-primary" onclick="submitTagCreate()">신규 태그 생성 확정</button>
    </div>
  </div>
</div>

<!-- 모달: 조건 그룹 저장 확인 (ADMN-USER-006-S2) -->
<div class="modal-backdrop" id="modalGroupSave" aria-hidden="true">
  <div class="modal-box" style="max-width:620px; width:94%;">
    <div class="modal-head">
      <span>👥 회원 그룹 생성 · 태그 연결 저장 (ADMN-USER-006-S2)</span>
      <button type="button" class="btn btn-sm btn-outline" onclick="closeGroupSaveModal()">✕</button>
    </div>
    <div class="modal-body">
      <table class="m3f-sum-table" style="margin-bottom:12px;">
        <tbody id="m3f-gs-summary"></tbody>
      </table>
      <div class="m3f-field" style="margin-bottom:0;">
        <label for="m3f-gs-memo">그룹 운영 메모 (선택)</label>
        <input type="text" id="m3f-gs-memo" class="f-input" style="width:100%;" placeholder="예: 10월 4주차 실기 대비 독려 알림톡 + 재수강 쿠폰 동시 발송 예정" />
      </div>
    </div>
    <div class="modal-foot">
      <button type="button" class="btn btn-outline" onclick="closeGroupSaveModal()">취소</button>
      <button type="button" class="btn btn-primary" onclick="m3fSaveGroup(true)">✓ 그룹 생성 및 태그 연결 확정</button>
    </div>
  </div>
</div>

<script data-m3f="user-001">
/* === [M3F-PATCH-v1] ADMN-USER-004 진도율 보정 원장 · ADMN-USER-006 태그/그룹 연결 === */
(function () {
  'use strict';

  /* ---------- 공통 ---------- */
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad(n, w) { n = String(n); while (n.length < w) n = '0' + n; return n; }
  function nowText() {
    var d = new Date();
    return d.getFullYear() + '.' + pad(d.getMonth() + 1, 2) + '.' + pad(d.getDate(), 2) + ' ' + pad(d.getHours(), 2) + ':' + pad(d.getMinutes(), 2);
  }
  function num(n) { return Number(n).toLocaleString('ko-KR'); }
  function toast(msg) { if (typeof window.showToast === 'function') window.showToast(msg); else alert(msg); }
  function openModalEl(id) {
    var el = $(id);
    if (!el) return;
    el.classList.remove('force-closed');
    el.style.removeProperty('display');
    el.classList.add('show');
    el.setAttribute('aria-hidden', 'false');
  }
  function closeModalEl(id) {
    var el = $(id);
    if (!el) return;
    el.classList.remove('show', 'open', 'active');
    el.setAttribute('aria-hidden', 'true');
  }
  function flashRow(tr) {
    if (!tr) return;
    tr.classList.remove('m3f-flash');
    void tr.offsetWidth;
    tr.classList.add('m3f-flash');
  }

  /* =====================================================================
   * 작업 1. 차시별 진도율 · 진도율 수동 보정 이력 원장
   * ===================================================================== */
  var TOTAL_RUNTIME_SEC = 237450;   /* 120강 전체 러닝타임 합계(초) — 가중평균 분모 */
  var COURSE_SHORT = '2026 산안기 올패스';
  var ADMIN_NAME = '운영1팀 이지훈 (admin_jh)';
  var prog = { overall: 92.4, completed: 111, totalUnits: 120, threshold: 90, adjCount: 1, seq: 41 };

  var units = [
    { no: 31, title: '설비보전 및 기계안전 핵심빈출 풀이', short: '설비보전 및 기계안전', run: 2645, watched: 2645, rate: 100.0, pos: 2645, last: '2026.10.15 20:11', adjusted: false, origRate: null, adjId: '' },
    { no: 32, title: '화학설비 위험방지 및 MSDS 핵심정리', short: '화학설비 위험방지', run: 3020, watched: 1122, rate: 37.1, pos: 1122, last: '2026.10.17 14:22', adjusted: false, origRate: null, adjId: '' },
    { no: 33, title: '전기안전 보호구 및 정전기 재해 예방', short: '전기안전 보호구', run: 2775, watched: 0, rate: 0.0, pos: 0, last: '', adjusted: false, origRate: null, adjId: '' },
    { no: 34, title: '건설안전 가설구조물 및 추락재해 방지', short: '건설안전 가설구조물', run: 2510, watched: 0, rate: 100.0, pos: 0, last: '2026.10.10 11:20', adjusted: true, origRate: 0.0, adjId: 'PRG-ADJ-2026-041' }
  ];

  var adjLog = [
    { id: 'PRG-ADJ-2026-041', at: '2026.10.10 11:20', target: COURSE_SHORT + ' · 34강', before: 0.0, after: 100.0, ovBefore: 91.6, ovAfter: 92.4, type: '플레이어·네트워크 장애', detail: '10/09 심야 CDN 일시 순단으로 시청 완료 로그 유실 확인', file: 'cdn_error_log_1009.txt', admin: ADMIN_NAME },
    { id: 'PRG-ADJ-2026-019', at: '2026.09.22 16:05', target: COURSE_SHORT + ' · 12강', before: 45.0, after: 100.0, ovBefore: 48.2, ovAfter: 49.0, type: '모바일 앱 동기화 오류', detail: 'iOS 앱 오프라인 재생 후 진도율 미전송 CS 확인', file: 'cs_capture_0922.png', admin: 'CS팀 김상담 (admin_kim)' }
  ];

  var evidenceName = 'cs_evidence_capture.png';

  function mmss(sec) { return pad(Math.floor(sec / 60), 2) + ':' + pad(sec % 60, 2); }
  function r1(v) { return Math.round(v * 10) / 10; }
  function pct(v) { return Number(v).toFixed(1) + '%'; }
  function findUnit(no) { for (var i = 0; i < units.length; i++) if (units[i].no === Number(no)) return units[i]; return null; }

  function posText(u) {
    if (u.adjusted) return '보정 완료';
    if (u.rate >= 100) return num(u.pos) + '초 (수강완료)';
    if (!u.pos) return '0초 (미수강)';
    return num(u.pos) + '초 (' + Math.floor(u.pos / 60) + '분 ' + (u.pos % 60) + '초)';
  }

  function renderUnits() {
    var body = $('m3f-unit-body');
    if (!body) return;
    body.innerHTML = units.map(function (u) {
      var rateHtml = u.adjusted
        ? '<strong style="color:var(--success);">' + pct(u.rate) + '</strong> <span style="color:var(--text-muted); font-size:11.5px;">(원본 ' + pct(u.origRate) + ')</span>'
        : '<strong' + (u.rate < 90 ? ' style="color:var(--warning);"' : '') + '>' + pct(u.rate) + '</strong>';
      var status = u.adjusted
        ? '<span class="badge badge-amber">🛠 수동보정 반영됨</span>'
        : '<span class="badge badge-green">정상</span>';
      var action = u.adjusted
        ? '<button type="button" class="btn btn-sm btn-outline" onclick="m3fShowAdjHistory(\'' + u.adjId + '\')">이력 확인</button>'
        : (u.rate >= 100
          ? '<button type="button" class="btn btn-sm btn-outline" onclick="openProgressAdjustModal(' + u.no + ')">보정</button>'
          : '<button type="button" class="btn btn-sm btn-primary" onclick="openProgressAdjustModal(' + u.no + ')">진도율 보정</button>');
      return '<tr data-unit="' + u.no + '"' + (u.adjusted ? ' class="m3f-row-adjusted"' : '') + '>' +
        '<td><strong>' + u.no + '강</strong></td>' +
        '<td>' + esc(u.title) + '</td>' +
        '<td>' + mmss(u.run) + '</td>' +
        '<td>' + mmss(u.watched) + '</td>' +
        '<td>' + rateHtml + '</td>' +
        '<td>' + posText(u) + '</td>' +
        '<td>' + (u.last || '—') + '</td>' +
        '<td>' + status + '</td>' +
        '<td>' + action + '</td></tr>';
    }).join('');

    $('m3f-overall-rate').textContent = pct(prog.overall);
    $('m3f-overall-sub').textContent = '(' + prog.completed + ' / ' + prog.totalUnits + '강 완료 · 환급 인정 기준 ' + prog.threshold + '% ' + (prog.overall >= prog.threshold ? '충족' : '미달') + ')';
    $('m3f-adj-count-badge').textContent = '보정 포함 ' + prog.adjCount + '건';
  }

  function renderAdjLog() {
    var body = $('m3f-adjlog-body');
    if (!body) return;
    body.innerHTML = adjLog.map(function (h) {
      var diff = r1(h.ovAfter - h.ovBefore);
      return '<tr data-adj="' + esc(h.id) + '">' +
        '<td><strong>' + esc(h.id) + '</strong><br><span style="font-size:11.5px; color:var(--text-muted);">' + esc(h.at) + '</span></td>' +
        '<td>' + esc(h.target) + '</td>' +
        '<td>' + pct(h.before) + ' ➔ <strong style="color:var(--success);">' + pct(h.after) + '</strong></td>' +
        '<td>' + pct(h.ovBefore) + ' ➔ <strong>' + pct(h.ovAfter) + '</strong> <span style="font-size:11.5px; color:' + (diff >= 0 ? 'var(--success)' : 'var(--danger)') + ';">(' + (diff >= 0 ? '+' : '') + diff.toFixed(1) + '%p)</span></td>' +
        '<td><span class="badge badge-blue">' + esc(h.type) + '</span></td>' +
        '<td>' + esc(h.detail) + ' <span style="color:var(--text-muted);">(첨부: ' + esc(h.file) + ')</span></td>' +
        '<td>' + esc(h.admin) + '</td></tr>';
    }).join('');
  }

  function fillUnitOptions(selectedNo) {
    var sel = $('m3f-pa-unit');
    var list = units.filter(function (u) { return !u.adjusted; });
    sel.innerHTML = list.map(function (u) {
      return '<option value="' + u.no + '"' + (u.no === selectedNo ? ' selected' : '') + '>' + u.no + '강 — ' + esc(u.short) + ' (현재 ' + pct(u.rate) + ')</option>';
    }).join('');
    return list.length;
  }

  function calcPreview() {
    var u = findUnit($('m3f-pa-unit').value);
    var raw = $('m3f-pa-rate').value;
    var rate = parseFloat(raw);
    if (!u) return { error: '보정 가능한 차시가 없습니다.' };
    if (raw === '' || isNaN(rate) || rate < 0 || rate > 100) return { error: '보정 후 진도율은 0 ~ 100% 범위로 입력해 주세요.' };
    rate = r1(rate);
    var next = r1(prog.overall + (rate - u.rate) * u.run / TOTAL_RUNTIME_SEC);
    if (next > 100) next = 100;
    if (next < 0) next = 0;
    return { unit: u, rate: rate, next: next };
  }

  window.m3fUpdateAdjustPreview = function () {
    var box = $('m3f-pa-preview');
    var p = calcPreview();
    if (p.error) { box.className = 'm3f-preview warn'; box.textContent = p.error; return; }
    var ok = p.next >= prog.threshold;
    box.className = 'm3f-preview' + (ok ? '' : ' warn');
    box.textContent = '보정 반영 시 전체 가중평균 진도율: ' + pct(prog.overall) + ' ➔ ' + pct(p.next) +
      ' (환급 인정 기준 ' + prog.threshold + '% ' + (ok ? '충족' : '미달') + ' · 환급 심사 화면에 [보정 포함] 배지 자동 노출)';
  };

  window.m3fUpdateReasonCount = function () {
    var len = $('m3f-pa-reason').value.trim().length;
    var el = $('m3f-pa-reason-count');
    el.textContent = '현재 ' + len + '자 / 최소 10자';
    el.style.color = len >= 10 ? 'var(--success)' : 'var(--text-muted)';
  };

  window.m3fSetRatePreset = function (v) { $('m3f-pa-rate').value = v; window.m3fUpdateAdjustPreview(); };

  window.m3fOnEvidenceSelected = function (input) {
    if (input.files && input.files[0]) evidenceName = input.files[0].name;
    $('m3f-pa-filename').textContent = evidenceName || '선택된 파일 없음';
  };
  window.m3fRemoveEvidence = function () {
    evidenceName = '';
    $('m3f-pa-file').value = '';
    $('m3f-pa-filename').textContent = '선택된 파일 없음';
  };

  window.openProgressAdjustModal = function (unitNo) {
    var target = findUnit(unitNo);
    if (!target || target.adjusted) {
      target = units.filter(function (u) { return !u.adjusted && u.rate < 100; })[0] || units.filter(function (u) { return !u.adjusted; })[0];
    }
    if (!target) { toast('보정 가능한 차시가 없습니다. (모든 차시 보정 완료)'); return; }
    fillUnitOptions(target.no);
    $('m3f-pa-rate').value = 100;
    $('m3f-pa-type').selectedIndex = 0;
    $('m3f-pa-reason').value = '';
    $('m3f-pa-file').value = '';
    evidenceName = 'cs_evidence_capture.png';
    $('m3f-pa-filename').textContent = evidenceName;
    window.m3fUpdateReasonCount();
    window.m3fUpdateAdjustPreview();
    openModalEl('modalProgressAdjust');
  };
  window.closeProgressAdjustModal = function () { closeModalEl('modalProgressAdjust'); };

  window.submitProgressAdjustLedger = function () {
    var p = calcPreview();
    if (p.error) { toast(p.error); return; }
    if (p.rate === p.unit.rate) { toast('보정 후 진도율이 현재 진도율과 동일합니다. 값을 확인해 주세요.'); return; }
    var reason = $('m3f-pa-reason').value.trim();
    if (reason.length < 10) { toast('상세 보정 사유를 최소 10자 이상 입력해 주세요 (감사 로그 기록 필수).'); $('m3f-pa-reason').focus(); return; }
    if (!evidenceName) { toast('근거 자료(증빙 파일)를 첨부해 주세요.'); return; }

    var u = p.unit;
    var before = u.rate;
    var ovBefore = prog.overall;
    var id = 'PRG-ADJ-2026-' + pad(++prog.seq, 3);
    var at = nowText();

    if (before < 100 && p.rate >= 100) prog.completed += 1;
    if (before >= 100 && p.rate < 100) prog.completed -= 1;
    u.origRate = before;
    u.rate = p.rate;
    u.adjusted = true;
    u.adjId = id;
    u.last = at;
    prog.overall = p.next;
    prog.adjCount += 1;

    adjLog.unshift({ id: id, at: at, target: COURSE_SHORT + ' · ' + u.no + '강', before: before, after: p.rate, ovBefore: ovBefore, ovAfter: p.next, type: $('m3f-pa-type').value, detail: reason, file: evidenceName, admin: ADMIN_NAME });

    renderUnits();
    renderAdjLog();
    flashRow(document.querySelector('#m3f-unit-body tr[data-unit="' + u.no + '"]'));
    flashRow(document.querySelector('#m3f-adjlog-body tr[data-adj="' + id + '"]'));
    window.closeProgressAdjustModal();
    toast('[' + id + '] ' + u.no + '강 진도율이 ' + pct(before) + ' ➔ ' + pct(p.rate) + '로 즉시 보정되었습니다. (가중평균 ' + pct(ovBefore) + ' ➔ ' + pct(p.next) + ' · 환급 심사 [진도율 보정 포함] 자동 분류)');
  };

  window.m3fShowAdjHistory = function (adjId) {
    var tr = document.querySelector('#m3f-adjlog-body tr[data-adj="' + adjId + '"]');
    if (!tr) { toast('해당 보정 이력을 찾을 수 없습니다.'); return; }
    tr.scrollIntoView({ behavior: 'smooth', block: 'center' });
    flashRow(tr);
  };

  window.m3fRecalcProgress = function () {
    $('m3f-recalc-at').textContent = nowText();
    renderUnits();
    toast('재생시간 가중평균 진도율을 실시간 재집계했습니다: ' + pct(prog.overall) + ' (' + prog.completed + ' / ' + prog.totalUnits + '강 완료 · 보정 포함 ' + prog.adjCount + '건)');
  };

  /* =====================================================================
   * 작업 2. 신규 태그 생성(S1) · 그룹 생성 & 다중 태그 연결(S2)
   * ===================================================================== */
  var CONSENT_RATIO = 0.9417;
  var AND_FACTOR = 0.533;
  var TOTAL_MEMBERS = 12480;
  var tagOrder = ['TAG-FREE-30D', 'TAG-CAFE-AUTH', 'TAG-PASS-2026', 'TAG-LOW-PROG', 'TAG-INACTIVE-14D'];
  var tagMeta = {
    'TAG-FREE-30D': { label: '무료회원×30일접속', count: 4208 },
    'TAG-CAFE-AUTH': { label: '산준모 카페 인증', count: 8940 },
    'TAG-PASS-2026': { label: '환급반 수강생', count: 1450 },
    'TAG-LOW-PROG': { label: '진도율 30% 미만', count: 1872 },
    'TAG-INACTIVE-14D': { label: '14일 미접속', count: 3315 }
  };
  var builder = { selected: ['TAG-FREE-30D', 'TAG-CAFE-AUTH', 'TAG-PASS-2026'], op: 'AND', mode: 'DYNAMIC', editing: null };
  var customTagSeq = 0;

  var groups = [
    { code: 'GRP-2026-01', name: '환급반 중도이탈 위험군 케어 그룹', tags: ['TAG-PASS-2026', 'TAG-LOW-PROG', 'TAG-INACTIVE-14D'], op: 'AND', mode: 'DYNAMIC', members: 412, consent: 388, updated: '2026.10.18 06:00' },
    { code: 'GRP-2026-02', name: '카페 인증 미결제 전환 타겟 그룹', tags: ['TAG-CAFE-AUTH', 'TAG-FREE-30D'], op: 'AND', mode: 'DYNAMIC', members: 1204, consent: 1089, updated: '2026.10.18 06:00' },
    { code: 'GRP-2026-03', name: '2026년 2회 정기시험 응시자 스냅샷', tags: ['TAG-PASS-2026', 'TAG-CAFE-AUTH'], op: 'OR', mode: 'STATIC', members: 2140, consent: 1950, updated: '2026.09.15 11:20' }
  ];
  var groupSeq = 3;

  function tagPill(code) {
    var m = tagMeta[code];
    return '<span class="m3f-tagpill">[' + esc(code) + (m ? ' ' + esc(m.label) : '') + ']</span>';
  }
  function modeLabel(mode) { return mode === 'STATIC' ? '정적 (명단 고정)' : '동적 (매일 06:00)'; }

  function estimate(tags, op) {
    if (!tags.length) return { members: 0, consent: 0 };
    var counts = tags.map(function (t) { return (tagMeta[t] && tagMeta[t].count) || 0; });
    var members;
    if (op === 'AND') {
      members = Math.round(Math.min.apply(null, counts) * Math.pow(AND_FACTOR, tags.length - 1));
    } else {
      var max = Math.max.apply(null, counts);
      var sum = counts.reduce(function (a, b) { return a + b; }, 0);
      members = Math.min(TOTAL_MEMBERS, Math.round(max + (sum - max) * 0.35));
    }
    return { members: members, consent: Math.round(members * CONSENT_RATIO) };
  }

  function renderChips() {
    var wrap = $('m3f-chip-wrap');
    if (!wrap) return;
    wrap.innerHTML = tagOrder.map(function (code) {
      var on = builder.selected.indexOf(code) !== -1;
      return '<button type="button" class="m3f-chip' + (on ? ' on' : '') + '" onclick="m3fToggleChip(\'' + code + '\')">' +
        (on ? '✓ ' : '') + esc(code) + ' ' + esc(tagMeta[code].label) + '</button>';
    }).join('');
  }

  function renderGroupPreview() {
    var e = estimate(builder.selected, builder.op);
    var pending = builder.selected.some(function (t) { return tagMeta[t] && tagMeta[t].pending; });
    $('m3f-grp-preview').textContent = builder.selected.length
      ? '예상 매칭 회원: ' + num(e.members) + '명 — 마케팅 수신동의 ' + num(e.consent) + '명 / 거부 ' + num(e.members - e.consent) + '명' + (pending ? ' (신규 태그 집계 대기 포함)' : '')
      : '연결할 태그를 1개 이상 선택해 주세요.';
  }

  function renderGroups() {
    var body = $('m3f-group-body');
    if (!body) return;
    body.innerHTML = groups.map(function (g) {
      var combo = g.tags.map(tagPill).join('<span class="m3f-op">' + g.op + '</span>');
      return '<tr data-grp="' + esc(g.code) + '">' +
        '<td><code>' + esc(g.code) + '</code></td>' +
        '<td><strong>' + esc(g.name) + '</strong>' + (g.memo ? '<div class="m3f-hint">' + esc(g.memo) + '</div>' : '') + '</td>' +
        '<td>' + combo + '</td>' +
        '<td><span class="badge ' + (g.mode === 'STATIC' ? 'badge-gray' : 'badge-blue') + '">' + modeLabel(g.mode) + '</span></td>' +
        '<td class="tr-right"><strong>' + num(g.members) + '명</strong> <span style="color:var(--text-muted);">(동의 ' + num(g.consent) + '명)</span></td>' +
        '<td>' + esc(g.updated) + '</td>' +
        '<td><div class="m3f-actions">' +
          '<button type="button" class="btn btn-sm btn-outline" onclick="m3fGroupMessage(\'' + g.code + '\')">단체 알림톡 발송</button>' +
          '<button type="button" class="btn btn-sm btn-outline" onclick="m3fGroupCoupon(\'' + g.code + '\')">쿠폰 발급</button>' +
          '<button type="button" class="btn btn-sm btn-outline" onclick="m3fEditGroup(\'' + g.code + '\')">태그 연결 수정</button>' +
        '</div></td></tr>';
    }).join('');
  }

  function syncBuilderRadios() {
    document.querySelectorAll('input[name="m3f-grp-op"]').forEach(function (r) { r.checked = (r.value === builder.op); });
    document.querySelectorAll('input[name="m3f-grp-mode"]').forEach(function (r) { r.checked = (r.value === builder.mode); });
  }

  function setEditMode(code) {
    builder.editing = code;
    var badge = $('m3f-grp-edit-badge');
    if (code) {
      badge.style.display = 'inline-block';
      badge.textContent = code + ' 태그 연결 수정 중';
      $('m3f-grp-save-btn').textContent = '✓ 태그 연결 수정 저장';
      $('m3f-grp-cancel-edit').style.display = 'block';
    } else {
      badge.style.display = 'none';
      $('m3f-grp-save-btn').textContent = '+ 그룹 생성 및 태그 연결 저장';
      $('m3f-grp-cancel-edit').style.display = 'none';
    }
  }

  function findGroup(code) { for (var i = 0; i < groups.length; i++) if (groups[i].code === code) return groups[i]; return null; }

  function validateBuilder() {
    var name = $('m3f-grp-name').value.trim();
    if (name.length < 2) { toast('그룹명을 2자 이상 입력해 주세요.'); $('m3f-grp-name').focus(); return null; }
    if (!builder.selected.length) { toast('연결할 태그를 1개 이상 선택해 주세요.'); return null; }
    return name;
  }

  window.m3fToggleChip = function (code) {
    var i = builder.selected.indexOf(code);
    if (i === -1) builder.selected.push(code); else builder.selected.splice(i, 1);
    renderChips();
    renderGroupPreview();
  };
  window.m3fSetGroupOp = function (v) { builder.op = v; renderGroupPreview(); };
  window.m3fSetGroupMode = function (v) { builder.mode = v; };

  window.openGroupSaveModal = function () {
    var name = validateBuilder();
    if (!name) return;
    var e = estimate(builder.selected, builder.op);
    $('m3f-gs-summary').innerHTML =
      '<tr><th>그룹명</th><td><strong>' + esc(name) + '</strong>' + (builder.editing ? ' <span class="badge badge-amber">' + esc(builder.editing) + ' 수정</span>' : '') + '</td></tr>' +
      '<tr><th>연결 태그 조합</th><td>' + builder.selected.map(tagPill).join('<span class="m3f-op">' + builder.op + '</span>') + '</td></tr>' +
      '<tr><th>결합 연산자</th><td>' + (builder.op === 'AND' ? 'AND (모든 태그 동시 충족)' : 'OR (하나라도 충족)') + '</td></tr>' +
      '<tr><th>갱신 방식</th><td>' + (builder.mode === 'STATIC' ? '정적 그룹 (생성 시점 대상자 명단 고정)' : '동적 그룹 (매일 06:00 조건 매칭 회원 자동 편입/이탈)') + '</td></tr>' +
      '<tr><th>예상 매칭 회원</th><td><strong>' + num(e.members) + '명</strong> — 마케팅 수신동의 ' + num(e.consent) + '명 / 거부 ' + num(e.members - e.consent) + '명</td></tr>';
    $('m3f-gs-memo').value = '';
    openModalEl('modalGroupSave');
  };
  window.closeGroupSaveModal = function () { closeModalEl('modalGroupSave'); };

  window.m3fSaveGroup = function (fromModal) {
    var name = validateBuilder();
    if (!name) return;
    var e = estimate(builder.selected, builder.op);
    var memo = fromModal ? $('m3f-gs-memo').value.trim() : '';
    var g, isNew = !builder.editing;
    if (isNew) {
      g = { code: 'GRP-2026-' + pad(++groupSeq, 2) };
      groups.unshift(g);
    } else {
      g = findGroup(builder.editing);
      if (!g) { isNew = true; g = { code: 'GRP-2026-' + pad(++groupSeq, 2) }; groups.unshift(g); }
    }
    g.name = name;
    g.tags = builder.selected.slice();
    g.op = builder.op;
    g.mode = builder.mode;
    g.members = e.members;
    g.consent = e.consent;
    g.updated = nowText();
    if (memo) g.memo = memo;

    renderGroups();
    flashRow(document.querySelector('#m3f-group-body tr[data-grp="' + g.code + '"]'));
    if (fromModal) window.closeGroupSaveModal();
    $('m3f-grp-name').value = '';
    setEditMode(null);
    toast((isNew ? '회원 그룹 [' + g.code + '] 이(가) 생성되고 ' : '[' + g.code + '] 태그 연결이 수정되고 ') + g.tags.length + '개 태그가 ' + g.op + ' 조건으로 연결되었습니다. (' + modeLabel(g.mode) + ' · ' + num(g.members) + '명)');
  };

  window.m3fEditGroup = function (code) {
    var g = findGroup(code);
    if (!g) return;
    builder.selected = g.tags.slice();
    builder.op = g.op;
    builder.mode = g.mode;
    $('m3f-grp-name').value = g.name;
    syncBuilderRadios();
    renderChips();
    renderGroupPreview();
    setEditMode(code);
    $('m3f-group-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  window.m3fCancelGroupEdit = function () { $('m3f-grp-name').value = ''; setEditMode(null); };

  window.m3fGroupMessage = function (code) {
    var g = findGroup(code);
    if (!g) return;
    if (confirm('[' + g.code + '] ' + g.name + '\n수신동의 ' + num(g.consent) + '명 대상 단체 알림톡 발송 화면(ADMN-CONF-004)으로 이동할까요?')) {
      window.location.href = 'ADMN-CONF-004_baseline.html?view=send&target=group&grp=' + encodeURIComponent(g.code) + '&cnt=' + g.consent;
    }
  };
  window.m3fGroupCoupon = function (code) {
    var g = findGroup(code);
    if (!g) return;
    if (confirm('[' + g.code + '] ' + g.name + '\n소속 회원 ' + num(g.members) + '명 대상 쿠폰 대량 발급 화면(ADMN-PROM-002)으로 이동할까요?')) {
      window.location.href = 'ADMN-PROM-002_baseline.html?target=group&grp=' + encodeURIComponent(g.code) + '&cnt=' + g.members;
    }
  };

  /* ---------- 모달 A: 신규 태그 생성 ---------- */
  window.openTagCreateModal = function () {
    ['m3f-tc-name', 'm3f-tc-code', 'm3f-tc-expr', 'm3f-tc-memo'].forEach(function (id) { $(id).value = ''; });
    document.querySelectorAll('input[name="m3f-tc-type"]').forEach(function (r) { r.checked = (r.value === 'AUTO'); });
    $('m3f-tc-domain').selectedIndex = 0;
    $('m3f-tc-cycle').selectedIndex = 0;
    $('m3f-tc-exit').selectedIndex = 0;
    window.m3fToggleTagRule();
    openModalEl('modalTagCreate');
  };
  window.closeTagCreateModal = function () { closeModalEl('modalTagCreate'); };

  window.m3fToggleTagRule = function () {
    var auto = (document.querySelector('input[name="m3f-tc-type"]:checked') || {}).value !== 'MANUAL';
    $('m3f-tc-rule').style.display = auto ? 'block' : 'none';
  };

  window.m3fAutoTagCode = function () {
    var code;
    do { code = 'TAG-CUSTOM-' + pad(++customTagSeq, 3); } while (tagMeta[code]);
    $('m3f-tc-code').value = code;
  };

  window.submitTagCreate = function () {
    var name = $('m3f-tc-name').value.trim();
    var code = $('m3f-tc-code').value.trim().toUpperCase();
    var auto = (document.querySelector('input[name="m3f-tc-type"]:checked') || {}).value !== 'MANUAL';
    var expr = $('m3f-tc-expr').value.trim();
    var memo = $('m3f-tc-memo').value.trim();

    if (name.length < 2) { toast('태그명을 2자 이상 입력해 주세요.'); $('m3f-tc-name').focus(); return; }
    if (!/^TAG-[A-Z0-9]+(-[A-Z0-9]+)*$/.test(code)) { toast('태그 코드는 TAG- 로 시작하는 영문 대문자·숫자·하이픈 조합으로 입력해 주세요. (예: TAG-LOW-PROG-30)'); $('m3f-tc-code').focus(); return; }
    if (tagMeta[code]) { toast('이미 존재하는 태그 코드입니다: ' + code); $('m3f-tc-code').focus(); return; }
    if (auto && expr.length < 5) { toast('자동 규칙 태그는 상세 조건식을 5자 이상 입력해 주세요.'); $('m3f-tc-expr').focus(); return; }

    var domain = $('m3f-tc-domain').value;
    var cycleSel = $('m3f-tc-cycle');
    var cycleText = cycleSel.options[cycleSel.selectedIndex].text;
    var exitText = $('m3f-tc-exit').value;
    var condHtml = auto
      ? '<span class="badge badge-blue">' + esc(domain) + '</span> ' + esc(expr) + '<div class="m3f-hint">평가: ' + esc(cycleText) + ' · 이탈 시: ' + esc(exitText) + '</div>'
      : '<span class="badge badge-gray">수동 부여</span> 관리자가 회원 선택 후 직접 부여';
    var countText = !auto ? '0 명 (수동 부여 대기)' : (cycleSel.value === 'REALTIME' ? '0 명 (실시간 집계 시작)' : '집계 대기 (다음 06:00 배치)');

    var body = $('tag-list-body');
    var tr = document.createElement('tr');
    tr.setAttribute('data-tag', code);
    tr.innerHTML =
      '<td><code>' + esc(code) + '</code> <span class="badge badge-green">신규</span></td>' +
      '<td><strong>' + esc(name) + '</strong></td>' +
      '<td>' + condHtml + '</td>' +
      '<td class="tr-right" style="font-weight:800; color:var(--text-muted);">' + countText + '</td>' +
      '<td>' + (memo ? esc(memo) : '—') + '</td>' +
      '<td><a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급 이동 ↗</a></td>';
    body.appendChild(tr);
    flashRow(tr);

    tagMeta[code] = { label: name, count: 0, pending: true };
    tagOrder.push(code);
    renderChips();
    renderGroupPreview();

    window.closeTagCreateModal();
    toast('신규 태그 [' + code + '] ' + name + ' 이(가) 생성되어 태그 목록과 그룹 연결 태그 선택에 즉시 추가되었습니다.');
  };

  /* ---------- 초기 렌더 ---------- */
  renderUnits();
  renderAdjLog();
  renderChips();
  renderGroupPreview();
  renderGroups();
})();
</script>
'''

USER_REQUIRED_IDS = [
    "m3f-progress-card", "m3f-unit-body", "m3f-adjlog-body", "modalProgressAdjust",
    "modalTagCreate", "modalGroupSave", "tag-list-body", "m3f-group-card", "m3f-group-body", "m3f-chip-wrap",
]


def patch_user_001(src):
    # 0) 스타일
    src = insert_before(src, "  </style>\n</head>", USER_CSS, "USER: </style></head>")

    # 1) view=course 하단 섹션 A/B (view-tags 직전의 </section>)
    #    기존 카드 번호 1(계약 목록)·2(기간 조정)·3(동시 접속 제어)과 겹치지 않도록 4·5번 부여
    src = insert_before(
        src,
        "      </section>\n\n      <!-- ================================================================= -->\n      <!-- VIEW 4: ADMN-USER-006",
        USER_COURSE_SECTIONS,
        "USER: view-course 종료부",
    )

    # 2-0) 태그 목록 카드에 번호 부여 (신규 '2.' 카드와 순번 정합)
    src = replace_once(
        src,
        '<div class="card-title">수평적 다중 태그(N:M) 그룹 관리',
        '<div class="card-title">1. 수평적 다중 태그(N:M) 그룹 관리',
        "USER: 태그 목록 카드 제목",
    )

    # 2-1) 신규 태그 생성 버튼 바인딩
    src = replace_once(
        src,
        "onclick=\"showToast('신규 커스텀 태그가 생성되었습니다.')\">＋ 신규 태그 생성</button>",
        "onclick=\"openTagCreateModal()\">＋ 신규 태그 생성</button>",
        "USER: 신규 태그 생성 버튼",
    )

    # 2-2) 태그 목록 tbody id 부여
    tag_head = ('<tr><th>태그 코드</th><th>태그명</th><th>조합 조건 (N:M)</th><th class="tr-right">소속 회원 수</th>'
                '<th>연동 프로모션 (ADMN-PROM-002)</th><th>관리</th></tr>\n              </thead>\n              <tbody>')
    src = replace_once(src, tag_head, tag_head[:-len("<tbody>")] + '<tbody id="tag-list-body">', "USER: 태그 목록 tbody")

    # 2-3) 그룹 조합에서 참조하는 태그 2종을 태그 목록에 등록 (TAG-PASS-2026 행 뒤)
    src = insert_after(
        src,
        '<td><a href="ADMN-SETT-006_baseline.html" class="btn btn-sm btn-outline">환급반 관리 ↗</a></td>\n                </tr>',
        USER_TAG_EXTRA_ROWS,
        "USER: TAG-PASS-2026 행",
    )

    # 2-4) view=tags 내부 섹션 2 (view-blacklist 직전의 </section>)
    src = insert_before(src, "      </section>\n\n      <!-- ==================== VIEW 5", USER_TAG_SECTION, "USER: view-tags 종료부")

    # 3) 모달 + JS
    src = insert_before(src, "</body>", USER_MODALS_AND_JS, "USER: </body>")
    return src, USER_REQUIRED_IDS


# =============================================================================
# [ADMN-RFD-002] 작업 3
# =============================================================================
RFD_CSS = r'''
    /* === [M3F-PATCH-v1] ADMN-RFD-003-S2 환불 완료 후 별도 보정 거래 스타일 === */
    #modalRefundAdjust { background: rgba(15, 23, 42, 0.55); }
    #modalRefundAdjust .modal-box { max-width: 780px; width: 95%; }
    .m3f-principle { background:#FFFBEB; border:1px solid #FDE68A; border-left:4px solid #D97706; border-radius:8px; padding:11px 14px; font-size:12.5px; color:#78350F; line-height:1.6; }
    .m3f-sec { border:1px solid #E2E8F0; border-radius:8px; padding:12px 14px; margin-bottom:12px; background:#FFFFFF; }
    .m3f-sec-title { font-size:12.5px; font-weight:800; color:#0F172A; margin-bottom:8px; }
    .m3f-req { color:#DC2626; }
    .m3f-lbl { display:block; font-size:12px; font-weight:700; margin-bottom:4px; color:#334155; }
    .m3f-sum-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; margin-top:8px; font-size:12px; }
    .m3f-sum-grid > div { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:8px 10px; }
    .m3f-sum-grid span { display:block; color:#64748B; font-size:11px; font-weight:600; margin-bottom:2px; }
    .m3f-type-row { display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; }
    .m3f-type-card { display:flex; gap:8px; align-items:flex-start; border:1px solid #CBD5E1; border-radius:8px; padding:9px 10px; cursor:pointer; font-size:12px; }
    .m3f-type-card strong { display:block; font-size:12.5px; margin-bottom:2px; }
    .m3f-type-card small { color:#64748B; line-height:1.45; }
    .m3f-type-card.on { border-color:#2563EB; background:#EFF6FF; }
    .m3f-grid3 { display:grid; grid-template-columns:1fr 1fr 1.3fr; gap:10px; }
    .m3f-settle { margin-top:8px; padding:8px 10px; border-radius:6px; background:#EFF6FF; border:1px solid #BFDBFE; color:#1E3A8A; font-size:12px; font-weight:700; }
    .m3f-prev-table { width:100%; border-collapse:collapse; font-size:12px; }
    .m3f-prev-table th, .m3f-prev-table td { border:1px solid #E2E8F0; padding:7px 9px; text-align:right; }
    .m3f-prev-table th { background:#F8FAFC; color:#475569; font-weight:700; }
    .m3f-prev-table td:first-child, .m3f-prev-table th:first-child { text-align:left; }
    .m3f-warn { display:none; margin-top:8px; padding:8px 10px; border-radius:6px; background:#FEF2F2; border:1px solid #FECACA; color:#991B1B; font-size:12px; font-weight:700; }
    .m3f-hint { font-size:11.5px; color:#64748B; margin-top:4px; }
    .m3f-flash td { animation: m3fFlash 2.6s ease-out; }
    @keyframes m3fFlash { 0% { background:#DCFCE7; } 100% { background:transparent; } }
    .m3f-toast { position:fixed; right:26px; bottom:26px; z-index:12000; max-width:520px; background:#0F172A; color:#FFFFFF; padding:13px 18px; border-radius:10px; font-size:13px; font-weight:700; box-shadow:0 12px 28px rgba(15,23,42,0.28); display:none; line-height:1.5; }
'''

RFD_LEDGER_CARD = r'''
        <!-- [M3F-PATCH-v1] ADMN-RFD-003-S2 환불 완료 후 별도 보정 거래 원장 -->
        <div class="card" id="m3f-rfd-adj-card" style="margin-top:16px;">
          <div class="card-header">
            <div class="card-title">
              <span>환불 완료 후 별도 보정 거래 원장 (원 거래 불변 · 사후 추가환불 / 환수 / 포인트 보정)</span>
              <span class="badge badge-purple">ADMN-RFD-003-S2</span>
            </div>
            <span class="badge badge-gray" id="m3f-rfd-adj-count">보정 거래 2건</span>
          </div>
          <div class="card-body" style="padding-bottom:4px;">
            <div class="m3f-principle">
              🔒 <strong>원 거래 불변 원칙</strong> — 이미 완료된 환불 원장(원 거래)의 금액과 이력은 회계 감사 추적을 위해 절대 직접 수정(Overwrite)하지 않으며, 착오 정정·추가 환불·과오납 회수·만료 포인트 추가 복원이 필요한 경우 원 환불번호에 연결된 <strong>[별도 보정 거래(Adjustment)]</strong> 전표를 생성하여 처리합니다.
            </div>
          </div>
          <div class="table-wrap">
            <table class="data-table">
              <thead>
                <tr>
                  <th>보정거래번호 / 등록일시</th>
                  <th>연결 원 환불번호 (주문번호)</th>
                  <th>회원명</th>
                  <th>보정 거래 유형</th>
                  <th class="num">금회 보정 금액 / 포인트</th>
                  <th class="num">보정 후 누적 환불액</th>
                  <th>집행 수단 · 정산 반영월</th>
                  <th>사유 및 처리자</th>
                </tr>
              </thead>
              <tbody id="m3f-rfd-adj-body">
                <tr><td colspan="8" style="text-align:center; color:#64748B;">보정 거래 원장을 불러오는 중입니다…</td></tr>
              </tbody>
            </table>
          </div>
        </div>
'''

RFD_MODAL_AND_JS = r'''
<!-- ==================== [M3F-PATCH-v1] ADMN-RFD-003-S2 환불 완료 건 별도 보정 거래 등록 모달 ==================== -->
<div class="modal-backdrop" id="modalRefundAdjust" aria-hidden="true">
  <div class="modal-box">
    <div class="modal-header" style="background:#EFF6FF; color:#1E3A8A; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-weight:800; font-size:13.5px;">➕ 환불 완료 건 별도 보정 거래 등록 (ADMN-RFD-003-S2 · 원 거래 불변)</span>
      <button type="button" class="btn btn-sm btn-outline" onclick="closeRefundAdjustModal()">✕</button>
    </div>
    <div class="modal-body" style="max-height:72vh; overflow-y:auto;">

      <div class="m3f-sec">
        <div class="m3f-sec-title">1. 대상 원 환불 건 선택 및 요약 (읽기 전용)</div>
        <select class="form-select" id="m3f-ra-rfd" style="width:100%; height:34px;" onchange="m3fRaRefresh()">
          <option value="RFD-2026-001120">RFD-2026-001120 | 박영희 | 원결제 385,000원 | 기 환불확정 297,111원 | 2026-10 정산반영</option>
          <option value="RFD-2026-001098">RFD-2026-001098 | 이민호 | 원결제 180,000원 | 기 환불확정 22,933원 | 원귀속 2026-08</option>
        </select>
        <div class="m3f-sum-grid" id="m3f-ra-summary"></div>
      </div>

      <div class="m3f-sec">
        <div class="m3f-sec-title">2. 보정 거래 유형 선택 <span class="m3f-req">*</span></div>
        <div class="m3f-type-row">
          <label class="m3f-type-card on" data-type="ADD">
            <input type="radio" name="m3f-ra-type" value="ADD" checked onchange="m3fRaTypeChange()" />
            <span><strong>추가 환불 지급 (+)</strong><small>이용일수·위약금 재산정에 따른 추가 환불금 지급</small></span>
          </label>
          <label class="m3f-type-card" data-type="RECOVER">
            <input type="radio" name="m3f-ra-type" value="RECOVER" onchange="m3fRaTypeChange()" />
            <span><strong>과오납 환불금 회수 (−)</strong><small>초과 환불금 고객 입금 환수 및 정산 복원</small></span>
          </label>
          <label class="m3f-type-card" data-type="POINT">
            <input type="radio" name="m3f-ra-type" value="POINT" onchange="m3fRaTypeChange()" />
            <span><strong>포인트 단독 보정 (P)</strong><small>현금 변동 없이 LIFO 복원 유상 포인트 또는 마이너스 부채 포인트 보정</small></span>
          </label>
        </div>
      </div>

      <div class="m3f-sec">
        <div class="m3f-sec-title">3. 금회 보정 금액 · 포인트 및 집행 / 정산 연동 방식</div>
        <div class="m3f-grid3">
          <div>
            <label class="m3f-lbl" for="m3f-ra-amount">금회 보정 금액 (원)</label>
            <input type="number" class="form-control" id="m3f-ra-amount" min="0" step="1" placeholder="예: 15824" style="width:100%; height:34px; font-weight:700;" oninput="m3fRaRefresh()" />
            <div class="m3f-hint" id="m3f-ra-amount-hint">양수로 입력 · 부호는 보정 유형에 따라 자동 적용</div>
          </div>
          <div>
            <label class="m3f-lbl" for="m3f-ra-point">금회 보정 포인트 (P)</label>
            <input type="number" class="form-control" id="m3f-ra-point" step="1" placeholder="예: 0" style="width:100%; height:34px; font-weight:700;" oninput="m3fRaRefresh()" />
            <div class="m3f-hint">복원은 양수(+), 차감은 음수(−)로 입력</div>
          </div>
          <div>
            <label class="m3f-lbl" for="m3f-ra-exec">금융 집행 방식</label>
            <select class="form-select" id="m3f-ra-exec" style="width:100%; height:34px;" onchange="m3fRaRefresh()">
              <option>토스페이먼츠 PG 추가 부분취소</option>
              <option>고객 환불계좌 무통장 입금</option>
              <option>고객 과오납 환수 입금 확인</option>
              <option>포인트 원장만 조정</option>
            </select>
          </div>
        </div>
        <div class="m3f-settle" id="m3f-ra-settle">정산 연동: 당월(2026-10) 미마감 ➔ 4단계 환불 공제 자동 합산</div>
      </div>

      <div class="m3f-sec">
        <div class="m3f-sec-title">4. 보정 전 · 후 누적 비교 프리뷰</div>
        <table class="m3f-prev-table">
          <thead>
            <tr><th>구분</th><th>기 확정 내역 (원 거래 불변)</th><th>금회 보정 증감</th><th>보정 반영 후 누적 최종값</th></tr>
          </thead>
          <tbody id="m3f-ra-preview"></tbody>
        </table>
        <div class="m3f-warn" id="m3f-ra-warn"></div>
      </div>

      <div class="m3f-sec" style="margin-bottom:0;">
        <div class="m3f-sec-title">5. 보정 거래 등록 사유 <span class="m3f-req">*</span> <span style="font-weight:500; color:#64748B;">(최소 10자 · 감사 로그 영구 기록)</span></div>
        <textarea class="form-control" id="m3f-ra-reason" rows="2" style="width:100%; font-size:12px;" placeholder="예) 휴강 일수(3일) 일할 계산 누락분 사후 추가 환불 (재무 이정산)" oninput="m3fRaReasonCount()"></textarea>
        <div class="m3f-hint" id="m3f-ra-reason-count">현재 0자 / 최소 10자</div>
      </div>
    </div>
    <div class="modal-footer" style="padding:12px 20px; background:#F8FAFC; border-top:1px solid #E2E8F0; display:flex; justify-content:flex-end; gap:8px;">
      <button type="button" class="btn btn-outline" onclick="closeRefundAdjustModal()">취소</button>
      <button type="button" class="btn btn-primary" id="m3f-ra-submit" onclick="submitRefundAdjust()">✓ 별도 보정 거래 전표 생성</button>
    </div>
  </div>
</div>
<div class="m3f-toast" id="m3f-toast"></div>

<script data-m3f="rfd-002">
/* === [M3F-PATCH-v1] ADMN-RFD-003-S2 환불 완료 후 별도 보정 거래 (원 거래 불변) === */
(function () {
  'use strict';

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad(n, w) { n = String(n); while (n.length < w) n = '0' + n; return n; }
  function won(n) { return Number(n).toLocaleString('ko-KR') + '원'; }
  function pts(n) { return Number(n).toLocaleString('ko-KR') + ' P'; }
  function signed(n, unit) { return (n > 0 ? '+' : n < 0 ? '−' : '') + Math.abs(n).toLocaleString('ko-KR') + unit; }
  function nowText() {
    var d = new Date();
    return d.getFullYear() + '-' + pad(d.getMonth() + 1, 2) + '-' + pad(d.getDate(), 2) + ' ' + pad(d.getHours(), 2) + ':' + pad(d.getMinutes(), 2);
  }
  function toast(msg) {
    var t = $('m3f-toast');
    if (!t) { alert(msg); return; }
    t.textContent = msg;
    t.style.display = 'block';
    clearTimeout(window.__m3fToastTimer);
    window.__m3fToastTimer = setTimeout(function () { t.style.display = 'none'; }, 4200);
  }

  var OPERATOR = '운영1팀 이지훈';
  var CURRENT_MONTH = '2026-10';
  var EXEC_BY_TYPE = { ADD: '토스페이먼츠 PG 추가 부분취소', RECOVER: '고객 과오납 환수 입금 확인', POINT: '포인트 원장만 조정' };

  /* 원 환불 건 (원 거래 금액은 불변 · 보정 누적은 별도 필드로 관리) */
  var RFD = {
    'RFD-2026-001120': { name: '박영희', order: 'SJM-20261001-002190', paid: 385000, origRefund: 297111, cumRefund: 312935, origPoint: 15000, cumPoint: 15000, month: '2026-10', closed: false, adjCount: 1 },
    'RFD-2026-001098': { name: '이민호', order: 'SJM-20260822-003110', paid: 180000, origRefund: 22933, cumRefund: 22933, origPoint: -32200, cumPoint: -31200, month: '2026-08', closed: true, adjCount: 1 }
  };

  var ledger = [
    { id: 'ADJ-2026-000032', at: '2026-10-16 14:20', rfd: 'RFD-2026-001120', type: 'ADD', typeLabel: '추가 환불 지급 (+현금)', amountText: '+15,824원 (포인트 0P)', cumText: '297,111원 ➔ 312,935원', execText: 'PG 추가 부분취소 · 2026-10 당월 정산 차감 반영', reason: '휴강 일수(3일) 일할 계산 누락분 사후 추가 환불', operator: '재무 이정산' },
    { id: 'ADJ-2026-000031', at: '2026-10-11 11:02', rfd: 'RFD-2026-001098', type: 'POINT', typeLabel: '포인트 보정 (+유상P 복원)', amountText: '0원 (+1,000 P 추가 복원)', cumText: '22,933원 (변동없음)', execText: '포인트 원장 직권 보정 (D+7 만료유예 부여) · 정산 무관', reason: 'LIFO 복원 시 만료일 경계 차감 오차 +1,000P 사후 복원', operator: 'CS 김상담' }
  ];
  var adjSeq = 32;

  var TYPE_BADGE = { ADD: 'badge-blue', RECOVER: 'badge-red', POINT: 'badge-purple' };

  function renderLedger() {
    var body = $('m3f-rfd-adj-body');
    if (!body) return;
    body.innerHTML = ledger.map(function (r) {
      var o = RFD[r.rfd] || {};
      return '<tr data-adj="' + esc(r.id) + '">' +
        '<td><strong>' + esc(r.id) + '</strong><br><span style="font-size:11.5px; color:#64748B;">' + esc(r.at) + '</span></td>' +
        '<td><strong>' + esc(r.rfd) + '</strong><br><span style="font-size:11.5px; color:#64748B;">(' + esc(o.order || '') + ')</span></td>' +
        '<td>' + esc(o.name || '') + '</td>' +
        '<td><span class="badge ' + (TYPE_BADGE[r.type] || 'badge-gray') + '">' + esc(r.typeLabel) + '</span></td>' +
        '<td class="num"><strong>' + esc(r.amountText) + '</strong></td>' +
        '<td class="num">' + esc(r.cumText) + '</td>' +
        '<td>' + esc(r.execText) + '</td>' +
        '<td>' + esc(r.reason) + ' <span style="color:#64748B;">(' + esc(r.operator) + ')</span></td></tr>';
    }).join('');
    var c = $('m3f-rfd-adj-count');
    if (c) c.textContent = '보정 거래 ' + ledger.length + '건';
  }

  function currentType() { return (document.querySelector('input[name="m3f-ra-type"]:checked') || {}).value || 'ADD'; }

  function settleInfo(o, type) {
    if (type === 'POINT') return { full: '정산 연동: 포인트 원장 직권 보정 ➔ 정산 무관 (현금 변동 없음)', short: '정산 무관' };
    if (!o.closed) {
      return {
        full: '정산 연동: 당월(' + CURRENT_MONTH + ') 미마감 ➔ 4단계 환불 공제 자동 합산',
        short: CURRENT_MONTH + ' 당월 정산 ' + (type === 'RECOVER' ? '복원' : '차감') + ' 반영'
      };
    }
    return {
      full: '정산 연동: 전월 마감 건 (원귀속 ' + o.month + ') ➔ 정산 수동 조정 전표 자동 생성 (ADMN-SETT-005 화면 이관)',
      short: '원귀속 ' + o.month + ' 마감 ➔ 정산 수동 조정 전표 생성'
    };
  }

  function readInputs() {
    var o = RFD[$('m3f-ra-rfd').value];
    var type = currentType();
    var amt = parseInt($('m3f-ra-amount').value, 10);
    var pt = parseInt($('m3f-ra-point').value, 10);
    amt = isNaN(amt) ? 0 : Math.abs(amt);
    pt = isNaN(pt) ? 0 : pt;
    if (type === 'POINT') amt = 0;
    var delta = type === 'RECOVER' ? -amt : amt;
    return { o: o, type: type, amt: amt, delta: delta, pt: pt, exec: $('m3f-ra-exec').value, reason: $('m3f-ra-reason').value.trim() };
  }

  function validate(v) {
    var finalRefund = v.o.cumRefund + v.delta;
    if (v.type === 'POINT') {
      if (v.pt === 0) return '포인트 단독 보정은 0이 아닌 보정 포인트(복원 +, 차감 −)를 입력해 주세요.';
      if (v.exec !== EXEC_BY_TYPE.POINT) return '포인트 단독 보정은 집행 방식을 [포인트 원장만 조정]으로 선택해 주세요.';
    } else {
      if (v.amt <= 0) return '금회 보정 금액(원)을 1원 이상 입력해 주세요.';
      if (v.exec === EXEC_BY_TYPE.POINT) return '현금 보정 거래는 [포인트 원장만 조정]을 집행 방식으로 선택할 수 없습니다.';
      if (v.type === 'ADD' && v.exec === EXEC_BY_TYPE.RECOVER) return '추가 환불 지급은 [고객 과오납 환수 입금 확인]을 집행 방식으로 선택할 수 없습니다.';
      if (v.type === 'RECOVER' && v.exec !== EXEC_BY_TYPE.RECOVER) return '과오납 환불금 회수는 집행 방식을 [고객 과오납 환수 입금 확인]으로 선택해 주세요.';
    }
    if (finalRefund > v.o.paid) return '보정 후 누적 환불액(' + won(finalRefund) + ')이 원 결제금액(' + won(v.o.paid) + ')을 초과합니다.';
    if (finalRefund < 0) return '회수 금액이 현재 누적 환불액(' + won(v.o.cumRefund) + ')을 초과합니다.';
    return '';
  }

  window.m3fRaRefresh = function () {
    var v = readInputs();
    var o = v.o;
    var finalRefund = o.cumRefund + v.delta;
    var finalPoint = o.cumPoint + v.pt;

    $('m3f-ra-summary').innerHTML =
      '<div><span>회원 / 주문번호</span><strong>' + esc(o.name) + '</strong><br>' + esc(o.order) + '</div>' +
      '<div><span>원 결제금액</span><strong>' + won(o.paid) + '</strong></div>' +
      '<div><span>원 환불확정액 (불변)</span><strong>' + won(o.origRefund) + '</strong><br>포인트 ' + signed(o.origPoint, ' P') + '</div>' +
      '<div><span>현재 누적 (기 보정 ' + o.adjCount + '건 포함)</span><strong style="color:#2563EB;">' + won(o.cumRefund) + '</strong><br>포인트 ' + signed(o.cumPoint, ' P') + '</div>';

    $('m3f-ra-amount').disabled = (v.type === 'POINT');
    $('m3f-ra-amount').style.background = (v.type === 'POINT') ? '#F1F5F9' : '#FFFFFF';
    $('m3f-ra-amount-hint').textContent = v.type === 'POINT' ? '포인트 단독 보정은 현금 변동 0원 고정' : (v.type === 'RECOVER' ? '양수로 입력 · 회수(−)로 자동 적용' : '양수로 입력 · 추가 지급(+)으로 자동 적용');
    $('m3f-ra-settle').textContent = settleInfo(o, v.type).full;

    var rateBefore = (o.cumRefund / o.paid * 100).toFixed(1);
    var rateAfter = (finalRefund / o.paid * 100).toFixed(1);
    $('m3f-ra-preview').innerHTML =
      '<tr><td>누적 환불액 (현금)</td><td>' + won(o.cumRefund) + '</td><td style="color:' + (v.delta < 0 ? '#DC2626' : '#2563EB') + '; font-weight:700;">' + signed(v.delta, '원') + '</td><td><strong>' + won(finalRefund) + '</strong></td></tr>' +
      '<tr><td>포인트 처리 누적</td><td>' + signed(o.cumPoint, ' P') + '</td><td style="font-weight:700;">' + signed(v.pt, ' P') + '</td><td><strong>' + signed(finalPoint, ' P') + '</strong></td></tr>' +
      '<tr><td>원 결제금액 대비 환불률</td><td>' + rateBefore + '%</td><td>—</td><td><strong>' + rateAfter + '%</strong></td></tr>' +
      '<tr><td>원 환불 거래 (' + esc($('m3f-ra-rfd').value) + ')</td><td>' + won(o.origRefund) + '</td><td>변경 없음 (불변)</td><td>' + won(o.origRefund) + '</td></tr>';

    var err = validate(v);
    var warn = $('m3f-ra-warn');
    var touched = $('m3f-ra-amount').value !== '' || $('m3f-ra-point').value !== '';
    warn.style.display = (err && touched) ? 'block' : 'none';
    warn.textContent = err ? '⚠ ' + err : '';
  };

  window.m3fRaTypeChange = function () {
    var type = currentType();
    document.querySelectorAll('#modalRefundAdjust .m3f-type-card').forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-type') === type); });
    $('m3f-ra-exec').value = EXEC_BY_TYPE[type];
    if (type === 'POINT') $('m3f-ra-amount').value = '';
    window.m3fRaRefresh();
  };

  window.m3fRaReasonCount = function () {
    var len = $('m3f-ra-reason').value.trim().length;
    var el = $('m3f-ra-reason-count');
    el.textContent = '현재 ' + len + '자 / 최소 10자';
    el.style.color = len >= 10 ? '#059669' : '#64748B';
  };

  window.openRefundAdjustModal = function (rfdNo) {
    var sel = $('m3f-ra-rfd');
    if (rfdNo && RFD[rfdNo]) sel.value = rfdNo;
    document.querySelectorAll('input[name="m3f-ra-type"]').forEach(function (r) { r.checked = (r.value === 'ADD'); });
    $('m3f-ra-amount').value = '';
    $('m3f-ra-point').value = '';
    $('m3f-ra-reason').value = '';
    window.m3fRaTypeChange();
    window.m3fRaReasonCount();
    var el = $('modalRefundAdjust');
    el.classList.remove('force-closed');
    el.style.removeProperty('display');
    el.classList.add('show');
    el.setAttribute('aria-hidden', 'false');
  };

  window.closeRefundAdjustModal = function () {
    var el = $('modalRefundAdjust');
    if (!el) return;
    el.classList.remove('show', 'open', 'active');
    el.setAttribute('aria-hidden', 'true');
  };

  window.submitRefundAdjust = function () {
    var v = readInputs();
    var err = validate(v);
    if (err) { toast('⚠ ' + err); $('m3f-ra-warn').style.display = 'block'; $('m3f-ra-warn').textContent = '⚠ ' + err; return; }
    if (v.reason.length < 10) { toast('⚠ 보정 거래 등록 사유를 최소 10자 이상 입력해 주세요 (감사 로그 기록).'); $('m3f-ra-reason').focus(); return; }

    var o = v.o;
    var rfdNo = $('m3f-ra-rfd').value;
    var before = o.cumRefund;
    var after = before + v.delta;
    var st = settleInfo(o, v.type);
    var typeLabel = v.type === 'ADD' ? '추가 환불 지급 (+현금)'
      : v.type === 'RECOVER' ? '과오납 환불금 회수 (−현금)'
      : (v.pt > 0 ? '포인트 보정 (+유상P 복원)' : '포인트 보정 (−P 차감)');
    var amountText = v.type === 'POINT'
      ? '0원 (' + signed(v.pt, ' P') + (v.pt > 0 ? ' 추가 복원' : ' 차감') + ')'
      : signed(v.delta, '원') + ' (포인트 ' + (v.pt ? signed(v.pt, ' P') : '0P') + ')';
    var cumText = v.delta !== 0 ? won(before) + ' ➔ ' + won(after) : won(before) + ' (변동없음)';
    var execShort = v.exec === EXEC_BY_TYPE.POINT ? '포인트 원장 직권 보정' : v.exec.replace('토스페이먼츠 ', '');

    var row = { id: 'ADJ-2026-' + pad(++adjSeq, 6), at: nowText(), rfd: rfdNo, type: v.type, typeLabel: typeLabel, amountText: amountText, cumText: cumText, execText: execShort + ' · ' + st.short, reason: v.reason, operator: OPERATOR };

    o.cumRefund = after;
    o.cumPoint += v.pt;
    o.adjCount += 1;
    ledger.unshift(row);
    renderLedger();

    var tr = document.querySelector('#m3f-rfd-adj-body tr[data-adj="' + row.id + '"]');
    if (tr) { tr.classList.add('m3f-flash'); }
    window.closeRefundAdjustModal();
    toast('✅ 보정 거래 전표 ' + row.id + ' 생성 완료 — 원 환불 ' + rfdNo + ' 불변 · ' + amountText + ' · ' + st.short);
    var card = $('m3f-rfd-adj-card');
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  renderLedger();
})();
</script>
'''

RFD_REQUIRED_IDS = ["m3f-rfd-adj-card", "m3f-rfd-adj-body", "modalRefundAdjust", "m3f-ra-preview", "m3f-toast"]


def patch_rfd_002(src):
    # 0) 스타일
    src = insert_before(src, "  </style>\n", RFD_CSS, "RFD: </style>")

    # 1) 카드 헤더 버튼 → 신규 모달
    src = replace_once(
        src,
        'onclick="openRfdAdjustModal()">➕ 사후 보정 거래 등록 (003-S2)</button>',
        'onclick="openRefundAdjustModal()">+ 환불 완료 건 별도 보정 거래 등록</button>',
        "RFD: 환불 완료 카드 헤더 버튼",
    )

    # 2) 환불 완료 원장 [사후 보정] 컬럼
    src = replace_once(src, "<th>정산 차감 반영월</th>",
                       "<th>정산 차감 반영월</th>\n                  <th>사후 보정</th>", "RFD: 정산 차감 반영월 th")
    src = insert_after(
        src,
        '<td><span class="badge badge-green">2026-10 정산 반영</span></td>',
        '\n                  <td><button type="button" class="btn btn-sm btn-outline" onclick="openRefundAdjustModal(\'RFD-2026-001120\')">+ 보정 거래 생성</button></td>',
        "RFD: RFD-2026-001120 행",
    )
    src = insert_after(
        src,
        '<td><span class="badge badge-blue">원귀속 2026-08 ➔ 2026-10 공제</span></td>',
        '\n                  <td><button type="button" class="btn btn-sm btn-outline" onclick="openRefundAdjustModal(\'RFD-2026-001098\')">+ 보정 거래 생성</button></td>',
        "RFD: RFD-2026-001098 행",
    )

    # 3) 하단 신규 원장 카드 (view-done 섹션 내부 마지막)
    src = insert_before(src, "      </section>\n\n    </main>", RFD_LEDGER_CARD, "RFD: view-done 종료부")

    # 4) 모달 + JS
    src = insert_before(src, "</body>", RFD_MODAL_AND_JS, "RFD: </body>")
    return src, RFD_REQUIRED_IDS


# =============================================================================
# 실행부
# =============================================================================
JOBS = [
    ("ADMN-USER-001_baseline.html", patch_user_001),
    ("ADMN-RFD-002_baseline.html", patch_rfd_002),
]


def main():
    ap = argparse.ArgumentParser(description="USER-003/006 · RFD-003-S2 누락 3대 기능 추가 패치")
    ap.add_argument("--dry-run", action="store_true", help="파일을 저장하지 않고 앵커/검증만 수행")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent), help="프로젝트 루트 (기본: 스크립트 위치)")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    print("=" * 72)
    print(f" patch_missing_3_features.py  {'(DRY-RUN)' if args.dry_run else ''}")
    print(f" root = {root}")
    print("=" * 72)

    results = []
    failed = False
    for d in TARGET_DIRS:
        for fname, fn in JOBS:
            path = root / d / fname
            rel = f"{d}/{fname}"
            if not path.exists():
                print(f"[FAIL] {rel} — 파일 없음")
                results.append((rel, "FAIL", "파일 없음"))
                failed = True
                continue
            src = path.read_text(encoding="utf-8")
            if MARKER in src:
                print(f"[SKIP] {rel} — 이미 패치됨 ({MARKER})")
                results.append((rel, "SKIP", "이미 패치됨"))
                continue
            try:
                out, req_ids = fn(src)
            except PatchError as e:
                print(f"[FAIL] {rel} — {e} (파일 미변경)")
                results.append((rel, "FAIL", str(e)))
                failed = True
                continue

            missing = [i for i in req_ids if f'id="{i}"' not in out]
            if missing:
                print(f"[FAIL] {rel} — 필수 ID 누락: {missing} (파일 미변경)")
                results.append((rel, "FAIL", f"필수 ID 누락 {missing}"))
                failed = True
                continue

            js_msgs = []
            js_ok = True
            for code in extract_m3f_scripts(out):
                ok, msg = js_syntax_check(code)
                js_msgs.append(msg)
                if ok is False:
                    js_ok = False
            if not js_ok:
                print(f"[FAIL] {rel} — 신규 JS 문법 오류: {js_msgs} (파일 미변경)")
                results.append((rel, "FAIL", "JS 문법 오류"))
                failed = True
                continue

            if not args.dry_run:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(out)
            delta = len(out.splitlines()) - len(src.splitlines())
            print(f"[ OK ] {rel} — +{delta} lines · 필수 ID {len(req_ids)}개 확인 · JS 검사 {', '.join(js_msgs)}"
                  f"{' (저장 생략)' if args.dry_run else ''}")
            results.append((rel, "OK", f"+{delta} lines"))

    print("-" * 72)
    for rel, st, msg in results:
        print(f"  {st:<4}  {rel}  {msg}")
    print("-" * 72)
    if failed:
        print("결과: 일부 파일 실패 — 위 로그를 분석 AI에 그대로 전달하세요.")
        return 1
    print("결과: 전체 성공")
    print("확인 URL: ADMN-USER-001_baseline.html?view=course / ?view=tags , ADMN-RFD-002_baseline.html?view=done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
