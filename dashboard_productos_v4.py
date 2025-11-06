"""
Dashboard interactivo v4.0 para análisis de productos de Mercado Libre
Con Chatbot IA integrado (Groq + LLama)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import io
from groq import Groq

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Productos ML v4",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FFE600;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #2D3561 0%, #3483FA 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Chat Widget Styles */
    .chat-widget-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
        transition: transform 0.3s ease;
    }
    
    .chat-widget-button:hover {
        transform: scale(1.1);
    }
    
    .chat-widget-container {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 400px;
        max-height: 600px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        z-index: 998;
        overflow: hidden;
    }
    
    .chat-widget-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .stChatFloatingInputContainer {
        bottom: 90px;
    }
</style>
""", unsafe_allow_html=True)


# Funciones auxiliares
def limpiar_precio(precio_str):
    """Convierte string de precio a número"""
    try:
        return int(str(precio_str).replace('$', '').replace('.', '').replace(',', ''))
    except:
        return 0


def extraer_marca(titulo):
    """Extrae la marca del título"""
    marcas_comunes = [
        'Samsung', 'Apple', 'Xiaomi', 'Motorola', 'iPhone', 'iPad',
        'Logitech', 'Redragon', 'HyperX', 'Razer', 'Corsair',
        'Sony', 'JBL', 'Harman', 'Bose', 'Audio-Technica',
        'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI',
        'Nike', 'Adidas', 'Puma', 'Reebok'
    ]
    
    titulo_upper = titulo.upper()
    for marca in marcas_comunes:
        if marca.upper() in titulo_upper:
            return marca
    
    return titulo.split()[0] if titulo.split() else "Sin marca"


def extraer_numero_vendidos(vendidos_str):
    """Extrae número de vendidos para ordenamiento"""
    if pd.isna(vendidos_str) or vendidos_str == "Sin ventas":
        return 0
    try:
        vendidos_lower = str(vendidos_str).lower()
        if 'mil' in vendidos_lower:
            numero = vendidos_lower.replace('+', '').replace('mil', '').replace('vendidos', '').strip()
            return float(numero) * 1000
        else:
            numero = vendidos_lower.replace('+', '').replace('vendidos', '').strip()
            return float(numero)
    except:
        return 0


def extraer_numero_descuento(descuento_str):
    """Extrae número de descuento para ordenamiento"""
    if pd.isna(descuento_str) or descuento_str in ["", "0%", "No"]:
        return 0
    try:
        numero = str(descuento_str).replace('%', '').replace('OFF', '').replace('off', '').strip()
        return float(numero)
    except:
        return 0


def clasificar_precio(precio, promedio):
    """Clasifica precio en categorías"""
    if precio < promedio * 0.9:
        return "Económico"
    elif precio > promedio * 1.1:
        return "Caro"
    else:
        return "Mediano"


@st.cache_data
def cargar_datos(archivo_json_productos, archivo_json_analisis=None):
    """Carga y procesa los datos del JSON, con join opcional de análisis"""
    # Cargar productos
    with open(archivo_json_productos, 'r', encoding='utf-8') as f:
        data_productos = json.load(f)
    
    productos = data_productos.get('productos', [])
    df = pd.DataFrame(productos)
    
    # Procesar datos básicos
    df['precio_numerico'] = df['precio_actual'].apply(limpiar_precio)
    df['marca'] = df['titulo'].apply(extraer_marca)
    df['cantidad_vendidos_num'] = df['vendidos'].apply(extraer_numero_vendidos)
    df['descuento_num'] = df['descuento'].apply(extraer_numero_descuento)
    df['envio_gratis_texto'] = df['envio_gratis'].apply(lambda x: 'Sí' if x else 'No')
    
    # Normalizar descuento: si es vacío o 0%, mostrar "No"
    df['descuento_mostrar'] = df['descuento'].apply(
        lambda x: "No" if pd.isna(x) or x in ["", "0%"] else x
    )
    
    # Clasificar por precio
    promedio = df['precio_numerico'].mean()
    df['categoria_precio'] = df['precio_numerico'].apply(lambda x: clasificar_precio(x, promedio))
    
    # JOIN con análisis de reseñas si existe
    data_analisis_completo = None
    if archivo_json_analisis and os.path.exists(archivo_json_analisis):
        try:
            with open(archivo_json_analisis, 'r', encoding='utf-8') as f:
                data_analisis_completo = json.load(f)
            
            df_analisis = pd.DataFrame(data_analisis_completo.get('productos', []))
            if not df_analisis.empty and 'producto_id' in df_analisis.columns:
                # JOIN por 'id' (productos) con 'producto_id' (análisis)
                df = df.merge(
                    df_analisis[['producto_id', 'resumen_ia', 'opiniones_1_estrella']],
                    left_on='id',
                    right_on='producto_id',
                    how='left'
                )
                # Eliminar columna duplicada producto_id
                if 'producto_id' in df.columns:
                    df = df.drop(columns=['producto_id'])
        except Exception as e:
            st.warning(f"No se pudo cargar análisis de reseñas: {e}")
    
    # Si no hay resumen_ia (no se hizo merge o no matcheó), crear columna con None
    if 'resumen_ia' not in df.columns:
        df['resumen_ia'] = None
    
    # Rellenar NaN en resumen_ia con texto descriptivo
    df['resumen_ia'] = df['resumen_ia'].fillna("Sin análisis disponible")
    
    # Retornar también los JSONs completos para el agente de IA
    return df, data_productos.get('producto_buscado', 'Productos'), data_productos, data_analisis_completo


def crear_excel_descargable(df_mostrar):
    """Crea un archivo Excel en memoria para descargar"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_mostrar.to_excel(writer, sheet_name='Productos', index=False)
        
        # Ajustar anchos de columna
        worksheet = writer.sheets['Productos']
        for idx, col in enumerate(df_mostrar.columns, 1):
            max_length = max(
                df_mostrar[col].astype(str).apply(len).max(),
                len(str(col))
            )
            max_length = min(max_length, 50)
            worksheet.column_dimensions[chr(64 + idx)].width = max_length + 2
    
    output.seek(0)
    return output


def ejecutar_scraping_producto(producto_nombre):
    """Ejecuta el scraping de productos usando buscar_productos_ml.py"""
    import subprocess
    try:
        # Ejecutar script de búsqueda de productos
        result = subprocess.run(
            ['python', 'buscar_productos_ml.py', producto_nombre],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos timeout
        )
        
        if result.returncode == 0:
            # Buscar el archivo JSON generado más reciente
            archivos = [f for f in os.listdir('.') if f.startswith('productos_') and producto_nombre.replace(' ', '_') in f and f.endswith('.json')]
            if archivos:
                archivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return True, archivos[0], "Productos extraídos exitosamente"
            else:
                return False, None, "No se generó el archivo JSON"
        else:
            return False, None, f"Error en scraping: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, None, "Timeout: El scraping tomó demasiado tiempo"
    except Exception as e:
        return False, None, f"Error inesperado: {str(e)}"


def ejecutar_analisis_resenias(archivo_productos):
    """Ejecuta el análisis de reseñas usando analizar_resenias_ia.py"""
    import subprocess
    try:
        # Ejecutar script de análisis de reseñas (versión simplificada - solo resumen IA)
        result = subprocess.run(
            ['python', 'analizar_resenias_ia.py', archivo_productos],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout (más rápido ahora sin opiniones individuales)
        )
        
        if result.returncode == 0:
            # Buscar el archivo JSON de análisis generado más reciente
            archivos = [f for f in os.listdir('.') if f.startswith('analisis_resenias_') and f.endswith('.json')]
            if archivos:
                archivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return True, archivos[0], "Análisis de reseñas completado"
            else:
                return False, None, "No se generó el archivo de análisis"
        else:
            return False, None, f"Error en análisis: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, None, "Timeout: El análisis tomó demasiado tiempo (>5 min)"
    except Exception as e:
        return False, None, f"Error inesperado: {str(e)}"


def analizar_con_ia(prompt, df, groq_client, json_productos=None, json_analisis=None):
    """Analiza datos usando Groq AI con acceso a JSONs completos"""
    try:
        # Preparar contexto con estadísticas
        stats = f"""
Datos del Dashboard:
- Total productos: {len(df)}
- Precio promedio: ${df['precio_numerico'].mean():,.0f}
- Precio mínimo: ${df['precio_numerico'].min():,.0f}
- Precio máximo: ${df['precio_numerico'].max():,.0f}
- Calificación promedio: {df['calificacion'].mean():.2f}
- Productos con envío gratis: {len(df[df['envio_gratis']==True])}
- Marcas principales: {', '.join(df['marca'].value_counts().head(5).index.tolist())}
"""
        
        # Agregar información de reseñas si existe
        if 'resumen_ia' in df.columns and df['resumen_ia'].notna().any():
            resumenes = df[df['resumen_ia'].notna()]['resumen_ia'].head(3).tolist()
            stats += f"\n\nEjemplos de Resúmenes de IA de ML:\n" + "\n".join([f"- {r[:200]}..." for r in resumenes if r])
        
        # Agregar contexto de JSONs completos si están disponibles
        contexto_json = ""
        if json_productos:
            # Incluir algunos productos de ejemplo
            productos_sample = json_productos.get('productos', [])[:5]
            contexto_json += f"\n\nEjemplo de estructura de productos (primeros 5 de {len(json_productos.get('productos', []))}):\n"
            contexto_json += json.dumps(productos_sample, ensure_ascii=False, indent=2)[:2000]
        
        if json_analisis:
            # Incluir análisis completos disponibles
            analisis_sample = json_analisis.get('productos', [])[:3]
            contexto_json += f"\n\nEjemplo de análisis con opiniones (primeros 3 de {json_analisis.get('total_con_resumen_ia', 0)} con resumen):\n"
            contexto_json += json.dumps(analisis_sample, ensure_ascii=False, indent=2)[:2000]
        
        system_prompt = """Eres un Data Analyst experto especializado en e-commerce y análisis de mercado.
Analizas datos de productos de Mercado Libre con un enfoque marketinero y práctico.
Tus análisis son concisos, accionables y orientados a resultados de negocio.
Tienes acceso completo a los datos de productos y reseñas de clientes.
Cuando te preguntan sobre opiniones, puedes hacer referencia a los resúmenes generados por IA y las opiniones negativas (1 estrella).
Cuando explicas insights, lo haces en lenguaje simple, con bullet points y orientado a decisiones de negocio."""

        # Llamar a Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{stats}{contexto_json}\n\nPregunta del usuario: {prompt}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1500
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error al procesar con IA: {str(e)}"


def main():
    # Verificar API Key de Groq
    groq_api_key = "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" # os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        groq_api_key = st.secrets.get("GROQ_API_KEY", None)
    
    groq_client = None
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
    
    # Header
    st.markdown('<div class="main-header">🛒 Dashboard de Análisis de Productos v4.0</div>', unsafe_allow_html=True)
    
    # Sidebar - Cargar archivo
    st.sidebar.title("📁 Configuración")
    
    # === BARRA DE BÚSQUEDA EN TIEMPO REAL ===
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Búsqueda en Tiempo Real")
    st.sidebar.caption("Busca un producto y obtén datos + reseñas")
    
    # Input de búsqueda
    with st.sidebar.form(key="search_form", clear_on_submit=False):
        producto_buscar = st.text_input(
            "Nombre del producto:",
            placeholder="ej: auriculares bluetooth",
            help="Escribe el nombre del producto a buscar en Mercado Libre"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            buscar_productos_btn = st.form_submit_button("🔍 Buscar", use_container_width=True)
        with col2:
            analizar_resenias_checkbox = st.checkbox("Incluir reseñas", value=True, help="Analizar reseñas (toma más tiempo)")
    
    # Procesar búsqueda
    if buscar_productos_btn and producto_buscar:
        with st.sidebar:
            with st.spinner(f"🔍 Buscando '{producto_buscar}'..."):
                # Paso 1: Scraping de productos
                exito_productos, archivo_productos_nuevo, mensaje_productos = ejecutar_scraping_producto(producto_buscar)
                
                if exito_productos:
                    st.success(f"✅ {mensaje_productos}")
                    st.info(f"📄 Archivo: {archivo_productos_nuevo}")
                    
                    # Paso 2: Análisis de reseñas (si está marcado)
                    if analizar_resenias_checkbox:
                        with st.spinner(f"🤖 Analizando reseñas... (puede tomar 2-5 min)"):
                            exito_analisis, archivo_analisis_nuevo, mensaje_analisis = ejecutar_analisis_resenias(archivo_productos_nuevo)
                            
                            if exito_analisis:
                                st.success(f"✅ {mensaje_analisis}")
                                st.info(f"📄 Archivo: {archivo_analisis_nuevo}")
                            else:
                                st.warning(f"⚠️ {mensaje_analisis}")
                    
                    st.success("🎉 ¡Búsqueda completada! Recarga la página o selecciona los nuevos archivos abajo.")
                    st.button("🔄 Recargar Dashboard", on_click=lambda: st.rerun())
                else:
                    st.error(f"❌ {mensaje_productos}")
    
    st.sidebar.markdown("---")
    
    # Listar archivos JSON disponibles
    archivos_productos = [f for f in os.listdir('.') if f.startswith('productos_') and f.endswith('.json')]
    archivos_analisis = [f for f in os.listdir('.') if f.startswith('analisis_resenias_') and f.endswith('.json')]
    
    if not archivos_productos:
        st.error("❌ No se encontraron archivos JSON de productos")
        st.info("💡 Ejecuta: `python buscar_productos_ml.py 'producto'`")
        return
    
    archivo_productos = st.sidebar.selectbox(
        "Archivo de productos:",
        archivos_productos,
        index=0
    )
    
    # Selector opcional de análisis
    archivo_analisis = None
    if archivos_analisis:
        usar_analisis = st.sidebar.checkbox("Incluir análisis de reseñas", value=True)
        if usar_analisis:
            archivo_analisis = st.sidebar.selectbox(
                "Archivo de análisis:",
                archivos_analisis,
                index=0
            )
    
    # Cargar datos (ahora retorna 4 valores: df, nombre_producto, json_productos, json_analisis)
    try:
        df, producto_buscado, json_productos_completo, json_analisis_completo = cargar_datos(archivo_productos, archivo_analisis)
    except Exception as e:
        st.error(f"❌ Error al cargar: {e}")
        return
    
    st.sidebar.success(f"✅ {len(df)} productos cargados")
    st.sidebar.info(f"🔍 Producto: **{producto_buscado}**")
    
    # FILTROS / SLICERS
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎚️ Filtros")
    
    # Filtro por marca
    marca_filtro = st.sidebar.multiselect(
        "Marca:",
        sorted(df['marca'].unique().tolist()),
        default=[]
    )
    
    # Filtro por envío gratis
    envio_filtro = st.sidebar.radio(
        "Envío gratis:",
        ["Todos", "Sí", "No"]
    )
    
    # Filtro por categoría de precio
    categoria_filtro = st.sidebar.multiselect(
        "Categoría de precio:",
        ["Económico", "Mediano", "Caro"],
        default=["Económico", "Mediano", "Caro"]
    )
    
    # Filtro por rango de calificación
    if df['calificacion'].max() > 0:
        cal_min, cal_max = st.sidebar.slider(
            "Rango de calificación:",
            float(df['calificacion'].min()),
            float(df['calificacion'].max()),
            (float(df['calificacion'].min()), float(df['calificacion'].max())),
            step=0.1
        )
    else:
        cal_min, cal_max = 0.0, 5.0
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if marca_filtro:
        df_filtrado = df_filtrado[df_filtrado['marca'].isin(marca_filtro)]
    
    if envio_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado['envio_gratis_texto'] == envio_filtro]
    
    if categoria_filtro:
        df_filtrado = df_filtrado[df_filtrado['categoria_precio'].isin(categoria_filtro)]
    
    df_filtrado = df_filtrado[
        (df_filtrado['calificacion'] >= cal_min) & 
        (df_filtrado['calificacion'] <= cal_max)
    ]
    
    st.sidebar.markdown(f"**📊 Productos filtrados: {len(df_filtrado)}**")
    
    # CARDS DE MÉTRICAS
    st.markdown("### 📊 Métricas Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Precio Mínimo", f"${df_filtrado['precio_numerico'].min():,.0f}")
    
    with col2:
        st.metric("💵 Precio Mediano", f"${df_filtrado['precio_numerico'].median():,.0f}")
    
    with col3:
        st.metric("💸 Precio Máximo", f"${df_filtrado['precio_numerico'].max():,.0f}")
    
    with col4:
        delta_text = f"{len(df_filtrado) - len(df)} filtrados" if len(df_filtrado) != len(df) else None
        st.metric("📦 Total Productos", f"{len(df_filtrado)}", delta=delta_text)
    
    st.markdown("---")
    
    # GRÁFICOS
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown("### 📈 Relación Precio vs Ventas")
        st.caption("¿A menor precio, más ventas?")
        
        df_scatter = df_filtrado[df_filtrado['cantidad_vendidos_num'] > 0].copy()
        
        if len(df_scatter) > 0:
            fig_scatter = px.scatter(
                df_scatter,
                x='precio_numerico',
                y='cantidad_vendidos_num',
                color='categoria_precio',
                size='calificacion',
                hover_data=['titulo', 'marca'],
                labels={
                    'precio_numerico': 'Precio ($)',
                    'cantidad_vendidos_num': 'Cantidad Vendidos',
                    'categoria_precio': 'Categoría'
                },
                color_discrete_map={
                    'Económico': '#2ecc71',
                    'Mediano': '#3498db',
                    'Caro': '#e74c3c'
                }
            )
            fig_scatter.update_layout(height=400, xaxis_tickformat='$,.0f')
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No hay datos de ventas disponibles")
    
    with col_der:
        st.markdown("### ⭐ Precio Promedio por Calificación")
        st.caption("Relación entre precio y satisfacción")
        
        df_calif = df_filtrado[df_filtrado['calificacion'] > 0].copy()
        
        if len(df_calif) > 0:
            df_calif['calificacion_redondeada'] = df_calif['calificacion'].round(1)
            precio_por_calif = df_calif.groupby('calificacion_redondeada')['precio_numerico'].mean().reset_index()
            precio_por_calif = precio_por_calif.sort_values('calificacion_redondeada')
            
            fig_barras = px.bar(
                precio_por_calif,
                x='calificacion_redondeada',
                y='precio_numerico',
                labels={
                    'calificacion_redondeada': 'Calificación',
                    'precio_numerico': 'Precio Promedio ($)'
                },
                color='precio_numerico',
                color_continuous_scale='Blues'
            )
            fig_barras.update_layout(height=400, yaxis_tickformat='$,.0f', showlegend=False)
            st.plotly_chart(fig_barras, use_container_width=True)
        else:
            st.info("No hay datos de calificación disponibles")
    
    st.markdown("---")
    
    # Gráfico de Torta
    col_torta, col_espacio = st.columns([2, 1])
    
    with col_torta:
        st.markdown("### 🏆 Marcas Más Populares")
        st.caption("Distribución de productos por marca")
        
        marcas_count = df_filtrado['marca'].value_counts().head(10)
        fig_torta = px.pie(
            values=marcas_count.values,
            names=marcas_count.index,
            hole=0.4
        )
        fig_torta.update_layout(height=500)
        fig_torta.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_torta, use_container_width=True)
    
    st.markdown("---")
    
    # TABLA DE DATOS
    st.markdown("### 📋 Tabla de Productos")
    st.caption(f"Total: {len(df_filtrado)} productos")
    
    # Columnas a mostrar (ahora incluye 'link')
    columnas_base = ['titulo', 'marca', 'precio_actual', 'categoria_precio',
                     'calificacion', 'vendidos', 'envio_gratis_texto', 'descuento_mostrar', 'link']
    
    if 'resumen_ia' in df_filtrado.columns:
        columnas_base.insert(4, 'resumen_ia')
    
    df_mostrar = df_filtrado[columnas_base].copy()
    
    # Renombrar columnas
    nombres_columnas = {
        'titulo': 'Título',
        'marca': 'Marca',
        'precio_actual': 'Precio',
        'categoria_precio': 'Categoría',
        'calificacion': 'Calificación',
        'vendidos': 'Vendidos',
        'envio_gratis_texto': 'Envío Gratis',
        'descuento_mostrar': 'Descuento',
        'link': 'Link'
    }
    
    if 'resumen_ia' in df_mostrar.columns:
        nombres_columnas['resumen_ia'] = 'Resumen IA'
    
    df_mostrar = df_mostrar.rename(columns=nombres_columnas)
    
    # Convertir columnas a tipos numéricos para filtrado dinámico
    # Columna Precio: Extraer valor numérico
    df_mostrar['Precio_num'] = df_filtrado['precio_numerico'].values
    
    # Columna Descuento: Extraer valor numérico entero
    df_mostrar['Descuento_num'] = df_filtrado['descuento_num'].values.astype(int)
    
    # Configurar columna config para sort, tipos y link clickeable
    column_config = {
        "Precio": st.column_config.NumberColumn(
            "Precio",
            help="Precio actual del producto",
            format="$%.0f"
        ),
        "Precio_num": st.column_config.NumberColumn(
            "Precio (num)",
            help="Precio numérico para filtrado",
            format="$%.2f"
        ),
        "Vendidos": st.column_config.TextColumn(
            "Vendidos",
            help="Cantidad de productos vendidos"
        ),
        "Descuento": st.column_config.TextColumn(
            "Descuento",
            help="Porcentaje de descuento"
        ),
        "Descuento_num": st.column_config.NumberColumn(
            "Descuento (%)",
            help="Descuento numérico para filtrado",
            format="%d%%"
        ),
        "Link": st.column_config.LinkColumn(
            "Link",
            help="Link al producto en Mercado Libre",
            display_text="Ver Producto 🔗"
        ),
        "Resumen IA": st.column_config.TextColumn(
            "Resumen IA",
            help="Resumen generado por IA de Mercado Libre",
            width="large"
        ),
    }
    
    # Mostrar tabla
    st.dataframe(
        df_mostrar,
        use_container_width=True,
        height=400,
        column_config=column_config
    )
    
    # Botón de descarga XLSX
    excel_file = crear_excel_descargable(df_mostrar)
    
    st.download_button(
        label="⬇️ Descargar datos filtrados (Excel)",
        data=excel_file,
        file_name=f"productos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # CHATBOT IA - Widget Flotante (al final de la página)
    st.markdown("---")
    st.markdown("## 🤖 Asistente IA - Data Analyst")
    
    # Inicializar estado del chat
    if "chat_abierto" not in st.session_state:
        st.session_state.chat_abierto = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if groq_client:
        # Toggle para abrir/cerrar chat
        col_chat1, col_chat2 = st.columns([3, 1])
        with col_chat1:
            st.markdown("**Pregunta al asistente sobre productos, precios, opiniones y estrategias de mercado**")
        with col_chat2:
            chat_expandido = st.checkbox("Abrir Chat", value=st.session_state.chat_abierto, key="toggle_chat")
            st.session_state.chat_abierto = chat_expandido
        
        if chat_expandido:
            # Prompts sugeridos en columnas
            st.markdown("##### 💬 Prompts Sugeridos:")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("💡 Avatar de Cliente", use_container_width=True):
                    st.session_state.prompt_sugerido = "Analiza todas las opiniones para crear un avatar de cliente ideal con características demográficas, psicográficas y necesidades específicas"
            
            with col2:
                if st.button("💰 Estrategia de Precio", use_container_width=True):
                    st.session_state.prompt_sugerido = "Sugerime una estrategia para encontrar el mejor precio de venta del producto analizado basado en la competencia y la percepción de valor"
            
            with col3:
                if st.button("📊 Explica Insights", use_container_width=True):
                    st.session_state.prompt_sugerido = "Explícame los insights más importantes de estos datos desde una perspectiva de marketing y ventas"
            
            with col4:
                if st.button("⭐ Análisis Opiniones", use_container_width=True):
                    st.session_state.prompt_sugerido = "Resume los puntos principales de las opiniones de clientes, tanto positivos como negativos"
            
            st.markdown("---")
            
            # Historial de mensajes (scrollable)
            chat_container = st.container(height=400)
            with chat_container:
                if len(st.session_state.messages) == 0:
                    st.info("👋 ¡Hola! Soy tu asistente de análisis de datos. Pregúntame lo que quieras sobre los productos.")
                
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            
            # Input de chat
            if "prompt_sugerido" in st.session_state:
                prompt = st.session_state.prompt_sugerido
                del st.session_state.prompt_sugerido
            else:
                prompt = st.chat_input("Escribe tu pregunta aquí...", key="chat_input_widget")
            
            # Procesar nuevo mensaje
            if prompt:
                # Agregar mensaje del usuario
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Generar respuesta con spinner
                with st.spinner("🧠 Analizando datos..."):
                    response = analizar_con_ia(
                        prompt, 
                        df_filtrado, 
                        groq_client,
                        json_productos_completo,
                        json_analisis_completo
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Rerun para mostrar los nuevos mensajes
                st.rerun()
            
            # Botón para limpiar historial
            if len(st.session_state.messages) > 0:
                if st.button("🗑️ Limpiar Chat"):
                    st.session_state.messages = []
                    st.rerun()
    else:
        st.warning("⚠️ Chatbot IA no disponible")
        st.info("Configura `GROQ_API_KEY` para usar el asistente de IA. Obtén tu API key en: https://console.groq.com/")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Powered by Tomas Cabrera - Apertura IA</p>
        <p>Datos de Mercado Libre Argentina 🇦🇷</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

