# Guía de uso detallada

Anexo del [README](../README.md) con el formato de datos, más ejemplos y troubleshooting.

## Formato de salida

`src/scraping/buscador_productos.py` genera un JSON con esta forma en `data/productos/`:

```json
{
  "producto_buscado": "auriculares",
  "fecha_busqueda": "2024-11-04 15:30:45",
  "total_productos": 48,
  "productos": [
    {
      "id": "a3f2c1d5",
      "titulo": "Auriculares Inalámbricos Bluetooth...",
      "link": "https://mercadolibre.com.ar/...",
      "precio_actual": "$42.000",
      "precio_anterior": "$50.000",
      "descuento": "16% OFF",
      "calificacion": 4.4,
      "vendidos": "+1000 vendidos",
      "imagen": "https://...",
      "envio_gratis": true
    }
  ]
}
```

`src/analisis/analizador_resenias.py` genera un JSON análogo en `data/resenias/`, con una lista de `productos` donde cada item tiene `producto_id` (que matchea con el `id` de arriba) y `resumen_ia`.

## Ejemplos de búsqueda

```bash
# Electrónica
python src/scraping/buscador_productos.py auriculares bluetooth
python src/scraping/buscador_productos.py "celulares iphone"
python src/scraping/buscador_productos.py "notebook gaming"

# Ropa y calzado
python src/scraping/buscador_productos.py "zapatillas nike"
python src/scraping/buscador_productos.py "campera north face"

# Hogar
python src/scraping/buscador_productos.py "smart tv 55"
python src/scraping/buscador_productos.py "cafetera nespresso"
```

También se puede correr sin argumentos (`python src/scraping/buscador_productos.py`) para el modo interactivo.

## Consideraciones de uso responsable

- No hagas requests demasiado frecuentes para evitar bloqueos de Mercado Libre.
- Si hacés múltiples búsquedas seguidas, agregá delays entre ellas.
- Revisá los términos de servicio de Mercado Libre.
- Los precios y la disponibilidad pueden cambiar rápidamente entre la extracción y el análisis.

## Troubleshooting

**No se obtienen resultados**
- Verificá tu conexión a internet.
- Asegurate de que el producto exista en ML Argentina.
- Agregá un delay si hiciste muchas requests seguidas.

**Caracteres extraños en el HTML**
- El script maneja el encoding automáticamente; si persiste, verificá la versión de `requests` y `beautifulsoup4`.

**Error de timeout**
- El timeout de las requests está configurado en 15 segundos en `src/scraping/html_ml.py`; podés aumentarlo ahí si tu conexión es lenta.

## Próximos pasos / ideas

- Tracking de precios en el tiempo
- Alertas de descuentos
- Comparación entre productos
- Scraping de otros marketplaces
