# 업무플로우 v5 마크업 덤프 (레이아웃 보정용)

## 1. wf- CSS 규칙
```css
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
#wf-root{padding:20px 16px 48px}
.wf-entry-grid,.wf-pairs{grid-template-columns:1fr}
.wf-branch{grid-template-columns:1fr}
.wf-hub::after{display:none}
.wf-fan{margin:12px 0 0 12px}
.wf-pair{grid-template-columns:1fr;gap:4px}
.wf-pair-arrow{display:none}
.wf-stage{grid-template-columns:1fr}
.wf-stage-num,.wf-stage::before{display:none}
#wf-dir-grid{display:block!important;column-width:300px;column-gap:16px}
#wf-dir-grid>.wf-dir-card{break-inside:avoid;display:inline-block;width:100%;margin:0 0 16px!important;vertical-align:top}
```

## 2. #wf-root 뼈대 (depth 9, 텍스트 24자)
```
<main#wf-root>
  <section.wf-intro>
    <h2>  "고객 응대부터 월 정산 마감까지"
    <p>  "상황별로 어느 화면에서 무엇을 처리하는지 순"
    <div.wf-entry-grid>
      <a.wf-entry.is-ops>
        <span.wf-entry-label>  "운영 업무"
        <strong>  "매일 들어오는 요청 처리"
        <span.wf-steps>
          <span>  "회원·수강"
          <span>  "출고·환불"
          <span>  "문의·환급"
        <span.wf-entry-go>  "흐름 보기 ↓"
      <a.wf-entry.is-sett>
        <span.wf-entry-label>  "월 정산"
        <strong>  "계약부터 지급까지"
        <span.wf-steps>
          <span>  "계약·상품 설정"
          <i>  "→"
          <span>  "사전 검증"
          <i>  "→"
          <span>  "정산·집행·감사"
        <span.wf-entry-go>  "흐름 보기 ↓"
  <section#wf-ops.wf-sec.is-ops>
    <header.wf-sec-hd>
      <span.wf-eyebrow>  "운영 업무"
      <h2.wf-sec-title>  "고객 요청 처리 흐름"
      <p.wf-sec-desc>  "회원·주문·문의처럼 매일 들어오는 요청을 어"
    <article.wf-lane>
      <div.wf-lane-hd>
        <span.wf-lane-tag>  "회원·수강"
        <h3>  "상황별 바로 처리"
        <p>  "순서 없이 상황이 생기면 해당 화면에서 처리"
      <div.wf-pairs>
        <div.wf-pair>
          <span.wf-pair-when>  "가입 완료"
          <span.wf-pair-arrow>  "→"
          <span.wf-pair-body>
            <span.wf-node-do>  "웰컴 혜택 발급"
            <span.wf-node-scr>  "자동 처리"
            <span.wf-node-out>  "무상 포인트·쿠폰 지급"
            <span.wf-chips>
              <span.wf-chip>  "5,000P·2년"
        <a.wf-pair>
          <span.wf-pair-when>  "중복 로그인 문의"
          <span.wf-pair-arrow>  "→"
          <span.wf-pair-body>
            <span.wf-node-do>  "강제 로그아웃·기기 초기화"
            <span.wf-node-scr>  "일반 회원 관리"
              <code.wf-code>  "USER-003"
            <span.wf-node-out>  "기존 세션 종료"
            <span.wf-chips>
              <span.wf-chip>  "1계정 1세션"
        <a.wf-pair>
          <span.wf-pair-when>  "진도율 오류·0초 강의"
          <span.wf-pair-arrow>  "→"
          <span.wf-pair-body>
            <span.wf-node-do>  "진도율 수동 보정"
            <span.wf-node-scr>  "일반 회원 관리"
              <code.wf-code>  "USER-004"
            <span.wf-node-out>  "환급 판정에 즉시 반영"
            <span.wf-chips>
              <span.wf-chip>  "사유 입력"
        <a.wf-pair>
          <span.wf-pair-when>  "수강 일시정지 요청"
          <span.wf-pair-arrow>  "→"
          <span.wf-pair-body>
            <span.wf-node-do>  "수강 홀딩"
            <span.wf-node-scr>  "일반 회원 관리"
              <code.wf-code>  "USER-003"
            <span.wf-node-out>  "수강 기간 연장"
            <span.wf-chips>
              <span.wf-chip>  "최대 3회·30일"
        <a.wf-pair>
          <span.wf-pair-when>  "특가 기획전 등록"
          <span.wf-pair-arrow>  "→"
          <span.wf-pair-body>
            <span.wf-node-do>  "쿠폰·적립 차단 켜기"
            <span.wf-node-scr>  "이벤트·기획전 관리"
              <code.wf-code>  "PROM-001"
            <span.wf-node-out>  "결제창 혜택 자동 잠금"
    <article.wf-lane>
      <div.wf-lane-hd>
        <span.wf-lane-tag>  "출고·환불"
        <h3>  "교재 출고부터 반품·환불까지"
        <p>  "교재가 포함된 주문은 매일 이 순서로 처리합"
      <ol.wf-flow>
        <li.is-start>
          <div.wf-node.is-start>
            <span.wf-node-tag>  "출발"
            <span.wf-node-do>  "교재 포함 결제 완료"
        <li>
          <a.wf-node>
            <span.wf-node-do>  "출고지시 다운로드"
            <span.wf-node-scr>  "주문·배송·3PL 관리"
              <code.wf-code>  "ORD-002"
            <span.wf-node-out>  "배송준비중 · 수험생 취소 잠금"
            <span.wf-chips>
              <span.wf-chip>  "매일 오전"
        <li>
          <a.wf-node>
            <span.wf-node-do>  "송장 일괄 업로드"
            <span.wf-node-scr>  "주문·배송·3PL 관리"
              <code.wf-code>  "ORD-002"
            <span.wf-node-out>  "배송중 · 재고 차감 · 알림톡"
        <li>
          <a.wf-node>
            <span.wf-node-do>  "반품 입고 검수"
            <span.wf-node-scr>  "주문·배송·3PL 관리"
              <code.wf-code>  "ORD-002"
            <span.wf-node-out>  "환불 심사로 이관"
        <li>
          <a.wf-node>
            <span.wf-node-do>  "환불 처리"
            <span.wf-node-scr>  "환불 요청·심사 관리"
              <code.wf-code>  "RFD-002"
            <span.wf-node-out>  "수강분·훼손분 공제 · 적립 P 회수 · P"
      <details.wf-exc>
        <summary>  "예외 상황 3건"
        <ul>
          <li>
            <b>  "가상계좌"
          <li>
            <b>  "휴대폰 결제"
          <li>
            <b>  "적립 P 부족"
    <article.wf-lane>
      <div.wf-lane-hd>
        <span.wf-lane-tag>  "문의·환급"
        <h3>  "1:1 문의 분기와 합격환급"
        <p>  "문의는 유형별 담당 화면으로 넘기고, 환급은"
      <div.wf-part>
        <p.wf-part-title>  "1:1 문의 분기"
        <div.wf-branch>
          <div.wf-hub>
            <a.wf-node>
              <span.wf-node-do>  "문의 접수·분류"
              <span.wf-node-scr>  "1:1 문의 관리"
                <code.wf-code>  "BRD-002"
              <span.wf-node-out>  "유형별 담당 화면으로 이관"
              <span.wf-chips>
                <span.wf-chip>  "답변 알림톡"
          <ul.wf-fan>
            <li>
              <a.wf-fan-item>
                <b>  "결제·환불"
                <span.wf-node-scr>  "환불 요청·심사 관리"
                  <code.wf-code>  "RFD-002"
            <li>
              <a.wf-fan-item>
                <b>  "배송 잠금"
                <span.wf-node-scr>  "주문·배송·3PL 관리"
                  <code.wf-code>  "ORD-002"
            <li>
              <a.wf-fan-item>
                <b>  "세션 초기화"
                <span.wf-node-scr>  "일반 회원 관리"
                  <code.wf-code>  "USER-003"
            <li>
              <a.wf-fan-item>
                <b>  "합격환급"
                <span.wf-node-scr>  "합격 환급반 관리"
                  <code.wf-code>  "SETT-006"
            <li>
              <div.wf-fan-item>
                <b>  "학습 질문"
                <span.wf-node-scr>  "네이버 카페 질문게시판 안내"
                <span.wf-chips>
                  <span.wf-chip>  "외부"
      <div.wf-part>
        <p.wf-part-title>  "합격환급"
        <ol.wf-flow>
          <li.is-start>
            <div.wf-node.is-start>
              <span.wf-node-tag>  "출발"
              <span.wf-node-do>  "수험생 환급 신청"
          <li>
            <a.wf-node>
              <span.wf-node-do>  "제출 자료 4종 심사"
              <span.wf-node-scr>  "합격 환급반 관리"
                <code.wf-code>  "SETT-006"
              <span.wf-node-out>  "합격증·합격수기·통장사본·실명계좌 확인"
          <li>
            <a.wf-node>
              <span.wf-node-do>  "환급금 지급"
              <span.wf-node-scr>  "합격 환급반 관리"
                <code.wf-code>  "SETT-006"
              <span.wf-node-out>  "교재 금액 제외 후 지급"
              <span.wf-chips>
                <span.wf-chip>  "제세공과금 22%"
          <li>
            <a.wf-node>
              <span.wf-node-do>  "강사 분담분 반영"
              <span.wf-node-scr>  "월 정산 사전 검증"
              <span.wf-node-out>  "지원금 한도 자동 복원"
      <a.wf-lane-link>  "월 정산 마감은 월 정산 흐름에서 보기 ↓"
  <section#wf-sett.wf-sec.is-sett>
    <header.wf-sec-hd>
      <span.wf-eyebrow>  "월 정산"
      <h2.wf-sec-title>  "계약부터 지급까지"
      <p.wf-sec-desc>  "판매 전 설정, 매월 초 사전 검증, 정산 "
    <div.wf-stages>
      <section#wf-stage-01.wf-stage>
        <div.wf-stage-num>  "01"
        <div.wf-stage-main>
          <div.wf-stage-hd>
            <span.wf-lane-tag>  "STAGE 01"
            <h3>  "계약·상품 설정"
            <span.wf-period>  "판매 오픈 전 · 계약 변경 시"
          <p.wf-stage-desc>  "강좌와 도서를 판매하기 전에 계약 조건과 권"
          <p.wf-row-title>  "계약·권리자"
          <ol.wf-flow>
            <li.is-start>
              <div.wf-node.is-start>
                <span.wf-node-tag>  "출발"
                <span.wf-node-do>  "오프라인 계약 체결"
                <span.wf-node-out>  "계약서·사업자등록증·통장사본 수취"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "계약 등록"
                <span.wf-node-scr>  "권리자 계약 원장"
                  <code.wf-code>  "INST-001"
                <span.wf-node-out>  "요율·최저보장·지원금·선급금 저장"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "사업자 상태 확인"
                <span.wf-node-scr>  "사업자등록 확인 이력"
                  <code.wf-code>  "SETT-008"
                <span.wf-node-out>  "과세유형 확정"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "파트너 계정 발급"
                <span.wf-node-scr>  "운영자 계정 · 역할 권한(RBAC)"
                  <code.wf-code>  "CONF-005"
                <span.wf-node-out>  "본인 데이터만 보이는 계정"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "수취인 나누기"
                <span.wf-node-scr>  "수취인 분할 관리"
                  <code.wf-code>  "SETT-007"
                <span.wf-node-out>  "소속사·상속인 몫 설정"
                <span.wf-chips>
                  <span.wf-chip>  "해당 시에만"
          <p.wf-row-title>  "상품 오픈"
          <ol.wf-flow>
            <li>
              <a.wf-node>
                <span.wf-node-do>  "도서 등록"
                <span.wf-node-scr>  "도서 공급 원장"
                  <code.wf-code>  "BOOK-001"
                <span.wf-node-out>  "정식 상품 코드 생성"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "교재 정가·할인 설정"
                <span.wf-node-scr>  "교재 관리"
                  <code.wf-code>  "PROD-004"
                <span.wf-node-out>  "실판매가 확정"
                <span.wf-chips>
                  <span.wf-chip>  "최대 10% 할인"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "지분 100% 매핑"
                <span.wf-node-scr>  "상품별 권리자 매핑"
                  <code.wf-code>  "SETT-001"
                <span.wf-node-out>  "판매 잠금 해제"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "패키지 판매 오픈"
                <span.wf-node-scr>  "패키지·환급반 상품 관리"
                  <code.wf-code>  "PROD-005"
                <span.wf-node-out>  "환급 조건 설정"
          <div.wf-sub>
            <div.wf-sub-hd>
              <strong>  "도서 출간 전"
              <span.wf-chips>
                <span.wf-chip>  "집필 계약 단계"
            <ol.wf-flow>
              <li>
                <a.wf-node>
                  <span.wf-node-do>  "집필 계약·가번호 발급"
                  <span.wf-node-scr>  "권리자 계약 원장"
              <li>
                <a.wf-node>
                  <span.wf-node-do>  "출간 후 정식 등록"
                  <span.wf-node-scr>  "도서 공급 원장"
          <details.wf-exc>
            <summary>  "예외 상황 4건"
            <ul>
              <li>
                <b>  "계약 조건 변경"
              <li>
                <b>  "선급금 잔액이 남은 계약"
              <li>
                <b>  "판매 이력이 있는 도서"
              <li>
                <b>  "자사 저작권 도서"
      <section#wf-stage-02.wf-stage>
        <div.wf-stage-num>  "02"
        <div.wf-stage-main>
          <div.wf-stage-hd>
            <span.wf-lane-tag>  "STAGE 02"
            <h3>  "월마감 전 사전 검증"
            <span.wf-period>  "매월 초"
          <p.wf-stage-desc>  "정산을 실행하기 전에 네 관문을 모두 통과해"
          <ol.wf-flow>
            <li>
              <a.wf-node.is-gate>
                <span.wf-node-tag>  "관문 1"
                <span.wf-node-do>  "PG 입금 대조"
                <span.wf-node-scr>  "PG 정산 원장 대사"
                  <code.wf-code>  "SETT-004"
                <span.wf-gate-pass>  "✓ 원인 모를 불일치 0건"
            <li>
              <a.wf-node.is-gate>
                <span.wf-node-tag>  "관문 2"
                <span.wf-node-do>  "약정금 검수"
                <span.wf-node-scr>  "약정금 마일스톤 검수"
                  <code.wf-code>  "INST-002"
                <span.wf-gate-pass>  "✓ 이번 달 약정금 승인 완료"
            <li>
              <a.wf-node.is-gate>
                <span.wf-node-tag>  "관문 3"
                <span.wf-node-do>  "환급 공제 확정"
                <span.wf-node-scr>  "합격 환급반 관리"
                  <code.wf-code>  "SETT-006"
                <span.wf-gate-pass>  "✓ 승인 확정 건 반영"
            <li>
              <a.wf-node.is-gate>
                <span.wf-node-tag>  "관문 4"
                <span.wf-node-do>  "사업자 상태 점검"
                <span.wf-node-scr>  "사업자등록 확인 이력"
                  <code.wf-code>  "SETT-008"
                <span.wf-gate-pass>  "✓ 세무 판정 보류 0건"
          <details.wf-exc>
            <summary>  "예외 상황 3건"
            <ul>
              <li>
                <b>  "원인 미상 소액 오차"
              <li>
                <b>  "국세청 조회 장애"
              <li>
                <b>  "과세유형 변경 감지"
      <section#wf-stage-03.wf-stage>
        <div.wf-stage-num>  "03"
        <div.wf-stage-main>
          <div.wf-stage-hd>
            <span.wf-lane-tag>  "STAGE 03"
            <h3>  "정산 실행·마감·집행·감사"
            <span.wf-period>  "매월 마감"
          <p.wf-stage-desc>  "정산서를 만들고 마감한 뒤 지급합니다. 감사"
          <ol.wf-flow>
            <li>
              <a.wf-node.is-key>
                <span.wf-node-do>  "월간 정산 실행"
                <span.wf-node-scr>  "월간 정산 및 집행"
                  <code.wf-code>  "SETT-002"
                <span.wf-node-out>  "권리자별 정산서 생성"
                <span.wf-chips>
                  <span.wf-chip>  "핵심 화면"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "정산 마감"
                <span.wf-node-scr>  "월간 정산 및 집행"
                  <code.wf-code>  "SETT-002"
                <span.wf-node-out>  "정산서 확정 · 수정 잠금"
            <li>
              <a.wf-node>
                <span.wf-node-do>  "역발행 승인·이체"
                <span.wf-node-scr>  "월간 정산 및 집행"
                  <code.wf-code>  "SETT-002"
                <span.wf-node-out>  "증빙 발행 · 이체"
          <div.wf-aside>
            <span.wf-row-title>  "함께 보는 화면"
            <a.wf-node>
              <span.wf-node-do>  "자사 몫 조회"
              <span.wf-node-scr>  "내부 정산 조회"
                <code.wf-code>  "SETT-009"
              <span.wf-node-out>  "자사 귀속분 확인"
              <span.wf-chips>
                <span.wf-chip>  "조회 전용"
          <details.wf-calc>
            <summary>  "정산 계산 순서 보기 (11단계)"
            <ol>
              <li>
                <span>  "전월 이월 불러오기"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-002"
              <li>
                <span>  "이번 달 발생액 집계"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-004"
                  <code.wf-code>  "SETT-001"
              <li>
                <span>  "최저보장 보전"
                <span.wf-calc-codes>
                  <code.wf-code>  "INST-001"
              <li>
                <span>  "환불·환급 공제"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-006"
              <li>
                <span>  "지원금 한도 적용"
                <span.wf-calc-codes>
                  <code.wf-code>  "INST-001"
              <li>
                <span>  "선급금 상계"
                <span.wf-calc-codes>
                  <code.wf-code>  "INST-001"
              <li>
                <span>  "약정금·일시금 더하기"
                <span.wf-calc-codes>
                  <code.wf-code>  "INST-002"
                  <code.wf-code>  "SETT-005"
              <li>
                <span>  "수취인별 나누기"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-007"
              <li>
                <span>  "세금 계산"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-008"
              <li>
                <span>  "반환·청구 확인"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-002"
              <li>
                <span>  "지급 확정 또는 이월"
                <span.wf-calc-codes>
                  <code.wf-code>  "SETT-002"
          <div.wf-sub>
            <div.wf-sub-hd>
              <strong>  "세무신고일"
              <span.wf-chips>
                <span.wf-chip>  "매월 10일·말일"
            <ol.wf-flow>
              <li>
                <a.wf-node>
                  <span.wf-node-do>  "신고 자료 추출"
                  <span.wf-node-scr>  "내부 정산 조회"
                  <span.wf-node-out>  "원천세·지급명세서 자료"
              <li>
                <a.wf-node>
                  <span.wf-node-do>  "열람 기록 확인"
                  <span.wf-node-scr>  "정산 감사 로그"
                  <span.wf-node-out>  "누가 언제 열람했는지 확인"
            <div.wf-sub-note>
              <span.wf-chips>
                <span.wf-chip>  "주민번호·계좌 열람 시 사유 입력 팝업 (U"
          <div.wf-sub>
            <div.wf-sub-hd>
              <strong>  "상시 감사"
              <span.wf-chips>
                <span.wf-chip>  "월마감 주기와 무관"
            <ol.wf-flow>
              <li>
                <a.wf-node>
                  <span.wf-node-do>  "변경·열람 기록 확인"
                  <span.wf-node-scr>  "정산 감사 로그"
                  <span.wf-node-out>  "변경 전·후 비교"
                <a.wf-node>
                  <span.wf-node-do>  "변경·열람 기록 확인"
                  <span.wf-node-scr>  "개인정보 열람 및 보안 감사로그"
                  <span.wf-node-out>  "변경 전·후 비교"
            <div.wf-sub-note>
              <span.wf-chips>
                <span.wf-chip>  "마스킹 해제 시 사유 입력"
                <span.wf-chip>  "일정 시간 후 자동 재마스킹"
          <details.wf-exc>
            <summary>  "예외 상황 5건"
            <ul>
              <li>
                <b>  "마감 후 오류 발견"
                <a>  "정산 수동 조정"
              <li>
                <b>  "이체 실패"
              <li>
                <b>  "소액 지급분"
              <li>
                <b>  "마이너스 금액 초과"
              <li>
                <b>  "보존기한 경과"
  <section#wf-dir.wf-sec.is-dir>
    <header.wf-sec-hd>
      <span.wf-eyebrow>  "전체 화면"
      <h2.wf-sec-title>  "화면 바로가기"
      <p.wf-sec-desc>  "왼쪽 메뉴와 같은 구성입니다."
    <div#wf-dir-grid.wf-dir-grid>
      <p.wf-dir-empty>  "메뉴를 불러오는 중입니다…"
```
