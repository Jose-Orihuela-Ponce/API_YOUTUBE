param(
    [switch]$RefreshYtDlp
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$VenvPath = Join-Path $ProjectRoot ".venv"
$PythonPath = Join-Path $VenvPath "Scripts\python.exe"
$VendorPath = Join-Path $ProjectRoot "vendor"
$YtDlpPath = Join-Path $VendorPath "yt-dlp.exe"
$BuildRequirements = Join-Path $ProjectRoot "requirements-build.txt"
$RuntimeRequirements = Join-Path $ProjectRoot "requirements.txt"
$OutputPath = Join-Path $ProjectRoot "dist"
$ReleaseUrl = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"

if (-not (Test-Path $PythonPath)) {
    New-Item -ItemType Directory -Force -Path $VenvPath | Out-Null
    $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($PyLauncher) {
        & $PyLauncher.Source -3 -m venv $VenvPath
    } else {
        $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if (-not $PythonCommand) {
            throw "Instala Python 3.10 o superior y vuelve a ejecutar este script."
        }
        & $PythonCommand.Source -m venv $VenvPath
    }
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo crear el entorno virtual del proyecto."
    }
}

$PythonVersion = & $PythonPath -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$PythonVersion -lt [version]"3.10") {
    throw "Se necesita Python 3.10 o superior. Versión encontrada: $PythonVersion"
}

Write-Host "Instalando dependencias de Python..."
& $PythonPath -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "No se pudo actualizar pip." }
& $PythonPath -m pip install -r $RuntimeRequirements -r $BuildRequirements
if ($LASTEXITCODE -ne 0) { throw "No se pudieron instalar las dependencias del proyecto." }

New-Item -ItemType Directory -Force -Path $VendorPath | Out-Null
if ($RefreshYtDlp -or -not (Test-Path $YtDlpPath)) {
    $DownloadPath = "$YtDlpPath.download"
    Write-Host "Descargando el ejecutable oficial de yt-dlp..."
    Invoke-WebRequest -Uri $ReleaseUrl -OutFile $DownloadPath
    if (-not (Test-Path $DownloadPath) -or (Get-Item $DownloadPath).Length -lt 1000000) {
        Remove-Item -LiteralPath $DownloadPath -Force -ErrorAction SilentlyContinue
        throw "La descarga de yt-dlp no produjo un ejecutable válido."
    }
    Move-Item -LiteralPath $DownloadPath -Destination $YtDlpPath -Force
}

Write-Host "Construyendo el ejecutable portable..."
$PyInstallerArguments = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--onefile",
    "--console",
    "--name", "Descargar",
    "--add-binary", "$YtDlpPath;.",
    "--distpath", $OutputPath,
    (Join-Path $ProjectRoot "descargar.py")
)
& $PythonPath @PyInstallerArguments
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller no pudo construir el ejecutable."
}

Write-Host "Ejecutable listo: $(Join-Path $OutputPath 'Descargar.exe')"
Write-Host "Necesita FFmpeg y Node.js para descargar y procesar videos en otros equipos."
