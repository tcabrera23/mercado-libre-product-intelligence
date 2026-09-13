"""Verifica el comportamiento real de src/analisis/analizador_resenias.py al
ejecutarse como subprocess (que es como lo invoca src/dashboard/app.py), sin
depender de red: usa un producto sin 'link' para forzar la rama que no hace
ninguna petición HTTP.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "analisis"
    / "analizador_resenias.py"
)


def test_sin_argumentos_termina_con_error_sin_pedir_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        input="",
    )

    assert result.returncode != 0
    assert "archivo JSON de productos" in result.stdout


def test_analiza_producto_sin_link_no_hace_red_y_genera_json(tmp_path):
    productos_json = tmp_path / "productos_test.json"
    productos_json.write_text(
        json.dumps(
            {
                "producto_buscado": "test",
                "productos": [
                    {
                        "id": "sin-link",
                        "titulo": "Producto sin link",
                        "link": "",
                        "calificacion": 0,
                        "precio_actual": "$1.000",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(productos_json)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=15,
    )

    assert result.returncode == 0, result.stderr

    salidas = list((tmp_path / "data" / "resenias").glob("analisis_resenias_*.json"))
    assert len(salidas) == 1

    data = json.loads(salidas[0].read_text(encoding="utf-8"))
    assert data["total_productos"] == 1
    assert data["productos"][0]["producto_id"] == "sin-link"
    assert data["productos"][0]["resumen_ia"] is None
