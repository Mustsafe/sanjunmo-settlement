# WORKFLOW FINAL CHECK

[A. 검수 범위]

### 1. scripts/qa/skill_playwright_e2e.py 에서 검수 대상 폴더(경로)를 정하는 줄 전부 (줄 번호 + 원문)
- scripts/qa/skill_playwright_e2e.py:5: - prototype_clean/ 38개 전체 화면 브라우저 렌더링 검수
- scripts/qa/skill_playwright_e2e.py:18: CLEAN_DIR = Path("prototype_clean").resolve()
- scripts/qa/skill_playwright_e2e.py:105:     files = sorted(CLEAN_DIR.glob("*.html"))
- scripts/qa/skill_playwright_e2e.py:118:         f"- 검수 대상: `prototype_clean/*.html` ({len(results)}개 화면)",

### 2. 직전 검수 실행에서 실제로 열린 화면 목록 (폴더명/파일명), 폴더별 개수
#### 실제로 열린 화면 목록
- prototype_clean/00_WORKFLOW_GUIDE_baseline.html
- prototype_clean/ADMN-BOOK-001_baseline.html
- prototype_clean/ADMN-BRD-001_baseline.html
- prototype_clean/ADMN-BRD-002_baseline.html
- prototype_clean/ADMN-BRD-005_baseline.html
- prototype_clean/ADMN-CONF-001_baseline.html
- prototype_clean/ADMN-CONF-002_baseline.html
- prototype_clean/ADMN-CONF-003_baseline.html
- prototype_clean/ADMN-CONF-004_baseline.html
- prototype_clean/ADMN-CONF-005_baseline.html
- prototype_clean/ADMN-CONF-010_baseline.html
- prototype_clean/ADMN-DASH-001_baseline.html
- prototype_clean/ADMN-INST-001_baseline.html
- prototype_clean/ADMN-INST-002_baseline.html
- prototype_clean/ADMN-LOGIN-001_baseline.html
- prototype_clean/ADMN-ORD-001_baseline.html
- prototype_clean/ADMN-PROD-001_baseline.html
- prototype_clean/ADMN-PROD-002_baseline.html
- prototype_clean/ADMN-PROD-003_baseline.html
- prototype_clean/ADMN-PROD-004_baseline.html
- prototype_clean/ADMN-PROD-005_baseline.html
- prototype_clean/ADMN-PROD-006_baseline.html
- prototype_clean/ADMN-PROD-007_baseline.html
- prototype_clean/ADMN-PROM-001_baseline.html
- prototype_clean/ADMN-PROM-002_baseline.html
- prototype_clean/ADMN-RFD-002_baseline.html
- prototype_clean/ADMN-SETT-001_baseline.html
- prototype_clean/ADMN-SETT-002_baseline.html
- prototype_clean/ADMN-SETT-004_baseline.html
- prototype_clean/ADMN-SETT-005_baseline.html
- prototype_clean/ADMN-SETT-006_baseline.html
- prototype_clean/ADMN-SETT-007_baseline.html
- prototype_clean/ADMN-SETT-008_baseline.html
- prototype_clean/ADMN-SETT-009_baseline.html
- prototype_clean/ADMN-SETT-011_baseline.html
- prototype_clean/ADMN-USER-001_baseline.html
- prototype_clean/ADMN-USER-007_baseline.html
- prototype_clean/patch_all_snb_v3.html

#### 폴더별 개수
- prototype_clean: 38개
- prototype: 0개

[B. prototype/ 업무플로우 렌더링]

### 3. Playwright 1440px prototype/00_WORKFLOW_GUIDE_baseline.html 렌더링 결과
#### 3-1. 상단 브레드크럼 crumb-group 텍스트
대시보드 · 통계

#### 3-2. #wf-dir-grid 카드별 [h4 텍스트 | 링크 개수], 링크 개수 합계
- [대시보드 · 통계 | 3]
- [회원 · 수강 관리 | 4]
- [주문 · 환불 · CS · 프로모션 | 8]
- [상품 · 강좌 · 교재 관리 | 7]
- [권리자 계약 · 지분 매핑 | 4]
- [정산 마감 전 사전 대사 | 4]
- [월간 정산 · 지급 · 조회 | 4]
- [개인정보 · 보안 감사 | 2]
- [사이트 · 약관 · 메시지 설정 | 6]
- 링크 개수 합계: 42개

#### 3-3. 브라우저 콘솔 에러 전부
0건

### 4. Playwright 1440px prototype/ADMN-SETT-002_baseline.html SNB 그룹 제목 9개 텍스트 및 메뉴 항목 개수
#### SNB 그룹 제목 9개 텍스트
1. 대시보드 · 통계
2. 회원 · 수강 관리
3. 주문 · 환불 · CS · 프로모션
4. 상품 · 강좌 · 교재 관리
5. 권리자 계약 · 지분 매핑
6. 정산 마감 전 사전 대사
7. 월간 정산 · 지급 · 조회
8. 개인정보 · 보안 감사
9. 사이트 · 약관 · 메시지 설정

#### 메뉴 항목 개수
43개

### 5. 캡처 이미지 경로 및 픽셀 크기
- .antigravity/reports/screens/final_proto_wf_top.png: 1440×900px
- .antigravity/reports/screens/final_proto_dir.png: 1116×841px

[C. 정답지 정리 사전 조회]

### 6. ADMN-BRD-005_baseline.html 에서 "정답지" 또는 "ANSWER_SHEET" 또는 "BRD-009" 가 들어간 모든 줄 (줄 번호 + 원문)

#### prototype_clean/ADMN-BRD-005_baseline.html
12:   <title>수강후기·합격수기·무료특강(빈출문제)·정답지 관리 — 산준모 백오피스</title>
714:         <h1 id="current-screen-title">수강후기·합격수기 분리 관리 및 무료특강(빈출문제)·정답지</h1>
716:         <p>수강후기(진도율/별점)와 합격수기(자격증 합격증빙 검수)를 분리 운영하고, 무료특강/빈출문제 및 정답지(웹 에디터)를 관리합니다.</p>
752:         📘 정답지 관리 (ADMN-BRD-009) <span class="cnt" id="cnt-errata">4</span>
1016:     <!-- ==================== 4. 정답지 관리 (ADMN-BRD-009) ==================== -->
1019:         <strong>[ADMN-BRD-009] 정답지 관리 (웹 에디터 적용):</strong> 수험서 교재별 <strong>[정답지 및 상세 해설 (<code>ANSWER_SHEET</code>)]</strong>을 관리합니다. 등록/수정 시 <strong>리치 웹 에디터(문항별 정답표/해설/수식/이미지 본문 작성 및 HTML 편집)</strong>와 첨부파일(PDF/HWP) 업로드를 지원하며, 연결된 교재 상세(<code>USER-BOOK-002</code>) 및 학습지원센터에 즉시 노출됩니다.
1031:             <input type="text" id="er-keyword" placeholder="연결 교재명, 정답지 제목, 단원/회차 검색..." oninput="renderErrata()" style="width:280px;" />
1034:             <button class="btn btn-primary" onclick="openErrataModal()">+ 정답지 등록 (웹 에디터)</button>
1043:               <th style="width:100px;">정답지 번호</th>
1047:               <th>정답지 제목 (웹 에디터 본문 포함)</th>
1250: <!-- ==================== 모달 C: 정답지 등록/수정 (ADMN-BRD-009 웹 에디터) ==================== -->
1254:       <h3 id="er-modal-title">[ADMN-BRD-009] 정답지 등록 및 수정 (웹 에디터)</h3>
1282:           <label class="form-label">정답지 첨부파일 (PDF / HWP 다운로드용)</label>
1283:           <input type="text" id="er-form-file" placeholder="예: 2026_산안기_필기_정답지_전문.pdf" />
1286:           <label class="form-label">정답지 제목 *</label>
1287:           <input type="text" id="er-form-title" placeholder="예: [정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설" />
1290:           <label class="form-label">정답지 상세 본문 (웹 에디터 — 문항별 정답표/해설/수식/HTML 편집 지원) *</label>
1307:       <button class="btn btn-primary" onclick="saveErrata()">정답지 저장</button>
1368:   // 4. 정답지 (ADMN-BRD-009) - 웹 에디터 본문 포함
1375:       title: '[정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설',
1376:       file: '2026_산안기_필기_정답지_전문.pdf',
1385:       title: '[정답지] 2026 산업안전기사 실기 필답형+작업형 모범답안 및 채점 키워드 정답지',
1386:       file: '2026_산안기_실기_모범답안_정답지.pdf',
1395:       title: '[정답지] 2026 건설안전기사 필기 빈출문제집 실전모의고사 빠른 정답표 및 해설',
1396:       file: '2026_건안기_빈출문제집_정답지.pdf',
1405:       title: '[정답지] 2026 위험물산업기사 핵심노트 단원별 확인문제 정답 및 화학반응식 풀이',
1406:       file: '2026_위험물_단원평가_정답지.pdf',
1446:       errata: ['ADMN-BRD-009', '정답지 관리 (웹 에디터)'],
1676:         <p style="margin:0; color:var(--text-sub); line-height:1.6;">산준모 정규 커리큘럼과 빈출문제 무료특강, 정답지 해설을 반복 회독하여 비전공자임에도 동차 합격할 수 있었습니다.</p>
1848:   // 4. 정답지 (ADMN-BRD-009)
1880:       ? `[ADMN-BRD-009] 정답지 수정 (${item.id})`
1881:       : '[ADMN-BRD-009] 정답지 신규 등록 (웹 에디터)';
1885:     document.getElementById('er-form-file').value = item ? item.file : '2026_산안기_정답지_및_해설.pdf';
1951:     if (!title) { alert('정답지 제목을 입력해주세요.'); return; }
1964:     showToast('정답지가 저장되어 교재 상세 페이지 및 학습지원센터에 반영되었습니다.');

#### prototype/ADMN-BRD-005_baseline.html
12:   <title>[ADMN-BRD-005] 수강후기·합격수기·무료특강(빈출문제)·정답지 관리 — 산준모 백오피스</title>
714:         <h1 id="current-screen-title">수강후기·합격수기 분리 관리 및 무료특강(빈출문제)·정답지</h1>
716:         <p>수강후기(진도율/별점)와 합격수기(자격증 합격증빙 검수)를 분리 운영하고, 무료특강/빈출문제 및 정답지(웹 에디터)를 관리합니다.</p>
752:         📘 정답지 관리 (ADMN-BRD-009) <span class="cnt" id="cnt-errata">4</span>
1016:     <!-- ==================== 4. 정답지 관리 (ADMN-BRD-009) ==================== -->
1019:         <strong>[ADMN-BRD-009] 정답지 관리 (웹 에디터 적용):</strong> 수험서 교재별 <strong>[정답지 및 상세 해설 (<code>ANSWER_SHEET</code>)]</strong>을 관리합니다. 등록/수정 시 <strong>리치 웹 에디터(문항별 정답표/해설/수식/이미지 본문 작성 및 HTML 편집)</strong>와 첨부파일(PDF/HWP) 업로드를 지원하며, 연결된 교재 상세(<code>USER-BOOK-002</code>) 및 학습지원센터에 즉시 노출됩니다.
1031:             <input type="text" id="er-keyword" placeholder="연결 교재명, 정답지 제목, 단원/회차 검색..." oninput="renderErrata()" style="width:280px;" />
1034:             <button class="btn btn-primary" onclick="openErrataModal()">+ 정답지 등록 (웹 에디터)</button>
1043:               <th style="width:100px;">정답지 번호</th>
1047:               <th>정답지 제목 (웹 에디터 본문 포함)</th>
1250: <!-- ==================== 모달 C: 정답지 등록/수정 (ADMN-BRD-009 웹 에디터) ==================== -->
1254:       <h3 id="er-modal-title">[ADMN-BRD-009] 정답지 등록 및 수정 (웹 에디터)</h3>
1282:           <label class="form-label">정답지 첨부파일 (PDF / HWP 다운로드용)</label>
1283:           <input type="text" id="er-form-file" placeholder="예: 2026_산안기_필기_정답지_전문.pdf" />
1286:           <label class="form-label">정답지 제목 *</label>
1287:           <input type="text" id="er-form-title" placeholder="예: [정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설" />
1290:           <label class="form-label">정답지 상세 본문 (웹 에디터 — 문항별 정답표/해설/수식/HTML 편집 지원) *</label>
1307:       <button class="btn btn-primary" onclick="saveErrata()">정답지 저장</button>
1368:   // 4. 정답지 (ADMN-BRD-009) - 웹 에디터 본문 포함
1375:       title: '[정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설',
1376:       file: '2026_산안기_필기_정답지_전문.pdf',
1385:       title: '[정답지] 2026 산업안전기사 실기 필답형+작업형 모범답안 및 채점 키워드 정답지',
1386:       file: '2026_산안기_실기_모범답안_정답지.pdf',
1395:       title: '[정답지] 2026 건설안전기사 필기 빈출문제집 실전모의고사 빠른 정답표 및 해설',
1396:       file: '2026_건안기_빈출문제집_정답지.pdf',
1405:       title: '[정답지] 2026 위험물산업기사 핵심노트 단원별 확인문제 정답 및 화학반응식 풀이',
1406:       file: '2026_위험물_단원평가_정답지.pdf',
1446:       errata: ['ADMN-BRD-009', '정답지 관리 (웹 에디터)'],
1676:         <p style="margin:0; color:var(--text-sub); line-height:1.6;">산준모 정규 커리큘럼과 빈출문제 무료특강, 정답지 해설을 반복 회독하여 비전공자임에도 동차 합격할 수 있었습니다.</p>
1848:   // 4. 정답지 (ADMN-BRD-009)
1880:       ? `[ADMN-BRD-009] 정답지 수정 (${item.id})`
1881:       : '[ADMN-BRD-009] 정답지 신규 등록 (웹 에디터)';
1885:     document.getElementById('er-form-file').value = item ? item.file : '2026_산안기_정답지_및_해설.pdf';
1951:     if (!title) { alert('정답지 제목을 입력해주세요.'); return; }
1964:     showToast('정답지가 저장되어 교재 상세 페이지 및 학습지원센터에 반영되었습니다.');

### 7. ADMN-BRD-005_baseline.html 탭 버튼 정의 줄 전부 및 탭 전환 함수 (이름과 시작 줄 번호)

#### prototype_clean/ADMN-BRD-005_baseline.html
##### 탭 버튼 정의 줄 전부
732:       <button class="sub-tab-btn active" onclick="switchTab('courseReview')" id="tab-btn-courseReview">
738:       <button class="sub-tab-btn" onclick="switchTab('passEssay')" id="tab-btn-passEssay">
744:       <button class="sub-tab-btn" onclick="switchTab('freeLecture')" id="tab-btn-freeLecture">
750:       <button class="sub-tab-btn" onclick="switchTab('errata')" id="tab-btn-errata">
756:       <button class="sub-tab-btn" onclick="switchTab('report')" id="tab-btn-report">

##### 탭 전환 함수
- 함수명: switchTab, 시작 줄 번호: 1426

#### prototype/ADMN-BRD-005_baseline.html
##### 탭 버튼 정의 줄 전부
732:       <button class="sub-tab-btn active" onclick="switchTab('courseReview')" id="tab-btn-courseReview">
738:       <button class="sub-tab-btn" onclick="switchTab('passEssay')" id="tab-btn-passEssay">
744:       <button class="sub-tab-btn" onclick="switchTab('freeLecture')" id="tab-btn-freeLecture">
750:       <button class="sub-tab-btn" onclick="switchTab('errata')" id="tab-btn-errata">
756:       <button class="sub-tab-btn" onclick="switchTab('report')" id="tab-btn-report">

##### 탭 전환 함수
- 함수명: switchTab, 시작 줄 번호: 1426

### 8. ADMN-CONF-005_baseline.html 에서 "정답지" 또는 "BRD-009" 가 들어간 모든 줄 (줄 번호 + 원문)

#### prototype_clean/ADMN-CONF-005_baseline.html
354:           <p>• <strong>접근 허용:</strong> 본인 저작 도서 판매량·인세(Royalty) 정산내역서 조회, 정답지(<code>ADMN-BRD-009</code>) 등록·수정<br/>• <strong>데이터 스코프:</strong> 바인딩된 저작권 계약코드(<code>CR-*</code> / <code>BOOK-*</code>)에 한정한 열람 허용</p>
471:               <td style="font-weight:700;">학습 Q&amp;A / 정답지 (BRD)</td>
477:               <td><strong>✓ 본인 정답지 등록</strong></td>
532:             <option value="ROLE_PARTNER_COPYRIGHT">[외부 파트너] 교재 저작권자/출판사 (ROLE_PARTNER_COPYRIGHT — 도서 인세 정산서 및 정답지 관리)</option>
569:     { id: 'copy_sanjunbook', name: '한출판 대표 (산준모북스 저작권자)', role: 'ROLE_PARTNER_COPYRIGHT', scope: 'CR-2026-002 / BK-2026-101 (본인 저작 도서 인세 정산서 ADMN-SETT-002-S2 및 정답지 ADMN-BRD-009 전용)', sec: '2FA 모바일 인증', lastLogin: '2026-10-18 16:30', status: 'ACTIVE' },
576:     { id: 'AUD-9919', dt: '2026-10-18 16:35', actor: 'copy_sanjunbook (저작권자)', type: '정답지 등록', detail: '[BK-2026-101 / BOOK-2601] 산업안전기사 필기 한권완성 정답지(ANSWER_SHEET) 웹 에디터 수정', ip: '58.120.89.11' },
640:       scopeInp.value = 'CR-2026-004 / BOOK-2605 (본인 저작 도서 인세 정산서 및 정답지 관리 전용)';

#### prototype/ADMN-CONF-005_baseline.html
354:           <p>• <strong>접근 허용:</strong> 본인 저작 도서 판매량·인세(Royalty) 정산내역서 조회, 정답지(<code>ADMN-BRD-009</code>) 등록·수정<br/>• <strong>데이터 스코프:</strong> 바인딩된 저작권 계약코드(<code>CR-*</code> / <code>BOOK-*</code>)에 한정한 열람 허용</p>
471:               <td style="font-weight:700;">학습 Q&amp;A / 정답지 (BRD)</td>
477:               <td><strong>✓ 본인 정답지 등록</strong></td>
532:             <option value="ROLE_PARTNER_COPYRIGHT">[외부 파트너] 교재 저작권자/출판사 (ROLE_PARTNER_COPYRIGHT — 도서 인세 정산서 및 정답지 관리)</option>
569:     { id: 'copy_sanjunbook', name: '한출판 대표 (산준모북스 저작권자)', role: 'ROLE_PARTNER_COPYRIGHT', scope: 'CR-2026-002 / BK-2026-101 (본인 저작 도서 인세 정산서 ADMN-SETT-002-S2 및 정답지 ADMN-BRD-009 전용)', sec: '2FA 모바일 인증', lastLogin: '2026-10-18 16:30', status: 'ACTIVE' },
576:     { id: 'AUD-9919', dt: '2026-10-18 16:35', actor: 'copy_sanjunbook (저작권자)', type: '정답지 등록', detail: '[BK-2026-101 / BOOK-2601] 산업안전기사 필기 한권완성 정답지(ANSWER_SHEET) 웹 에디터 수정', ip: '58.120.89.11' },
640:       scopeInp.value = 'CR-2026-004 / BOOK-2605 (본인 저작 도서 인세 정산서 및 정답지 관리 전용)';

### 9. prototype_clean/common-snb.js 의 TEXT_REPLACEMENTS · EXTRA_MAP 안에서 "정답지" 또는 "BRD-009" 또는 "ANSWER_SHEET" 가 들어간 줄 (줄 번호 + 원문)
#### TEXT_REPLACEMENTS (L171 ~ L351)
204:     ["정답지 및 상세 해설 (ANSWER_SHEET)", "정답지 및 상세 해설"],
296:     ["ADMN-BRD-005", "후기·무료특강·정답지"],
297:     ["ADMN-BRD-009", "정답지 관리"],

#### EXTRA_MAP (L437 ~ L627)
507:   "ANSWER_SHEET": "정답지",

### 10. docs/ 전체 .md 에서 "ANSWER_SHEET" 가 들어간 줄 (파일명 + 줄 번호 + 원문, 최대 40줄)
0건

[D. 옛 단계명 잔재]

### 11. prototype/ · prototype_clean/ 의 *.html 에서 groupTitle 이 들어간 줄 전부 (파일명 + 줄 번호 + 원문)

#### prototype/ADMN-BOOK-001_baseline.html
1348:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1354:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1366:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1375:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1384:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1392:         groupTitle: "4단계 · 보안 및 감사 통제",
1406:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype/ADMN-PROD-003_baseline.html
1338:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1344:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1356:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1365:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1374:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1382:         groupTitle: "4단계 · 보안 및 감사 통제",
1396:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype/ADMN-PROD-004_baseline.html
1526:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1532:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1544:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1553:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1562:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1570:         groupTitle: "4단계 · 보안 및 감사 통제",
1584:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype/ADMN-PROD-005_baseline.html
1283:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1289:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1301:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1310:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1319:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1327:         groupTitle: "4단계 · 보안 및 감사 통제",
1341:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype/ADMN-PROD-006_baseline.html
986:         groupTitle: "0단계 · 전체 업무 플로우 안내",
992:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1004:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1013:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1022:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1030:         groupTitle: "4단계 · 보안 및 감사 통제",
1044:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype/patch_all_snb_v3.html
232:     groupTitle: "0단계 · 전체 업무 플로우 안내",
238:     groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
250:     groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
259:     groupTitle: "2단계 · 월마감 전 검증 (Gate)",
268:     groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
276:     groupTitle: "4단계 · 보안 및 감사 통제",
287:     SCREEN_META_MAP[it.code] = { ...it, groupTitle: g.groupTitle };
307:         <div class="snb-group-title">${grp.groupTitle}</div>
949:       <span class="crumb-group">${meta.groupTitle}</span>

#### prototype_clean/ADMN-BOOK-001_baseline.html
1348:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1354:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1366:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1375:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1384:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1392:         groupTitle: "4단계 · 보안 및 감사 통제",
1406:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype_clean/ADMN-PROD-003_baseline.html
1338:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1344:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1356:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1365:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1374:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1382:         groupTitle: "4단계 · 보안 및 감사 통제",
1396:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype_clean/ADMN-PROD-004_baseline.html
1526:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1532:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1544:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1553:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1562:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1570:         groupTitle: "4단계 · 보안 및 감사 통제",
1584:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype_clean/ADMN-PROD-005_baseline.html
1283:         groupTitle: "0단계 · 전체 업무 플로우 안내",
1289:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1301:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1310:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1319:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1327:         groupTitle: "4단계 · 보안 및 감사 통제",
1341:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype_clean/ADMN-PROD-006_baseline.html
986:         groupTitle: "0단계 · 전체 업무 플로우 안내",
992:         groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
1004:         groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
1013:         groupTitle: "2단계 · 월마감 전 검증 (Gate)",
1022:         groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
1030:         groupTitle: "4단계 · 보안 및 감사 통제",
1044:           <div class="snb-group-title">${g.groupTitle}</div>

#### prototype_clean/patch_all_snb_v3.html
232:     groupTitle: "0단계 · 전체 업무 플로우 안내",
238:     groupTitle: "상품 · 강좌 · 교재 관리 (PROD)",
250:     groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",
259:     groupTitle: "2단계 · 월마감 전 검증 (Gate)",
268:     groupTitle: "3단계 · 월간 정산 · 집행 · 조회",
276:     groupTitle: "4단계 · 보안 및 감사 통제",
287:     SCREEN_META_MAP[it.code] = { ...it, groupTitle: g.groupTitle };
307:         <div class="snb-group-title">${grp.groupTitle}</div>
949:       <span class="crumb-group">${meta.groupTitle}</span>

### 12. 11번이 나온 파일 각각에서 그 groupTitle 정의를 실제로 읽어 쓰는 코드가 있는지: 해당 변수/배열 이름이 정의 줄 말고 다른 곳에서 참조되는 줄 전부

#### prototype/ADMN-BOOK-001_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1406: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1404: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1402: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L1837: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype/ADMN-PROD-003_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1396: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1394: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1392: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2246: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype/ADMN-PROD-004_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1584: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1582: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1580: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2253: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype/ADMN-PROD-005_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1341: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1339: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1337: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2031: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype/ADMN-PROD-006_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1044: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1042: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1040: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L1433: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype/patch_all_snb_v3.html
- 정의 변수: `SNB_NAV_DATA` (L230), `SCREEN_META_MAP` (L226)
- `groupTitle` 참조 줄:
  - L287: SCREEN_META_MAP[it.code] = { ...it, groupTitle: g.groupTitle };
  - L307: <div class="snb-group-title">${grp.groupTitle}</div>
  - L949: <span class="crumb-group">${meta.groupTitle}</span>
- 변수 `SNB_NAV_DATA` 참조 줄:
- 실행 분석: 오프라인 HTML 일괄 패치 도구 UI로 브라우저에서 실행 시 patchAllScreens()를 통해 사용되나, 백오피스 서비스 런타임 화면은 아님.

#### prototype_clean/ADMN-BOOK-001_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1406: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1404: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1402: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L1837: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype_clean/ADMN-PROD-003_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1396: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1394: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1392: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2246: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype_clean/ADMN-PROD-004_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1584: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1582: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1580: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2253: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype_clean/ADMN-PROD-005_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1341: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1339: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1337: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L2031: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype_clean/ADMN-PROD-006_baseline.html
- 정의 변수: `MASTER_NAV_GROUPS` (L1346 등)
- `groupTitle` 참조 줄:
  - L1044: <div class="snb-group-title">${g.groupTitle}</div>
- 변수 `MASTER_NAV_GROUPS` 참조 줄:
  - L1042: container.innerHTML = MASTER_NAV_GROUPS.map(g => `
- `renderMasterSnb` 함수 정의 및 호출 줄:
  - L1040: function renderMasterSnb() { if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;
  - L1433: renderMasterSnb();
- 실행 분석: `renderMasterSnb()` 함수의 첫 머리에 `if (true) return; if (true) return; if (true) return; if (true) return; if (true) return;` 가 하드코딩되어 있어, 호출되더라도 1행에서 즉시 탈출(return)하므로 `MASTER_NAV_GROUPS` 및 `groupTitle`은 런타임에 일체 렌더링되거나 실행되지 않는 사장된 코드(Dead Code)임. 실제 사이드바는 `common-snb.js`의 `SNB_GROUPS`가 전담 렌더링함.

#### prototype_clean/patch_all_snb_v3.html
- 정의 변수: `SNB_NAV_DATA` (L230), `SCREEN_META_MAP` (L226)
- `groupTitle` 참조 줄:
  - L287: SCREEN_META_MAP[it.code] = { ...it, groupTitle: g.groupTitle };
  - L307: <div class="snb-group-title">${grp.groupTitle}</div>
  - L949: <span class="crumb-group">${meta.groupTitle}</span>
- 변수 `SNB_NAV_DATA` 참조 줄:
- 실행 분석: 오프라인 HTML 일괄 패치 도구 UI로 브라우저에서 실행 시 patchAllScreens()를 통해 사용되나, 백오피스 서비스 런타임 화면은 아님.
