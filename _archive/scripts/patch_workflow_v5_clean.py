# patch_workflow_v5_clean.py
# 업무플로우 페이지 전면개편 (prototype_clean 전용)
# - #v4-page-body 내부 교체 (내부 <script> 보존) + #wf-root 범위 스타일 추가
# - 원본 백업: _archive/backup/
import re
import sys
import shutil
from pathlib import Path

ROOT = Path.cwd()
CLEAN = ROOT / "prototype_clean"
WF = CLEAN / "00_WORKFLOW_GUIDE_baseline.html"
BACKUP = ROOT / "_archive" / "backup" / "00_WORKFLOW_GUIDE_baseline.clean.pre_v5.html"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"


# ---------------- 컴포넌트 헬퍼 ----------------
def F(code, q=""):
    return f"ADMN-{code}_baseline.html{q}"


def C(code):
    return f'<code class="wf-code">{code}</code>'


def chips(*items):
    items = [i for i in items if i]
    if not items:
        return ""
    return '<span class="wf-chips">' + "".join(f'<span class="wf-chip">{i}</span>' for i in items) + "</span>"


def _wrap(inner, cls, href):
    el = "a" if href else "div"
    attr = f' href="{href}"' if href else ""
    return f'<{el} class="{cls}"{attr}>{inner}</{el}>'


def node(do, scr="", code="", out="", chip=(), href="", tag="", cls="", extra=""):
    h = []
    if tag:
        h.append(f'<span class="wf-node-tag">{tag}</span>')
    h.append(f'<span class="wf-node-do">{do}</span>')
    if scr or code:
        h.append(f'<span class="wf-node-scr">{scr}{C(code) if code else ""}</span>')
    if out:
        h.append(f'<span class="wf-node-out">{out}</span>')
    if extra:
        h.append(extra)
    h.append(chips(*chip))
    return _wrap("".join(h), ("wf-node " + cls).strip(), href)


def start(text, out=""):
    return node(text, out=out, tag="출발", cls="is-start")


def gate(n, do, scr, code, cond, href):
    return node(do, scr, code, tag=f"관문 {n}", href=href, cls="is-gate",
                extra=f'<span class="wf-gate-pass">✓ {cond}</span>')


def flow(*nodes):
    lis = []
    for n in nodes:
        c = ' class="is-start"' if "is-start" in n[:60] else ""
        lis.append(f"<li{c}>{n}</li>")
    return '<ol class="wf-flow">' + "".join(lis) + "</ol>"


def exc(items):
    lis = "".join(f"<li><b>{t}</b> {d}</li>" for t, d in items)
    return f'<details class="wf-exc"><summary>예외 상황 {len(items)}건</summary><ul>{lis}</ul></details>'


def pair(when, do, scr="", code="", out="", chip="", href=""):
    body = f'<span class="wf-node-do">{do}</span>'
    if scr or code:
        body += f'<span class="wf-node-scr">{scr}{C(code) if code else ""}</span>'
    if out:
        body += f'<span class="wf-node-out">{out}</span>'
    body += chips(chip)
    inner = (f'<span class="wf-pair-when">{when}</span>'
             f'<span class="wf-pair-arrow">→</span>'
             f'<span class="wf-pair-body">{body}</span>')
    return _wrap(inner, "wf-pair", href)


def fan(label, scr, code="", href="", chip=""):
    inner = f'<b>{label}</b><span class="wf-node-scr">{scr}{C(code) if code else ""}</span>{chips(chip)}'
    return "<li>" + _wrap(inner, "wf-fan-item", href) + "</li>"


def sec_head(label, title, desc):
    return (f'<header class="wf-sec-hd"><span class="wf-eyebrow">{label}</span>'
            f'<h2 class="wf-sec-title">{title}</h2><p class="wf-sec-desc">{desc}</p></header>')


def lane(tag, title, desc, body):
    return (f'<article class="wf-lane"><div class="wf-lane-hd"><span class="wf-lane-tag">{tag}</span>'
            f'<h3>{title}</h3><p>{desc}</p></div>{body}</article>')


def stage(num, sid, title, period, desc, body):
    return (f'<section class="wf-stage" id="{sid}"><div class="wf-stage-num">{num}</div><div class="wf-stage-main">'
            f'<div class="wf-stage-hd"><span class="wf-lane-tag">STAGE {num}</span><h3>{title}</h3>'
            f'<span class="wf-period">{period}</span></div><p class="wf-stage-desc">{desc}</p>{body}</div></section>')


def sub(title, chip, body):
    return (f'<div class="wf-sub"><div class="wf-sub-hd"><strong>{title}</strong>{chips(chip)}</div>{body}</div>')


USER_C = F("USER-001", "?view=course")
ORD = F("ORD-001")

# ---------------- 본문 ----------------
INTRO = (
    '<section class="wf-intro">'
    '<h2>고객 응대부터 월 정산 마감까지</h2>'
    '<p>상황별로 어느 화면에서 무엇을 처리하는지 순서대로 안내합니다. 카드를 누르면 해당 흐름으로 이동합니다.</p>'
    '<div class="wf-entry-grid">'
    '<a class="wf-entry is-ops" href="#wf-ops"><span class="wf-entry-label">운영 업무</span>'
    '<strong>매일 들어오는 요청 처리</strong>'
    '<span class="wf-steps"><span>회원·수강</span><span>출고·환불</span><span>문의·환급</span></span>'
    '<span class="wf-entry-go">흐름 보기 ↓</span></a>'
    '<a class="wf-entry is-sett" href="#wf-sett"><span class="wf-entry-label">월 정산</span>'
    '<strong>계약부터 지급까지</strong>'
    '<span class="wf-steps"><span>계약·상품 설정</span><i>→</i><span>사전 검증</span><i>→</i><span>정산·집행·감사</span></span>'
    '<span class="wf-entry-go">흐름 보기 ↓</span></a>'
    "</div></section>"
)

SET1 = lane(
    "회원·수강", "상황별 바로 처리", "순서 없이 상황이 생기면 해당 화면에서 처리합니다.",
    '<div class="wf-pairs">'
    + pair("가입 완료", "웰컴 혜택 발급", "자동 처리", "", "무상 포인트·쿠폰 지급", "5,000P·2년")
    + pair("중복 로그인 문의", "강제 로그아웃·기기 초기화", "일반 회원 관리 ", "USER-003", "기존 세션 종료", "1계정 1세션", USER_C)
    + pair("진도율 오류·0초 강의", "진도율 수동 보정", "일반 회원 관리 ", "USER-004", "환급 판정에 즉시 반영", "사유 입력", USER_C)
    + pair("수강 일시정지 요청", "수강 홀딩", "일반 회원 관리 ", "USER-003", "수강 기간 연장", "최대 3회·30일", USER_C)
    + pair("특가 기획전 등록", "쿠폰·적립 차단 켜기", "이벤트·기획전 관리 ", "PROM-001", "결제창 혜택 자동 잠금", "", F("PROM-001"))
    + "</div>"
)

SET3 = lane(
    "출고·환불", "교재 출고부터 반품·환불까지", "교재가 포함된 주문은 매일 이 순서로 처리합니다.",
    flow(
        start("교재 포함 결제 완료"),
        node("출고지시 다운로드", "주문·배송·3PL 관리 ", "ORD-002", "배송준비중 · 수험생 취소 잠금", ("매일 오전",), ORD),
        node("송장 일괄 업로드", "주문·배송·3PL 관리 ", "ORD-002", "배송중 · 재고 차감 · 알림톡", (), ORD),
        node("반품 입고 검수", "주문·배송·3PL 관리 ", "ORD-002", "환불 심사로 이관", (), ORD),
        node("환불 처리", "환불 요청·심사 관리 ", "RFD-002", "수강분·훼손분 공제 · 적립 P 회수 · PG 취소", (), F("RFD-002")),
    )
    + exc([
        ("가상계좌", "입금이 완료된 뒤에만 수강 권한이 열리고 출고됩니다."),
        ("휴대폰 결제", "익월이라 취소가 안 되면 등록 계좌로 현금 환불합니다."),
        ("적립 P 부족", "회수할 포인트가 모자라면 환불 현금에서 빼거나 마이너스 잔액으로 남깁니다."),
    ])
)

SET4 = lane(
    "문의·환급", "1:1 문의 분기와 합격환급", "문의는 유형별 담당 화면으로 넘기고, 환급은 심사 후 지급합니다.",
    '<div class="wf-part"><p class="wf-part-title">1:1 문의 분기</p><div class="wf-branch">'
    + '<div class="wf-hub">' + node("문의 접수·분류", "1:1 문의 관리 ", "BRD-002", "유형별 담당 화면으로 이관", ("답변 알림톡",), F("BRD-002")) + "</div>"
    + '<ul class="wf-fan">'
    + fan("결제·환불", "환불 요청·심사 관리 ", "RFD-002", F("RFD-002"))
    + fan("배송 잠금", "주문·배송·3PL 관리 ", "ORD-002", ORD)
    + fan("세션 초기화", "일반 회원 관리 ", "USER-003", USER_C)
    + fan("합격환급", "합격 환급반 관리 ", "SETT-006", F("SETT-006"))
    + fan("학습 질문", "네이버 카페 질문게시판 안내", "", "", "외부")
    + "</ul></div></div>"
    + '<div class="wf-part"><p class="wf-part-title">합격환급</p>'
    + flow(
        start("수험생 환급 신청"),
        node("제출 자료 4종 심사", "합격 환급반 관리 ", "SETT-006", "합격증·합격수기·통장사본·실명계좌 확인", (), F("SETT-006")),
        node("환급금 지급", "합격 환급반 관리 ", "SETT-006", "교재 금액 제외 후 지급", ("제세공과금 22%",), F("SETT-006")),
        node("강사 분담분 반영", "월 정산 사전 검증", "", "지원금 한도 자동 복원", (), "#wf-stage-02"),
    )
    + "</div>"
    + '<a class="wf-lane-link" href="#wf-sett">월 정산 마감은 월 정산 흐름에서 보기 ↓</a>'
)

OPS = (
    '<section id="wf-ops" class="wf-sec is-ops">'
    + sec_head("운영 업무", "고객 요청 처리 흐름", "회원·주문·문의처럼 매일 들어오는 요청을 어느 화면에서 처리하는지 보여줍니다.")
    + SET1 + SET3 + SET4 + "</section>"
)

CALC = [
    ("전월 이월 불러오기", ["SETT-002"]),
    ("이번 달 발생액 집계", ["SETT-004", "SETT-001"]),
    ("최저보장 보전", ["INST-001"]),
    ("환불·환급 공제", ["SETT-006"]),
    ("지원금 한도 적용", ["INST-001"]),
    ("선급금 상계", ["INST-001"]),
    ("약정금·일시금 더하기", ["INST-002", "SETT-005"]),
    ("수취인별 나누기", ["SETT-007"]),
    ("세금 계산", ["SETT-008"]),
    ("반환·청구 확인", ["SETT-002"]),
    ("지급 확정 또는 이월", ["SETT-002"]),
]
CALC_HTML = ('<details class="wf-calc"><summary>정산 계산 순서 보기 (11단계)</summary><ol>'
             + "".join(f'<li><span>{n}</span><span class="wf-calc-codes">{"".join(C(c) for c in cs)}</span></li>' for n, cs in CALC)
             + "</ol></details>")

ST1 = stage(
    "01", "wf-stage-01", "계약·상품 설정", "판매 오픈 전 · 계약 변경 시",
    "강좌와 도서를 판매하기 전에 계약 조건과 권리자 지분을 설정합니다.",
    '<p class="wf-row-title">계약·권리자</p>'
    + flow(
        start("오프라인 계약 체결", "계약서·사업자등록증·통장사본 수취"),
        node("계약 등록", "권리자 계약 원장 ", "INST-001", "요율·최저보장·지원금·선급금 저장", (), F("INST-001")),
        node("사업자 상태 확인", "사업자등록 확인 이력 ", "SETT-008", "과세유형 확정", (), F("SETT-008")),
        node("파트너 계정 발급", "권한 관리 ", "CONF-005", "본인 데이터만 보이는 계정", (), F("CONF-005")),
        node("수취인 나누기", "수취인 분할 관리 ", "SETT-007", "소속사·상속인 몫 설정", ("해당 시에만",), F("SETT-007")),
    )
    + '<p class="wf-row-title">상품 오픈</p>'
    + flow(
        node("도서 등록", "도서 공급 원장 ", "BOOK-001", "정식 상품 코드 생성", (), F("BOOK-001")),
        node("교재 정가·할인 설정", "교재 관리 ", "PROD-004", "실판매가 확정", ("최대 10% 할인",), F("PROD-004")),
        node("지분 100% 매핑", "상품별 권리자 매핑 ", "SETT-001", "판매 잠금 해제", (), F("SETT-001")),
        node("패키지 판매 오픈", "패키지·환급반 상품 관리 ", "PROD-005", "환급 조건 설정", (), F("PROD-005")),
    )
    + sub("도서 출간 전", "집필 계약 단계", flow(
        node("집필 계약·가번호 발급", "권리자 계약 원장 ", "INST-001", "", (), F("INST-001")),
        node("출간 후 정식 등록", "도서 공급 원장 ", "BOOK-001", "", (), F("BOOK-001")),
    ))
    + exc([
        ("계약 조건 변경", "기존 내용을 고치지 않고 새 적용일로 이력을 추가합니다."),
        ("선급금 잔액이 남은 계약", "수취인을 나눌 수 없습니다."),
        ("판매 이력이 있는 도서", "공급 형태를 바꿀 수 없습니다."),
        ("자사 저작권 도서", "인세는 지급하지 않고, 지원금은 정상 반영됩니다."),
    ])
)

ST2 = stage(
    "02", "wf-stage-02", "월마감 전 사전 검증", "매월 초",
    "정산을 실행하기 전에 네 관문을 모두 통과해야 합니다.",
    flow(
        gate(1, "PG 입금 대조", "PG 정산 원장 대사 ", "SETT-004", "원인 모를 불일치 0건", F("SETT-004")),
        gate(2, "약정금 검수", "약정금 마일스톤 검수 ", "INST-002", "이번 달 약정금 승인 완료", F("INST-002")),
        gate(3, "환급 공제 확정", "합격 환급반 관리 ", "SETT-006", "승인 확정 건 반영", F("SETT-006")),
        gate(4, "사업자 상태 점검", "사업자등록 확인 이력 ", "SETT-008", "세무 판정 보류 0건", F("SETT-008")),
    )
    + exc([
        ("원인 미상 소액 오차", "일괄 정리 후 통과시킵니다."),
        ("국세청 조회 장애", "증빙을 첨부하고 재무팀이 수기로 예외 지정합니다."),
        ("과세유형 변경 감지", "자동 반영하지 않고 담당자 승인 후 새 적용일로 반영합니다."),
    ])
)

ST3 = stage(
    "03", "wf-stage-03", "정산 실행·마감·집행·감사", "매월 마감",
    "정산서를 만들고 마감한 뒤 지급합니다. 감사 기록은 상시 확인합니다.",
    flow(
        node("월간 정산 실행", "월간 정산 및 집행 ", "SETT-002", "권리자별 정산서 생성", ("핵심 화면",), F("SETT-002"), cls="is-key"),
        node("정산 마감", "월간 정산 및 집행 ", "SETT-002", "정산서 확정 · 수정 잠금", (), F("SETT-002")),
        node("역발행 승인·이체", "월간 정산 및 집행 ", "SETT-002", "증빙 발행 · 이체", (), F("SETT-002")),
    )
    + '<div class="wf-aside"><span class="wf-row-title">함께 보는 화면</span>'
    + node("자사 몫 조회", "내부 정산 조회 ", "SETT-009", "자사 귀속분 확인", ("조회 전용",), F("SETT-009"))
    + "</div>"
    + CALC_HTML
    + sub("세무신고일", "매월 10일·말일",
          flow(
              node("신고 자료 추출", "내부 정산 조회 ", "SETT-009", "원천세·지급명세서 자료", (), F("SETT-009", "?view=tax-report")),
              node("열람 기록 확인", "정산 감사 로그 ", "CONF-010", "누가 언제 열람했는지 확인", (), F("CONF-010")),
          )
          + f'<div class="wf-sub-note">{chips("주민번호·계좌 열람 시 사유 입력 팝업 (USER-007)")}</div>')
    + sub("상시 감사", "월마감 주기와 무관",
          flow(node("변경·열람 기록 확인", "정산 감사 로그 ", "CONF-010", "변경 전·후 비교", (), F("CONF-010")))
          + f'<div class="wf-sub-note">{chips("마스킹 해제 시 사유 입력", "일정 시간 후 자동 재마스킹")}</div>')
    + exc([
        ("마감 후 오류 발견", f'마감을 취소하지 않고 다음 달에 조정합니다. → <a href="{F("SETT-005")}">정산 수동 조정</a>'),
        ("이체 실패", "다음 달로 이월합니다."),
        ("소액 지급분", "최소 지급 기준 미만이면 다음 달로 이월합니다."),
        ("마이너스 금액 초과", "권리자에게 반환을 청구합니다."),
        ("보존기한 경과", "개인정보만 파기하고 금액 기록은 보존합니다."),
    ])
)

SETT = (
    '<section id="wf-sett" class="wf-sec is-sett">'
    + sec_head("월 정산", "계약부터 지급까지", "판매 전 설정, 매월 초 사전 검증, 정산 실행·집행 순서로 진행합니다.")
    + '<div class="wf-stages">' + ST1 + ST2 + ST3 + "</div></section>"
)

DIR = (
    '<section id="wf-dir" class="wf-sec is-dir">'
    + sec_head("전체 화면", "화면 바로가기", "왼쪽 메뉴와 같은 구성입니다.")
    + '<div id="wf-dir-grid" class="wf-dir-grid"><p class="wf-dir-empty">메뉴를 불러오는 중입니다…</p></div>'
    + "</section>"
)

DIR_JS = r"""
<script id="wf-v5-dir">
(function () {
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function build() {
    var snb = document.getElementById('v4-master-snb');
    var box = document.getElementById('wf-dir-grid');
    if (!snb || !box) return false;
    var nodes = snb.querySelectorAll('.snb-group-title, a[href]');
    var groups = [], cur = null;
    Array.prototype.forEach.call(nodes, function (n) {
      if (n.classList.contains('snb-group-title')) { cur = { title: n.textContent.trim(), items: [] }; groups.push(cur); return; }
      var href = n.getAttribute('href') || '';
      if (!/\.html/.test(href) || /00_WORKFLOW_GUIDE/.test(href)) return;
      if (!cur) { cur = { title: '메뉴', items: [] }; groups.push(cur); }
      var codeEl = n.querySelector('.snb-code, .nav-code');
      var code = codeEl ? codeEl.textContent.trim() : '';
      var label = n.textContent.replace(code, '').replace(/\s+/g, ' ').trim();
      cur.items.push({ href: href, code: code, label: label });
    });
    groups = groups.filter(function (g) { return g.items.length; });
    if (!groups.length) return false;
    box.innerHTML = groups.map(function (g) {
      return '<div class="wf-dir-card"><h4>' + esc(g.title) + '</h4><ul>' + g.items.map(function (it) {
        return '<li><a href="' + esc(it.href) + '"><span>' + esc(it.label) + '</span>' +
          (it.code ? '<code class="wf-code">' + esc(it.code) + '</code>' : '') + '</a></li>';
      }).join('') + '</ul></div>';
    }).join('');
    return true;
  }
  var tries = 0;
  (function poll() {
    if (build()) return;
    if (++tries > 40) {
      var box = document.getElementById('wf-dir-grid');
      if (box) box.innerHTML = '<p class="wf-dir-empty">왼쪽 메뉴에서 화면을 선택하세요.</p>';
      return;
    }
    setTimeout(poll, 100);
  })();
})();
</script>
"""

NEW_BODY = '\n<main id="wf-root" data-wf="v5">\n' + INTRO + OPS + SETT + DIR + "\n</main>\n" + DIR_JS

CSS = r"""
<style id="wf-v5-style">
html{scroll-behavior:smooth}
#wf-root{--wf-ops:var(--emerald,#059669);--wf-ops-soft:var(--emerald-soft,#ECFDF5);--wf-ops-line:var(--emerald-border,#A7F3D0);
--wf-sett:var(--primary,#2563EB);--wf-sett-soft:var(--primary-soft,#EFF6FF);--wf-sett-line:var(--primary-border,#BFDBFE);
--wf-exc:var(--amber,#D97706);--wf-exc-soft:var(--amber-soft,#FFFBEB);--wf-exc-line:var(--amber-border,#FDE68A);
--wf-ink:var(--navy-900,#0F172A);--wf-sub:var(--slate-500,#64748B);--wf-line:var(--slate-200,#E2E8F0);
display:block;max-width:1280px;margin:0 auto;padding:32px 32px 72px;color:var(--wf-ink);
font-family:var(--font-sans,var(--font,Pretendard,sans-serif));font-size:14px;line-height:1.55}
#wf-root *{box-sizing:border-box}
#wf-root a{color:inherit;text-decoration:none}
#wf-root .is-ops,#wf-root .wf-entry.is-ops{--c:var(--wf-ops);--cs:var(--wf-ops-soft);--cl:var(--wf-ops-line)}
#wf-root .is-sett,#wf-root .wf-entry.is-sett{--c:var(--wf-sett);--cs:var(--wf-sett-soft);--cl:var(--wf-sett-line)}
#wf-root .is-dir{--c:var(--slate-600,#475569);--cs:var(--slate-100,#F1F5F9);--cl:var(--wf-line)}

/* intro */
.wf-intro h2{margin:0 0 8px;font-size:28px;font-weight:800;letter-spacing:-.03em}
.wf-intro>p{margin:0;color:var(--wf-sub);font-size:15px}
.wf-entry-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:24px}
.wf-entry{display:flex;flex-direction:column;gap:12px;padding:22px 24px;background:#fff;border:1px solid var(--wf-line);border-top:4px solid var(--c);border-radius:16px;transition:box-shadow .15s,transform .15s}
.wf-entry:hover{box-shadow:0 10px 28px rgba(15,23,42,.08);transform:translateY(-2px)}
.wf-entry-label{font-size:12px;font-weight:800;color:var(--c)}
.wf-entry strong{font-size:19px;font-weight:800;letter-spacing:-.02em}
.wf-steps{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.wf-steps span{padding:5px 10px;border-radius:8px;background:var(--cs);color:var(--wf-ink);font-size:13px;font-weight:700}
.wf-steps i{font-style:normal;color:var(--c);font-weight:800}
.wf-entry-go{margin-top:auto;font-size:13px;font-weight:800;color:var(--c)}

/* section */
.wf-sec{scroll-margin-top:84px;margin-top:56px;padding-top:40px;border-top:1px solid var(--wf-line)}
.wf-sec-hd{margin-bottom:8px}
.wf-eyebrow{display:inline-block;padding:4px 10px;border-radius:999px;background:var(--cs);color:var(--c);font-size:12px;font-weight:800}
.wf-sec-title{margin:10px 0 6px;font-size:23px;font-weight:800;letter-spacing:-.02em}
.wf-sec-desc{margin:0;color:var(--wf-sub);font-size:14px}

/* lane */
.wf-lane{margin-top:20px;padding:22px 24px;background:#fff;border:1px solid var(--wf-line);border-radius:16px}
.wf-lane-hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;margin-bottom:16px}
.wf-lane-hd h3{margin:0;font-size:17px;font-weight:800}
.wf-lane-hd p{margin:0;width:100%;color:var(--wf-sub);font-size:13px}
.wf-lane-tag{font-size:12px;font-weight:800;color:var(--c);letter-spacing:.02em}
.wf-lane-link{display:inline-block;margin-top:16px;font-size:13px;font-weight:800;color:var(--wf-sett)!important}
.wf-part+.wf-part{margin-top:24px;padding-top:20px;border-top:1px dashed var(--wf-line)}
.wf-part-title,.wf-row-title{margin:0 0 10px;font-size:12.5px;font-weight:800;color:var(--slate-600,#475569)}
.wf-row-title{margin-top:18px}

/* flow */
.wf-flow{display:flex;gap:28px;margin:0;padding:4px 2px 8px;list-style:none;overflow-x:auto}
.wf-flow>li{position:relative;display:flex;flex:1 1 0;min-width:136px}
.wf-flow>li.is-start{flex:0 0 124px;min-width:124px}
.wf-flow>li:only-child{flex:0 1 320px}
.wf-flow>li+li::before{content:"";position:absolute;left:-23px;top:50%;width:14px;height:2px;background:var(--cl)}
.wf-flow>li+li::after{content:"";position:absolute;left:-11px;top:calc(50% - 5px);border:5px solid transparent;border-left:7px solid var(--c)}

/* node */
.wf-node{display:flex;flex-direction:column;gap:6px;width:100%;padding:14px 14px 12px;background:#fff;border:1px solid var(--wf-line);border-top:3px solid var(--c);border-radius:12px;transition:border-color .15s,box-shadow .15s}
a.wf-node:hover,a.wf-pair:hover,a.wf-fan-item:hover{border-color:var(--c);box-shadow:0 6px 18px rgba(15,23,42,.07)}
.wf-node-tag{font-size:11px;font-weight:800;color:var(--c);letter-spacing:.02em}
.wf-node-do{font-size:14.5px;font-weight:800;line-height:1.35}
.wf-node-scr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 6px;color:var(--slate-600,#475569);font-size:12.5px}
.wf-node-out{padding-top:6px;border-top:1px dashed var(--wf-line);font-size:12.5px}
.wf-code{padding:0 5px;border:1px solid var(--wf-line);border-radius:4px;background:var(--slate-50,#F8FAFC);color:var(--slate-400,#94A3B8);font-family:inherit;font-size:11px;font-weight:600}
.wf-chips{display:flex;flex-wrap:wrap;gap:4px}
.wf-chip{padding:2px 8px;border-radius:999px;background:var(--cs);color:var(--c);font-size:11.5px;font-weight:700}
.wf-node.is-start{justify-content:center;background:var(--cs);border:1px dashed var(--cl)}
.wf-node.is-key{border:2px solid var(--c);box-shadow:0 0 0 4px var(--cs)}
.wf-gate-pass{font-size:12px;font-weight:700;color:var(--emerald,#059669)}

/* pairs */
.wf-pairs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.wf-pair{display:grid;grid-template-columns:128px 16px 1fr;align-items:center;gap:10px;padding:14px 16px;background:#fff;border:1px solid var(--wf-line);border-radius:12px}
.wf-pair-when{color:var(--slate-600,#475569);font-size:13px;font-weight:700}
.wf-pair-arrow{color:var(--c);font-weight:800}
.wf-pair-body{display:flex;flex-direction:column;gap:5px}

/* branch */
.wf-branch{display:grid;grid-template-columns:minmax(190px,250px) 1fr;align-items:center}
.wf-hub{position:relative}
.wf-hub::after{content:"";position:absolute;right:-28px;top:50%;width:28px;height:2px;background:var(--cl)}
.wf-fan{position:relative;display:flex;flex-direction:column;gap:8px;margin:0 0 0 28px;padding:0 0 0 22px;list-style:none;border-left:2px solid var(--cl)}
.wf-fan>li{position:relative}
.wf-fan>li::before{content:"";position:absolute;left:-22px;top:50%;width:16px;height:2px;background:var(--cl)}
.wf-fan-item{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;padding:9px 12px;background:#fff;border:1px solid var(--wf-line);border-radius:10px;font-size:13px}
.wf-fan-item b{min-width:84px;font-weight:800}

/* exceptions */
.wf-exc{margin-top:16px;background:var(--wf-exc-soft);border:1px dashed var(--wf-exc-line);border-radius:10px;font-size:13px}
.wf-exc>summary,.wf-calc>summary{display:flex;align-items:center;gap:8px;padding:10px 14px;cursor:pointer;list-style:none;font-weight:800}
.wf-exc>summary{color:var(--wf-exc)}
.wf-exc>summary::-webkit-details-marker,.wf-calc>summary::-webkit-details-marker{display:none}
.wf-exc>summary::before,.wf-calc>summary::before{content:"▸";transition:transform .15s}
.wf-exc[open]>summary::before,.wf-calc[open]>summary::before{transform:rotate(90deg)}
.wf-exc ul{display:flex;flex-direction:column;gap:6px;margin:0;padding:0 14px 12px 34px}
.wf-exc b{font-weight:800}
.wf-exc a{color:var(--wf-exc)!important;font-weight:700;text-decoration:underline!important}

/* stages */
.wf-stages{margin-top:24px}
.wf-stage{position:relative;display:grid;grid-template-columns:48px 1fr;gap:20px;padding-bottom:40px;scroll-margin-top:84px}
.wf-stage::before{content:"";position:absolute;left:23px;top:52px;bottom:4px;width:2px;background:var(--wf-sett-line)}
.wf-stage:last-child{padding-bottom:0}
.wf-stage:last-child::before{display:none}
.wf-stage-num{display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--wf-sett);color:#fff;font-size:16px;font-weight:800}
.wf-stage-main{min-width:0;padding:20px 22px;background:#fff;border:1px solid var(--wf-line);border-radius:16px}
.wf-stage-hd{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px}
.wf-stage-hd h3{margin:0;font-size:18px;font-weight:800}
.wf-period{padding:3px 10px;border-radius:999px;background:var(--slate-100,#F1F5F9);color:var(--slate-600,#475569);font-size:12px;font-weight:700}
.wf-stage-desc{margin:6px 0 4px;color:var(--wf-sub);font-size:13.5px}
.wf-aside{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;margin-top:14px}
.wf-aside .wf-row-title{margin:0}
.wf-aside .wf-node{max-width:320px}
.wf-sub{margin-top:16px;padding:16px 18px;background:var(--slate-50,#F8FAFC);border-left:3px solid var(--c);border-radius:12px}
.wf-sub-hd{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:12px}
.wf-sub-hd strong{font-size:14px;font-weight:800}
.wf-sub-note{margin-top:8px}
.wf-calc{margin-top:16px;background:#fff;border:1px solid var(--wf-line);border-radius:10px}
.wf-calc>summary{color:var(--c);font-size:13px}
.wf-calc ol{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;margin:0;padding:2px 14px 14px;list-style:none;counter-reset:wfs}
.wf-calc li{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:8px 10px;background:var(--slate-50,#F8FAFC);border-radius:8px;font-size:13px;counter-increment:wfs}
.wf-calc li::before{content:counter(wfs);min-width:18px;color:var(--c);font-weight:800}
.wf-calc-codes{display:flex;gap:4px;margin-left:auto}

/* directory */
.wf-dir-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-top:20px}
.wf-dir-card{padding:16px 18px;background:#fff;border:1px solid var(--wf-line);border-radius:14px}
.wf-dir-card h4{margin:0 0 8px;color:var(--slate-600,#475569);font-size:12.5px;font-weight:800}
.wf-dir-card ul{display:flex;flex-direction:column;gap:2px;margin:0;padding:0;list-style:none}
.wf-dir-card a{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:9px 10px;border-radius:8px;font-size:13.5px}
.wf-dir-card a:hover{background:var(--slate-50,#F8FAFC)}
.wf-dir-empty{color:var(--wf-sub)}

@media (max-width:860px){
#wf-root{padding:20px 16px 48px}
.wf-entry-grid,.wf-pairs{grid-template-columns:1fr}
.wf-branch{grid-template-columns:1fr}
.wf-hub::after{display:none}
.wf-fan{margin:12px 0 0 12px}
.wf-pair{grid-template-columns:1fr;gap:4px}
.wf-pair-arrow{display:none}
.wf-stage{grid-template-columns:1fr}
.wf-stage-num,.wf-stage::before{display:none}
}
</style>
"""


# ---------------- 교체 로직 ----------------
def mask(s):
    blank = lambda m: " " * len(m.group(0))
    s = re.sub(r"<script\b.*?</script\s*>", blank, s, flags=re.S | re.I)
    s = re.sub(r"<style\b.*?</style\s*>", blank, s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", blank, s, flags=re.S)
    return s


def find_page_body(src):
    m = re.search(r"<div\b[^>]*\bid=[\"']v4-page-body[\"'][^>]*>", src, re.I)
    if not m:
        return None
    masked = mask(src)
    depth = 1
    for t in re.finditer(r"<div\b|</div\s*>", masked[m.end():], re.I):
        if t.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                close = m.end() + t.start()
                return m.end(), close
        else:
            depth += 1
    return None


def main():
    if not WF.exists():
        print("[ERROR] 대상 파일 없음:", WF)
        sys.exit(1)
    src = WF.read_text(encoding="utf-8")
    if 'id="wf-root"' in src or "wf-v5-style" in src:
        print("[SKIP] 이미 v5 적용됨")
        sys.exit(0)

    # 링크 대상 검증
    missing = sorted({h.split("?")[0] for h in re.findall(r'href="(ADMN-[^"]+)"', NEW_BODY)
                      if not (CLEAN / h.split("?")[0]).exists()})
    if missing:
        print("[ABORT] 링크 대상 파일 없음 (파일 미변경):", *missing, sep="\n  - ")
        sys.exit(2)

    # head
    if "</head>" not in src:
        print("[ABORT] </head> 없음")
        sys.exit(2)
    src = src.replace("</head>", CSS + "</head>", 1)
    src = re.sub(r"<title>.*?</title>", lambda m: "<title>업무 플로우 가이드 — 산준모 백오피스</title>", src, count=1, flags=re.S)
    src, n_h1 = re.subn(r'(<h1[^>]*id="header-screen-title"[^>]*>).*?(</h1>)',
                        lambda m: m.group(1) + "업무 플로우 가이드" + m.group(2), src, count=1, flags=re.S)

    # body
    pos = find_page_body(src)
    if not pos:
        print("[ABORT] #v4-page-body 블록을 찾지 못함 (파일 미변경)")
        sys.exit(2)
    a, b = pos
    inner = src[a:b]
    kept = re.findall(r"<script\b.*?</script\s*>", inner, flags=re.S | re.I)
    new_src = src[:a] + NEW_BODY + "\n" + "\n".join(kept) + "\n" + src[b:]

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(WF, BACKUP)
    WF.write_text(new_src, encoding="utf-8")

    nodes = NEW_BODY.count('class="wf-node')
    links = len(re.findall(r'href="ADMN-', NEW_BODY))
    print(f"[OK] {WF.relative_to(ROOT)} 갱신")
    print(f"     백업: {BACKUP.relative_to(ROOT)}")
    print(f"     노드 {nodes}개 · 화면 링크 {links}개 · 보존 스크립트 {len(kept)}개 · 상단 제목 교체 {n_h1}건")

    if PLAN.exists():
        t = PLAN.read_text(encoding="utf-8")
        t = t.replace("4. [ ] 마크업 패치 스크립트 (clean)", "4. [x] 마크업 패치 스크립트 (clean) · patch_workflow_v5_clean.py", 1)
        t = t.rstrip() + "\n- 2026-10-21 · 마크업 v5 적용(clean). 디렉터리는 SNB DOM 런타임 미러링. 운영 진입 카드는 순서 없음 → 화살표 미사용\n"
        PLAN.write_text(t, encoding="utf-8")
        print("[OK] 플랜 파일 진행 단계 갱신")


if __name__ == "__main__":
    main()
