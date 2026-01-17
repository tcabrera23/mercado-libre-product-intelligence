# 🐳 Configuración con Docker

Este proyecto ahora incluye soporte completo para Docker, facilitando su despliegue con **Ollama** (modelo local) o **Groq** (API en la nube).

## 📋 Prerrequisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (normalmente viene con Docker Desktop)

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

Esta opción levanta automáticamente:
- La aplicación Streamlit
- Ollama con modelos locales

```bash
# 1. Clonar o descargar el proyecto
cd "Analisis de Productos"

# 2. (Opcional) Configurar variables de entorno
cp .env.example .env
# Edita .env si quieres usar Groq además de Ollama

# 3. Levantar los servicios
docker-compose up -d

# 4. Descargar modelo de Ollama (primera vez)
docker exec -it analisis-productos-ollama ollama pull llama3.2:8b

# 5. Acceder a la aplicación
# Abre tu navegador en: http://localhost:8501
```

### Opción 2: Solo Docker (sin Ollama)

Si solo quieres usar Groq (no Ollama local):

```bash
# 1. Construir imagen
docker build -t analisis-productos .

# 2. Ejecutar contenedor
docker run -d \
  -p 8501:8501 \
  -e GROQ_API_KEY=tu_api_key \
  -v $(pwd)/productos:/app/productos \
  -v $(pwd)/resenias:/app/resenias \
  --name analisis-productos \
  analisis-productos

# 3. Acceder
# Abre tu navegador en: http://localhost:8501
```

## 🤖 Configuración de Modelos IA

### Usar Ollama (Modelo Local)

**Ventajas:**
- ✅ Gratis y sin límites
- ✅ Privacidad total (datos locales)
- ✅ No requiere API keys

**Desventajas:**
- ⚠️ Requiere más recursos (RAM/GPU)
- ⚠️ Más lento que Groq

```bash
# Descargar modelos disponibles
docker exec -it analisis-productos-ollama ollama pull llama3.2:8b
docker exec -it analisis-productos-ollama ollama pull llama3.2:3b   # Más liviano
docker exec -it analisis-productos-ollama ollama pull mistral:7b

# Listar modelos instalados
docker exec -it analisis-productos-ollama ollama list

# En el dashboard, selecciona:
# Proveedor: ollama
# URL: http://ollama:11434 (ya configurado en docker-compose)
# Modelo: llama3.2:8b
```

### Usar Groq (API en la nube)

**Ventajas:**
- ✅ Muy rápido
- ✅ No requiere recursos locales
- ✅ Modelos potentes (llama-3.3-70b)

**Desventajas:**
- ⚠️ Requiere API key (gratis con límites)
- ⚠️ Envía datos a la nube

```bash
# 1. Obtén tu API key en: https://console.groq.com/

# 2. Configura la variable de entorno
# Edita .env:
GROQ_API_KEY=tu_api_key_aqui

# 3. Reinicia los servicios
docker-compose down
docker-compose up -d

# En el dashboard, selecciona:
# Proveedor: groq
```

## 📦 Estructura de Carpetas

```
Analisis de Productos/
├── productos/           # JSONs de productos (persistentes)
├── resenias/            # JSONs de reseñas (persistentes)
├── dashboard_productos_v4.py
├── buscar_productos_ml.py
├── analizar_resenias_ia.py
├── llm_config.py        # Módulo de configuración LLM
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

Los datos en `productos/` y `resenias/` se mantienen aunque elimines los contenedores.

## 🔧 Comandos Útiles

```bash
# Ver logs de la aplicación
docker-compose logs -f app

# Ver logs de Ollama
docker-compose logs -f ollama

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra modelos de Ollama)
docker-compose down -v

# Actualizar la aplicación
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Entrar al contenedor de la app
docker exec -it analisis-productos-app bash

# Entrar al contenedor de Ollama
docker exec -it analisis-productos-ollama bash
```

## 🐛 Troubleshooting

### Error: "No se pudo conectar a Ollama"

```bash
# Verificar que Ollama esté corriendo
docker ps | grep ollama

# Ver logs de Ollama
docker-compose logs ollama

# Reiniciar Ollama
docker-compose restart ollama
```

### Error: "No hay modelos en Ollama"

```bash
# Descargar un modelo
docker exec -it analisis-productos-ollama ollama pull llama3.2:8b

# Verificar modelos instalados
docker exec -it analisis-productos-ollama ollama list
```

### La aplicación no carga

```bash
# Ver logs de la app
docker-compose logs app

# Verificar que el puerto 8501 esté libre
netstat -an | grep 8501  # Linux/Mac
netstat -an | findstr 8501  # Windows
```

### Puerto 11434 ya en uso

Si ya tienes Ollama instalado localmente:

```bash
# Opción 1: Usar Ollama local (sin Docker)
# Edita docker-compose.yml y comenta el servicio ollama
# En .env configura: OLLAMA_BASE_URL=http://host.docker.internal:11434

# Opción 2: Cambiar puerto en docker-compose.yml
# ports:
#   - "11435:11434"  # Cambiar a puerto diferente
```

## 📊 Recomendaciones de Modelos

### Para hardware limitado (< 8GB RAM):
- `llama3.2:3b` - Modelo pequeño y rápido
- `phi3:mini` - Muy eficiente

### Para hardware medio (8-16GB RAM):
- `llama3.2:8b` - **Recomendado**, buen balance
- `mistral:7b` - Alternativa sólida

### Para hardware potente (> 16GB RAM + GPU):
- `llama3.1:13b` - Excelente calidad
- `mixtral:8x7b` - Muy potente

### Usar Groq (recomendado para producción):
- No requiere recursos locales
- Modelos más potentes: `llama-3.3-70b-versatile`
- Límite gratuito: suficiente para uso normal

## 🌐 Producción

Para desplegar en producción:

```bash
# 1. Edita docker-compose.yml
# Comenta la línea de montar código:
# - .:/app  # <-- Comentar esta línea

# 2. Configura .env con tus API keys

# 3. Levanta servicios
docker-compose up -d

# 4. (Opcional) Usa un proxy inverso como nginx
```

## 📝 Notas

- Los modelos de Ollama se descargan la primera vez (pueden ser varios GB)
- Los datos en `productos/` y `resenias/` persisten entre reinicios
- Puedes usar Groq + Ollama simultáneamente, cambiando en el dashboard
- Para mejor rendimiento con Ollama, considera usar GPU (requiere NVIDIA Docker)

---

**¿Problemas?** Abre un issue en el repositorio o consulta la documentación de [Ollama](https://ollama.ai) o [Groq](https://groq.com).
