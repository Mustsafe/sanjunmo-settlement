import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# 1. prototype/ADMN-USER-001_baseline.html 수정
# ==============================================================================
user_html_path = os.path.join("prototype", "ADMN-USER-001_baseline.html")

with open(user_html_path, "r", encoding="utf-8") as f:
    user_content = f.read()

# 1-1. MEMBERS 배열 내 데이터 수정
# USR-0941: ptFree 6600, ptPaid 14000 (이서연/이합격 - 유상 14,000P 보유 예시)
# USR-1205: ptFree -3500, ptPaid 0 (박준혁/정재훈 - 유상 0P, 마이너스 부채 -3,500P)
old_usr_0941 = """      {
        uid: "USR-0941",
        name: "이합격",
        email: "pass_lee@gmail.com",
        phone: "010-****-3310",
        cafeId: "pass_lee",
        joinType: "EMAIL",
        joinLabel: "이메일 가입",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "AUTO_5FAIL",
        lockedLabel: "🔒 5회오류 잠금",
        ptFree: 6600,
        ptPaid: 0,
        tags: ["산준모카페인증"],
        mkt: "Y",
        lastLogin: "2026-10-16 11:40",
        diInfo: "생애 최초 가입 (웰컴 혜택 지급완료)"
      },
      {
        uid: "USR-1205",
        name: "정재훈",
        email: "jung_jh@kakao.com",
        phone: "010-****-8820",
        cafeId: "jung_safety",
        joinType: "KAKAO",
        joinLabel: "카카오 간편",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "UNLOCKED",
        lockedLabel: "잠금없음 (0/5)",
        ptFree: -3500,
        ptPaid: 14000,
        tags: ["마이너스부채"],
        mkt: "N",
        lastLogin: "2026-10-15 19:05",
        diInfo: "적립 포인트 선사용 후 환불로 마이너스 부채(-3,500P) 보유"
      },"""

new_usr_0941 = """      {
        uid: "USR-0941",
        name: "이합격",
        email: "pass_lee@gmail.com",
        phone: "010-****-3310",
        cafeId: "pass_lee",
        joinType: "EMAIL",
        joinLabel: "이메일 가입",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "AUTO_5FAIL",
        lockedLabel: "🔒 5회오류 잠금",
        ptFree: 6600,
        ptPaid: 14000,
        tags: ["산준모카페인증"],
        mkt: "Y",
        lastLogin: "2026-10-16 11:40",
        diInfo: "생애 최초 가입 (웰컴 혜택 지급완료 · 유상 14,000P 보유)"
      },
      {
        uid: "USR-1205",
        name: "정재훈",
        email: "jung_jh@kakao.com",
        phone: "010-****-8820",
        cafeId: "jung_safety",
        joinType: "KAKAO",
        joinLabel: "카카오 간편",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "UNLOCKED",
        lockedLabel: "잠금없음 (0/5)",
        ptFree: -3500,
        ptPaid: 0,
        tags: ["마이너스부채"],
        mkt: "N",
        lastLogin: "2026-10-15 19:05",
        diInfo: "환불 회수 시 무상 우선 차감 → 부족분 유상 차감 → 전액 소진 후 부족분만 마이너스 부채(-3,500P) 전환 (DI 해시 승계)"
      },"""

if old_usr_0941 in user_content:
    user_content = user_content.replace(old_usr_0941, new_usr_0941, 1)
    print("[OK] Updated MEMBERS in ADMN-USER-001_baseline.html")
else:
    print("[WARN] MEMBERS pattern not found in ADMN-USER-001_baseline.html")

# 1-2. 카드 3(보유 포인트 요약 테이블)의 안내 문구 보강
old_pt_card = """            <!-- 카드 3: 보유 포인트(유/무상) · 마이너스 부채 · 쿠폰 요약 -->
            <div class="card">
              <div class="card-header">
                <div class="card-title">
                  <span>🪙 보유 포인트(유/무상 분리) · 쿠폰 원장</span>
                  <span class="badge badge-purple">PROM-002 연동</span>
                </div>
                <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm">쿠폰·포인트 원장 상세 ↗</a>
              </div>
              <div class="card-body">
                <table class="kv-table">
                  <tbody>
                    <tr>
                      <th>무상 포인트 (FREE)</th>
                      <td id="dt-pt-free"><b>12,500 P</b> <span style="font-size:11.5px; color:var(--text-muted);">(보유 상한 200,000P Cap 이내 · FIFO 차감)</span></td>
                    </tr>
                    <tr>
                      <th>유상 포인트 (PAID)</th>
                      <td id="dt-pt-paid"><b>0 P</b> <span style="font-size:11.5px; color:var(--text-muted);">(환불·전환 원장 분리)</span></td>
                    </tr>
                    <tr>
                      <th>보유 쿠폰 (user_coupon)</th>
                      <td id="dt-coupons">
                        <span class="badge badge-blue">가을 얼리버드 15% (~2026.09.30)</span>
                        <span class="badge badge-slate">웰컴 10% (사용완료)</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>"""

new_pt_card = """            <!-- 카드 3: 보유 포인트(유/무상) · 마이너스 부채 · 쿠폰 요약 -->
            <div class="card">
              <div class="card-header">
                <div class="card-title">
                  <span>🪙 보유 포인트(유/무상 분리) · 쿠폰 원장</span>
                  <span class="badge badge-purple">PROM-002 연동</span>
                </div>
                <a href="ADMN-PROM-002_baseline.html" class="btn btn-sm">쿠폰·포인트 원장 상세 ↗</a>
              </div>
              <div class="card-body">
                <div style="background:#F8FAFC; border:1px solid var(--border-color); border-radius:8px; padding:10px 12px; margin-bottom:12px; font-size:11.5px; color:var(--text-secondary); line-height:1.55;">
                  • <b>포인트 회수 원칙:</b> 환불 회수 시 <b>무상(FREE) 우선 차감 → 부족분 유상(PAID) 차감 → 전액 소진 후 부족분만 마이너스(-) 부채 전환 (DI 해시 기반 재가입 시 승계)</b>을 엄격 준수합니다.
                </div>
                <table class="kv-table">
                  <tbody>
                    <tr>
                      <th>무상 포인트 (FREE)</th>
                      <td id="dt-pt-free"><b>12,500 P</b> <span style="font-size:11.5px; color:var(--text-muted);">(보유 상한 200,000P Cap 이내 · FIFO 차감)</span></td>
                    </tr>
                    <tr>
                      <th>유상 포인트 (PAID)</th>
                      <td id="dt-pt-paid"><b>0 P</b> <span style="font-size:11.5px; color:var(--text-muted);">(환불·전환 원장 분리)</span></td>
                    </tr>
                    <tr>
                      <th>보유 쿠폰 (user_coupon)</th>
                      <td id="dt-coupons">
                        <span class="badge badge-blue">가을 얼리버드 15% (~2026.09.30)</span>
                        <span class="badge badge-slate">웰컴 10% (사용완료)</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>"""

if old_pt_card in user_content:
    user_content = user_content.replace(old_pt_card, new_pt_card, 1)
    print("[OK] Updated Point Card in ADMN-USER-001_baseline.html")
else:
    print("[WARN] Point Card pattern not found in ADMN-USER-001_baseline.html")

with open(user_html_path, "w", encoding="utf-8") as f:
    f.write(user_content)


# ==============================================================================
# 2. prototype/ADMN-PROM-002_baseline.html 수정
# ==============================================================================
prom_html_path = os.path.join("prototype", "ADMN-PROM-002_baseline.html")

with open(prom_html_path, "r", encoding="utf-8") as f:
    prom_content = f.read()

# 2-1. 뷰 3의 카드 헤더 / 안내 배너 보강 (환불 시 적립 포인트 회수 순서 명시)
old_prom_pt_header = """            <div class="card-title">
              <span>🪙 포인트(유상 PAID / 무상 FREE) 물리 분리 원장 및 200,000P Cap 통제</span>
              <span class="badge badge-green">FIFO 차감 · LIFO 환불 복원</span>
            </div>
            <button type="button" class="btn btn-sm btn-primary" onclick="openPointModal()">+ 관리자 포인트 수동 지급/차감</button>
          </div>
          <div style="overflow-x:auto;">"""

new_prom_pt_header = """            <div class="card-title">
              <span>🪙 포인트(유상 PAID / 무상 FREE) 물리 분리 원장 및 200,000P Cap 통제</span>
              <span class="badge badge-green">FIFO 차감 · LIFO 환불 복원</span>
            </div>
            <button type="button" class="btn btn-sm btn-primary" onclick="openPointModal()">+ 관리자 포인트 수동 지급/차감</button>
          </div>
          <div class="card-body" style="background:#F8FAFC; border-bottom:1px solid var(--border-color); font-size:12px; color:var(--text-secondary); line-height:1.6;">
            • <b>환불 시 적립 포인트 회수 순서:</b> <b>① 무상 포인트 우선 회수 → ② 부족 시 유상 포인트 회수 → ③ 유·무상 잔액(0P) 모두 소진 후 초과분만 마이너스(-) 부채 전환</b> (DI 해시 기반 재가입 시에도 부채 복원).
          </div>
          <div style="overflow-x:auto;">"""

if old_prom_pt_header in prom_content:
    prom_content = prom_content.replace(old_prom_pt_header, new_prom_pt_header, 1)
    print("[OK] Updated Point Header in ADMN-PROM-002_baseline.html")
else:
    print("[WARN] Point Header pattern not found in ADMN-PROM-002_baseline.html")

# 2-2. 포인트 원장 테이블의 정재훈/박준혁 (USR-1205) 행 잔액 표기 및 로그 수정
old_prom_usr_1205 = """                <tr>
                  <td><b>TX-PT-0750</b><br/><span style="font-size:11px; color:var(--text-muted);">2026-10-12 11:05</span></td>
                  <td><b>정재훈</b> (USR-1205)</td>
                  <td class="ct"><span class="badge badge-green">무상 (FREE)</span></td>
                  <td class="ct"><span class="badge badge-red">DEBT (부채)</span></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b></td>
                  <td>적립 포인트 선사용 후 강좌 환불(<code>ADMN-RFD-002-P1</code>) 발생 — 마이너스 포인트 부채 기록 (재가입 시에도 복원)</td>
                </tr>"""

new_prom_usr_1205 = """                <tr>
                  <td><b>TX-PT-0750</b><br/><span style="font-size:11px; color:var(--text-muted);">2026-10-12 11:05</span></td>
                  <td><b>정재훈</b> (USR-1205)</td>
                  <td class="ct"><span class="badge badge-purple">통합 원장</span></td>
                  <td class="ct"><span class="badge badge-red">DEBT (부채)</span></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b><br/><span style="font-size:10.5px; color:var(--text-muted);">유상 0P / 무상 0P</span></td>
                  <td>적립 포인트 선사용 후 강좌 환불(<code>ADMN-RFD-002-P1</code>) 회수 — 무상(0P)·유상(0P) 전액 소진 후 미회수 부채 <b>-3,500P</b> 기록 (DI 해시 승계)</td>
                </tr>"""

if old_prom_usr_1205 in prom_content:
    prom_content = prom_content.replace(old_prom_usr_1205, new_prom_usr_1205, 1)
    print("[OK] Updated USR-1205 row in ADMN-PROM-002_baseline.html")
else:
    print("[WARN] USR-1205 row not found in ADMN-PROM-002_baseline.html")

with open(prom_html_path, "w", encoding="utf-8") as f:
    f.write(prom_content)

print("[COMPLETE] Both files updated successfully.")
