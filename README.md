# Plantilla de proyecto Python (uv + ruff + pytest + CI)

Plantilla base para proyectos de análisis de datos / BI, pensada para sustituir
el flujo de "script de PowerShell + venv manual" por algo reproducible y
verificable automáticamente.

## Estructura

```
.
├── .github/workflows/ci.yml   # CI: lint + tests en cada push/PR
├── .pre-commit-config.yaml    # Hooks de ruff antes de cada commit
├── pyproject.toml             # Metadatos, dependencias y config de ruff/pytest
├── scripts/setup.ps1          # Bootstrap en Windows (llama a uv por debajo)
├── src/mi_paquete/            # Código instalable (renombra el paquete)
│   ├── __init__.py
│   └── main.py
└── tests/
    └── test_main.py
```

## Primer uso

1. Instala [uv](https://docs.astral.sh/uv/) una sola vez (o deja que
   `scripts/setup.ps1` lo haga por ti):
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```
2. Copia esta carpeta como base de un proyecto nuevo y renombra
   `src/mi_paquete` (y las referencias en `pyproject.toml` / `tests/`) al
   nombre real de tu proyecto.
3. Desde la raíz del proyecto:
   ```powershell
   .\scripts\setup.ps1
   ```
   Esto crea el entorno virtual (`.venv`), instala dependencias + extras de
   dev, e instala los hooks de pre-commit. Ya no necesitas activar el venv a
   mano: usa siempre `uv run <comando>`.

## Comandos habituales

| Acción                       | Comando                              |
|-------------------------------|---------------------------------------|
| Ejecutar el script principal | `uv run python src/mi_paquete/main.py`|
| Añadir una dependencia        | `uv add nombre-paquete`               |
| Añadir dependencia de dev     | `uv add --dev nombre-paquete`         |
| Lanzar Jupyter                | `uv run jupyter lab`                  |
| Correr tests                  | `uv run pytest`                       |
| Lint / formato manual         | `uv run ruff check .` / `uv run ruff format .` |

## Qué te da esto "gratis"

- **Reproducibilidad**: `uv.lock` fija versiones exactas; cualquiera que
  clone el repo y corra `uv sync` obtiene el mismo entorno.
- **Calidad automática**: pre-commit corre ruff antes de cada commit, así que
  el código que subes ya está formateado y sin errores obvios.
- **CI real**: cada push a `main` o cada PR corre lint + tests en GitHub
  Actions. Esto es lo que un revisor de portfolio nota primero: el repo tiene
  un check ✅ verde, no solo notebooks sueltos.
- **Separación de capas**: `src/` es el paquete instalable; notebooks,
  datos y reportes viven fuera, sin mezclarse con el código reutilizable.

## Notas

- Ajusta `.gitignore` si tu proyecto sí necesita versionar algún CSV pequeño
  de ejemplo (quita la línea `*.csv` o usa una carpeta `data/sample/` aparte).
- Si un proyecto concreto necesita librerías extra (scikit-learn, plotly,
  etc.), añádelas con `uv add` en vez de editar `pyproject.toml` a mano —
  así el lock file se actualiza automáticamente.
