# 📝 Changelog - Sistema de Scraping Mercado Libre

Registro de cambios y mejoras del proyecto.

---

## [v2.1] - 2025-11-04

### ✨ Mejoras Importantes

#### 🔧 Extracción de Campos Corregida

**Problema**: Los campos `calificacion`, `vendidos` y `envio` no se estaban extrayendo correctamente del HTML.

**Solución**: Actualización completa de los selectores CSS basados en la estructura HTML real de Mercado Libre.

#### 📊 Cambios en el Formato de Datos

1. **Campo `calificacion`**
   - Antes: `"calificacion": "4.5"` (string)
   - Ahora: `"calificacion": 4.5` (float o null)
   - Selector: `<span class="poly-phrase-label">4.5</span>`

2. **Campo `vendidos`**
   - Antes: No se extraía correctamente
   - Ahora: `"vendidos": "+25 vendidos"` (string con texto completo)
   - Selector: `<span class="poly-phrase-label">| +25 vendidos</span>`
   - Nota: Se limpia el carácter "|" inicial

3. **Campo `envio` → `envio_gratis`**
   - Antes: `"envio": "Envío gratis"` (string)
   - Ahora: `"envio_gratis": true` (boolean)
   - Selector: `<div class="poly-component__shipping">`
   - Lógica: `true` si el texto contiene la palabra "gratis"

#### 🎨 Mejoras en la UI

**Resumen en Consola**:
```
⭐ 5.0 | +25 vendidos
🚚 ✅ Envío gratis
```

**Antes**:
```
⭐ No disponible | No disponible
🚚 No disponible
```

### 📝 Archivos Modificados

- ✅ `buscar_productos_ml.py` - Lógica de extracción actualizada
- ✅ `ejemplo_uso.py` - Ejemplos actualizados para nuevos campos
- ✅ `README.md` - Documentación actualizada
- ✅ `GUIA_RAPIDA.md` - Ejemplos JSON actualizados
- ✅ `RESUMEN_PROYECTO.md` - Especificaciones técnicas actualizadas

### 🧪 Tests Realizados

✅ Búsqueda "ipad" - 50 productos extraídos correctamente
- Calificaciones: 5.0, 4.9 (float)
- Vendidos: "+25 vendidos", "+100 vendidos", "+10mil vendidos"
- Envío gratis: 100% de los productos (true)

### 💡 Ejemplo de Datos Antes/Después

#### Antes (v2.0)
```json
{
  "calificacion": "No disponible",
  "vendidos": "No disponible",
  "envio": "No disponible"
}
```

#### Después (v2.1)
```json
{
  "calificacion": 5.0,
  "vendidos": "+25 vendidos",
  "envio_gratis": true
}
```

---

## [v2.0] - 2025-11-04

### 🎉 Versión Dinámica

#### ✨ Características Principales

- ✅ Búsqueda dinámica por URL (cualquier producto)
- ✅ Bypass anti-scraping con headers HTTP
- ✅ Manejo de encoding UTF-8 en Windows
- ✅ Extracción inteligente de sección HTML
- ✅ IDs únicos por producto (UUID)
- ✅ Export a JSON con timestamp
- ✅ Resumen visual en consola
- ✅ Manejo robusto de errores

#### 📁 Archivos Creados

- `buscar_productos_ml.py` - Script principal
- `get_html.py` - Función para obtener HTML
- `ejemplo_uso.py` - 7 ejemplos de uso
- `README.md` - Documentación completa
- `GUIA_RAPIDA.md` - Tutorial rápido
- `RESUMEN_PROYECTO.md` - Especificaciones técnicas
- `INICIO.md` - Punto de entrada

#### 🔧 Mejoras vs v1.0

| Aspecto | v1.0 | v2.0 |
|---------|------|------|
| HTML | Manual (copiar/pegar) | ✅ Automático |
| Producto | Solo "auriculares" | ✅ Cualquiera |
| Anti-scraping | ❌ Bloqueado | ✅ Bypass completo |
| Encoding | ❌ Caracteres raros | ✅ UTF-8 |
| Documentación | Ninguna | ✅ Completa |

---

## [v1.0] - 2025-11-03 (Legacy)

### 📌 Versión Original

- Script `get_products.py`
- HTML hardcodeado (estatico)
- Solo funciona con "auriculares"
- Sin bypass anti-scraping
- Sin documentación

**Estado**: Movido a `backup/` como referencia

---

## 🔮 Próximas Versiones (Roadmap)

### [v2.2] - Planificado
- [ ] Paginación (extraer más de 50 productos)
- [ ] Filtros de búsqueda (precio min/max)
- [ ] Export a CSV/Excel
- [ ] Retry automático en caso de error

### [v3.0] - Futuro
- [ ] Dashboard con Streamlit
- [ ] Base de datos SQLite
- [ ] Tracking histórico de precios
- [ ] API REST
- [ ] Análisis de reseñas con IA

---

## 📊 Estadísticas por Versión

| Versión | Archivos | Líneas Código | Tests | Docs |
|---------|----------|---------------|-------|------|
| v1.0    | 1        | ~138          | 0     | ❌   |
| v2.0    | 3        | ~650          | 2     | ✅   |
| v2.1    | 3        | ~670          | 3     | ✅   |

---

## 🐛 Bugs Conocidos

### v2.1
- Ninguno reportado

### v2.0
- ~~Campos calificacion, vendidos y envio no se extraen~~ → ✅ Corregido en v2.1

---

## 🙏 Agradecimientos

- Usuario por reportar el bug de extracción de campos
- DeepSeek por la versión original
- Comunidad de BeautifulSoup

---

**Última actualización**: 2025-11-04

