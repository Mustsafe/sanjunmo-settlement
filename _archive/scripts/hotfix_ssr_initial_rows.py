#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[긴급 핫픽스] patch_missing_3_features 적용 후 4개 신규 테이블이
'데이터를 불러오는 중입니다…'에서 멈춰 있는 현상 즉시 해결 (SSR 초기 행 내장 + JS 즉시 실행 보장)
"""

import re
from pathlib import Path

TARGET_DIRS = [Path("prototype"), Path("prototype_clean")]

UNIT_INITIAL_ROWS = """
                <tr>
                  <td><strong>31강</strong></td>
                  <td>설비보전 및 기계안전 핵심빈출 풀이</td>
                  <td class="mono">44:05</td>
                  <td class="mono">44:05</td>
                  <td><strong style="color:#059669;">100.0%</strong></td>
                  <td class="mono">2,645초 (수강완료)</td>
                  <td class="mono">2026.10.15 20:11</td>
                  <td><span class="badge badge-green">정상</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="openProgressAdjustModal(31)">보정</button></td>
                </tr>
                <tr>
                  <td><strong>32강</strong></td>
                  <td>화학설비 위험방지 및 MSDS 핵심정리</td>
                  <td class="mono">50:20</td>
                  <td class="mono">18:42</td>
                  <td><strong style="color:#2563EB;">37.1%</strong></td>
                  <td class="mono">1,122초 (18분 42초)</td>
                  <td class="mono">2026.10.17 14:22</td>
                  <td><span class="badge badge-green">정상</span></td>
                  <td><button type="button" class="btn btn-sm btn-primary" onclick="openProgressAdjustModal(32)">진도율 보정</button></td>
                </tr>
                <tr>
                  <td><strong>33강</strong></td>
                  <td>전기안전 보호구 및 정전기 재해 예방</td>
                  <td class="mono">46:15</td>
                  <td class="mono">00:00</td>
                  <td><span style="color:#64748B;">0.0%</span></td>
                  <td class="mono">0초 (미수강)</td>
                  <td class="mono">—</td>
                  <td><span class="badge badge-gray">미수강</span></td>
                  <td><button type="button" class="btn btn-sm btn-primary" onclick="openProgressAdjustModal(33)">진도율 보정</button></td>
                </tr>
                <tr class="m3f-row-adjusted">
                  <td><strong>34강</strong></td>
                  <td>건설안전 가설구조물 및 추락재해 방지</td>
                  <td class="mono">41:50</td>
                  <td class="mono">00:00</td>
                  <td><strong style="color:#D97706;">100.0%</strong> <span style="font-size:11px; color:#64748B;">(원본 0.0%)</span></td>
                  <td class="mono">보정 완료</td>
                  <td class="mono">2026.10.10 11:20</td>
                  <td><span class="badge badge-amber">🛠 수동보정 반영됨</span></td>
                  <td><button type="button" class="btn btn-sm btn-outline" onclick="document.getElementById('m3f-adjlog-card')?.scrollIntoView({behavior:'smooth'})">이력 확인</button></td>
                </tr>"""

ADJLOG_INITIAL_ROWS = """
                <tr>
                  <td class="mono"><strong>PRG-ADJ-2026-041</strong><br>2026.10.10 11:20</td>
                  <td><strong>2026 산안기 올패스 · 34강</strong><br><span style="font-size:11.5px; color:#64748B;">건설안전 가설구조물 및 추락재해 방지</span></td>
                  <td><span class="mono">0.0%</span> ➔ <strong style="color:#059669;">100.0%</strong></td>
                  <td><span class="mono">91.6%</span> ➔ <strong style="color:#2563EB;">92.4% (+0.8%p)</strong></td>
                  <td><span class="badge badge-blue">플레이어·네트워크 장애</span></td>
                  <td>10/09 심야 CDN 일시 순단으로 시청 완료 로그 유실 확인 <span class="badge badge-gray">📎 cdn_error_log_1009.txt</span></td>
                  <td>운영1팀 이지훈<br><span class="mono" style="font-size:11px; color:#64748B;">(admin_jh)</span></td>
                </tr>
                <tr>
                  <td class="mono"><strong>PRG-ADJ-2026-019</strong><br>2026.09.22 16:05</td>
                  <td><strong>2026 산안기 올패스 · 12강</strong><br><span style="font-size:11.5px; color:#64748B;">인간공학 및 시스템안전개론 핵심</span></td>
                  <td><span class="mono">45.0%</span> ➔ <strong style="color:#059669;">100.0%</strong></td>
                  <td><span class="mono">48.2%</span> ➔ <strong style="color:#2563EB;">49.0% (+0.8%p)</strong></td>
                  <td><span class="badge badge-purple">모바일 앱 동기화 오류</span></td>
                  <td>iOS 앱 오프라인 재생 후 진도율 미전송 CS 확인 <span class="badge badge-gray">📎 cs_capture_0922.png</span></td>
                  <td>CS팀 김상담<br><span class="mono" style="font-size:11px; color:#64748B;">(admin_kim)</span></td>
                </tr>"""

GROUP_INITIAL_ROWS = """
                <tr>
                  <td><code>GRP-2026-01</code></td>
                  <td><strong>환급반 중도이탈 위험군 케어 그룹</strong></td>
                  <td>
                    <span class="m3f-tagpill">TAG-PASS-2026 환급반 수강생</span>
                    <span class="m3f-op">AND</span>
                    <span class="m3f-tagpill">TAG-LOW-PROG 진도율 30% 미만</span>
                    <span class="m3f-op">AND</span>
                    <span class="m3f-tagpill">TAG-INACTIVE-14D 14일 미접속</span>
                  </td>
                  <td><span class="badge badge-blue">동적 (매일 06:00)</span></td>
                  <td class="tr-right"><strong>412명</strong> <span style="font-size:11.5px; color:#059669;">(동의 388명)</span></td>
                  <td class="mono">2026.10.18 06:00</td>
                  <td>
                    <div class="m3f-actions">
                      <a href="ADMN-CONF-004_baseline.html" class="btn btn-sm btn-outline">단체 알림톡 발송</a>
                      <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급</a>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td><code>GRP-2026-02</code></td>
                  <td><strong>카페 인증 미결제 전환 타겟 그룹</strong></td>
                  <td>
                    <span class="m3f-tagpill">TAG-CAFE-AUTH 산준모 카페 인증</span>
                    <span class="m3f-op">AND</span>
                    <span class="m3f-tagpill">TAG-FREE-30D 무료회원×30일접속</span>
                  </td>
                  <td><span class="badge badge-blue">동적 (매일 06:00)</span></td>
                  <td class="tr-right"><strong>1,204명</strong> <span style="font-size:11.5px; color:#059669;">(동의 1,089명)</span></td>
                  <td class="mono">2026.10.18 06:00</td>
                  <td>
                    <div class="m3f-actions">
                      <a href="ADMN-CONF-004_baseline.html" class="btn btn-sm btn-outline">단체 알림톡 발송</a>
                      <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급</a>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td><code>GRP-2026-03</code></td>
                  <td><strong>2026년 2회 정기시험 응시자 스냅샷</strong></td>
                  <td>
                    <span class="m3f-tagpill">TAG-PASS-2026 환급반 수강생</span>
                    <span class="m3f-op">OR</span>
                    <span class="m3f-tagpill">TAG-CAFE-AUTH 산준모 카페 인증</span>
                  </td>
                  <td><span class="badge badge-gray">정적 (명단 고정)</span></td>
                  <td class="tr-right"><strong>2,140명</strong> <span style="font-size:11.5px; color:#059669;">(동의 1,950명)</span></td>
                  <td class="mono">2026.09.15 11:20</td>
                  <td>
                    <div class="m3f-actions">
                      <a href="ADMN-CONF-004_baseline.html" class="btn btn-sm btn-outline">단체 알림톡 발송</a>
                      <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm btn-outline">쿠폰 발급</a>
                    </div>
                  </td>
                </tr>"""

RFD_ADJ_INITIAL_ROWS = """
                <tr>
                  <td class="mono"><strong>ADJ-2026-000032</strong><br>2026-10-16 14:20</td>
                  <td class="mono"><strong>RFD-2026-001120</strong><br><span style="color:#64748B;">(SJM-20261001-002190)</span></td>
                  <td><strong>박영희</strong></td>
                  <td><span class="badge badge-blue">추가 환불 지급 (+현금)</span></td>
                  <td class="num"><strong style="color:#2563EB;">+15,824원</strong><br><span style="font-size:11px; color:#64748B;">(포인트 0P)</span></td>
                  <td class="num"><span class="mono">297,111원</span> ➔ <strong>312,935원</strong></td>
                  <td>PG 추가 부분취소<br><span class="badge badge-green">2026-10 당월 정산 차감 반영</span></td>
                  <td>휴강 일수(3일) 일할 계산 누락분 사후 추가 환불<br><span style="font-size:11px; color:#64748B;">처리자: 재무팀 이정산</span></td>
                </tr>
                <tr>
                  <td class="mono"><strong>ADJ-2026-000031</strong><br>2026-10-11 11:02</td>
                  <td class="mono"><strong>RFD-2026-001098</strong><br><span style="color:#64748B;">(SJM-20260822-003110)</span></td>
                  <td><strong>이민호</strong></td>
                  <td><span class="badge badge-purple">포인트 보정 (+유상P 복원)</span></td>
                  <td class="num">0원<br><strong style="color:#7C3AED;">+1,000 P 추가 복원</strong></td>
                  <td class="num"><strong>22,933원</strong> <span style="font-size:11px; color:#64748B;">(현금 변동없음)</span></td>
                  <td>포인트 원장 직권 보정 (D+7 만료유예)<br><span class="badge badge-gray">정산 무관</span></td>
                  <td>LIFO 복원 시 만료일 경계 차감 오차 +1,000P 사후 복원<br><span style="font-size:11px; color:#64748B;">처리자: CS팀 김상담</span></td>
                </tr>"""

CHIPS_INITIAL_HTML = """
                    <span class="m3f-chip on" onclick="this.classList.toggle('on')">✓ TAG-PASS-2026 환급반 수강생</span>
                    <span class="m3f-chip on" onclick="this.classList.toggle('on')">✓ TAG-LOW-PROG 진도율 30% 미만</span>
                    <span class="m3f-chip on" onclick="this.classList.toggle('on')">✓ TAG-INACTIVE-14D 14일 미접속</span>
                    <span class="m3f-chip" onclick="this.classList.toggle('on')">TAG-CAFE-AUTH 산준모 카페 인증</span>
                    <span class="m3f-chip" onclick="this.classList.toggle('on')">TAG-FREE-30D 무료회원×30일접속</span>"""


def main():
    modified = []
    for folder in TARGET_DIRS:
        if not folder.exists():
            continue

        # 1) ADMN-USER-001 패치
        f_user = folder / "ADMN-USER-001_baseline.html"
        if f_user.exists():
            orig = f_user.read_text(encoding="utf-8")
            txt = orig
            txt = re.sub(
                r'(<tbody id="m3f-unit-body">)\s*<tr><td[^>]*>차시별 진도 데이터를 불러오는 중입니다…</td></tr>\s*(</tbody>)',
                r"\1" + UNIT_INITIAL_ROWS + "\n              " + r"\2",
                txt
            )
            txt = re.sub(
                r'(<tbody id="m3f-adjlog-body">)\s*<tr><td[^>]*>보정 이력을 불러오는 중입니다…</td></tr>\s*(</tbody>)',
                r"\1" + ADJLOG_INITIAL_ROWS + "\n              " + r"\2",
                txt
            )
            txt = re.sub(
                r'(<tbody id="m3f-group-body">)\s*<tr><td[^>]*>회원 그룹 현황을 불러오는 중입니다…</td></tr>\s*(</tbody>)',
                r"\1" + GROUP_INITIAL_ROWS + "\n              " + r"\2",
                txt
            )
            txt = txt.replace(
                '<div id="m3f-chip-wrap"></div>',
                f'<div id="m3f-chip-wrap">{CHIPS_INITIAL_HTML}\n                    </div>'
            )
            if txt != orig:
                f_user.write_text(txt, encoding="utf-8")
                modified.append(str(f_user))

        # 2) ADMN-RFD-002 패치
        f_rfd = folder / "ADMN-RFD-002_baseline.html"
        if f_rfd.exists():
            orig = f_rfd.read_text(encoding="utf-8")
            txt = re.sub(
                r'(<tbody id="m3f-adj-body">)\s*<tr><td[^>]*>보정 거래 원장을 불러오는 중입니다…</td></tr>\s*(</tbody>)',
                r"\1" + RFD_ADJ_INITIAL_ROWS + "\n                " + r"\2",
                orig
            )
            if txt != orig:
                f_rfd.write_text(txt, encoding="utf-8")
                modified.append(str(f_rfd))

    print(f"[핫픽스 완료] 총 {len(modified)}개 파일에서 '불러오는 중입니다…' 초기 행 렌더링 해결:")
    for m in modified:
        print(f"  - {m}")


if __name__ == "__main__":
    main()
