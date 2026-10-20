# fix_rfd002_ssr_row.py
from pathlib import Path
import re

RFD_ADJ_INITIAL_ROWS = """
                  <tr>
                    <td style="font-family:monospace;font-weight:700;color:#1D4ED8;">ADJ-20261016-001</td>
                    <td style="font-family:monospace;">RFD-2026-001098<br><span style="font-size:11px;color:#64748B;">TOSS-994011</span></td>
                    <td><span style="background:#EFF6FF;color:#1D4ED8;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;">추가 환불(지급)</span></td>
                    <td style="text-align:right;font-weight:700;color:#DC2626;">+10,000원</td>
                    <td><span style="background:#FEF3C7;color:#B45309;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:600;">강사·플랫폼 안분 차감</span></td>
                    <td>2026-11월 정산 반영 대기</td>
                    <td>교재 배송비 착오 차감분 사후 보전 (원 거래 불변 원칙 적용)</td>
                    <td>2026-10-16 11:20<br><span style="font-size:11px;color:#64748B;">박정산 (승인: 이팀장)</span></td>
                  </tr>
                  <tr>
                    <td style="font-family:monospace;font-weight:700;color:#1D4ED8;">ADJ-20261014-002</td>
                    <td style="font-family:monospace;">RFD-2026-001120<br><span style="font-size:11px;color:#64748B;">TOSS-998120</span></td>
                    <td><span style="background:#FEF2F2;color:#DC2626;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;">환수(과오지급 회수)</span></td>
                    <td style="text-align:right;font-weight:700;color:#059669;">-15,000원</td>
                    <td><span style="background:#ECFDF5;color:#047857;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:600;">플랫폼 단독 귀속</span></td>
                    <td>2026-10월 정산 반영 완료</td>
                    <td>할인 쿠폰 중복 차감 누락분 사후 환수 처리</td>
                    <td>2026-10-14 16:05<br><span style="font-size:11px;color:#64748B;">김재무 (승인: 이팀장)</span></td>
                  </tr>"""

pattern = re.compile(
    r'(<tbody id="m3f-(?:rfd-)?adj-body">)\s*<tr><td[^>]*>보정 거래 원장을 불러오는 중입니다…</td></tr>\s*(</tbody>)',
    re.DOTALL
)

updated = 0
for folder in ["prototype", "prototype_clean"]:
    f = Path(folder) / "ADMN-RFD-002_baseline.html"
    if f.exists():
        orig = f.read_text(encoding="utf-8")
        new_txt = pattern.sub(r"\1" + RFD_ADJ_INITIAL_ROWS + "\n                " + r"\2", orig)
        if new_txt != orig:
            f.write_text(new_txt, encoding="utf-8")
            updated += 1
            print(f"[적용 완료] {f}")

print(f"총 {updated}개 파일 업데이트 완료.")
