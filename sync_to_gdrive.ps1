# sync_to_gdrive.ps1
# 로컬 Settlement 프로젝트 (docs, prototype) -> 구글 드라이브 공유 문서함 폴더 자동 동기화

$ErrorActionPreference = "Stop"

# 1. G: 또는 H: 드라이브에서 구글 드라이브 내 드라이브 및 바로가기 탐색
$targetRoot = $null
$drives = @("G:\", "H:\")

foreach ($d in $drives) {
    if (Test-Path $d) {
        $myDrive = Get-ChildItem $d -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "내 드라이브|My Drive" }
        if ($myDrive) {
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
    Write-Error "구글 드라이브 바로가기 대상 폴더를 찾을 수 없습니다. (G:\내 드라이브\정산시스템.lnk 확인 필요)"
    exit 1
}

Write-Host "=========================================="
Write-Host ">> 구글 드라이브 동기화 대상:"
Write-Host ">> $targetRoot"
Write-Host "=========================================="

# 2. 화면설계 HTML 복사 (prototype -> 화면설계)
$gdriveHtml = Join-Path $targetRoot "화면설계"
if (-not (Test-Path $gdriveHtml)) {
    New-Item -ItemType Directory -Path $gdriveHtml -Force | Out-Null
}

$localPrototypes = Get-ChildItem -Path "d:\Work\Settlement\prototype\*.html"
foreach ($file in $localPrototypes) {
    $dest = Join-Path $gdriveHtml $file.Name
    Copy-Item -LiteralPath $file.FullName -Destination $dest -Force
    Write-Host " [HTML 복사] $($file.Name)"
}

# 구버전 파일 삭제 (ADMN-CONF-008, ADMN-USER-004, test.html)
$obsoleteFiles = @("ADMN-CONF-008_baseline.html", "ADMN-USER-004_baseline.html", "test.html")
foreach ($obs in $obsoleteFiles) {
    $obsPath = Join-Path $gdriveHtml $obs
    if (Test-Path -LiteralPath $obsPath) {
        Remove-Item -LiteralPath $obsPath -Force
        Write-Host " [구버전 삭제] $obs"
    }
}

# 3. 기획서 마크다운 복사 (docs -> 대상 루트)
$docs = Get-ChildItem -Path "d:\Work\Settlement\docs\*.md"
foreach ($doc in $docs) {
    $targetName = $doc.Name -replace "^\[산준모 정산시스템\]_", ""
    $dest = Join-Path $targetRoot $targetName
    Copy-Item -LiteralPath $doc.FullName -Destination $dest -Force
    Write-Host " [기획서 복사] $($doc.Name) -> $targetName"
}

Write-Host "=========================================="
Write-Host ">> 구글 드라이브 동기화 완료! (클라우드 자동 업로드 대기)"
Write-Host "=========================================="