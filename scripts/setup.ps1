# Bootstrap the project environment with uv.

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv no está instalado. Instalando..."
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
}

Write-Host "Sincronizando dependencias (incluye grupo dev)..."
uv sync --all-extras
if ($LASTEXITCODE -ne 0) {
    throw "uv sync failed."
}

Write-Host "Instalando hooks de pre-commit..."
\.venv\Scripts\python.exe -m pre_commit install
if ($LASTEXITCODE -ne 0) {
    throw "pre-commit installation failed."
}

Write-Host ""
Write-Host "Entorno listo."
Write-Host "  - Procesar VCF:                  .\.venv\Scripts\python.exe src\variantes_genomicas\explore_vcf.py"
Write-Host "  - Generar figuras:               .\.venv\Scripts\python.exe src\variantes_genomicas\EDA.py"
Write-Host "  - Correr tests:                  .\.venv\Scripts\python.exe -m pytest"
Write-Host "  - Lint manual:                   .\.venv\Scripts\ruff.exe check ."
