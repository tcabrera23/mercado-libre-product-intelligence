# 🏠 INICIO - Sistema de Scraping Mercado Libre

> **Sistema dinámico para extraer productos de Mercado Libre Argentina**

---

## 🚀 ¿Nuevo aquí? Empieza aquí

### ⚡ Inicio Ultra Rápido (2 minutos)

```bash
# 1. Instalar dependencias
pip install requests beautifulsoup4

# 2. Ejecutar primera búsqueda
python buscar_productos_ml.py auriculares

# 3. ✅ ¡Listo! Revisa el archivo JSON generado
```

---

## 📚 Documentación

### Para Usuarios Nuevos
1. **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** ⭐ EMPIEZA AQUÍ
   - Instalación paso a paso
   - Ejemplos básicos
   - Solución de problemas comunes

### Para Usuarios Avanzados
2. **[README.md](README.md)** 📖
   - Documentación completa
   - Arquitectura del sistema
   - API de funciones

3. **[ejemplo_uso.py](ejemplo_uso.py)** 💻
   - 7 ejemplos de código
   - Casos de uso reales
   - Filtros y análisis

### Para Desarrolladores
4. **[RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md)** 🔧
   - Arquitectura técnica
   - Métricas del proyecto
   - Roadmap futuro

---

## 🎯 Archivos Principales

### Scripts Ejecutables

| Archivo | Uso | Comando |
|---------|-----|---------|
| **buscar_productos_ml.py** | 🎯 Buscar productos | `python buscar_productos_ml.py "producto"` |
| **ejemplo_uso.py** | 📚 Ver ejemplos | `python ejemplo_uso.py` |
| **get_html.py** | 🔍 Solo HTML (testing) | `python get_html.py` |

### Funciones Importables

```python
# Opción 1: Todo en uno
from buscar_productos_ml import buscar_producto_mercadolibre
productos = buscar_producto_mercadolibre("notebook")

# Opción 2: Solo HTML
from get_html import obtener_html_mercadolibre
soup, seccion = obtener_html_mercadolibre("celulares")

# Opción 3: Solo parsing
from buscar_productos_ml import extraer_productos_con_id
productos = extraer_productos_con_id(html_section)
```

---

## 🎓 Tutoriales Rápidos

### Tutorial 1: Primera Búsqueda (2 min)
```bash
python buscar_productos_ml.py auriculares
```
✅ Genera: `productos_auriculares_FECHA.json`

### Tutorial 2: Búsqueda con Espacios (2 min)
```bash
python buscar_productos_ml.py "celulares samsung"
```
✅ Genera: `productos_celulares_samsung_FECHA.json`

### Tutorial 3: Modo Interactivo (3 min)
```bash
python buscar_productos_ml.py
# Ingresa el producto cuando te lo pida
```

### Tutorial 4: Múltiples Búsquedas (5 min)
```bash
python buscar_productos_ml.py auriculares
python buscar_productos_ml.py "auriculares bluetooth"
python buscar_productos_ml.py "auriculares gaming"
# Comparar los 3 JSON generados
```

### Tutorial 5: Análisis con Python (10 min)
```bash
python ejemplo_uso.py
# Selecciona opción 4: Productos con descuento
```

---

## 📊 Ejemplos de Búsquedas

### Electrónica
```bash
python buscar_productos_ml.py auriculares
python buscar_productos_ml.py "celulares samsung"
python buscar_productos_ml.py "notebook gaming"
python buscar_productos_ml.py "smart tv 55"
python buscar_productos_ml.py "playstation 5"
```

### Hogar
```bash
python buscar_productos_ml.py "licuadora"
python buscar_productos_ml.py "cafetera nespresso"
python buscar_productos_ml.py "aspiradora robot"
```

### Deportes
```bash
python buscar_productos_ml.py "zapatillas nike"
python buscar_productos_ml.py "bicicleta mtb"
python buscar_productos_ml.py "pelota futbol"
```

### Moda
```bash
python buscar_productos_ml.py "campera north face"
python buscar_productos_ml.py "reloj smartwatch"
```

---

## 🎯 Casos de Uso Populares

### 1. 💰 Comparar Precios
```bash
# Buscar notebook más barato
python buscar_productos_ml.py notebook
# Revisar campo "precio_actual" en el JSON
```

### 2. 🎁 Encontrar Ofertas
```bash
# Buscar productos en descuento
python buscar_productos_ml.py "smart tv"
# Filtrar por campo "descuento" != ""
```

### 3. 📈 Tracking de Precios
```bash
# Día 1
python buscar_productos_ml.py "iphone 15"

# Día 2
python buscar_productos_ml.py "iphone 15"

# Comparar ambos JSON
```

### 4. 📊 Análisis de Mercado
```bash
# Buscar categoría completa
python buscar_productos_ml.py auriculares
# Analizar: precios promedio, marcas, descuentos
```

---

## 🔥 Comandos Más Usados

```bash
# El comando que usarás el 90% del tiempo
python buscar_productos_ml.py "NOMBRE_PRODUCTO"

# Para aprender más
python ejemplo_uso.py

# Para testing
python get_html.py
```

---

## 🗂️ Estructura del Proyecto

```
📁 Analisis de Productos/
│
├── 🎯 INICIO.md (este archivo)
├── 📖 README.md (documentación completa)
├── ⚡ GUIA_RAPIDA.md (empezar aquí)
├── 📊 RESUMEN_PROYECTO.md (info técnica)
│
├── 🐍 Scripts Principales
│   ├── buscar_productos_ml.py ⭐ (principal)
│   ├── get_html.py
│   └── ejemplo_uso.py
│
├── 🐍 Scripts Legacy
│   ├── get_products.py (no usar)
│   └── get_resenias.py
│
├── 📄 JSON Generados
│   ├── productos_auriculares_*.json
│   ├── productos_celulares_samsung_*.json
│   └── ... (se crean automáticamente)
│
└── 💾 Backup
    └── backup/
```

---

## ❓ FAQ - Preguntas Frecuentes

### ¿Qué hace este proyecto?
Busca productos en Mercado Libre y extrae su información (precio, descuento, link, etc.) automáticamente.

### ¿Es legal?
Sí, para uso personal y educativo. No hagas scraping masivo ni abuses del sistema.

### ¿Funciona con otros países?
Actualmente solo Argentina (.com.ar), pero es fácil adaptarlo.

### ¿Necesito conocimientos de programación?
No para uso básico. Solo ejecuta: `python buscar_productos_ml.py "producto"`

### ¿Cuántos productos encuentra?
Aproximadamente 48-52 productos por búsqueda (primera página de ML).

### ¿Puedo buscar más páginas?
Actualmente no, pero está en el roadmap para futuras versiones.

### ¿Qué hago con el JSON?
- Abrirlo en Excel/Google Sheets
- Analizarlo con Python/pandas
- Visualizarlo con Power BI
- Importarlo a una base de datos

---

## 🆘 Necesitas Ayuda?

### 1. Revisa la documentación
- [GUIA_RAPIDA.md](GUIA_RAPIDA.md) → Problemas comunes
- [README.md](README.md) → Documentación completa

### 2. Ejecuta los ejemplos
```bash
python ejemplo_uso.py
```

### 3. Verifica los logs
El programa muestra mensajes descriptivos de cada paso.

---

## 🎉 ¡Listo para Empezar!

### Opción 1: Guiado (Recomendado)
```bash
# Abre y sigue:
GUIA_RAPIDA.md
```

### Opción 2: Directo al Código
```bash
pip install requests beautifulsoup4
python buscar_productos_ml.py auriculares
```

### Opción 3: Ver Ejemplos Primero
```bash
python ejemplo_uso.py
```

---

## 📊 Estado del Proyecto

- ✅ **Funcional**: 100%
- ✅ **Documentado**: Completo
- ✅ **Testeado**: Windows + Python 3
- ✅ **Producción**: Listo para usar

---

## 🚀 Siguiente Paso

👉 **Lee [GUIA_RAPIDA.md](GUIA_RAPIDA.md)** y ejecuta tu primera búsqueda

---

**¿Dudas? Todos los archivos están comentados y documentados.**

**¡Éxito con tu análisis de productos! 🎯**

