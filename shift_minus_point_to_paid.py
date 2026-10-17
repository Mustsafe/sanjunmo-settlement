import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# 1. prototype/ADMN-USER-001_baseline.html 수정
# ==============================================================================
user_html_path = os.path.join("prototype", "ADMN-USER-001_baseline.html")

with open(user_html_path, "r", encoding="utf-8") as f:
    user_content = f.read()

# 1-1. MEMBERS 배열 내 데이터 수정:
# USR-0941 이서연: ptFree: 12000, ptPaid: 14000
# USR-1205 박준혁: ptFree: 0, ptPaid: -3500
old_members_block = """      {
        uid: "USR-0941",
        name: "이서연",
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
        name: "박준혁",
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

new_members_block = """      {
        uid: "USR-0941",
        name: "이서연",
        email: "pass_lee@gmail.com",
        phone: "010-****-3310",
        cafeId: "pass_lee",
        joinType: "EMAIL",
        joinLabel: "이메일 가입",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "AUTO_5FAIL",
        lockedLabel: "🔒 5회오류 잠금",
        ptFree: 12000,
        ptPaid: 14000,
        tags: ["산준모카페인증"],
        mkt: "Y",
        lastLogin: "2026-10-16 11:40",
        diInfo: "생애 최초 가입 (웰컴 혜택 지급완료 · 유상 14,000P / 무상 12,000P 보유)"
      },
      {
        uid: "USR-1205",
        name: "박준혁",
        email: "jung_jh@kakao.com",
        phone: "010-****-8820",
        cafeId: "jung_safety",
        joinType: "KAKAO",
        joinLabel: "카카오 간편",
        status: "NORMAL",
        statusLabel: "정상",
        locked: "UNLOCKED",
        lockedLabel: "잠금없음 (0/5)",
        ptFree: 0,
        ptPaid: -3500,
        tags: ["마이너스부채"],
        mkt: "N",
        lastLogin: "2026-10-15 19:05",
        diInfo: "환불 회수 시 무상(0P) 전액 소진 후 부족분 유상 포인트 마이너스(-3,500P) 부채 전환 (DI 해시 승계)"
      },"""

if old_members_block in user_content:
    user_content = user_content.replace(old_members_block, new_members_block, 1)
    print("[OK] Updated MEMBERS in ADMN-USER-001_baseline.html")
else:
    print("[WARN] MEMBERS pattern not found in ADMN-USER-001_baseline.html")

# 1-2. renderMemberGrid() 함수 내 포인트 표시 수정 (무상, 유상 마이너스 시 빨간색 강조 및 라벨링)
old_grid_render = """        const freeColor = m.ptFree < 0 ? "var(--danger)" : "var(--text-primary)";

        return `
          <tr onclick="openMemberDetail('${m.uid}')">
            <td><b style="color:var(--primary); font-family:monospace;">${m.uid}</b></td>
            <td>
              <div style="font-weight:800;">${m.name}</div>
              <div style="font-size:11.5px; color:var(--text-muted);">${m.email} · ${m.phone}</div>
            </td>
            <td><b style="color:var(--teal);">${m.cafeId}</b></td>
            <td class="ct"><span class="badge badge-slate">${m.joinLabel}</span></td>
            <td class="ct">${stBadge} ${lkBadge}</td>
            <td class="num">
              <div style="font-weight:800; color:${freeColor};">무상 ${m.ptFree.toLocaleString()} P</div>
              <div style="font-size:11px; color:var(--purple);">유상 ${m.ptPaid.toLocaleString()} P</div>
            </td>"""

new_grid_render = """        const freeColor = m.ptFree < 0 ? "var(--danger)" : "var(--text-primary)";
        const paidColor = m.ptPaid < 0 ? "var(--danger)" : "var(--purple)";
        const paidLabel = m.ptPaid < 0 ? `유상 ${m.ptPaid.toLocaleString()} P (환불 회수 부채)` : `유상 ${m.ptPaid.toLocaleString()} P`;

        return `
          <tr onclick="openMemberDetail('${m.uid}')">
            <td><b style="color:var(--primary); font-family:monospace;">${m.uid}</b></td>
            <td>
              <div style="font-weight:800;">${m.name}</div>
              <div style="font-size:11.5px; color:var(--text-muted);">${m.email} · ${m.phone}</div>
            </td>
            <td><b style="color:var(--teal);">${m.cafeId}</b></td>
            <td class="ct"><span class="badge badge-slate">${m.joinLabel}</span></td>
            <td class="ct">${stBadge} ${lkBadge}</td>
            <td class="num">
              <div style="font-weight:800; color:${paidColor};">${paidLabel}</div>
              <div style="font-size:11px; color:${freeColor};">무상 ${m.ptFree.toLocaleString()} P</div>
            </td>"""

if old_grid_render in user_content:
    user_content = user_content.replace(old_grid_render, new_grid_render, 1)
    print("[OK] Updated renderMemberGrid in ADMN-USER-001_baseline.html")
else:
    print("[WARN] renderMemberGrid pattern not found in ADMN-USER-001_baseline.html")

# 1-3. openMemberDetail() 함수 내 상세 포인트 렌더링 수정 (유상 마이너스 시 빨간색 강조)
old_detail_render = """      document.getElementById("dt-pt-free").innerHTML = `<b style="color:${m.ptFree < 0 ? 'var(--danger)' : 'var(--text-primary)'};">${m.ptFree.toLocaleString()} P</b> <span style="font-size:11.5px; color:var(--text-muted);">(200,000P Cap 이내)</span>`;
      document.getElementById("dt-pt-paid").innerHTML = `<b>${m.ptPaid.toLocaleString()} P</b>`;"""

new_detail_render = """      document.getElementById("dt-pt-free").innerHTML = `<b style="color:${m.ptFree < 0 ? 'var(--danger)' : 'var(--text-primary)'};">${m.ptFree.toLocaleString()} P</b> <span style="font-size:11.5px; color:var(--text-muted);">(200,000P Cap 이내)</span>`;
      const paidDetailStr = m.ptPaid < 0 ? `<b style="color:var(--danger);">${m.ptPaid.toLocaleString()} P (환불 회수 미차감 부채)</b>` : `<b>${m.ptPaid.toLocaleString()} P</b>`;
      document.getElementById("dt-pt-paid").innerHTML = paidDetailStr;"""

if old_detail_render in user_content:
    user_content = user_content.replace(old_detail_render, new_detail_render, 1)
    print("[OK] Updated openMemberDetail in ADMN-USER-001_baseline.html")
else:
    print("[WARN] openMemberDetail pattern not found in ADMN-USER-001_baseline.html")

# 1-4. 뷰 2 카드 3 상단 안내 문구 보강
old_pt_notice = """                <div style="background:#F8FAFC; border:1px solid var(--border-color); border-radius:8px; padding:10px 12px; margin-bottom:12px; font-size:11.5px; color:var(--text-secondary); line-height:1.55;">
                  • <b>포인트 회수 원칙:</b> 환불 회수 시 <b>무상(FREE) 우선 차감 → 부족분 유상(PAID) 차감 → 전액 소진 후 부족분만 마이너스(-) 부채 전환 (DI 해시 기반 재가입 시 승계)</b>을 엄격 준수합니다.
                </div>"""

new_pt_notice = """                <div style="background:#F8FAFC; border:1px solid var(--border-color); border-radius:8px; padding:10px 12px; margin-bottom:12px; font-size:11.5px; color:var(--text-secondary); line-height:1.55;">
                  • <b>포인트 회수 원칙:</b> 기적립(구매 1%) 포인트 환불 회수 시 <b>무상(FREE) 포인트를 0P까지 먼저 차감한 뒤 유상(PAID) 포인트를 차감</b>하므로, 최종 부족분은 <b>유상 포인트 마이너스(-3,500P) 부채</b>로 기록되며 DI 해시 기반 재가입 시에도 복원·승계됩니다.
                </div>"""

if old_pt_notice in user_content:
    user_content = user_content.replace(old_pt_notice, new_pt_notice, 1)
    print("[OK] Updated Point Notice in ADMN-USER-001_baseline.html")
else:
    print("[WARN] Point Notice pattern not found in ADMN-USER-001_baseline.html")

with open(user_html_path, "w", encoding="utf-8") as f:
    f.write(user_content)


# ==============================================================================
# 2. prototype/ADMN-PROM-002_baseline.html 수정
# ==============================================================================
prom_html_path = os.path.join("prototype", "ADMN-PROM-002_baseline.html")

with open(prom_html_path, "r", encoding="utf-8") as f:
    prom_content = f.read()

# 2-1. USR-1205 박준혁 행: 배지를 무상(FREE) -> 유상(PAID)으로 변경, 잔액 표기를 유상 -3,500P / 무상 0P 로 변경
old_prom_row = """                <tr>
                  <td><b>TX-PT-0750</b><br/><span style="font-size:11px; color:var(--text-muted);">2026-10-12 11:05</span></td>
                  <td><b>박준혁</b> (USR-1205)</td>
                  <td class="ct"><span class="badge badge-purple">통합 원장</span></td>
                  <td class="ct"><span class="badge badge-red">DEBT (부채)</span></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b><br/><span style="font-size:10.5px; color:var(--text-muted);">유상 0P / 무상 0P</span></td>
                  <td>적립 포인트 선사용 후 강좌 환불(<code>ADMN-RFD-002-P1</code>) 회수 — 무상(0P)·유상(0P) 전액 소진 후 미회수 부채 <b>-3,500P</b> 기록 (DI 해시 승계)</td>
                </tr>"""

new_prom_row = """                <tr>
                  <td><b>TX-PT-0750</b><br/><span style="font-size:11px; color:var(--text-muted);">2026-10-12 11:05</span></td>
                  <td><b>박준혁</b> (USR-1205)</td>
                  <td class="ct"><span class="badge badge-purple">유상 (PAID)</span></td>
                  <td class="ct"><span class="badge badge-red">DEBT (부채)</span></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b></td>
                  <td class="num"><b style="color:var(--danger);">-3,500 P</b><br/><span style="font-size:10.5px; color:var(--text-muted);">유상 -3,500P / 무상 0P</span></td>
                  <td>적립 포인트 선사용 후 강좌 환불(<code>ADMN-RFD-002-P1</code>) 회수 — 무상(0P) 우선 전액 차감 후 부족분이 유상 원장 마이너스 부채(<b>-3,500P</b>)로 기록 (DI 해시 승계)</td>
                </tr>"""

if old_prom_row in prom_content:
    prom_content = prom_content.replace(old_prom_row, new_prom_row, 1)
    print("[OK] Updated USR-1205 row in ADMN-PROM-002_baseline.html")
else:
    print("[WARN] USR-1205 row pattern not found in ADMN-PROM-002_baseline.html")

with open(prom_html_path, "w", encoding="utf-8") as f:
    f.write(prom_content)

print("[COMPLETE] Script executed successfully.")
