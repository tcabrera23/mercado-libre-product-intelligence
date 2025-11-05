# 🛒 Análisis de Productos - Mercado Libre Argentina

Sistema completo para extraer, analizar y visualizar información de productos de Mercado Libre Argentina.

## 📋 Descripción

Este proyecto permite buscar cualquier producto en Mercado Libre, extraer automáticamente su información (precios, calificaciones, envíos, etc.) y guardarla en formato JSON para su posterior análisis.

## ✨ Características

### 🎯 Extracción de Productos (buscar_productos_ml.py)
- 🔍 **Búsqueda dinámica**: Busca cualquier producto en Mercado Libre Argentina
- 🤖 **Anti-scraping bypass**: Headers configurados para evitar bloqueos
- 📊 **Extracción completa**: Precios, descuentos, calificaciones, envíos, imágenes
- ✅ **Campos siempre completos**: Valores por defecto para campos null (v2.0)
- 💾 **Export a JSON**: Guarda los resultados con timestamp
- 🎯 **ID único**: Cada producto recibe un identificador único

### 🤖 Análisis de Reseñas (analizar_resenias_ia_v2.py) ⭐ NUEVO v3.0
- 🌐 **Selenium**: Filtrado dinámico con interacción real
- 🎯 **Filtro automático**: Click en opiniones de 1 estrella
- 🤖 **Resumen de IA**: Extrae el resumen generado por IA de ML
- ⭐ **Top 5 negativas**: Reseñas de 1 estrella filtradas
- 💾 **JSON estructurado**: Listo para análisis

### 📊 Export a Excel (export_to_excel.py) ⭐ NUEVO v3.0
- 📁 **Conversión automática**: JSON → Excel (.xlsx)
- 🏷️ **Clasificación de precios**: Económico/Mediano/Caro
- 🏢 **Extracción de marcas**: Del título del producto
- 📋 **Dos hojas**: Productos + Resumen con estadísticas
- 📏 **Formato automático**: Anchos de columna ajustados

### 📊 Dashboard Interactivo (dashboard_productos.py) ⭐ NUEVO v3.0
- 📊 **Cards de métricas**: Min, Median, Max precio, Total productos
- 📋 **Tabla interactiva**: Con scroll, búsqueda y ordenamiento
- 📈 **Gráfico dispersión**: Precio vs Ventas (correlación)
- 📊 **Gráfico barras**: Precio promedio por calificación
- 🥧 **Gráfico torta**: Marcas más populares (Top 10)
- 🎚️ **Filtros dinámicos**: Marca, envío, categoría, calificación
- ⬇️ **Descarga CSV**: Datos filtrados exportables

## 🚀 Uso Rápido

### 🎯 Demo v2.0 - Flujo Completo

```bash
# Paso 1: Extraer productos
python buscar_productos_ml.py "auriculares bluetooth"

# Paso 2: Analizar reseñas con IA
python analizar_resenias_ia.py productos_auriculares_bluetooth_*.json
```

**Ver [DEMO_V2.0.md](DEMO_V2.0.md) para guía completa** ⭐

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
├── 🎯 Scripts Principales
│   ├── buscar_productos_ml.py      # ⭐ Extracción de productos
│   └── analizar_resenias_ia.py     # ⭐ Análisis de reseñas (NUEVO v2.0)
│
├── 🔧 Funciones y Utilidades
│   ├── get_html.py                 # Función para obtener HTML de ML
│   └── ejemplo_uso.py              # Ejemplos avanzados
│
├── 📚 Documentación
│   ├── README.md                   # Este archivo
│   ├── DEMO_V2.0.md               # ⭐ Guía completa v2.0
│   ├── GUIA_RAPIDA.md             # Tutorial rápido
│   ├── INICIO.md                   # Punto de entrada
│   └── CHANGELOG.md                # Historial de cambios
│
├── 📄 Datos Generados
│   ├── productos_*.json            # Productos extraídos
│   └── analisis_resenias_*.json   # Análisis de reseñas (NUEVO)
│
└── 💾 Backup
    ├── get_products.py             # Script original (legacy)
    └── get_resenias.py             # Versión anterior
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
      "calificacion": 4.4,
      "vendidos": "+1000 vendidos",
      "imagen": "https://...",
      "envio_gratis": true
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
