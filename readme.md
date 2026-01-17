# 🛒 Análisis de Productos - Mercado Libre Argentina

Sistema completo para extraer, analizar y visualizar información de productos de Mercado Libre Argentina.

## 🐳 Nuevo: Soporte Docker + Ollama

¡Ahora puedes ejecutar el proyecto con **Docker** y usar modelos locales con **Ollama** (además de Groq)!

- ✅ **Sin complicaciones**: Un solo comando para levantar todo
- ✅ **Modelos locales**: Ollama con llama3.2, mistral, etc.
- ✅ **Gratis**: No requiere API keys (aunque Groq sigue disponible)
- ✅ **Carpetas organizadas**: Los JSON se guardan en `productos/` y `resenias/`

### Inicio Rápido con Docker:

```bash
# Levantar servicios (app + Ollama)
docker-compose up -d

# Descargar modelo de Ollama
docker exec -it analisis-productos-ollama ollama pull llama3.2:8b

# Abrir en navegador: http://localhost:8501
```

📖 **[Ver guía completa de Docker →](DOCKER_SETUP.md)**

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

### 🤖 Análisis de Reseñas (analizar_resenias_ia.py) ⭐ ACTUALIZADO v3.0
- 🌐 **Web Scraping**: Extrae opiniones de productos de Mercado Libre
- 🤖 **Resumen de IA**: Extrae el resumen generado por IA de ML
- 💾 **JSON estructurado**: Listo para análisis

### 📊 Export a Excel (export_to_excel.py) ⭐ NUEVO v3.0
- 📁 **Conversión automática**: JSON → Excel (.xlsx)
- 🏷️ **Clasificación de precios**: Económico/Mediano/Caro
- 🏢 **Extracción de marcas**: Del título del producto
- 📋 **Dos hojas**: Productos + Resumen con estadísticas
- 📏 **Formato automático**: Anchos de columna ajustados

### 📊 Dashboard Interactivo (dashboard_productos_v4.py) ⭐ ACTUALIZADO v4.3
- 📊 **Cards de métricas**: Min, Median, Max precio, Total productos
- 📋 **Tabla mejorada**: 
  - ✅ Resumen IA (join corregido: productos.id ↔ análisis.producto_id)
  - 🔗 Links clicables a productos de ML
  - 🔢 Precio_num y Descuento_num (columnas numéricas para filtrado dinámico)
  - Título, Marca, Precio, Categoría, Calificación, Vendidos, Envío, Descuento
- 🔢 **Sort inteligente**: Ordena correctamente Vendidos, Descuento, Precio (numéricamente)
- 🔍 **Búsqueda en Tiempo Real**: 
  - Barra de búsqueda integrada en sidebar
  - Ejecuta scraping directamente desde el dashboard
  - Checkbox opcional para incluir análisis de reseñas
  - Recarga automática después del scraping
- ⬇️ **Descarga Excel**: Formato .xlsx en lugar de CSV
- 📈 **Gráfico dispersión**: Precio vs Ventas (correlación)
- 📊 **Gráfico barras**: Precio promedio por calificación
- 🥧 **Gráfico torta**: Marcas más populares (Top 10)
- 🎚️ **Filtros dinámicos**: Marca, envío, categoría, calificación
- 🤖 **Chatbot IA con múltiples proveedores**: ⭐ **NUEVO v5.0**
  - 🔄 **Groq** (API en la nube, rápido) o **Ollama** (local, gratis, privado)
  - 📍 Ubicación: Final de la página (antes del footer)
  - 💬 Expandible con checkbox
  - 🧠 Acceso completo a JSONs de productos y reseñas
  - 📊 4 Prompts sugeridos en fila horizontal
  - 💾 Historial scrollable (400px) + botón de limpieza
  - 🎯 Análisis proactivo en lenguaje marketinero
- ⚡ **Análisis Simplificado**: Solo extrae resumen IA (80% más rápido) ✨ v4.3
  - ⏱️ 2-5 minutos (antes: 10+ minutos)
  - ✅ Sin Selenium (más confiable)
  - 🎯 Solo resumen IA (sin opiniones individuales)

## 🚀 Uso Rápido

### 🎯 Opción 1: Búsqueda desde el Dashboard (v4.3) ⭐ RECOMENDADO

```bash
# 1. Ejecutar Dashboard
streamlit run dashboard_productos_v4.py

# 2. En el sidebar:
#    - Sección "🔍 Búsqueda en Tiempo Real"
#    - Escribir nombre del producto (ej: "ipad pro")
#    - Marcar/Desmarcar "Incluir reseñas"
#    - Click "🔍 Buscar"
#    - Esperar ~30-60 seg (productos) + ~2-5 min (reseñas, opcional)
#    - Click "🔄 Recargar Dashboard"

# 3. ¡Listo! Los datos ya están en la tabla
```

### 🎯 Opción 2: Flujo Manual (desde terminal)

```bash
# Paso 1: Extraer productos
python buscar_productos_ml.py "auriculares bluetooth"

# Paso 2: Analizar reseñas con IA (opcional pero recomendado)
python analizar_resenias_ia.py productos_auriculares_bluetooth_*.json

# Paso 3: Ejecutar Dashboard Interactivo
streamlit run dashboard_productos_v4.py

# Paso 4 (Opcional): Verificar sistema antes de ejecutar
python test_dashboard_v4.py
```

**Ver [FIX_TIMEOUT_FINAL.md](FIX_TIMEOUT_FINAL.md) para el fix definitivo del timeout** ⭐ **v4.3.1 - NUEVO**

**📋 Changelogs anteriores**: [CAMBIOS_V4.3_SIMPLIFICACION.md](CAMBIOS_V4.3_SIMPLIFICACION.md) | [CHANGELOG_V4.2.md](CHANGELOG_V4.2.md) | [FIX_EOFERROR_ANALISIS.md](FIX_EOFERROR_ANALISIS.md)

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
│   ├── buscar_productos_ml.py       # ⭐ Extracción de productos
│   ├── analizar_resenias_ia.py      # ⭐ Análisis de reseñas
│   ├── dashboard_productos.py       # Dashboard interactivo (versión base/simplificada)
│   ├── dashboard_productos_v4.py    # ⭐ Dashboard interactivo con IA (versión principal)
│   └── llm_config.py                # 🆕 Configuración LLM (Groq/Ollama)
│
├── 🔧 Funciones y Utilidades
│   ├── parse_html/get_html.py       # Función para obtener HTML de ML
│   ├── export_to_excel.py           # Exportar a Excel
│   └── ejemplo_uso.py               # Ejemplos avanzados
│
├── 🐳 Docker
│   ├── Dockerfile                   # 🆕 Imagen de la app
│   ├── docker-compose.yml           # 🆕 Orquestación (app + Ollama)
│   └── DOCKER_SETUP.md              # 🆕 Guía completa de Docker
│
├── 📚 Documentación
│   ├── README.md                    # Este archivo
│   ├── INICIO.md                    # Punto de entrada
│   └── documentacion/               # Changelogs y guías
│
├── 📄 Datos Generados (Organizados en carpetas)
│   ├── productos/                   # 🆕 JSONs de productos
│   │   └── productos_*.json
│   └── resenias/                    # 🆕 JSONs de análisis de reseñas
│       └── analisis_resenias_*.json
│
├── ⚙️ Configuración
│   ├── env.example                  # 🆕 Plantilla de variables de entorno
│   ├── requirements.txt             # Dependencias Python
│   └── .gitignore
│
└── 💾 Backup y Tests
    ├── backup/                      # Scripts legacy
    └── tests/                       # Tests del proyecto
```

## 🛠️ Instalación

### Opción 1: Docker (Recomendado) 🐳

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Descargar modelo de Ollama
docker exec -it analisis-productos-ollama ollama pull llama3.2:8b

# 3. Abrir http://localhost:8501
```

📖 **[Ver guía completa de Docker →](DOCKER_SETUP.md)**

### Opción 2: Instalación Local

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias:**

```bash
# Dependencias completas
pip install -r requirements.txt
```

3. **Configurar variables de entorno** (opcional):

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tu configuración:
# - GROQ_API_KEY (para Groq)
# - OLLAMA_BASE_URL (para Ollama local)
```

**Para usar Groq:**
- Obtén tu API key gratis en: https://console.groq.com/
- Configura `GROQ_API_KEY` en `.env`

**Para usar Ollama:**
- Instala Ollama: https://ollama.ai
- Ejecuta: `ollama pull llama3.2:8b`
- Configura `OLLAMA_BASE_URL=http://localhost:11434` en `.env`

4. **Ejecutar:**

```bash
# Extracción de productos
python buscar_productos_ml.py "producto deseado"

# Dashboard interactivo
streamlit run dashboard_productos_v4.py
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

### `parse_html/get_html.py`
Contiene la función `obtener_html_mercadolibre()` que:
- Recibe el nombre del producto
- Construye la URL de búsqueda
- Envía headers para evitar anti-scraping
- Extrae solo la sección de resultados del HTML

### `buscar_productos_ml.py`
Script principal que:
- Usa `parse_html/get_html.py` para obtener el HTML
- Extrae información de cada producto
- Genera IDs únicos
- Guarda resultados en JSON
- Muestra resumen en consola

### `analizar_resenias_ia.py`
Script principal que:
- Usa `parse_html/get_html.py` para obtener el HTML de la página de reseñas (a través de `requests`)
- Extrae el resumen generado por IA de Mercado Libre.
- Guarda los resultados en JSON.

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
- Si tu conexión es lenta, puedes aumentarlo en `parse_html/get_html.py`

## 📝 Notas

Este proyecto fue creado con fines educativos para análisis de mercado y comparación de productos.

## 🤝 Contribuciones

Ideas y mejoras son bienvenidas!

Autor: Tomas Cabrera

---

**Última actualización**: Enero 2026
