"""Verifica que las dependencias declaradas en requirements.txt estén instaladas."""

import importlib

import pytest

DEPENDENCIAS = ["streamlit", "pandas", "plotly", "groq", "openpyxl"]


@pytest.mark.parametrize("modulo", DEPENDENCIAS)
def test_dependencia_instalada(modulo):
    importlib.import_module(modulo)
