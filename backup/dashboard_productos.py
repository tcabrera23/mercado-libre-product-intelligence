"""
Dashboard interactivo para análisis de productos de Mercado Libre
Creado con Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Productos Mercado Libre",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3483FA;
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


def extraer_cantidad_vendidos(vendidos_str):
    """Extrae número de vendidos del string"""
    try:
        if 'mil' in vendidos_str.lower():
            numero = vendidos_str.replace('+', '').replace('mil', '').replace('vendidos', '').strip()
            return float(numero) * 1000
        else:
            numero = vendidos_str.replace('+', '').replace('vendidos', '').strip()
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
def cargar_datos(archivo_json):
    """Carga y procesa los datos del JSON"""
    # Si el archivo no tiene ruta completa, asumimos que está en productos/
    if not os.path.dirname(archivo_json):
        archivo_json = os.path.join("productos", archivo_json)
    
    with open(archivo_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    productos = data.get('productos', [])
    df = pd.DataFrame(productos)
    
    # Procesar datos
    df['precio_numerico'] = df['precio_actual'].apply(limpiar_precio)
    df['marca'] = df['titulo'].apply(extraer_marca)
    df['cantidad_vendidos'] = df['vendidos'].apply(extraer_cantidad_vendidos)
    df['envio_gratis_texto'] = df['envio_gratis'].apply(lambda x: 'Sí' if x else 'No')
    
    # Clasificar por precio
    promedio = df['precio_numerico'].mean()
    df['categoria_precio'] = df['precio_numerico'].apply(lambda x: clasificar_precio(x, promedio))
    
    return df, data.get('producto_buscado', 'Productos')


def main():
    # Header
    st.markdown('<div class="main-header">🛒 Dashboard de Análisis de Productos</div>', unsafe_allow_html=True)
    
    # Sidebar - Cargar archivo
    st.sidebar.title("📁 Configuración")
    
    # Listar archivos JSON disponibles en la carpeta productos/
    carpeta_productos = "productos"
    if not os.path.exists(carpeta_productos):
        st.error("❌ No se encontró la carpeta 'productos/'")
        st.info("💡 Ejecuta primero: `python buscar_productos_ml.py 'producto'`")
        return
    
    archivos_json = [f for f in os.listdir(carpeta_productos) if f.startswith('productos_') and f.endswith('.json')]
    
    if not archivos_json:
        st.error("❌ No se encontraron archivos JSON de productos en la carpeta 'productos/'")
        st.info("💡 Ejecuta primero: `python buscar_productos_ml.py 'producto'`")
        return
    
    archivo_seleccionado = st.sidebar.selectbox(
        "Selecciona archivo JSON:",
        archivos_json,
        index=0
    )
    
    # Cargar datos
    try:
        df, producto_buscado = cargar_datos(archivo_seleccionado)
    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return
    
    st.sidebar.success(f"✅ {len(df)} productos cargados")
    st.sidebar.info(f"🔍 Producto: **{producto_buscado}**")
    
    # FILTROS / SLICERS
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎚️ Filtros")
    
    # Filtro por marca
    marcas_disponibles = ['Todas'] + sorted(df['marca'].unique().tolist())
    marca_filtro = st.sidebar.multiselect(
        "Marca:",
        marcas_disponibles[1:],  # Sin 'Todas'
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
        st.metric(
            label="💰 Precio Mínimo",
            value=f"${df_filtrado['precio_numerico'].min():,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="💵 Precio Mediano",
            value=f"${df_filtrado['precio_numerico'].median():,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="💸 Precio Máximo",
            value=f"${df_filtrado['precio_numerico'].max():,.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="📦 Total Productos",
            value=f"{len(df_filtrado)}",
            delta=f"{len(df_filtrado) - len(df)} filtrados" if len(df_filtrado) != len(df) else None
        )
    
    st.markdown("---")
    
    # GRÁFICOS
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        # Gráfico de Dispersión: Precio vs Ventas
        st.markdown("### 📈 Relación Precio vs Ventas")
        st.caption("¿A menor precio, más ventas?")
        
        df_scatter = df_filtrado[df_filtrado['cantidad_vendidos'] > 0].copy()
        
        if len(df_scatter) > 0:
            fig_scatter = px.scatter(
                df_scatter,
                x='precio_numerico',
                y='cantidad_vendidos',
                color='categoria_precio',
                size='calificacion',
                hover_data=['titulo', 'marca'],
                title='',
                labels={
                    'precio_numerico': 'Precio ($)',
                    'cantidad_vendidos': 'Cantidad Vendidos',
                    'categoria_precio': 'Categoría'
                },
                color_discrete_map={
                    'Económico': '#2ecc71',
                    'Mediano': '#3498db',
                    'Caro': '#e74c3c'
                }
            )
            
            fig_scatter.update_layout(
                height=400,
                xaxis_tickformat='$,.0f'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No hay datos de ventas disponibles")
    
    with col_der:
        # Gráfico de Barras: Precio Promedio por Calificación
        st.markdown("### ⭐ Precio Promedio por Calificación")
        st.caption("Relación entre precio y satisfacción del cliente")
        
        df_calif = df_filtrado[df_filtrado['calificacion'] > 0].copy()
        
        if len(df_calif) > 0:
            # Redondear calificaciones para agrupar
            df_calif['calificacion_redondeada'] = df_calif['calificacion'].round(1)
            
            precio_por_calif = df_calif.groupby('calificacion_redondeada')['precio_numerico'].mean().reset_index()
            precio_por_calif = precio_por_calif.sort_values('calificacion_redondeada')
            
            fig_barras = px.bar(
                precio_por_calif,
                x='calificacion_redondeada',
                y='precio_numerico',
                title='',
                labels={
                    'calificacion_redondeada': 'Calificación',
                    'precio_numerico': 'Precio Promedio ($)'
                },
                color='precio_numerico',
                color_continuous_scale='Blues'
            )
            
            fig_barras.update_layout(
                height=400,
                yaxis_tickformat='$,.0f',
                showlegend=False
            )
            
            st.plotly_chart(fig_barras, use_container_width=True)
        else:
            st.info("No hay datos de calificación disponibles")
    
    st.markdown("---")
    
    # Gráfico de Torta: Marcas más populares
    col_torta, col_espacio = st.columns([2, 1])
    
    with col_torta:
        st.markdown("### 🏆 Marcas Más Populares")
        st.caption("Distribución de productos por marca")
        
        marcas_count = df_filtrado['marca'].value_counts().head(10)
        
        fig_torta = px.pie(
            values=marcas_count.values,
            names=marcas_count.index,
            title='',
            hole=0.4  # Dona
        )
        
        fig_torta.update_layout(height=500)
        fig_torta.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig_torta, use_container_width=True)
    
    st.markdown("---")
    
    # TABLA DE DATOS
    st.markdown("### 📋 Tabla de Productos")
    st.caption(f"Total: {len(df_filtrado)} productos")
    
    # Seleccionar columnas a mostrar
    columnas_mostrar = [
        'titulo', 'marca', 'precio_actual', 'categoria_precio',
        'calificacion', 'vendidos', 'envio_gratis_texto', 'descuento'
    ]
    
    df_mostrar = df_filtrado[columnas_mostrar].copy()
    df_mostrar.columns = [
        'Título', 'Marca', 'Precio', 'Categoría',
        'Calificación', 'Vendidos', 'Envío Gratis', 'Descuento'
    ]
    
    # Configurar display
    st.dataframe(
        df_mostrar,
        use_container_width=True,
        height=400
    )
    
    # Botón de descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=csv,
        file_name=f"productos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Datos extraídos de Mercado Libre Argentina 🇦🇷</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

