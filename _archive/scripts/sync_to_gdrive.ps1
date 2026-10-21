# sync_to_gdrive.ps1
# 로컬 Settlement 프로젝트 (docs, prototype, root) -> 구글 드라이브 공유 문서함(04.설계서) 자동 동기화

$ErrorActionPreference = "Stop"

# 1. G: 드라이브에서 구글 드라이브 내 드라이브 및 바로가기 탐색
$targetRoot = $null
$drives = @("G:\")

foreach ($d in $drives) {
    if (Test-Path $d) {
        $myDrive = Get-ChildItem $d -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "내 드라이브|My Drive" }
        if ($myDrive) {
            # 1-1. 신규 바로가기: Works\산준모 닷컴.lnk 탐색
            $worksLnk = Join-Path $myDrive.FullName "Works\산준모 닷컴.lnk"
            if (Test-Path $worksLnk) {
                $sh = New-Object -ComObject WScript.Shell
                $sc = $sh.CreateShortcut($worksLnk)
                if ($sc -and (Test-Path $sc.TargetPath)) {
                    $designDir = Join-Path $sc.TargetPath "04.설계서"
                    if (Test-Path $designDir) {
                        $targetRoot = $designDir
                        break
                    }
                }
            }
            # 1-2. 기존 바로가기 폴백 (*정산시스템*.lnk)
            $lnk = Get-ChildItem $myDrive.FullName -Filter "*정산시스템*.lnk" -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($lnk) {
                $sh = New-Object -ComObject WScript.Shell
                $sc = $sh.CreateShortcut($lnk.FullName)
                if ($sc -and (Test-Path $sc.TargetPath)) {
                    $targetRoot = $sc.TargetPath
                    break
                }
            }
        }
    }
}

if (-not $targetRoot) {
    Write-Error "구글 드라이브 바로가기 대상 폴더를 찾을 수 없습니다. (G:\내 드라이브\Works\산준모 닷컴.lnk 확인 필요)"
    exit 1
}

Write-Host "=========================================="
Write-Host ">> 구글 드라이브 동기화 대상:"
Write-Host ">> $targetRoot"
Write-Host "=========================================="

# 2. 루트 문서 동기화 (README.md, index.html)
Copy-Item -LiteralPath "d:\Work\Settlement\README.md" -Destination (Join-Path $targetRoot "README.md") -Force
Copy-Item -LiteralPath "d:\Work\Settlement\index.html" -Destination (Join-Path $targetRoot "index.html") -Force
Write-Host " [루트 동기화] README.md, index.html"

# 3. 화면설계 HTML 및 에셋 복사 (prototype -> prototype)
$gdriveHtml = Join-Path $targetRoot "prototype"
if (-not (Test-Path $gdriveHtml)) {
    $altHtml = Join-Path $targetRoot "화면설계"
    if (Test-Path $altHtml) {
        $gdriveHtml = $altHtml
    } else {
        New-Item -ItemType Directory -Path $gdriveHtml -Force | Out-Null
    }
}

$localPrototypes = Get-ChildItem -Path "d:\Work\Settlement\prototype\*" -Include "*.html", "*.css", "*.js"
foreach ($file in $localPrototypes) {
    $dest = Join-Path $gdriveHtml $file.Name
    Copy-Item -LiteralPath $file.FullName -Destination $dest -Force
    Write-Host " [프로토타입 복사] $($file.Name)"
}

# 3-1. 이미지 에셋 (prototype/img)
$localImg = "d:\Work\Settlement\prototype\img"
if (Test-Path $localImg) {
    $gdriveImg = Join-Path $gdriveHtml "img"
    if (-not (Test-Path $gdriveImg)) { New-Item -ItemType Directory -Path $gdriveImg -Force | Out-Null }
    Get-ChildItem -Path "$localImg\*" | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $gdriveImg $_.Name) -Force
        Write-Host " [에셋 복사: img] $($_.Name)"
    }
}

# 3-2. 폰트 에셋 (prototype/fonts)
$localFonts = "d:\Work\Settlement\prototype\fonts"
if (Test-Path $localFonts) {
    $gdriveFonts = Join-Path $gdriveHtml "fonts"
    if (-not (Test-Path $gdriveFonts)) { New-Item -ItemType Directory -Path $gdriveFonts -Force | Out-Null }
    Get-ChildItem -Path "$localFonts\*" | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $gdriveFonts $_.Name) -Force
        Write-Host " [에셋 복사: fonts] $($_.Name)"
    }
}

# 3-3. 구버전 파일 삭제 (ADMN-MKT-001, ADMN-CONF-008, ADMN-USER-004, test.html)
$obsoleteFiles = @("ADMN-MKT-001_baseline.html", "ADMN-CONF-008_baseline.html", "ADMN-USER-004_baseline.html", "test.html")
foreach ($obs in $obsoleteFiles) {
    $obsPath = Join-Path $gdriveHtml $obs
    if (Test-Path -LiteralPath $obsPath) {
        Remove-Item -LiteralPath $obsPath -Force
        Write-Host " [구버전 삭제] $obs"
    }
}

# 3-4. 실무 클린 어드민 복사 (prototype_clean -> prototype_clean)
$localClean = "d:\Work\Settlement\prototype_clean"
if (Test-Path $localClean) {
    $gdriveClean = Join-Path $targetRoot "prototype_clean"
    if (-not (Test-Path $gdriveClean)) { New-Item -ItemType Directory -Path $gdriveClean -Force | Out-Null }
    Get-ChildItem -Path "$localClean\*" -Include "*.html", "*.css", "*.js" | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $gdriveClean $_.Name) -Force
    }
    foreach ($sub in @("img", "fonts")) {
        $srcSub = Join-Path $localClean $sub
        if (Test-Path $srcSub) {
            $dstSub = Join-Path $gdriveClean $sub
            if (-not (Test-Path $dstSub)) { New-Item -ItemType Directory -Path $dstSub -Force | Out-Null }
            Get-ChildItem -Path "$srcSub\*" | ForEach-Object {
                Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $dstSub $_.Name) -Force
            }
        }
    }
    Write-Host " [실무 클린 어드민 복사: prototype_clean] 동기화 완료"
}

# 4. 기획서 마크다운 복사 (docs -> docs)
$gdriveDocs = Join-Path $targetRoot "docs"
if (-not (Test-Path $gdriveDocs)) {
    $gdriveDocs = $targetRoot
}

# 4-1. docs/*.md 원본 및 정제본 복사
$docs = Get-ChildItem -Path "d:\Work\Settlement\docs\*.md"
foreach ($doc in $docs) {
    # 깃헙 원본 파일명 복사
    Copy-Item -LiteralPath $doc.FullName -Destination (Join-Path $gdriveDocs $doc.Name) -Force
    # 접두어 제거 파일명도 호환성 유지 복사
    $cleanName = $doc.Name -replace "^\[산준모 정산시스템\]_", ""
    if ($cleanName -ne $doc.Name) {
        Copy-Item -LiteralPath $doc.FullName -Destination (Join-Path $gdriveDocs $cleanName) -Force
    }
    Write-Host " [기획서 복사] $($doc.Name)"
}

# 4-2. docs/screen_spec 하위 폴더 전체 동기화
$localScreenSpec = "d:\Work\Settlement\docs\screen_spec"
if (Test-Path $localScreenSpec) {
    $gdriveScreenSpec = Join-Path $gdriveDocs "screen_spec"
    if (-not (Test-Path $gdriveScreenSpec)) { New-Item -ItemType Directory -Path $gdriveScreenSpec -Force | Out-Null }
    Get-ChildItem -Path "$localScreenSpec\*" | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $gdriveScreenSpec $_.Name) -Force
        Write-Host " [화면설계서 복사: screen_spec] $($_.Name)"
    }
}

# 구버전 기획서 파일(*_v4.0.0.md) 정리
$obsoleteDocs = @(
    "00_INDEX_라우팅맵_및_거버넌스_v4.0.0.md",
    "01_비즈니스정책_계약_도서_이월_기획서_v4.0.0.md",
    "02_SSOT_정산연산엔진_및_세무증빙_명세서_v4.0.0.md",
    "03_백오피스화면_외부연동_및_데이터사전_v4.0.0.md",
    "04_QA_정산케이스스펙_및_회귀테스트_법령근거_v4.0.0.md",
    "산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md",
    "SET1_TO_4_ALIGNMENT_PLAN.md",
    "BACKOFFICE_ALIGNMENT_MASTER_PLAN.md",
    "AGENT_PIPELINE_MEMORY.md",
    "JARGON_SCAN_REPORT.md",
    "PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md"
)
foreach ($obsDoc in $obsoleteDocs) {
    $obsDocPath = Join-Path $gdriveDocs $obsDoc
    if (Test-Path -LiteralPath $obsDocPath) {
        Remove-Item -LiteralPath $obsDocPath -Force
        Write-Host " [구버전 기획서 삭제] $obsDoc"
    }
}

Write-Host "=========================================="
Write-Host ">> 구글 드라이브 동기화 완료! (클라우드 자동 업로드 대기)"
Write-Host "=========================================="