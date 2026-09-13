"""Verifica el merge entre productos y análisis de reseñas (productos.id <-> analisis.producto_id),
el mismo join que hace src/dashboard/app.py para agregar la columna 'resumen_ia'.
"""

import pandas as pd


def test_columnas_clave_presentes(productos_sample, analisis_sample):
    df_productos = pd.DataFrame(productos_sample["productos"])
    df_analisis = pd.DataFrame(analisis_sample["productos"])

    assert "id" in df_productos.columns
    assert "producto_id" in df_analisis.columns


def test_merge_agrega_columna_resumen_ia(productos_sample, analisis_sample):
    df_productos = pd.DataFrame(productos_sample["productos"])
    df_analisis = pd.DataFrame(analisis_sample["productos"])

    df_merged = df_productos.merge(
        df_analisis[["producto_id", "resumen_ia", "opiniones_1_estrella"]],
        left_on="id",
        right_on="producto_id",
        how="left",
    )

    assert "resumen_ia" in df_merged.columns
    assert len(df_merged) == len(df_productos)


def test_producto_con_analisis_trae_su_resumen(productos_sample, analisis_sample):
    df_productos = pd.DataFrame(productos_sample["productos"])
    df_analisis = pd.DataFrame(analisis_sample["productos"])

    df_merged = df_productos.merge(
        df_analisis[["producto_id", "resumen_ia"]],
        left_on="id",
        right_on="producto_id",
        how="left",
    )

    fila = df_merged[df_merged["id"] == "fc48da47"].iloc[0]
    assert fila["resumen_ia"] == "Los compradores destacan la calidad de sonido y la batería duradera."


def test_producto_sin_analisis_queda_nulo(productos_sample, analisis_sample):
    df_productos = pd.DataFrame(productos_sample["productos"])
    df_analisis = pd.DataFrame(analisis_sample["productos"])

    df_merged = df_productos.merge(
        df_analisis[["producto_id", "resumen_ia"]],
        left_on="id",
        right_on="producto_id",
        how="left",
    )

    fila = df_merged[df_merged["id"] == "sin-analisis"].iloc[0]
    assert pd.isna(fila["resumen_ia"])
