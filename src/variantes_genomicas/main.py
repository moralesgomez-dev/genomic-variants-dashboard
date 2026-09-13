"""Punto de entrada de ejemplo.

Reemplaza esto por la lógica real de tu análisis o pipeline.
"""

from __future__ import annotations

import pandas as pd


def resumen_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """Ejemplo: agrupa ventas por categoría y suma el importe.

    Args:
        df: DataFrame con al menos las columnas 'categoria' e 'importe'.

    Returns:
        DataFrame agregado por categoría, ordenado de mayor a menor.
    """
    return (
        df.groupby("categoria", as_index=False)["importe"]
        .sum()
        .sort_values("importe", ascending=False)
        .reset_index(drop=True)
    )


def main() -> None:
    datos = pd.DataFrame(
        {
            "categoria": ["Calzado", "Ropa", "Calzado", "Accesorios"],
            "importe": [120.5, 80.0, 45.0, 15.0],
        }
    )
    print(resumen_ventas(datos))


if __name__ == "__main__":
    main()
