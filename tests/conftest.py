"""Fixtures compartidas para los tests del proyecto."""

import pytest


@pytest.fixture
def productos_sample():
    """Datos de ejemplo con la forma que genera src/scraping/buscador_productos.py."""
    return {
        "producto_buscado": "auriculares bluetooth",
        "fecha_busqueda": "2025-11-04 21:28:57",
        "total_productos": 3,
        "productos": [
            {
                "id": "fc48da47",
                "titulo": "Auriculares Inalámbricos Bluetooth XYZ",
                "link": "https://mercadolibre.com.ar/auriculares-xyz",
                "precio_actual": "$42.000",
                "precio_anterior": "$50.000",
                "descuento": "16% OFF",
                "calificacion": 4.4,
                "vendidos": "+1000 vendidos",
                "imagen": "https://example.com/img1.jpg",
                "envio_gratis": True,
            },
            {
                "id": "a1b2c3d4",
                "titulo": "Auriculares Deportivos ABC",
                "link": "https://mercadolibre.com.ar/auriculares-abc",
                "precio_actual": "$18.500",
                "precio_anterior": "",
                "descuento": "0%",
                "calificacion": 4.0,
                "vendidos": "+50 vendidos",
                "imagen": "https://example.com/img2.jpg",
                "envio_gratis": False,
            },
            {
                "id": "sin-analisis",
                "titulo": "Auriculares Genéricos Sin Reseñas",
                "link": "https://mercadolibre.com.ar/auriculares-generico",
                "precio_actual": "$9.000",
                "precio_anterior": "",
                "descuento": "0%",
                "calificacion": 0.0,
                "vendidos": "Sin ventas",
                "imagen": "https://example.com/img3.jpg",
                "envio_gratis": False,
            },
        ],
    }


@pytest.fixture
def analisis_sample():
    """Datos de ejemplo con la forma que genera src/analisis/analizador_resenias.py.

    A propósito no incluye análisis para 'sin-analisis', para poder testear
    el caso de un producto sin resumen_ia después del merge.
    """
    return {
        "producto_analizado": "auriculares bluetooth",
        "fecha_analisis": "2025-11-04 21:33:19",
        "total_productos": 2,
        "total_con_resumen_ia": 2,
        "productos": [
            {
                "producto_id": "fc48da47",
                "producto_titulo": "Auriculares Inalámbricos Bluetooth XYZ",
                "producto_link": "https://mercadolibre.com.ar/auriculares-xyz",
                "producto_calificacion": 4.4,
                "producto_precio": "$42.000",
                "resumen_ia": "Los compradores destacan la calidad de sonido y la batería duradera.",
                "opiniones_1_estrella": "Algunos reportan fallas de conexión intermitentes.",
                "timestamp_extraccion": "2025-11-04 21:33:20",
            },
            {
                "producto_id": "a1b2c3d4",
                "producto_titulo": "Auriculares Deportivos ABC",
                "producto_link": "https://mercadolibre.com.ar/auriculares-abc",
                "producto_calificacion": 4.0,
                "producto_precio": "$18.500",
                "resumen_ia": "Buena relación precio-calidad para uso deportivo diario.",
                "opiniones_1_estrella": "",
                "timestamp_extraccion": "2025-11-04 21:33:25",
            },
        ],
    }
