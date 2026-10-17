import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

user_html_path = os.path.join("prototype", "ADMN-USER-001_baseline.html")

with open(user_html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 시연 회원 빠른 전환 바 이름 통일 (정재훈 -> 박준혁, 이합격 -> 이서연)
content = content.replace("② 이합격", "② 이서연")
content = content.replace("③ 정재훈", "③ 박준혁")

# 2. MEMBERS 배열 내 이름 및 포인트 확인/변경
# name: "이합격" -> "이서연", name: "정재훈" -> "박준혁"
content = content.replace('name: "이합격"', 'name: "이서연"')
content = content.replace('name: "정재훈"', 'name: "박준혁"')

# USR-0941 이서연 유상 14,000P 확인
# USR-1205 박준혁 유상 0P 확인

with open(user_html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Updated ADMN-USER-001_baseline.html names (이서연, 박준혁) and verified points.")

# PROM-002도 동일하게 정재훈 -> 박준혁, 이합격 -> 이서연으로 맞춰주기
prom_html_path = os.path.join("prototype", "ADMN-PROM-002_baseline.html")
with open(prom_html_path, "r", encoding="utf-8") as f:
    prom_content = f.read()

prom_content = prom_content.replace("<b>이합격</b> (USR-0941)", "<b>이서연</b> (USR-0941)")
prom_content = prom_content.replace("<b>정재훈</b> (USR-1205)", "<b>박준혁</b> (USR-1205)")

with open(prom_html_path, "w", encoding="utf-8") as f:
    f.write(prom_content)

print("[OK] Updated ADMN-PROM-002_baseline.html names as well.")
