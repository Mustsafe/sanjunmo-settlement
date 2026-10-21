# ANSWERSHEET SRC 01

## 1. prototype_clean/ADMN-BRD-005_baseline.html 요청 구간 원문

### 1-1. L705~760 (제목 · 탭 버튼)
705: 
706:   <div id="v4-page-body">
707: 
708:     <div class="page-header">
709: 
710:       <div class="page-title-wrap">
711: 
712:         <span class="code-badge" id="current-screen-code">ADMN-BRD-005</span>
713: 
714:         <h1 id="current-screen-title">수강후기·합격수기 분리 관리 및 무료특강(빈출문제)·정답지</h1>
715: 
716:         <p>수강후기(진도율/별점)와 합격수기(자격증 합격증빙 검수)를 분리 운영하고, 무료특강/빈출문제 및 정답지(웹 에디터)를 관리합니다.</p>
717: 
718:       </div>
719: 
720:       <div>
721: 
722:         <a href="ADMN-BRD-001_baseline.html" class="btn btn-outline">← 공지·FAQ·문의·당첨자 발표 (ADMN-BRD-001)</a>
723: 
724:       </div>
725: 
726:     </div>
727: 
728: 
729: 
730:     <div class="domain-switch-bar">
731: 
732:       <button class="sub-tab-btn active" onclick="switchTab('courseReview')" id="tab-btn-courseReview">
733: 
734:         ⭐ 수강후기 관리 (강좌/별점) <span class="cnt" id="cnt-courseReview">4</span>
735: 
736:       </button>
737: 
738:       <button class="sub-tab-btn" onclick="switchTab('passEssay')" id="tab-btn-passEssay">
739: 
740:         🎓 합격수기 검수 관리 (합격증빙/회차) <span class="cnt" id="cnt-passEssay">4</span>
741: 
742:       </button>
743: 
744:       <button class="sub-tab-btn" onclick="switchTab('freeLecture')" id="tab-btn-freeLecture">
745: 
746:         🎬 무료특강 및 빈출문제 (ADMN-BRD-006) <span class="cnt" id="cnt-freeLecture">4</span>
747: 
748:       </button>
749: 
750:       <button class="sub-tab-btn" onclick="switchTab('errata')" id="tab-btn-errata">
751: 
752:         📘 정답지 관리 (ADMN-BRD-009) <span class="cnt" id="cnt-errata">4</span>
753: 
754:       </button>
755: 
756:       <button class="sub-tab-btn" onclick="switchTab('report')" id="tab-btn-report">
757: 
758:         🚨 커뮤니티/신고 관리 (ADMN-BRD-007/008) <span class="cnt" id="cnt-report">3</span>
759: 
760:       </button>

### 1-2. L1010~1050 (정답지 섹션)
1010:       </div>
1011: 
1012:     </section>
1013: 
1014: 
1015: 
1016:     <!-- ==================== 4. 정답지 관리 (ADMN-BRD-009) ==================== -->
1017:     <section id="view-errata" class="view-section">
1018:       <div class="info-callout">
1019:         <strong>[ADMN-BRD-009] 정답지 관리 (웹 에디터 적용):</strong> 수험서 교재별 <strong>[정답지 및 상세 해설 (<code>ANSWER_SHEET</code>)]</strong>을 관리합니다. 등록/수정 시 <strong>리치 웹 에디터(문항별 정답표/해설/수식/이미지 본문 작성 및 HTML 편집)</strong>와 첨부파일(PDF/HWP) 업로드를 지원하며, 연결된 교재 상세(<code>USER-BOOK-002</code>) 및 학습지원센터에 즉시 노출됩니다.
1020:       </div>
1021: 
1022:       <div class="card">
1023:         <div class="filter-grid">
1024:           <div class="filter-left">
1025:             <select id="er-type-filter" onchange="renderErrata()">
1026:               <option value="ALL">자격증 종목 전체</option>
1027:               <option value="산업안전기사">산업안전기사</option>
1028:               <option value="건설안전기사">건설안전기사</option>
1029:               <option value="위험물산업기사">위험물산업기사</option>
1030:             </select>
1031:             <input type="text" id="er-keyword" placeholder="연결 교재명, 정답지 제목, 단원/회차 검색..." oninput="renderErrata()" style="width:280px;" />
1032:           </div>
1033:           <div class="filter-right">
1034:             <button class="btn btn-primary" onclick="openErrataModal()">+ 정답지 등록 (웹 에디터)</button>
1035:           </div>
1036:         </div>
1037:       </div>
1038: 
1039:       <div class="card" style="padding:0; overflow:hidden;">
1040:         <table class="data-table">
1041:           <thead>
1042:             <tr>
1043:               <th style="width:100px;">정답지 번호</th>
1044:               <th style="width:130px;">자격증 종목</th>
1045:               <th style="width:260px;">연결 교재 (ADMN-PROD-003)</th>
1046:               <th style="width:140px;">대상 판쇄 / 수록 범위</th>
1047:               <th>정답지 제목 (웹 에디터 본문 포함)</th>
1048:               <th style="width:180px;">첨부파일 (PDF/HWP)</th>
1049:               <th style="width:110px;">등록일</th>
1050:               <th style="width:130px;">관리</th>

### 1-3. 무료특강(freeLecture) 섹션 전체 (L922~1012)
922:     <!-- ==================== 3. 무료특강 및 빈출문제 (ADMN-BRD-006) ==================== -->
923: 
924:     <section id="view-freeLecture" class="view-section">
925: 
926:       <div class="info-callout">
927: 
928:         <strong>[ADMN-BRD-006] 무료특강 및 빈출문제 운영 정책:</strong> 사용자 웹 <code>USER-FREE-001 ~ 003</code>에 노출되는 무료 학습 콘텐츠입니다. 콘텐츠 구분은 <strong>[무료특강 영상 (<code>FREE_LECTURE</code>)]</strong>과 <strong>[빈출문제 해설 (<code>FREQ_EXAM</code>)]</strong>로 운영하며, 빈출문제 PDF 시험지/해설지 다운로드 및 플레이어 VOD 연동을 지원합니다.
929: 
930:       </div>
931: 
932: 
933: 
934:       <div class="card">
935: 
936:         <div class="filter-grid">
937: 
938:           <div class="filter-left">
939: 
940:             <select id="fl-type-filter" onchange="renderFreeLectures()">
941: 
942:               <option value="ALL">콘텐츠 구분 전체</option>
943: 
944:               <option value="FREE_LECTURE">무료특강 영상 (FREE_LECTURE)</option>
945: 
946:               <option value="FREQ_EXAM">빈출문제 해설 (FREQ_EXAM)</option>
947: 
948:             </select>
949: 
950:             <select id="fl-cert-filter" onchange="renderFreeLectures()">
951: 
952:               <option value="ALL">자격증 종목 전체</option>
953: 
954:               <option value="산업안전기사">산업안전기사</option>
955: 
956:               <option value="건설안전기사">건설안전기사</option>
957: 
958:               <option value="위험물산업기사">위험물산업기사</option>
959: 
960:             </select>
961: 
962:           </div>
963: 
964:           <div class="filter-right">
965: 
966:             <button class="btn btn-primary" onclick="openFreeLectureModal()">+ 무료특강 / 빈출문제 등록</button>
967: 
968:           </div>
969: 
970:         </div>
971: 
972:       </div>
973: 
974: 
975: 
976:       <div class="card" style="padding:0; overflow:hidden;">
977: 
978:         <table class="data-table">
979: 
980:           <thead>
981: 
982:             <tr>
983: 
984:               <th style="width:95px;">콘텐츠 ID</th>
985: 
986:               <th style="width:150px;">콘텐츠 구분</th>
987: 
988:               <th style="width:160px;">자격증 종목 / 대비연도</th>
989: 
990:               <th>제목</th>
991: 
992:               <th style="width:150px;">연동 VOD / 러닝타임</th>
993: 
994:               <th style="width:170px;">빈출문제/교안 PDF 첨부</th>
995: 
996:               <th style="width:95px;">조회수</th>
997: 
998:               <th style="width:100px;">노출상태</th>
999: 
1000:               <th style="width:130px;">관리</th>
1001: 
1002:             </tr>
1003: 
1004:           </thead>
1005: 
1006:           <tbody id="fl-tbody"></tbody>
1007: 
1008:         </table>
1009: 
1010:       </div>
1011: 
1012:     </section>

### 1-4. L1245~1310 (모달 C: 정답지 등록/수정)
1245: 
1246: </div>
1247: 
1248: 
1249: 
1250: <!-- ==================== 모달 C: 정답지 등록/수정 (ADMN-BRD-009 웹 에디터) ==================== -->
1251: <div class="modal-backdrop" id="modal-errata">
1252:   <div class="modal-box" style="max-width:920px;">
1253:     <div class="modal-header">
1254:       <h3 id="er-modal-title">[ADMN-BRD-009] 정답지 등록 및 수정 (웹 에디터)</h3>
1255:       <button class="btn btn-outline btn-sm" onclick="closeModal('modal-errata')">닫기 ✕</button>
1256:     </div>
1257:     <div class="modal-body">
1258:       <input type="hidden" id="er-edit-id" />
1259:       <div class="form-grid">
1260:         <div class="form-group">
1261:           <label class="form-label">자격증 종목 *</label>
1262:           <select id="er-form-type">
1263:             <option value="산업안전기사">산업안전기사</option>
1264:             <option value="건설안전기사">건설안전기사</option>
1265:             <option value="위험물산업기사">위험물산업기사</option>
1266:           </select>
1267:         </div>
1268:         <div class="form-group">
1269:           <label class="form-label">연결 대상 교재 선택 (ADMN-PROD-003) *</label>
1270:           <select id="er-form-book">
1271:             <option value="[BK-2026-101 / BOOK-2601] 2026 산준모 산업안전기사 필기 한권끝장">[BK-2026-101 / BOOK-2601] 2026 산준모 산업안전기사 필기 한권끝장</option>
1272:             <option value="[BOOK-2602] 2026 산준모 산업안전기사 실기 필답형+작업형">[BOOK-2602] 2026 산준모 산업안전기사 실기 필답형+작업형</option>
1273:             <option value="[BOOK-2603] 2026 산준모 건설안전기사 필기 빈출문제집">[BOOK-2603] 2026 산준모 건설안전기사 필기 빈출문제집</option>
1274:             <option value="[BOOK-2604] 2026 산준모 위험물산업기사 필기·실기 핵심노트">[BOOK-2604] 2026 산준모 위험물산업기사 필기·실기 핵심노트</option>
1275:           </select>
1276:         </div>
1277:         <div class="form-group">
1278:           <label class="form-label">대상 판쇄 / 수록 단원·회차 범위</label>
1279:           <input type="text" id="er-form-page" placeholder="예: 2026년판 / 전 단원 빈출문제 및 실전모의고사" />
1280:         </div>
1281:         <div class="form-group">
1282:           <label class="form-label">정답지 첨부파일 (PDF / HWP 다운로드용)</label>
1283:           <input type="text" id="er-form-file" placeholder="예: 2026_산안기_필기_정답지_전문.pdf" />
1284:         </div>
1285:         <div class="form-group full">
1286:           <label class="form-label">정답지 제목 *</label>
1287:           <input type="text" id="er-form-title" placeholder="예: [정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설" />
1288:         </div>
1289:         <div class="form-group full">
1290:           <label class="form-label">정답지 상세 본문 (웹 에디터 — 문항별 정답표/해설/수식/HTML 편집 지원) *</label>
1291:           <div class="rich-editor-shell">
1292:             <div class="rich-toolbar">
1293:               <button type="button" onclick="execCmd('er-form-body','bold')"><b>B 굵게</b></button>
1294:               <button type="button" onclick="execCmd('er-form-body','underline')"><u>U 밑줄</u></button>
1295:               <button type="button" onclick="insertAnswerTableTemplate()">📊 단원별 정답 및 해설표 삽입</button>
1296:               <button type="button" onclick="insertQuickAnswerGridTemplate()">🔢 빠른 정답표(1~20번 그리드) 삽입</button>
1297:               <button type="button" onclick="toggleErrataHtmlSource()">&lt;/&gt; HTML 소스 보기 전환</button>
1298:             </div>
1299:             <div id="er-form-body" class="rich-area" contenteditable="true"></div>
1300:             <textarea id="er-form-source" style="display:none; width:100%; min-height:200px; border:none; padding:12px; font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, 'Malgun Gothic', sans-serif; font-variant-numeric: tabular-nums; font-size:12px;"></textarea>
1301:           </div>
1302:         </div>
1303:       </div>
1304:     </div>
1305:     <div class="modal-footer">
1306:       <button class="btn btn-outline" onclick="closeModal('modal-errata')">취소</button>
1307:       <button class="btn btn-primary" onclick="saveErrata()">정답지 저장</button>
1308:     </div>
1309:   </div>
1310: </div>

### 1-5. L1365~1450 (더미데이터)
1365: 
1366: 
1367: 
1368:   // 4. 정답지 (ADMN-BRD-009) - 웹 에디터 본문 포함
1369:   let ERRATA_LIST = [
1370:     {
1371:       id: 'ANS-404',
1372:       type: '산업안전기사',
1373:       book: '[BK-2026-101 / BOOK-2601] 2026 산준모 산업안전기사 필기 한권끝장',
1374:       page: '2026년판 / 전 단원 빈출문제',
1375:       title: '[정답지] 2026 산업안전기사 필기 한권끝장 단원별 빈출문제 정답 및 상세해설',
1376:       file: '2026_산안기_필기_정답지_전문.pdf',
1377:       date: '2026-10-18',
1378:       body: `<table><thead><tr><th>단원</th><th>문항번호</th><th>정답</th><th>핵심 해설</th></tr></thead><tbody><tr><td>1과목 안전관리론</td><td>01번 ~ 05번</td><td>[3], [2], [4], [1], [3]</td><td>하인리히 법칙 1:29:300 비율 적용</td></tr><tr><td>2과목 인간공학</td><td>01번 ~ 05번</td><td>[2], [4], [1], [3], [2]</td><td>Fitts의 법칙 및 작업공간 배치 기준</td></tr></tbody></table>`
1379:     },
1380:     {
1381:       id: 'ANS-403',
1382:       type: '산업안전기사',
1383:       book: '[BOOK-2602] 2026 산준모 산업안전기사 실기 필답형+작업형',
1384:       page: '2026년판 / 실기 필답형 모의고사 1~10회',
1385:       title: '[정답지] 2026 산업안전기사 실기 필답형+작업형 모범답안 및 채점 키워드 정답지',
1386:       file: '2026_산안기_실기_모범답안_정답지.pdf',
1387:       date: '2026-10-15',
1388:       body: `<table><thead><tr><th>회차 / 문항</th><th>모범 정답 키워드</th><th>배점 및 부분점수 채점 기준</th></tr></thead><tbody><tr><td>제1회 04번</td><td>안전보건관리규정, 안전보건교육, 작업환경측정</td><td>3가지 모두 기재 시 4점 만점</td></tr><tr><td>제2회 07번</td><td>조도 기준 150 Lux 이상 (정밀작업 300 Lux)</td><td>단위(Lux) 누락 시 1점 감점</td></tr></tbody></table>`
1389:     },
1390:     {
1391:       id: 'ANS-402',
1392:       type: '건설안전기사',
1393:       book: '[BOOK-2603] 2026 산준모 건설안전기사 필기 빈출문제집',
1394:       page: '2026년판 / 실전모의고사 1~5회',
1395:       title: '[정답지] 2026 건설안전기사 필기 빈출문제집 실전모의고사 빠른 정답표 및 해설',
1396:       file: '2026_건안기_빈출문제집_정답지.pdf',
1397:       date: '2026-10-11',
1398:       body: `<p>실전모의고사 1회~5회 문항별 빠른 정답표 및 계산문제 상세 풀이입니다.</p>`
1399:     },
1400:     {
1401:       id: 'ANS-401',
1402:       type: '위험물산업기사',
1403:       book: '[BOOK-2604] 2026 산준모 위험물산업기사 필기·실기 핵심노트',
1404:       page: '2026년판 / 제1류~제6류 단원평가',
1405:       title: '[정답지] 2026 위험물산업기사 핵심노트 단원별 확인문제 정답 및 화학반응식 풀이',
1406:       file: '2026_위험물_단원평가_정답지.pdf',
1407:       date: '2026-10-08',
1408:       body: `<p>제1류~제6류 위험물 화학반응식 계수 맞추기 및 소화약제 정답 해설지입니다.</p>`
1409:     }
1410:   ];
1411: 
1412:   // 5. 신고 관리
1413: 
1414:   let REPORT_LIST = [
1415: 
1416:     { id: 'RPT-103', reason: '불법 강의 공유/양도 시도', content: '산준모 산업안전기사 실기 패스 계정 반값에 공유하실 분 구합니다.', user: '양도꾼 (share_id99)', count: 6, status: 'PENDING' },
1417: 
1418:     { id: 'RPT-102', reason: '상업적 광고/홍보 스팸', content: '타 학원 자격증 홍보 링크 도배 게시글', user: '스팸봇 (ad_bot12)', count: 4, status: 'BLINDED' },
1419: 
1420:     { id: 'RPT-101', reason: '욕설/비방', content: '자유게시판 댓글 비속어 포함', user: '김철수 (cskim44)', count: 2, status: 'PENDING' }
1421: 
1422:   ];
1423: 
1424: 
1425: 
1426:   function switchTab(tab) {
1427: 
1428:     document.querySelectorAll('.sub-tab-btn').forEach(b => b.classList.remove('active'));
1429: 
1430:     document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
1431: 
1432:     document.getElementById('tab-btn-' + tab).classList.add('active');
1433: 
1434:     document.getElementById('view-' + tab).classList.add('active');
1435: 
1436: 
1437: 
1438:     const meta = {
1439: 
1440:       courseReview: ['ADMN-BRD-005-A', '수강후기 관리 (강좌 진도율·별점·베스트 선정)'],
1441: 
1442:       passEssay: ['ADMN-BRD-005-B', '합격수기 검수 관리 (자격증 합격증빙 심사·축하 포인트)'],
1443: 
1444:       freeLecture: ['ADMN-BRD-006', '무료특강 및 빈출문제 관리'],
1445: 
1446:       errata: ['ADMN-BRD-009', '정답지 관리 (웹 에디터)'],
1447: 
1448:       report: ['ADMN-BRD-007/008', '커뮤니티 게시글 및 신고 관리']
1449: 
1450:     };

### 1-6. L1420~1440 (switchTab 함수)
1420:     { id: 'RPT-101', reason: '욕설/비방', content: '자유게시판 댓글 비속어 포함', user: '김철수 (cskim44)', count: 2, status: 'PENDING' }
1421: 
1422:   ];
1423: 
1424: 
1425: 
1426:   function switchTab(tab) {
1427: 
1428:     document.querySelectorAll('.sub-tab-btn').forEach(b => b.classList.remove('active'));
1429: 
1430:     document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
1431: 
1432:     document.getElementById('tab-btn-' + tab).classList.add('active');
1433: 
1434:     document.getElementById('view-' + tab).classList.add('active');
1435: 
1436: 
1437: 
1438:     const meta = {
1439: 
1440:       courseReview: ['ADMN-BRD-005-A', '수강후기 관리 (강좌 진도율·별점·베스트 선정)'],

### 1-7. L1845~1970 (렌더링 · 저장 로직)
1845: 
1846: 
1847: 
1848:   // 4. 정답지 (ADMN-BRD-009)
1849:   function renderErrata() {
1850:     const tp = document.getElementById('er-type-filter').value;
1851:     const kw = (document.getElementById('er-keyword').value || '').trim().toLowerCase();
1852:     const list = ERRATA_LIST.filter(item =>
1853:       (tp === 'ALL' || item.type === tp) &&
1854:       (!kw || item.book.toLowerCase().includes(kw) || item.title.toLowerCase().includes(kw) || item.page.toLowerCase().includes(kw))
1855:     );
1856:     document.getElementById('cnt-errata').textContent = ERRATA_LIST.length;
1857:     document.getElementById('er-tbody').innerHTML = list.map(item => `
1858:       <tr>
1859:         <td style="font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, 'Malgun Gothic', sans-serif; font-variant-numeric: tabular-nums; font-weight:700;">${item.id}</td>
1860:         <td><span class="badge badge-blue">📘 ${item.type}</span></td>
1861:         <td style="font-weight:700;">${item.book}</td>
1862:         <td>${item.page}</td>
1863:         <td>
1864:           <div style="font-weight:700;">${item.title}</div>
1865:           <div style="font-size:11.5px; color:var(--text-sub);">웹 에디터 정답표·해설 본문 등록됨</div>
1866:         </td>
1867:         <td style="color:var(--primary); font-weight:600;">📎 ${item.file}</td>
1868:         <td>${item.date}</td>
1869:         <td>
1870:           <button class="btn btn-outline btn-sm" onclick="openErrataModal('${item.id}')">에디터 수정</button>
1871:         </td>
1872:       </tr>
1873:     `).join('');
1874:   }
1875: 
1876:   function openErrataModal(id) {
1877:     const item = ERRATA_LIST.find(e => e.id === id);
1878:     document.getElementById('er-edit-id').value = item ? item.id : '';
1879:     document.getElementById('er-modal-title').textContent = item
1880:       ? `[ADMN-BRD-009] 정답지 수정 (${item.id})`
1881:       : '[ADMN-BRD-009] 정답지 신규 등록 (웹 에디터)';
1882:     document.getElementById('er-form-type').value = item ? item.type : '산업안전기사';
1883:     document.getElementById('er-form-book').value = item ? item.book : '[BK-2026-101 / BOOK-2601] 2026 산준모 산업안전기사 필기 한권끝장';
1884:     document.getElementById('er-form-page').value = item ? item.page : '2026년판 / 전 단원 빈출문제';
1885:     document.getElementById('er-form-file').value = item ? item.file : '2026_산안기_정답지_및_해설.pdf';
1886:     document.getElementById('er-form-title').value = item ? item.title : '';
1887:     document.getElementById('er-form-body').style.display = 'block';
1888:     document.getElementById('er-form-source').style.display = 'none';
1889:     if (item) {
1890:       document.getElementById('er-form-body').innerHTML = item.body;
1891:     } else {
1892:       insertAnswerTableTemplate();
1893:     }
1894:     document.getElementById('modal-errata').classList.add('open');
1895:   }
1896: 
1897:   function insertAnswerTableTemplate() {
1898:     document.getElementById('er-form-body').innerHTML = `
1899:       <p><strong>[단원별 빈출문제 정답 및 상세 해설표]</strong></p>
1900:       <table>
1901:         <thead>
1902:           <tr><th>단원 / 회차</th><th>문항 번호</th><th>정답</th><th>핵심 해설 및 관련 법령 근거</th></tr>
1903:         </thead>
1904:         <tbody>
1905:           <tr><td>제1과목 안전관리론</td><td>01번 ~ 05번</td><td>[3], [2], [4], [1], [3]</td><td>산업안전보건법령상 안전보건관리책임자 선임 기준</td></tr>
1906:           <tr><td>제2과목 인간공학</td><td>06번 ~ 10번</td><td>[2], [4], [1], [3], [2]</td><td>FTA 결함수와 최소컷셋(Minimal Cut Set) 신뢰도 계산</td></tr>
1907:         </tbody>
1908:       </table>
1909:     `;
1910:   }
1911: 
1912:   function insertQuickAnswerGridTemplate() {
1913:     document.getElementById('er-form-body').innerHTML = `
1914:       <p><strong>[실전모의고사 빠른 정답표 (1번 ~ 10번)]</strong></p>
1915:       <table>
1916:         <thead>
1917:           <tr><th>문항</th><th>01</th><th>02</th><th>03</th><th>04</th><th>05</th><th>06</th><th>07</th><th>08</th><th>09</th><th>10</th></tr>
1918:         </thead>
1919:         <tbody>
1920:           <tr><td><strong>정답</strong></td><td>[3]</td><td>[2]</td><td>[4]</td><td>[1]</td><td>[3]</td><td>[2]</td><td>[4]</td><td>[1]</td><td>[3]</td><td>[2]</td></tr>
1921:         </tbody>
1922:       </table>
1923:     `;
1924:   }
1925: 
1926:   function toggleErrataHtmlSource() {
1927:     const bodyEl = document.getElementById('er-form-body');
1928:     const srcEl = document.getElementById('er-form-source');
1929:     if (srcEl.style.display === 'none') {
1930:       srcEl.value = bodyEl.innerHTML.trim();
1931:       bodyEl.style.display = 'none';
1932:       srcEl.style.display = 'block';
1933:     } else {
1934:       bodyEl.innerHTML = srcEl.value;
1935:       srcEl.style.display = 'none';
1936:       bodyEl.style.display = 'block';
1937:     }
1938:   }
1939: 
1940:   function saveErrata() {
1941:     const editId = document.getElementById('er-edit-id').value;
1942:     const type = document.getElementById('er-form-type').value;
1943:     const book = document.getElementById('er-form-book').value;
1944:     const page = document.getElementById('er-form-page').value.trim();
1945:     const file = document.getElementById('er-form-file').value.trim() || '-';
1946:     const title = document.getElementById('er-form-title').value.trim();
1947:     const srcEl = document.getElementById('er-form-source');
1948:     const bodyEl = document.getElementById('er-form-body');
1949:     const body = srcEl.style.display !== 'none' ? srcEl.value : bodyEl.innerHTML;
1950: 
1951:     if (!title) { alert('정답지 제목을 입력해주세요.'); return; }
1952: 
1953:     if (editId) {
1954:       const target = ERRATA_LIST.find(e => e.id === editId);
1955:       if (target) Object.assign(target, { type, book, page, file, title, body, date: '2026-10-19' });
1956:     } else {
1957:       ERRATA_LIST.unshift({
1958:         id: 'ANS-' + (405 + ERRATA_LIST.length),
1959:         type, book, page, title, file, date: '2026-10-19', body
1960:       });
1961:     }
1962:     closeModal('modal-errata');
1963:     renderErrata();
1964:     showToast('정답지가 저장되어 교재 상세 페이지 및 학습지원센터에 반영되었습니다.');
1965:   }
1966: 
1967:   // 5. 신고 렌더링
1968: 
1969:   function renderReports() {
1970: 

## 2. prototype/ADMN-BRD-005_baseline.html 과 prototype_clean/ADMN-BRD-005_baseline.html 의 unified diff 전문

```diff
--- prototype/ADMN-BRD-005_baseline.html
+++ prototype_clean/ADMN-BRD-005_baseline.html
@@ -9,7 +9,7 @@
 
   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
 
-  <title>[ADMN-BRD-005] 수강후기·합격수기·무료특강(빈출문제)·정답지 관리 — 산준모 백오피스</title>
+  <title>수강후기·합격수기·무료특강(빈출문제)·정답지 관리 — 산준모 백오피스</title>
 
   <link rel="stylesheet" href="common-v84.css" />
```

## 3. prototype_clean/ADMN-CONF-005_baseline.html 에서 "정답지"가 들어간 7줄 (앞뒤 2줄 포함 원문)

### L354 기준 (범위 L352~L356)
   352:           <span class="badge badge-blue">ROLE_PARTNER_COPYRIGHT</span>
   353:           <h4>[2] 교재 저작권자 / 출판사 권한</h4>
>> 354:           <p>• <strong>접근 허용:</strong> 본인 저작 도서 판매량·인세(Royalty) 정산내역서 조회, 정답지(<code>ADMN-BRD-009</code>) 등록·수정<br/>• <strong>데이터 스코프:</strong> 바인딩된 저작권 계약코드(<code>CR-*</code> / <code>BOOK-*</code>)에 한정한 열람 허용</p>
   355:         </div>
   356:         <div class="role-card partner">

### L471 기준 (범위 L469~L473)
   469:             </tr>
   470:             <tr>
>> 471:               <td style="font-weight:700;">학습 Q&amp;A / 정답지 (BRD)</td>
   472:               <td>전체</td>
   473:               <td>✕ 접근불가</td>

### L477 기준 (범위 L475~L479)
   475:               <td>1:1문의/FAQ</td>
   476:               <td><strong>✓ 본인 강좌 Q&amp;A 답변</strong></td>
>> 477:               <td><strong>✓ 본인 정답지 등록</strong></td>
   478:               <td>✕ 접근불가</td>
   479:             </tr>

### L532 기준 (범위 L530~L534)
   530:             <option value="ROLE_CS_ADMIN">[내부] 고객센터 CS 전담 (ROLE_CS_ADMIN)</option>
   531:             <option value="ROLE_PARTNER_INST">[외부 파트너] 강사 전용 (ROLE_PARTNER_INST — 본인 강좌 Q&amp;A 및 강의 정산서)</option>
>> 532:             <option value="ROLE_PARTNER_COPYRIGHT">[외부 파트너] 교재 저작권자/출판사 (ROLE_PARTNER_COPYRIGHT — 도서 인세 정산서 및 정답지 관리)</option>
   533:             <option value="ROLE_PARTNER_3PL">[외부 파트너] 외부 물류 3PL (ROLE_PARTNER_3PL — 교재 출고지시서 및 송장 등록)</option>
   534:           </select>

### L569 기준 (범위 L567~L571)
   567:     { id: 'cs_lead01', name: '최상담 (고객감동팀)', role: 'ROLE_CS_ADMIN', scope: 'USER / ORD / BRD (CS 상담 및 환불접수)', sec: '2FA OTP', lastLogin: '2026-10-19 11:05', status: 'ACTIVE' },
   568:     { id: 'inst_leejh', name: '정종대 강사 (대표강사 파트너 · RH-0025)', role: 'ROLE_PARTNER_INST', scope: 'RH-0025 / CON-2026-001 (정종대 강사 · 본인 담당 강좌 Q&A 및 정산서 ADMN-SETT-002-S2 전용)', sec: '2FA 모바일 인증', lastLogin: '2026-10-18 21:10', status: 'ACTIVE' },
>> 569:     { id: 'copy_sanjunbook', name: '한출판 대표 (산준모북스 저작권자)', role: 'ROLE_PARTNER_COPYRIGHT', scope: 'CR-2026-002 / BK-2026-101 (본인 저작 도서 인세 정산서 ADMN-SETT-002-S2 및 정답지 ADMN-BRD-009 전용)', sec: '2FA 모바일 인증', lastLogin: '2026-10-18 16:30', status: 'ACTIVE' },
   570:     { id: '3pl_cjlogis', name: '정물류 매니저 (CJ파주물류센터 3PL)', role: 'ROLE_PARTNER_3PL', scope: '3PL-PAJU-01 (실물 교재 출고대상 열람 및 송장 업로드 전용 / 금액 비노출)', sec: '물류센터 고정 IP 제한', lastLogin: '2026-10-19 08:30', status: 'ACTIVE' }
   571:   ];

### L576 기준 (범위 L574~L578)
   574:     { id: 'AUD-9921', dt: '2026-10-19 11:32', actor: 'fin_manager (재무관리)', type: '정산 계좌번호 마스킹 해제', detail: '정종대 강사(RH-0025 / CON-2026-001) 10월 정산금 이체 대조를 위한 계좌번호 열람 (ADMN-USER-007 10자 사유 통과)', ip: '211.45.120.18' },
   575:     { id: 'AUD-9920', dt: '2026-10-19 10:48', actor: '3pl_cjlogis (외부물류 3PL)', type: '출고 송장 엑셀 업로드', detail: '2026-10-19 오전 출고분 실물 교재 64건 CJ대한통운 송장번호 일괄 매핑', ip: '121.160.44.92' },
>> 576:     { id: 'AUD-9919', dt: '2026-10-18 16:35', actor: 'copy_sanjunbook (저작권자)', type: '정답지 등록', detail: '[BK-2026-101 / BOOK-2601] 산업안전기사 필기 한권완성 정답지(ANSWER_SHEET) 웹 에디터 수정', ip: '58.120.89.11' },
   577:     { id: 'AUD-9918', dt: '2026-10-18 14:12', actor: 'admin_white (최고관리자)', type: '파트너 권한 분리 설정', detail: '한출판 계정에 ROLE_PARTNER_COPYRIGHT(교재 저작권자 전용) 권한 및 도서 스코프 부여', ip: '211.45.120.10' }
   578:   ];

### L640 기준 (범위 L638~L642)
   638:       scopeInp.value = 'INST-2026-005 (본인 담당 강좌 Q&A 및 강의 정산서 전용)';
   639:     } else if (r === 'ROLE_PARTNER_COPYRIGHT') {
>> 640:       scopeInp.value = 'CR-2026-004 / BOOK-2605 (본인 저작 도서 인세 정산서 및 정답지 관리 전용)';
   641:     } else if (r === 'ROLE_PARTNER_3PL') {
   642:       scopeInp.value = '3PL-LOGIS-02 (실물 교재 출고 목록 조회 및 송장 등록 전용)';

## 4. ADMN-BOOK-001, ADMN-PROD-003~006(양쪽 폴더) 선언 시작/끝 줄 및 함수 시작/끝 줄 번호

### prototype_clean/ADMN-BOOK-001_baseline.html
- MASTER_NAV_GROUPS: 시작 1346줄, 끝 1398줄
- renderMasterSnb 함수: 시작 1402줄, 끝 1422줄

### prototype/ADMN-BOOK-001_baseline.html
- MASTER_NAV_GROUPS: 시작 1346줄, 끝 1398줄
- renderMasterSnb 함수: 시작 1402줄, 끝 1422줄

### prototype_clean/ADMN-PROD-003_baseline.html
- MASTER_NAV_GROUPS: 시작 1336줄, 끝 1388줄
- renderMasterSnb 함수: 시작 1392줄, 끝 1412줄

### prototype/ADMN-PROD-003_baseline.html
- MASTER_NAV_GROUPS: 시작 1336줄, 끝 1388줄
- renderMasterSnb 함수: 시작 1392줄, 끝 1412줄

### prototype_clean/ADMN-PROD-004_baseline.html
- MASTER_NAV_GROUPS: 시작 1524줄, 끝 1576줄
- renderMasterSnb 함수: 시작 1580줄, 끝 1600줄

### prototype/ADMN-PROD-004_baseline.html
- MASTER_NAV_GROUPS: 시작 1524줄, 끝 1576줄
- renderMasterSnb 함수: 시작 1580줄, 끝 1600줄

### prototype_clean/ADMN-PROD-005_baseline.html
- MASTER_NAV_GROUPS: 시작 1281줄, 끝 1333줄
- renderMasterSnb 함수: 시작 1337줄, 끝 1357줄

### prototype/ADMN-PROD-005_baseline.html
- MASTER_NAV_GROUPS: 시작 1281줄, 끝 1333줄
- renderMasterSnb 함수: 시작 1337줄, 끝 1357줄

### prototype_clean/ADMN-PROD-006_baseline.html
- MASTER_NAV_GROUPS: 시작 984줄, 끝 1036줄
- renderMasterSnb 함수: 시작 1040줄, 끝 1060줄

### prototype/ADMN-PROD-006_baseline.html
- MASTER_NAV_GROUPS: 시작 984줄, 끝 1036줄
- renderMasterSnb 함수: 시작 1040줄, 끝 1060줄

## 5. patch_all_snb_v3.html 을 참조하는 줄 (레포 전체, _archive/ 제외)

- .antigravity/WORKFLOW_REDESIGN_PLAN.md:119: - 2026-10-21 · patch_all_snb_v3.html 은 화면 아님 → 디렉터리 제외
- .antigravity/WORKFLOW_REDESIGN_PLAN.md:136: - BOOK-001·PROD-003~006·patch_all_snb_v3.html 스크립트 안 옛 단계명 groupTitle 잔재 (사용 여부 미확인)
- .antigravity/WORKFLOW_REDESIGN_PLAN.md:151: - 다음 과제: 정답지 정리 패치(BRD-005 정답지 탭·제목·SNB명, BRD-009 매핑, CONF-005 권한 문구·'정답지 등록' 배지), CONF-005 탭명 괄호 중복, 옛 groupTitle 잔재(BOOK-001·PROD-003~006·patch_all_snb_v3.html)
- .antigravity/reports/JARGON_SCAN_REPORT.md:76: | `patch_all_snb_v3.html` | 0 | 0 | 0 | 0 | 0 |
- .antigravity/reports/JARGON_SCAN_REPORT.md:274: - `patch_all_snb_v3.html`
- .antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md:44: | `patch_all_snb_v3.html` | **PASS** | 0건 | 0개 탭 | 1행 | ✓ 정상 | 정상 (모달/탭/렌더링 통과) |
- .antigravity/reports/SNB_DIFF_01.md:682: - prototype/patch_all_snb_v3.html:949:       <span class="crumb-group">${meta.groupTitle}</span>
- .antigravity/reports/WORKFLOW_FINAL_CHECK.md:50: - prototype_clean/patch_all_snb_v3.html
- .antigravity/reports/WORKFLOW_FINAL_CHECK.md:279: #### prototype/patch_all_snb_v3.html
- .antigravity/reports/WORKFLOW_FINAL_CHECK.md:335: #### prototype_clean/patch_all_snb_v3.html
- .antigravity/reports/WORKFLOW_FINAL_CHECK.md:403: #### prototype/patch_all_snb_v3.html
- .antigravity/reports/WORKFLOW_FINAL_CHECK.md:467: #### prototype_clean/patch_all_snb_v3.html
- .antigravity/reports/WORKFLOW_LOOKUP_01.md:104: 38. `patch_all_snb_v3.html`
- .antigravity/reports/WORKFLOW_LOOKUP_02.md:86: - `patch_all_snb_v3.html` Line 232: `    groupTitle: "0단계 · 전체 업무 플로우 안내",`
- .antigravity/reports/WORKFLOW_LOOKUP_02.md:87: - `patch_all_snb_v3.html` Line 250: `    groupTitle: "1단계 · 계약 · 상품 · 매핑 설정",`
- .antigravity/reports/WORKFLOW_LOOKUP_02.md:88: - `patch_all_snb_v3.html` Line 259: `    groupTitle: "2단계 · 월마감 전 검증 (Gate)",`
- .antigravity/reports/WORKFLOW_LOOKUP_02.md:89: - `patch_all_snb_v3.html` Line 268: `    groupTitle: "3단계 · 월간 정산 · 집행 · 조회",`
- .antigravity/reports/WORKFLOW_LOOKUP_02.md:90: - `patch_all_snb_v3.html` Line 276: `    groupTitle: "4단계 · 보안 및 감사 통제",`
