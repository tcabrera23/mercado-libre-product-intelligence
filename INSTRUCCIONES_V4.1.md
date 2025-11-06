# 🎉 Dashboard v4.1 - Listo para Usar!

## ✅ Cambios Implementados

### 1. 🔗 JOIN Corregido
- **Problema resuelto**: La columna "Resumen IA" ahora muestra correctamente el texto
- **Causa**: El campo era `"id"` en productos y `"producto_id"` en reseñas
- **Solución**: Usamos `left_on='id'` y `right_on='producto_id'` en el merge

### 2. 🌐 Link Clickeable en Tabla
- Se agregó la columna "Link" con enlaces directos a Mercado Libre
- Configurada como `LinkColumn` con texto "Ver Producto 🔗"

### 3. 💬 Chat Widget Mejorado
- **Ubicación**: Sidebar (minimizable con checkbox)
- **Características**:
  - 4 prompts sugeridos
  - Historial scrollable (300px de alto)
  - Botón para limpiar chat
  - Acceso completo a JSONs de productos y reseñas

### 4. 🧠 Agente IA con Más Contexto
- Ahora recibe los JSONs completos
- Puede "consultar" la base de datos completa
- System prompt mejorado para análisis marketinero

---

## 🚀 Cómo Probar el Dashboard

### Paso 1: Verificar el Sistema

```bash
python test_dashboard_v4.py
```

Este script verifica:
- ✅ Archivos JSON de productos disponibles
- ✅ Archivos JSON de análisis disponibles
- ✅ Estructura correcta de JSONs (campos id y producto_id)
- ✅ Dependencias instaladas (streamlit, pandas, plotly, groq, openpyxl)
- ✅ API Key de Groq configurada

### Paso 2: Ejecutar el Dashboard

```bash
streamlit run dashboard_productos_v4.py
```

### Paso 3: Explorar las Funcionalidades

#### 📊 Dashboard Principal
1. **Sidebar Izquierdo**:
   - Selecciona archivo de productos
   - Selecciona archivo de análisis (opcional)
   - Aplica filtros: Marca, Envío, Categoría, Calificación

2. **Métricas Principales** (Cards):
   - Precio Mínimo, Mediano, Máximo
   - Total de Productos

3. **Gráficos Interactivos**:
   - **Scatter**: Precio vs Ventas (¿A menor precio, más ventas?)
   - **Barras**: Precio promedio por calificación
   - **Torta**: Marcas más populares (Top 10)

4. **Tabla de Productos**:
   - Columnas: Título, Marca, Precio, Categoría, **Resumen IA**, Calificación, Vendidos, Envío, Descuento, **Link**
   - Ordenamiento: Click en encabezados para ordenar
   - Descarga: Botón "⬇️ Descargar datos filtrados (Excel)"

#### 🤖 Chat con IA (Sidebar)

1. **Marcar checkbox** "Abrir Asistente IA"

2. **Usar Prompts Sugeridos**:
   - 💡 **Avatar de Cliente Ideal**: Analiza opiniones para crear buyer persona
   - 💰 **Estrategia de Precio**: Recomienda pricing óptimo
   - 📊 **Explica los Insights**: Explica los datos en lenguaje simple
   - ⭐ **Análisis de Opiniones**: Resume opiniones positivas y negativas

3. **O escribe tus propias preguntas**:
   - "¿Cuál es el producto con mejor relación precio-calidad?"
   - "Resume las quejas más comunes de los clientes"
   - "¿Qué marca tiene mejor reputación?"
   - "Dame 3 insights clave sobre estos productos"

4. **Ver respuestas del IA**:
   - Análisis en lenguaje marketinero
   - Bullet points accionables
   - Referencias a datos reales del dashboard

5. **Limpiar historial**: Click en "🗑️ Limpiar Chat"

---

## 🔑 Configurar API Key de Groq (Si no lo hiciste)

### Opción 1: Variable de Entorno (Recomendado)

#### Windows PowerShell:
```powershell
$env:GROQ_API_KEY="tu_api_key_aqui"
```

#### Windows CMD:
```cmd
set GROQ_API_KEY=tu_api_key_aqui
```

#### Linux/Mac:
```bash
export GROQ_API_KEY=tu_api_key_aqui
```

### Opción 2: Hardcodeado (Solo para testing)

En `dashboard_productos_v4.py`, línea ~286:

```python
groq_api_key = "tu_api_key_aqui"  # ⚠️ No commitear a git!
```

### Obtener tu API Key:
1. Ve a: https://console.groq.com/
2. Crea una cuenta (gratis)
3. Ve a "API Keys"
4. Crea una nueva key
5. Cópiala y configúrala

---

## 📁 Archivos Creados/Actualizados

### ✨ Nuevos Archivos:
- `CHANGELOG_V4.1.md` - Changelog detallado de v4.1
- `test_dashboard_v4.py` - Script de verificación del sistema
- `INSTRUCCIONES_V4.1.md` - Este archivo (guía de uso)

### 📝 Archivos Actualizados:
- `dashboard_productos_v4.py` - Todas las correcciones y mejoras
- `README.md` - Actualizado con info de v4.1
- `requirements.txt` - Ya incluía groq

---

## 🎯 Próximos Pasos Sugeridos

### Corto Plazo:
- [ ] Probar el dashboard con diferentes productos
- [ ] Experimentar con los prompts del chatbot
- [ ] Exportar datos filtrados a Excel

### Mediano Plazo:
- [ ] Agregar más productos a la base de datos
- [ ] Comparar diferentes categorías de productos
- [ ] Generar reportes PDF automáticos

### Largo Plazo:
- [ ] Widget flotante CSS puro (fuera del sidebar)
- [ ] Análisis de tendencias temporales
- [ ] Integración con otras fuentes de datos

---

## 🆘 Troubleshooting

### ❌ "No se encontraron archivos JSON"
**Solución**: Ejecuta primero el scraper
```bash
python buscar_productos_ml.py "producto"
```

### ❌ "Resumen IA muestra None"
**Causa**: No hay archivo de análisis de reseñas
**Solución**: Ejecuta el analizador
```bash
python analizar_resenias_ia.py productos_*.json
```

### ❌ "Chatbot IA no disponible"
**Causa**: Falta la API Key de Groq
**Solución**: Ver sección "🔑 Configurar API Key de Groq" arriba

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
**Causa**: Faltan dependencias
**Solución**:
```bash
pip install -r requirements.txt
```

### ❌ "Error al procesar con IA: ..."
**Posibles causas**:
1. API Key inválida o expirada
2. Límite de rate de Groq alcanzado (espera unos minutos)
3. Sin conexión a internet

**Solución**: Verifica tu API Key y conexión

---

## 📊 Datos de Ejemplo

Si aún no tienes datos, aquí te dejo el flujo completo:

```bash
# 1. Extraer productos de "auriculares bluetooth"
python buscar_productos_ml.py "auriculares bluetooth"

# 2. Analizar reseñas (toma ~5-10 min para 50 productos)
python analizar_resenias_ia.py productos_auriculares_bluetooth_*.json

# 3. Ejecutar dashboard
streamlit run dashboard_productos_v4.py

# 4. Abrir en navegador: http://localhost:8501
```

---

## 💡 Tips de Uso

### Para Análisis de Mercado:
1. Filtra por marca específica
2. Analiza relación precio-ventas en el scatter plot
3. Pregunta al chatbot: "¿Qué estrategia de pricing me recomendás?"

### Para Investigación de Competencia:
1. Filtra por categoría de precio "Caro"
2. Lee los resúmenes de IA de productos premium
3. Pregunta: "¿Qué valoran los clientes de productos premium?"

### Para Definir Buyer Persona:
1. Incluye análisis de reseñas
2. Lee opiniones negativas (1 estrella)
3. Pregunta: "Crea un avatar de cliente ideal basado en las opiniones"

---

## 📞 Contacto y Feedback

Si encuentras bugs o tienes sugerencias:
- Crea un issue en el repositorio
- Documenta el error con capturas de pantalla
- Incluye el archivo de log si es posible

---

**¡Disfruta analizando productos con IA!** 🚀🛒📊

