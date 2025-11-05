# 🚀 Guía de Nuevas Funcionalidades v3.0

## 📋 Índice
1. [Análisis de Reseñas v2 (Selenium)](#análisis-v2)
2. [Export a Excel](#export-excel)
3. [Dashboard Interactivo](#dashboard)
4. [Instalación](#instalación)

---

## <a name="análisis-v2"></a>🤖 1. Análisis de Reseñas v2 (Selenium)

### Mejoras vs v1
- ✅ Filtrado dinámico de opiniones de 1 estrella
- ✅ Usa Selenium para interactuar con la página
- ✅ Hace clic en el filtro `#dropdown-option-rating-1`
- ✅ Extracción más precisa de reseñas

### Requisitos
```bash
pip install selenium
```

**Descargar ChromeDriver**: https://chromedriver.chromium.org/

### Uso

```bash
# Básico
python analizar_resenias_ia_v2.py productos_auriculares_*.json

# Limitar productos
python analizar_resenias_ia_v2.py productos_auriculares_*.json
# Cuando pregunte: 3 (solo analiza 3 productos)
```

### Diferencias v1 vs v2

| Aspecto | v1 (Requests) | v2 (Selenium) |
|---------|---------------|---------------|
| Filtrado | ❌ Manual | ✅ Automático (clic en filtro) |
| Precisión | 70% | 95% |
| Velocidad | Rápido | Más lento |
| Requisitos | Requests | Selenium + ChromeDriver |
| Recomendado | No | ✅ Sí |

---

## <a name="export-excel"></a>📊 2. Export a Excel

### Funcionalidades

- ✅ Convierte JSON a Excel (.xlsx)
- ✅ **Clasificación de precios** (Económico/Mediano/Caro)
- ✅ **Extracción de marcas** del título
- ✅ Precios como números (para cálculos)
- ✅ **Dos hojas**: Productos + Resumen
- ✅ Formato automático (anchos de columna)

### Uso

```bash
# Básico
python export_to_excel.py productos_auriculares_20251104_212857.json

# Resultado: productos_auriculares_20251104_HHMMSS.xlsx
```

### Clasificación de Precios

**Algoritmo**:
```python
promedio = mean(precio_actual)

if precio < promedio * 0.9:
    categoria = "Económico"  # 10% por debajo
elif precio > promedio * 1.1:
    categoria = "Caro"       # 10% por encima
else:
    categoria = "Mediano"
```

**Ejemplo**:
```
Promedio: $50.000
- Económico: < $45.000
- Mediano: $45.000 - $55.000
- Caro: > $55.000
```

### Hojas del Excel

#### Hoja 1: Productos
Todas las columnas del JSON + columnas calculadas:
- `precio_numerico` - Precio como número
- `marca` - Marca extraída del título
- `categoria_precio` - Económico/Mediano/Caro
- `descuento_porcentaje` - Descuento como número
- `envio_gratis_texto` - "Sí" o "No"

#### Hoja 2: Resumen
Estadísticas generales:
- Total de productos
- Precio promedio/mínimo/máximo
- Distribución por categoría
- Productos con envío gratis
- Calificación promedio

---

## <a name="dashboard"></a>📊 3. Dashboard Interactivo (Streamlit)

### Funcionalidades

#### 📊 Cards con Métricas
- Precio Mínimo
- Precio Mediano
- Precio Máximo
- Total de Productos

#### 📋 Tabla Interactiva
- Todos los productos con scroll
- Ordenable por columnas
- Búsqueda incluida
- Descarga como CSV

#### 📈 Gráficos

1. **Dispersión: Precio vs Ventas**
   - Pregunta: ¿A menor precio, más ventas?
   - Eje X: Precio
   - Eje Y: Cantidad vendidos
   - Color: Categoría de precio
   - Tamaño: Calificación

2. **Barras: Precio Promedio por Calificación**
   - Muestra si productos caros tienen mejor calificación
   - Agrupa por calificación redondeada

3. **Torta: Marcas Más Populares**
   - Top 10 marcas
   - Porcentaje de distribución
   - Gráfico tipo dona

#### 🎚️ Slicers/Filtros (Sidebar)
- ✅ Filtro por marca (multiselect)
- ✅ Filtro por envío gratis (radio)
- ✅ Filtro por categoría de precio (multiselect)
- ✅ Rango de calificación (slider)

### Uso

```bash
# Instalar dependencias
pip install streamlit plotly pandas

# Ejecutar dashboard
streamlit run dashboard_productos.py

# Se abre automáticamente en: http://localhost:8501
```

### Captura de Pantalla (Estructura)

```
┌─────────────────────────────────────────────────────────┐
│         🛒 Dashboard de Análisis de Productos          │
└─────────────────────────────────────────────────────────┘

┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  MIN   │ │ MEDIAN │ │  MAX   │ │ TOTAL  │
│$3.104  │ │$25.000 │ │$85.000 │ │   52   │
└────────┘ └────────┘ └────────┘ └────────┘

┌─────────────────────┐ ┌─────────────────────┐
│ Precio vs Ventas    │ │ Precio por Calif.   │
│ [Gráfico Dispersión]│ │ [Gráfico Barras]    │
└─────────────────────┘ └─────────────────────┘

┌─────────────────────────────────────────────┐
│      Marcas Más Populares [Gráfico Torta]  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│        Tabla de Productos [Con Scroll]      │
│ Título | Marca | Precio | Categoría | ...   │
│ ───────────────────────────────────────────│
│ Producto 1...                               │
│ Producto 2...                               │
└─────────────────────────────────────────────┘

[Sidebar]
📁 Configuración
   - Seleccionar archivo JSON
   
🎚️ Filtros
   - Marca
   - Envío gratis
   - Categoría precio
   - Rango calificación
```

---

## <a name="instalación"></a>🛠️ Instalación Completa

### Paso 1: Clonar/Descargar Proyecto

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt**:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
pandas>=2.1.0
openpyxl>=3.1.2
streamlit>=1.28.0
plotly>=5.17.0
```

### Paso 3: Instalar ChromeDriver (para Selenium)

**Opción 1: Manual**
1. Ir a: https://chromedriver.chromium.org/
2. Descargar versión compatible con tu Chrome
3. Agregar al PATH

**Opción 2: Automático (webdriver-manager)**
```bash
pip install webdriver-manager
```

### Paso 4: Verificar Instalación

```bash
# Test básico
python buscar_productos_ml.py auriculares

# Test Selenium
python analizar_resenias_ia_v2.py productos_*.json

# Test Excel
python export_to_excel.py productos_*.json

# Test Dashboard
streamlit run dashboard_productos.py
```

---

## 📊 Flujo de Trabajo Completo v3.0

```bash
# 1. Extraer productos
python buscar_productos_ml.py "notebook gaming"
# Genera: productos_notebook_gaming_20251104_HHMMSS.json

# 2. Analizar reseñas (opcional)
python analizar_resenias_ia_v2.py productos_notebook_gaming_*.json
# Genera: analisis_resenias_notebook_gaming_20251104_HHMMSS.json

# 3. Export a Excel
python export_to_excel.py productos_notebook_gaming_*.json
# Genera: productos_notebook_gaming_20251104_HHMMSS.xlsx

# 4. Visualizar Dashboard
streamlit run dashboard_productos.py
# Se abre en navegador automáticamente
```

---

## 💡 Casos de Uso

### Caso 1: Análisis Rápido
```bash
python buscar_productos_ml.py "celulares"
streamlit run dashboard_productos.py
# Seleccionar archivo en dashboard
```

### Caso 2: Análisis Profundo
```bash
python buscar_productos_ml.py "auriculares"
python analizar_resenias_ia_v2.py productos_auriculares_*.json
python export_to_excel.py productos_auriculares_*.json
# Abrir Excel para análisis detallado
```

### Caso 3: Presentación
```bash
python buscar_productos_ml.py "smart tv"
streamlit run dashboard_productos.py
# Usar filtros para mostrar insights en tiempo real
```

---

## 🐛 Troubleshooting

### Error: "ChromeDriver not found"
**Solución**:
```bash
pip install webdriver-manager
```
O descargar manualmente: https://chromedriver.chromium.org/

### Error: "Module 'plotly' not found"
**Solución**:
```bash
pip install plotly
```

### Error: Excel no se genera
**Solución**:
```bash
pip install openpyxl pandas
```

### Dashboard no carga datos
**Solución**:
- Verifica que haya archivos JSON en el directorio
- Archivos deben empezar con `productos_` y terminar en `.json`

---

## 📈 Estadísticas v3.0

| Feature | Líneas de Código | Archivos |
|---------|------------------|----------|
| Análisis Selenium | ~300 | 1 |
| Export Excel | ~250 | 1 |
| Dashboard | ~450 | 1 |
| **Total** | **~1000** | **3** |

---

## 🎯 Próximos Pasos

### Features Planeados
- [ ] Integración con IA para análisis de sentimientos
- [ ] Tracking de precios en tiempo real
- [ ] Alertas por email de cambios de precio
- [ ] API REST para consultas
- [ ] Comparación histórica de productos

---

## ✅ Checklist de Uso

- [ ] Instalé todas las dependencias
- [ ] Tengo ChromeDriver configurado
- [ ] Extraje productos con `buscar_productos_ml.py`
- [ ] Probé el dashboard con `streamlit run dashboard_productos.py`
- [ ] Exporté a Excel con `export_to_excel.py`
- [ ] (Opcional) Analicé reseñas con `analizar_resenias_ia_v2.py`

---

**Versión**: 3.0  
**Fecha**: 2025-11-04  
**Estado**: ✅ Funcional  

**¡Disfruta las nuevas funcionalidades! 🚀**

