# scripts/setup.ps1
# Bootstrap del entorno del proyecto usando uv en lugar de venv manual.

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv no está instalado. Instalando..."
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
}

Write-Host "Sincronizando dependencias (incluye grupo dev)..."
uv sync --all-extras

Write-Host "Instalando hooks de pre-commit..."
uv run pre-commit install

Write-Host ""
Write-Host "Entorno listo."
Write-Host "  - Ejecutar el script principal: uv run python src/mi_paquete/main.py"
Write-Host "  - Lanzar Jupyter:                uv run jupyter lab"
Write-Host "  - Correr tests:                  uv run pytest"
Write-Host "  - Lint manual:                   uv run ruff check ."
