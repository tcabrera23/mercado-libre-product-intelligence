# 🛒 Análisis de Productos - Mercado Libre Argentina

Sistema completo para extraer, analizar y visualizar información de productos de Mercado Libre Argentina.

## 📋 Descripción

Este proyecto permite buscar cualquier producto en Mercado Libre, extraer automáticamente su información (precios, calificaciones, envíos, etc.) y guardarla en formato JSON para su posterior análisis.

## ✨ Características

- 🔍 **Búsqueda dinámica**: Busca cualquier producto en Mercado Libre Argentina
- 🤖 **Anti-scraping bypass**: Headers configurados para evitar bloqueos
- 📊 **Extracción completa**: Precios, descuentos, calificaciones, envíos, imágenes
- 💾 **Export a JSON**: Guarda los resultados con timestamp para análisis posterior
- 🎯 **ID único**: Cada producto recibe un identificador único
- 📝 **Resumen visual**: Muestra los primeros productos encontrados en consola

## 🚀 Uso Rápido

### Opción 1: Modo Interactivo

```bash
python buscar_productos_ml.py
```

El programa te pedirá que ingreses el producto que deseas buscar.

### Opción 2: Línea de Comandos

```bash
python buscar_productos_ml.py auriculares
python buscar_productos_ml.py "celulares samsung"
python buscar_productos_ml.py "notebook gaming"
```

## 📁 Estructura del Proyecto

```
Analisis de Productos/
│
├── buscar_productos_ml.py      # 🎯 Script principal (USAR ESTE)
├── get_html.py                  # Función para obtener HTML de ML
├── get_products.py              # Script original (legacy)
├── get_resenias.py              # Extracción de reseñas
├── productos_con_id.json        # Ejemplo de productos extraídos
├── resenas_productos_*.json     # Ejemplo de reseñas extraídas
│
└── backup/                      # Versiones anteriores
    ├── deepseek_v1.py
    ├── deepseek_V2.py
    └── productos*.json
```

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias:**

```bash
pip install requests beautifulsoup4
```

3. **Ejecutar:**

```bash
python buscar_productos_ml.py
```

## 📊 Formato de Salida

El programa genera un archivo JSON con el siguiente formato:

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
      "calificacion": "4.4",
      "vendidos": "+1000 vendidos",
      "imagen": "https://...",
      "envio": "Envío gratis"
    }
  ]
}
```

## 🔧 Módulos

### `get_html.py`
Contiene la función `obtener_html_mercadolibre()` que:
- Recibe el nombre del producto
- Construye la URL de búsqueda
- Envía headers para evitar anti-scraping
- Extrae solo la sección de resultados del HTML

### `buscar_productos_ml.py`
Script principal que:
- Usa `get_html.py` para obtener el HTML
- Extrae información de cada producto
- Genera IDs únicos
- Guarda resultados en JSON
- Muestra resumen en consola

### `get_resenias.py`
Para extraer reseñas de productos específicos.

## 💡 Ejemplos de Búsqueda

```bash
# Electrónica
python buscar_productos_ml.py auriculares bluetooth
python buscar_productos_ml.py "celulares iphone"
python buscar_productos_ml.py "notebook gaming"

# Ropa y calzado
python buscar_productos_ml.py "zapatillas nike"
python buscar_productos_ml.py "campera north face"

# Hogar
python buscar_productos_ml.py "smart tv 55"
python buscar_productos_ml.py "cafetera nespresso"
```

## 📈 Próximos Pasos / Ideas

- [ ] 📊 Visualización con Streamlit
- [ ] 📑 Export a Excel para Power BI
- [ ] 🤖 Análisis de reseñas con IA
- [ ] 📉 Tracking de precios en el tiempo
- [ ] 🔔 Alertas de descuentos
- [ ] 📊 Comparación entre productos
- [ ] 🌐 Scraping de múltiples marketplaces

## ⚠️ Consideraciones

- **Uso responsable**: No hagas requests demasiado frecuentes para evitar bloqueos
- **Delays**: Si haces múltiples búsquedas, agrega delays entre ellas
- **TOS**: Revisa los términos de servicio de Mercado Libre
- **Datos**: Los precios y disponibilidad pueden cambiar rápidamente

## 🐛 Troubleshooting

### No se obtienen resultados
- Verifica tu conexión a internet
- Asegúrate de que el producto exista en ML Argentina
- Agrega un delay si hiciste muchas requests seguidas

### Caracteres extraños en el HTML
- El script ya maneja el encoding automáticamente
- Si persiste, verifica la versión de `requests` y `beautifulsoup4`

### Error de timeout
- El timeout está configurado en 15 segundos
- Si tu conexión es lenta, puedes aumentarlo en `get_html.py`

## 📝 Notas

Este proyecto fue creado con fines educativos para análisis de mercado y comparación de productos.

## 🤝 Contribuciones

Ideas y mejoras son bienvenidas!

---

**Última actualización**: Noviembre 2024
