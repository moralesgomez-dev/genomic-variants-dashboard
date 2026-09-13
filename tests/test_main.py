import pandas as pd

from variantes_genomicas.main import resumen_ventas


def test_resumen_ventas_agrupa_y_ordena():
    df = pd.DataFrame(
        {
            "categoria": ["A", "B", "A"],
            "importe": [10, 50, 20],
        }
    )

    resultado = resumen_ventas(df)

    assert list(resultado["categoria"]) == ["B", "A"]
    assert resultado.loc[resultado["categoria"] == "A", "importe"].iloc[0] == 30
