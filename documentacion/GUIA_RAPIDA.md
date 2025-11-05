# 🚀 Guía Rápida - Buscador de Productos Mercado Libre

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar dependencias
```bash
pip install requests beautifulsoup4
```

### 2️⃣ Ejecutar búsqueda
```bash
python buscar_productos_ml.py auriculares
```

### 3️⃣ Ver resultados
El programa generará un archivo JSON con todos los productos:
```
productos_auriculares_20251104_202812.json
```

---

## 📝 Ejemplos de Uso

### Búsqueda Simple
```bash
# Buscar auriculares
python buscar_productos_ml.py auriculares

# Buscar notebooks
python buscar_productos_ml.py notebook

# Buscar celulares específicos
python buscar_productos_ml.py "celulares samsung"
```

### Modo Interactivo
```bash
python buscar_productos_ml.py
# El programa te pedirá que ingreses el producto
```

### Explorar Ejemplos Avanzados
```bash
python ejemplo_uso.py
# Menú interactivo con 7 ejemplos diferentes
```

---

## 📊 Estructura del JSON Generado

```json
{
  "producto_buscado": "auriculares",
  "fecha_busqueda": "2025-11-04 20:28:12",
  "total_productos": 52,
  "productos": [
    {
      "id": "09032fc4",
      "titulo": "Auriculares...",
      "link": "https://...",
      "precio_actual": "$25.109",
      "precio_anterior": "$34.375",
      "descuento": "26% OFF",
      "calificacion": 4.5,
      "vendidos": "+1000 vendidos",
      "imagen": "https://...",
      "envio_gratis": true
    }
  ]
}
```

---

## 🎯 Casos de Uso

### 1. Análisis de Precios
Busca un producto y analiza el rango de precios:
```bash
python buscar_productos_ml.py "notebook gaming"
# Revisar el JSON para encontrar el mejor precio
```

### 2. Encontrar Descuentos
Busca productos en oferta:
```bash
python buscar_productos_ml.py "smart tv 55"
# Filtrar en el JSON por campo "descuento"
```

### 3. Comparar Productos
Busca y compara diferentes categorías:
```bash
python buscar_productos_ml.py "zapatillas nike"
python buscar_productos_ml.py "zapatillas adidas"
# Comparar ambos JSON
```

### 4. Tracking de Precios
Ejecuta búsquedas periódicas:
```bash
# Hoy
python buscar_productos_ml.py "iphone 15"

# Mañana (genera nuevo JSON con timestamp)
python buscar_productos_ml.py "iphone 15"

# Comparar ambos archivos para ver cambios
```

---

## 🔧 Archivos del Proyecto

| Archivo | Descripción | Cuándo usar |
|---------|-------------|-------------|
| `buscar_productos_ml.py` | **Script principal** | ✅ Usar siempre para búsquedas |
| `get_html.py` | Función para obtener HTML | Solo si necesitas customizar |
| `ejemplo_uso.py` | 7 ejemplos avanzados | Para aprender más funciones |
| `get_products.py` | Script original (legacy) | No usar, mantener como backup |
| `get_resenias.py` | Extraer reseñas | Para análisis de opiniones |

---

## 💡 Tips y Mejores Prácticas

### ✅ Hacer
- Agregar delays entre búsquedas múltiples (3-5 segundos)
- Revisar el JSON generado para validar datos
- Usar nombres descriptivos al buscar productos
- Guardar los JSON con timestamp para comparaciones

### ❌ Evitar
- Hacer muchas requests seguidas (riesgo de bloqueo)
- Usar caracteres especiales en las búsquedas
- Eliminar los archivos JSON antiguos (útiles para comparar)
- Buscar productos muy genéricos (ej: solo "celular")

---

## 🐛 Solución de Problemas

### No encuentra productos
```
✅ Solución:
- Verifica tu conexión a internet
- Prueba con otro producto
- Revisa que el producto exista en ML Argentina
```

### Caracteres extraños
```
✅ Solución:
- El script ya maneja UTF-8 automáticamente
- Si persiste, actualiza: pip install --upgrade requests beautifulsoup4
```

### Error de timeout
```
✅ Solución:
- Tu conexión puede ser lenta
- El timeout está en 15 segundos
- Puedes aumentarlo en get_html.py línea 40: timeout=30
```

### Bloqueado por anti-scraping
```
✅ Solución:
- Espera 5-10 minutos antes de volver a buscar
- Reduce la frecuencia de búsquedas
- Usa diferentes productos en lugar de repetir el mismo
```

---

## 🎓 Ejemplos Avanzados

### Buscar y Filtrar en Python
```python
from buscar_productos_ml import buscar_producto_mercadolibre

# Buscar productos
productos = buscar_producto_mercadolibre("notebook")

# Filtrar solo los que tienen descuento
con_descuento = [p for p in productos if p['descuento']]

# Filtrar por precio menor a $100,000
baratos = [p for p in productos 
           if int(p['precio_actual'].replace('$','').replace('.','')) < 100000]

print(f"Productos con descuento: {len(con_descuento)}")
print(f"Productos baratos: {len(baratos)}")
```

### Comparar Precios Automáticamente
```python
import json

# Cargar dos JSON de diferentes fechas
with open('productos_notebook_20251104_100000.json') as f:
    datos_ayer = json.load(f)

with open('productos_notebook_20251104_200000.json') as f:
    datos_hoy = json.load(f)

# Comparar precios (implementación personalizada)
```

---

## 📈 Próximos Pasos

Después de extraer los datos, puedes:

1. **Análisis en Excel/PowerBI**
   - Abrir JSON en Excel
   - Crear tablas dinámicas
   - Visualizar tendencias

2. **Visualización con Python**
   ```bash
   # Crear gráficos con matplotlib/seaborn
   pip install matplotlib pandas
   ```

3. **Dashboard con Streamlit**
   ```bash
   pip install streamlit
   # Crear app interactiva
   ```

4. **Análisis de Sentimientos**
   - Usar `get_resenias.py` para extraer opiniones
   - Analizar con IA (OpenAI, Anthropic, etc.) y obtener el Avatar del Cliente Ideal

5. **Automatización**
   - Crear un script que se ejecute diariamente
   - Usar Windows Task Scheduler o cron (Linux)

---

## 📞 Soporte

Si tienes dudas o problemas:
1. Revisa el `README.md` completo
2. Ejecuta `ejemplo_uso.py` para ver ejemplos
3. Verifica los archivos de backup en `/backup/`

---

**¡Listo para empezar! 🚀**

```bash
python buscar_productos_ml.py
```

