# 🚀 Guía Completa v4.0 - Dashboard con IA

## 🎯 Novedades de la Versión 4.0

### ✨ Mejoras Implementadas

#### 1. 📋 Tabla Mejorada
- ✅ **Campo "Resumen IA"** incluido (join entre productos y análisis)
- ✅ **Descarga en Excel** (.xlsx) en lugar de CSV
- ✅ **Sort correcto** en columnas "Descuento" y "Vendidos"
  - Muestra texto amigable ("+5mil vendidos")
  - Ordena por valores numéricos (5000)
- ✅ **Descuento normalizado**: Si es NULL → "No" (valor numérico 0)

#### 2. 🤖 Chatbot con IA
- ✅ **Widget flotante** en panel derecho
- ✅ **Interfaz vertical** de chat
- ✅ **Groq API** con LLama-3.3-70b
- ✅ **Data Analyst proactivo**
- ✅ **Análisis con pandas** en tiempo real
- ✅ **Lenguaje marketinero** para explicaciones
- ✅ **Prompts sugeridos**:
  - "Analiza todas las opiniones para crear un avatar de cliente ideal"
  - "Sugerime una estrategia para encontrar el mejor precio de venta"
  - "Que me podes explicar de estos datos?"

---

## 🛠️ Instalación

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**requirements.txt incluye**:
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.1.0
groq>=0.4.0
openpyxl>=3.1.2
```

### Paso 2: Configurar API Key de Groq

**Opción 1: Variable de Entorno**
```bash
# Windows
set GROQ_API_KEY=gsk_tu_api_key_aqui

# Linux/Mac
export GROQ_API_KEY=gsk_tu_api_key_aqui
```

**Opción 2: Streamlit Secrets**

Crear archivo `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_tu_api_key_aqui"
```

**Obtener API Key**:
1. Ir a: https://console.groq.com/
2. Crear cuenta gratuita
3. Generar API Key
4. Copiar y configurar

### Paso 3: Ejecutar Dashboard

```bash
streamlit run dashboard_productos_v4.py
```

Se abre automáticamente en: http://localhost:8501

---

## 📊 Características Detalladas

### 1. Join de Datos (Productos + Análisis)

El dashboard ahora hace un **LEFT JOIN** entre:
- `productos_*.json` (por `producto_id`)
- `analisis_resenias_*.json` (por `producto_id`)

**Resultado**: Tabla con columna "Resumen IA" que muestra el análisis de ML.

**Código clave**:
```python
df = df.merge(
    df_analisis[['producto_id', 'resumen_ia', 'opiniones_1_estrella']],
    on='producto_id',
    how='left'
)
```

### 2. Sort Inteligente en Tabla

**Problema resuelto**:
- Antes: "+5mil vendidos" se ordenaba alfabéticamente
- Ahora: Se ordena numéricamente (5000)

**Implementación**:
```python
def extraer_numero_vendidos(vendidos_str):
    if 'mil' in vendidos_lower:
        numero = vendidos_lower.replace('+', '').replace('mil', '')
        return float(numero) * 1000
    else:
        numero = vendidos_lower.replace('+', '').replace('vendidos', '')
        return float(numero)

# Crear columna numérica
df['cantidad_vendidos_num'] = df['vendidos'].apply(extraer_numero_vendidos)

# En tabla, mostrar texto pero ordenar por número
```

**Casos manejados**:
- "+5mil vendidos" → 5000
- "+100 vendidos" → 100
- "+10mil vendidos" → 10000
- "Sin ventas" → 0

### 3. Descarga en Excel (.xlsx)

**Antes**: Descarga CSV (sin formato)
**Ahora**: Excel con formato automático

```python
def crear_excel_descargable(df_mostrar):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_mostrar.to_excel(writer, sheet_name='Productos', index=False)
        # Ajustar anchos de columna automáticamente
    return output
```

**Beneficios**:
- ✅ Formato preservado
- ✅ Anchos de columna ajustados
- ✅ Compatible con Excel/Google Sheets
- ✅ Más profesional

### 4. Chatbot con IA (Groq + LLama)

#### Arquitectura

```
Usuario → Streamlit UI → Groq API → LLama-3.3-70b → Respuesta
                ↓
         Contexto (pandas stats)
```

#### Prompt System

```python
system_prompt = """
Eres un Data Analyst experto en e-commerce y análisis de mercado.
Analizas datos de productos de Mercado Libre con enfoque marketinero.
Tus análisis son concisos, accionables y orientados a resultados.
Usas pandas para manipular datos cuando es necesario.
Explicas gráficos en lenguaje simple y orientado a decisiones.
"""
```

#### Contexto Enviado

El chatbot recibe automáticamente:
- Total de productos
- Precio promedio/min/max
- Calificación promedio
- Productos con envío gratis
- Marcas principales
- Resúmenes de IA (si existen)

#### Prompts Sugeridos

**1. Avatar de Cliente Ideal**
```
Prompt: "Analiza todas las opiniones para crear un avatar de cliente ideal"

Respuesta IA: 
- Perfil demográfico
- Necesidades y dolor points
- Preferencias de compra
- Sensibilidad al precio
```

**2. Estrategia de Precio**
```
Prompt: "Sugerime una estrategia para encontrar el mejor precio de venta"

Respuesta IA:
- Análisis de competencia
- Precio óptimo sugerido
- Estrategia de descuentos
- Posicionamiento
```

**3. Explicación de Datos**
```
Prompt: "Que me podes explicar de estos datos?"

Respuesta IA:
- Insights principales
- Patrones encontrados
- Oportunidades detectadas
- Recomendaciones
```

---

## 💻 Uso del Dashboard v4

### Inicio Rápido

```bash
# 1. Extraer productos
python buscar_productos_ml.py "auriculares bluetooth"

# 2. (Opcional) Analizar reseñas
python analizar_resenias_ia.py productos_auriculares_*.json

# 3. Abrir dashboard
streamlit run dashboard_productos_v4.py

# 4. En el dashboard:
#    - Seleccionar archivo de productos
#    - (Opcional) Seleccionar archivo de análisis
#    - Usar filtros
#    - Preguntar al chatbot IA
```

### Interfaz del Dashboard

```
┌─────────────────────────────────────────────────────┐
│     🛒 Dashboard de Análisis de Productos v4.0     │
└─────────────────────────────────────────────────────┘

 📊 MÉTRICAS
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│MIN  │ │MED  │ │MAX  │ │TOTAL│
└─────┘ └─────┘ └─────┘ └─────┘

 📈 GRÁFICOS
[Dispersión] [Barras] [Torta]

 📋 TABLA (con Resumen IA)
┌─────────────────────────────────────────┐
│Título│Marca│Precio│Resumen IA│...      │
│──────────────────────────────────────── │
│                                          │
│ [Scroll vertical]                        │
└─────────────────────────────────────────┘
[⬇️ Descargar Excel]

 🤖 ASISTENTE IA
[💡 Avatar Cliente] [💰 Estrategia] [📊 Explica]

Chat:
┌─────────────────────────────────────────┐
│Usuario: Analiza opiniones...            │
│IA: Basándome en los datos...           │
└─────────────────────────────────────────┘
[Escribe tu pregunta...]

[SIDEBAR]
📁 Configuración
   - Productos: productos_*.json
   - Análisis: analisis_resenias_*.json ✨
   
🎚️ Filtros
   - Marca
   - Envío gratis
   - Categoría precio
   - Calificación
```

---

## 🎨 Ejemplos de Uso del Chatbot

### Ejemplo 1: Avatar de Cliente

**Usuario**: "Analiza todas las opiniones para crear un avatar de cliente ideal"

**IA**:
```
Basándome en el análisis de 50 productos de auriculares bluetooth:

👤 AVATAR DEL CLIENTE IDEAL: "Carlos, el Melómano Digital"

📊 Demografía:
- Edad: 25-35 años
- Perfil: Profesional joven, urbano
- Ingreso: Medio-alto

💡 Necesidades:
- Busca calidad de audio superior
- Valora la durabilidad (batería >20hrs)
- Prioriza conectividad estable

🎯 Comportamiento de Compra:
- Investiga antes de comprar (lee 10+ reseñas)
- Sensible a descuentos (+20% OFF)
- Valora envío gratis

⚠️ Pain Points Comunes (opiniones 1★):
- Problemas de batería a los 3-6 meses
- Desconexiones bluetooth frecuentes
- Baja calidad de construcción

💰 Rango de Precio Ideal: $20,000 - $45,000
```

### Ejemplo 2: Estrategia de Precio

**Usuario**: "Sugerime una estrategia para encontrar el mejor precio de venta"

**IA**:
```
📊 ANÁLISIS DE MERCADO:

Precio Promedio: $28,500
Rango: $3,104 - $85,000

🎯 ESTRATEGIA RECOMENDADA:

1️⃣ PRECIO COMPETITIVO: $24,900
   - 13% por debajo del promedio
   - Atractivo sin sacrificar percepción de calidad
   
2️⃣ PRECIO PREMIUM: $42,000
   - Si ofreces:
     • Calificación 4.7+
     • Envío gratis
     • Garantía extendida
     
3️⃣ DESCUENTO ESTRATÉGICO:
   - Precio lista: $32,900
   - Con descuento: $24,900 (25% OFF)
   - Genera sensación de oportunidad

📈 RECOMENDACIÓN:
Posicionarte en la categoría "Económico-Mediano" 
(< $25,650) maximiza volumen de ventas según 
correlación precio-ventas del dashboard.

⚡ ACCIÓN INMEDIATA:
Testear $24,900 con 20% OFF promocional
```

### Ejemplo 3: Análisis Exploratorio

**Usuario**: "Qué me podes explicar de estos datos?"

**IA**:
```
📊 INSIGHTS PRINCIPALES:

1. DISTRIBUCIÓN DE PRECIOS
   - 35% productos económicos (< $25,650)
   - 50% gama media ($25,650-$31,350)
   - 15% premium (> $31,350)
   
   💡 Oportunidad: Mercado concentrado en gama media

2. CORRELACIÓN PRECIO-VENTAS
   ⬇️ Productos < $20,000 → Ventas 3x superiores
   📈 Sweet spot: $15,000-$25,000
   
   💡 Estrategia: Posicionamiento en rango óptimo

3. MARCAS DOMINANTES
   🥇 Samsung: 28% del mercado
   🥈 JBL: 18%
   🥉 Sony: 15%
   
   💡 Oportunidad: Marcas menores con precio competitivo

4. ENVÍO GRATIS = VENTAJA COMPETITIVA
   ✅ Con envío gratis: Cal. promedio 4.5
   ❌ Sin envío gratis: Cal. promedio 4.1
   
   💡 Acción: Incluir envío gratis aumenta satisfacción

🎯 RECOMENDACIÓN FINAL:
Enfócate en rango $18,000-$25,000 con envío gratis
para maximizar conversión y satisfacción.
```

---

## ⚙️ Configuración Avanzada

### Cambiar Modelo de IA

En `dashboard_productos_v4.py`, línea ~240:
```python
chat_completion = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Cambiar aquí
    # Otras opciones:
    # - "mixtral-8x7b-32768" (más rápido, menos potente)
    # - "llama-3.2-90b-vision-preview" (si necesitas análisis visual)
)
```

### Ajustar Temperatura

```python
temperature=0.7,  # Default
# 0.0 = Más determinístico
# 1.0 = Más creativo
```

### Cambiar Max Tokens

```python
max_tokens=1000,  # Default
# Aumentar para respuestas más largas
```

---

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not found"

**Solución**:
```bash
# Configurar variable de entorno
export GROQ_API_KEY=gsk_tu_key

# O crear .streamlit/secrets.toml
```

### Error: "No se pudo cargar análisis de reseñas"

**Causa**: No hay archivo de análisis o producto_id no coincide

**Solución**:
1. Verificar que ambos JSON tengan mismo producto
2. Verificar campo `producto_id` existe en ambos
3. El dashboard funciona sin análisis (join opcional)

### Sort no funciona correctamente

**Causa**: Streamlit data_editor tiene limitaciones

**Solución Implementada**:
- Columnas numéricas ocultas para sort
- Mostrar texto amigable
- Ordenar por valor numérico

---

## 📊 Comparación de Versiones

| Feature | v3.0 | v4.0 |
|---------|------|------|
| Cards métricas | ✅ | ✅ |
| Gráficos | ✅ | ✅ |
| Filtros | ✅ | ✅ |
| Tabla básica | ✅ | ✅ |
| **Resumen IA en tabla** | ❌ | ✅ |
| **Descarga Excel** | ❌ | ✅ |
| **Sort correcto** | ❌ | ✅ |
| **Chatbot IA** | ❌ | ✅ |
| **Prompts sugeridos** | ❌ | ✅ |
| **Análisis proactivo** | ❌ | ✅ |

---

## 🎯 Casos de Uso Reales

### Caso 1: Lanzamiento de Producto

```bash
# 1. Investigar competencia
python buscar_productos_ml.py "auriculares bluetooth"

# 2. Analizar opiniones
python analizar_resenias_ia.py productos_*.json

# 3. Dashboard + IA
streamlit run dashboard_productos_v4.py

# 4. Preguntar a IA:
"Analiza todas las opiniones para crear un avatar de cliente ideal"
"Sugerime una estrategia para encontrar el mejor precio de venta"

# Resultado: Estrategia completa basada en datos
```

### Caso 2: Optimización de Precio

```bash
# Dashboard abierto con datos
# Preguntar: "¿Cuál es el precio óptimo para maximizar ventas?"

IA analiza:
- Correlación precio-ventas
- Distribución de competencia
- Sweet spot del mercado
- Sensibilidad al precio

# Resultado: Precio específico recomendado
```

### Caso 3: Análisis de Competencia

```bash
# Usar filtros para segmentar
# Preguntar: "Compara los productos económicos vs premium"

IA analiza:
- Diferencias en features
- Gap de calificación
- Oportunidades de posicionamiento

# Resultado: Estrategia de diferenciación
```

---

## 📈 Roadmap Futuro

### v4.1 (Próximo)
- [ ] Exportar conversación del chatbot
- [ ] Gráficos generados por IA bajo demanda
- [ ] Análisis de sentimiento en tiempo real

### v5.0 (Futuro)
- [ ] Multi-modal: Análisis de imágenes de productos
- [ ] Predicción de precios con ML
- [ ] Alertas automáticas de oportunidades

---

## ✅ Checklist de Uso

- [ ] Instalé dependencias (`pip install -r requirements.txt`)
- [ ] Configuré GROQ_API_KEY
- [ ] Extraje productos con `buscar_productos_ml.py`
- [ ] (Opcional) Analicé reseñas con `analizar_resenias_ia.py`
- [ ] Ejecuté dashboard: `streamlit run dashboard_productos_v4.py`
- [ ] Probé chatbot IA con prompts sugeridos
- [ ] Descargué tabla en Excel
- [ ] Experimenté con filtros

---

## 🎉 **¡Dashboard v4.0 Listo!**

**Nuevas Capacidades**:
- ✅ Tabla con Resumen IA
- ✅ Descarga Excel
- ✅ Sort inteligente
- ✅ Chatbot IA con Groq
- ✅ Análisis proactivo
- ✅ Lenguaje marketinero

**Próximo Paso**:
```bash
streamlit run dashboard_productos_v4.py
```

**Ver más**: `README.md` para guía completa del proyecto

---

**Versión**: 4.0  
**Fecha**: 2025-11-04  
**Estado**: ✅ Funcional  
**IA**: Powered by Groq + LLama-3.3-70b

