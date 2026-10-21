# PAREN_FIX_SRC_02 — 잔여 괄호 중복 원문 위치 (prototype_clean, 원문)

## ADMN-BOOK-001 · "도서 공급형태"
- L763: `<h2 class="card-title">4대 도서 공급형태(book_supply_type) · 자사저작권(개발지원금) · 정가 이력(book_price_history) 정합성 원장</h2>`

## ADMN-CONF-005 · "파트너 강사"
- L342: `이던 외부 파트너를 역할과 정산·업무 범위에 따라 <strong>[1] 파트너 강사(<code>ROLE_PARTNER_INST</code>)</strong>, <strong>[2] 교재 저작권자/출판사(<code>ROLE_PARTNER_COPYRIGHT</code>)</strong>, <strong>[3] 외부 물류 3PL(<code>ROLE_PARTNER_3PL</`
- L348: `<h4>[1] 파트너 강사 전용 권한</h4>`
- L414: `le="background:#f5f3ff; color:#6d28d9;">파트너 강사<br/>(PARTNER_INST)</th>`

## ADMN-CONF-005 · "외부 물류 3PL"
- L342: `COPYRIGHT</code>)</strong>, <strong>[3] 외부 물류 3PL(<code>ROLE_PARTNER_3PL</code>)</strong>로 명확히 분리하여, 타 파트너의 매출·정산서·회원 개인정보에 접근할 수 없도록 <strong>데이터 스코프(Data Scope: 본인 ID 격리)</strong>와 <strong>기능 스코프(Action Scope`
- L374: `<option value="ROLE_PARTNER_3PL">[파트너] 외부 물류 3PL (ROLE_PARTNER_3PL)</option>`
- L416: `le="background:#fffbeb; color:#b45309;">외부 물류 3PL<br/>(PARTNER_3PL)</th>`
- L533: `ption value="ROLE_PARTNER_3PL">[외부 파트너] 외부 물류 3PL (ROLE_PARTNER_3PL — 교재 출고지시서 및 송장 등록)</option>`

## ADMN-CONF-010 · "상품별 권리자 매핑"
- L376: `on value="ADMN-SETT-001">ADMN-SETT-001 (상품별 권리자 매핑)</option>`

## ADMN-CONF-010 · "수취인 분할 관리"
- L377: `on value="ADMN-SETT-007">ADMN-SETT-007 (수취인 분할 관리)</option>`

## ADMN-CONF-010 · "약정금 마일스톤 검수"
- L378: `on value="ADMN-INST-002">ADMN-INST-002 (약정금 마일스톤 검수)</option>`

## ADMN-CONF-010 · "정산 수동 조정"
- L369: `<option value="FINANCE">2. 정산 수동 조정 · 계정 간 대체 · 수기 검수 (SETT-005 / INST-002)</option>`
- L379: `on value="ADMN-SETT-005">ADMN-SETT-005 (정산 수동 조정)</option>`

## ADMN-CONF-010 · "도서 공급 원장"
- L382: `on value="ADMN-BOOK-001">ADMN-BOOK-001 (도서 공급 원장)</option>`

## ADMN-CONF-010 · "민감정보 열람통제"
0건

## ADMN-INST-001 · "자사저작권 도서"
- L2599: `ipelines:["온라인 R/S (1.1)","개발지원금 (5.1 · 자사저작권 도서 연동 · CONDITIONAL)","선급금"],`
- L2607: `summaryNote:"[v4.0.0 대표 사례] 자사저작권 도서(자사 저작권 보유) 매출연동 지원금 15% + 선급금 상계 허용(CONDITIONAL)"`
- L2802: `/* 정종대 강사(CT-2026-0501) 선택 시 자사저작권 도서(PROD-BK-1004) 지원금 매핑 시연 데이터 자동 세팅 */`

## ADMN-INST-002 · "매출연동("
- L480: `ode>LUMPSUM_ADD</code>) 이관 검수와, <strong>매출연동(<code>매출연동 (REVENUE_SHARE)</code>) 개발지원금 약정 체결 시 최초 1회 검수</strong>만 수행합니다. (매출연동형의 월별 지급분은 자동 연산되므로 매월 검수하지 않으며, 사입 도서 매입채무(AP)는 회계 시스템 경로로 분리됩니다.)`
- L503: `<div class="k-title">🟣 매출연동(R/S) 지원금 1회 검수</div>`
- L527: `<div class="card-title">약정금 마일스톤 및 매출연동(R/S) 지원금 약정 검수 큐</div>`
- L922: `// Gate B: 매출연동(REVENUE_SHARE) 지원금 필수값`
- L1096: `lor:var(--purple); font-size:12.5px;">🟣 매출연동(REVENUE_SHARE) 지원금 약정 체결 1회 필수값 검증</strong>`
- L1150: `<span><strong>[Gate B] 매출연동(R/S) 지원금 필수값 · 약정 대상(≥1건)</strong><br>${g.gateBMsg}</span>`

## ADMN-INST-002 · "매출연동<"
0건

## ADMN-INST-002 · "매출연동 ("
- L480: `_ADD</code>) 이관 검수와, <strong>매출연동(<code>매출연동 (REVENUE_SHARE)</code>) 개발지원금 약정 체결 시 최초 1회 검수</strong>만 수행합니다. (매출연동형의 월별 지급분은 자동 연산되므로 매월 검수하지 않으며, 사입 도서 매입채무(AP)는 회계 시스템 경로로 분리됩니다.)`

## ADMN-LOGIN-001 · "보안 감사 로그"
- L241: `<div>• 모든 로그인 성공 · 실패 · 잠금 이력은 보안 감사 로그(<strong>ADMN-CONF-010</strong>)에 자동 기록됩니다.</div>`

## ADMN-ORD-001 · "인세 도서"
- L1132: `-size:11px;color:var(--text-muted);">도서 인세 도서 인세 (+1권)</span>`

## ADMN-ORD-001 · "수강권 직권부여"
- L1756: `문 유형: <b class="mono">DIRECT_GRANT</b> (수강권 직권부여 · 구 ADMN-ORD-003 통합)<br>`

## ADMN-PROD-003 · "권리자 계약 원장"
- L1000: `<div class="field-hint">ADMN-INST-001(권리자 계약 원장)에 등록된 강사 마스터와 연동됩니다.</div>`

## ADMN-PROD-004 · "도서 공급 원장 연결"
- L1214: `<th>도서 공급 원장 연결<br>(ADMN-BOOK-001)</th>`

## ADMN-PROD-004 · "예약판매 설정"
- L1245: `<th>예약판매 설정<br>(<code>is_preorder</code>)</th>`

## ADMN-PROD-005 · "정산 차감 정책 설정"
- L1155: `color:var(--violet);">5. 합격 환급반 달성 조건 및 정산 차감 정책 설정 (ADMN-SETT-006 연동)</h3>`

## ADMN-PROD-007 · "일반 상품 판매매출"
- L336: `(--text-main);">일반 상품 마스터 (공급 형태 · 재고 · 일반 상품 판매매출 일반상품 매출)</strong>`
- L358: `g>자사 권리자 100%로 자동 매핑</strong>되어 <strong>일반 상품 판매매출(<code>일반상품 매출</code>)</strong>로 집계되며, 매입 대금은 정산 엔진(펌뱅킹)을 거치지 않고 <strong>회계 매입채무(AP · <code>INVENTORY_PURCHASE</code>)</strong> 경로로 지급됩니다.`
- L386: `class="k-top"><span class="k-title">당월 일반 상품 판매매출</span><span class="badge badge-purple">일반상품 매출</span></div>`
- L540: `px;">외부 권리자 수익 배분 검증 면제 · 매출 전액 <strong>일반 상품 판매매출</strong>로 집계 (매핑 유효기간 외에는 신규 판매 자동 차단)</span>`
- L933: `.textContent = '일반 상품 마스터 (공급 형태 · 재고 · 일반 상품 판매매출)';`

## ADMN-SETT-002 · "온라인 강좌 수익배분"
- L1075: `<option value="P1_1">온라인 강좌 수익배분 (강좌 수익배분)</option>`
- L2264: `pipeline: "Pipeline 1.1 (온라인 강좌 수익배분)",`
- L2936: `// [B] 온라인 강좌 수익배분`
- L2942: `<div class="s1-card-title">🎓 [테이블 B] 온라인 강좌 수익배분 산출 명세 (강좌 수익배분)</div>`

## ADMN-SETT-002 · "자사 발행 도서 인세"
- L1076: `<option value="P2_1">자사 발행 도서 인세 (도서 인세)</option>`
- L2285: `pipeline: "Pipeline 2.1 (자사 발행 도서 인세)",`

## ADMN-SETT-002 · "위탁 도서 판매대금 정산"
- L1077: `<option value="P2_2">위탁 도서 판매대금 정산 (위탁도서 정산)</option>`
- L1487: `pipelineText: "위탁 도서 판매대금 정산 (수수료 차감지급)",`

## ADMN-SETT-002 · "지원금 종료 일시정산"
- L1455: `pipelineText: "강좌(1.1) + 지원금 종료 일시정산(LUMP_SETTLE, 7단계)",`

## ADMN-SETT-002 · "매출연동 개발지원금 단독"
- L1520: `pipelineText: "매출연동 개발지원금 단독 (Pipeline 5.1 · 무한도형)",`

## ADMN-SETT-004 · "매입 재판매 도서"
- L543: `매입 재판매 도서(<code>매입 재판매 도서 (PURCHASED_RESALE)</code>) 및 사은품(<code>강좌 부속·사은품 (BUNDLED)</code>), 배송비(<code>SHIPPING_FEE</code>)는 정산 엔진 비인입 대상이므로 <strong>정산서 총액과 전사 결제 매출 총액`

## ADMN-SETT-009 · "온라인 강좌 수익배분"
- L352: `<option value="P1_1">온라인 강좌 수익배분 (강좌 수익배분)</option>`
- L661: `pipeName: "온라인 강좌 수익배분",`
- L680: `pipeName: "온라인 강좌 수익배분",`
- L699: `pipeName: "온라인 강좌 수익배분",`

## ADMN-SETT-009 · "자사 발행 도서 인세"
- L353: `<option value="P2_1">자사 발행 도서 인세 및 자사저작권 (도서 인세)</option>`
- L718: `pipeName: "자사 발행 도서 인세",`

## ADMN-SETT-009 · "위탁 도서 판매대금 정산"
- L354: `<option value="P2_2">위탁 도서 판매대금 정산 (위탁도서 정산)</option>`
- L756: `pipeName: "위탁 도서 판매대금 정산",`

## ADMN-SETT-009 · "일반 상품 판매매출"
- L300: `al = true</code>) 귀속분</strong>과 <strong>일반 상품 판매매출(일반상품 매출, <code>TX-13</code>)</strong>을 외부 권리자 지급액과 함께 대조하는 <strong>조회 전용(View-only)</strong> 화면입니다. 자사 귀속 라인은 펌뱅킹 이체 리스트 및 전자(세금)계산서 역발행 루프에서 <strong>자동 제외(Byp`
- L355: `<option value="P2_3">일반 상품 판매매출 (일반상품 매출 · 소비재)</option>`
- L491: `<h3>📦 일반 상품 판매매출(일반상품 매출 · TX-13) 및 매입 재판매 도서(Case 11) 내부 집계</h3>`
- L496: `tem_type = GOODS_ITEM</code>)</strong>는 일반 상품 판매매출로 인입하여 1단계 상위 공식에서 <strong>공급가액과 부가가치세(10%, 총액 역산)를 분리 산출</strong>하고 9단계에서 <strong>일반 과세 재화 공급(TX-13)</strong>을 부여합니다. 원천징수 산식은 호출하지 않으며 외부 지급액 0원으로 자사 마감 집계만 수`
- L516: `<td><span class="badge b-teal">일반 상품 판매매출 (일반상품 매출)</span></td>`
- L528: `<td><span class="badge b-teal">일반 상품 판매매출 (일반상품 매출)</span></td>`
- (외 1건 생략)

## ADMN-SETT-009 · "원천징수 사건 성립"
- L588: `<code>taxable_base IS NOT NULL</code> 및 원천징수 사건 성립(<code>payment_event_date IS NOT NULL</code>) 확정 라인만 집계. 지급 하한 미달 보류(<code>PRE_TAX</code>), 보류 음수(<code>pending_negative_base</code>), 재화 공급(<code>TX-11·12·13</`

## ADMN-USER-007 · "정산 감사로그"
0건
