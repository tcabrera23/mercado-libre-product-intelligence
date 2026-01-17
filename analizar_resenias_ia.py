"""
Script para analizar reseñas de productos de Mercado Libre (VERSIÓN SIMPLIFICADA)

Este script:
1. Lee los JSON de productos generados por buscar_productos_ml.py
2. Extrae solo el "Resumen de opiniones generado por IA" de cada producto
3. Genera un JSON con los resultados

NOTA: Esta versión NO extrae opiniones individuales (más rápido y eficiente)
"""

from bs4 import BeautifulSoup
import requests
import json
import time
import sys
import io
import os
from datetime import datetime

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except Exception:
        pass


def extraer_resumen_ia(url_producto, producto_id):
    """
    Extrae solo el resumen de IA de un producto
    
    Args:
        url_producto: URL del producto en Mercado Libre
        producto_id: ID único del producto
        
    Returns:
        str: Resumen de IA o None si no se encuentra
    """
    try:
        # Headers para simular un navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
        
        # Hacer la petición a la página del producto
        response = requests.get(url_producto, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # EXTRAER RESUMEN DE IA
        reviews_section = soup.find('div', id='reviews_capability_v3')
        
        if reviews_section:
            # Buscar el párrafo con el resumen de IA
            resumen_container = reviews_section.find('div', class_='ui-review-capability__summary__plain_text')
            
            if resumen_container:
                resumen_p = resumen_container.find('p')
                if resumen_p:
                    resumen = resumen_p.get_text().strip()
                    print(f"  ✅ Resumen de IA encontrado ({len(resumen)} caracteres)")
                    return resumen
                else:
                    print(f"  ⚠️  No se encontró el elemento <p> del resumen de IA")
            else:
                print(f"  ⚠️  No se encontró el contenedor del resumen de IA")
        else:
            print(f"  ⚠️  No se encontró la sección de reviews")
        
        return None
        
    except requests.Timeout:
        print(f"  ⏱️  Timeout al acceder a {url_producto}")
        return None
    except requests.RequestException as e:
        print(f"  ❌ Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return None


def analizar_productos_desde_json(archivo_json, max_productos=None, delay=2):
    """
    Analiza productos desde un archivo JSON
    
    Args:
        archivo_json: Path al archivo JSON de productos
        max_productos: Número máximo de productos a analizar (None = todos)
        delay: Segundos de espera entre peticiones
        
    Returns:
        tuple: (lista de resultados, nombre del producto buscado)
    """
    print(f"\n{'='*100}")
    print(f"🔍 ANÁLISIS DE RESEÑAS DE MERCADO LIBRE (VERSIÓN SIMPLIFICADA)")
    print(f"{'='*100}\n")
    
    # Cargar el JSON de productos
    print(f"📂 Cargando: {archivo_json}")
    
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_json}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo no es un JSON válido")
        sys.exit(1)
    
    productos = data.get('productos', [])
    producto_buscado = data.get('producto_buscado', 'Desconocido')
    
    total_productos = len(productos)
    productos_a_analizar = min(max_productos, total_productos) if max_productos else total_productos
    
    print(f"✅ Archivo cargado correctamente")
    print(f"📊 Total de productos en archivo: {total_productos}")
    print(f"🎯 Productos a analizar: {productos_a_analizar}")
    print(f"⏱️  Delay entre peticiones: {delay} segundos")
    print(f"\n{'='*100}\n")
    
    resultados = []
    productos_con_resumen = 0
    
    # Procesar cada producto
    for idx, producto in enumerate(productos[:productos_a_analizar], 1):
        producto_id = producto.get('id', f'unknown_{idx}')
        titulo = producto.get('titulo', 'Sin título')
        link = producto.get('link', '')
        calificacion = producto.get('calificacion', 0)
        precio = producto.get('precio_actual', 'N/A')
        
        print(f"[{idx}/{productos_a_analizar}] 🔍 Analizando: {titulo[:60]}...")
        print(f"  📍 ID: {producto_id}")
        print(f"  ⭐ Calificación: {calificacion}")
        print(f"  💰 Precio: {precio}")
        
        if not link:
            print(f"  ⚠️  Producto sin link, saltando...")
            resultados.append({
                'producto_id': producto_id,
                'producto_titulo': titulo,
                'producto_link': link,
                'producto_calificacion': calificacion,
                'producto_precio': precio,
                'resumen_ia': None,
                'timestamp_extraccion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            continue
        
        # Extraer resumen de IA
        resumen_ia = extraer_resumen_ia(link, producto_id)
        
        if resumen_ia:
            productos_con_resumen += 1
        
        # Guardar resultado
        resultados.append({
            'producto_id': producto_id,
            'producto_titulo': titulo,
            'producto_link': link,
            'producto_calificacion': calificacion,
            'producto_precio': precio,
            'resumen_ia': resumen_ia,
            'timestamp_extraccion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        print(f"  ✅ Análisis completado\n")
        
        # Delay entre peticiones para no saturar el servidor
        if idx < productos_a_analizar:
            time.sleep(delay)
    
    print(f"{'='*100}\n")
    print(f"📊 RESUMEN DEL ANÁLISIS:")
    print(f"  • Total productos analizados: {productos_a_analizar}")
    print(f"  • Productos con resumen IA: {productos_con_resumen}")
    print(f"  • Productos sin resumen: {productos_a_analizar - productos_con_resumen}")
    print(f"\n{'='*100}\n")
    
    return resultados, producto_buscado


def mostrar_resumen_analisis(resultados, producto_buscado):
    """Muestra un resumen del análisis realizado"""
    print(f"\n{'='*100}")
    print(f"📊 RESUMEN DE ANÁLISIS - {producto_buscado.upper()}")
    print(f"{'='*100}\n")
    
    total_productos = len(resultados)
    total_con_resumen = sum(1 for r in resultados if r['resumen_ia'])
    
    print(f"📦 Total de productos: {total_productos}")
    print(f"✅ Con resumen IA: {total_con_resumen}")
    print(f"❌ Sin resumen IA: {total_productos - total_con_resumen}")
    
    if total_con_resumen > 0:
        porcentaje = (total_con_resumen / total_productos) * 100
        print(f"📈 Tasa de éxito: {porcentaje:.1f}%")
        
        # Mostrar algunos ejemplos de resúmenes
        print(f"\n🌟 EJEMPLOS DE RESÚMENES:")
        ejemplos = [r for r in resultados if r['resumen_ia']][:3]
        
        for idx, ejemplo in enumerate(ejemplos, 1):
            print(f"\n  [{idx}] {ejemplo['producto_titulo'][:50]}...")
            print(f"      Resumen: {ejemplo['resumen_ia'][:150]}...")
    
    print(f"\n{'='*100}\n")


def guardar_resultados(resultados, producto_buscado):
    """Guarda los resultados en un archivo JSON en la carpeta resenias/"""
    # Crear carpeta resenias/ si no existe
    carpeta_resenias = "resenias"
    if not os.path.exists(carpeta_resenias):
        os.makedirs(carpeta_resenias)
        print(f"📁 Carpeta '{carpeta_resenias}/' creada")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"analisis_resenias_{producto_buscado.replace(' ', '_')}_{timestamp}.json"
    ruta_completa = os.path.join(carpeta_resenias, nombre_archivo)
    
    datos_salida = {
        'producto_analizado': producto_buscado,
        'fecha_analisis': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_productos': len(resultados),
        'total_con_resumen_ia': sum(1 for r in resultados if r['resumen_ia']),
        'productos': resultados
    }
    
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(datos_salida, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Resultados guardados en: {ruta_completa}")
    return ruta_completa


if __name__ == "__main__":
    print(f"\n{'#'*100}")
    print(f"# ANÁLISIS DE RESEÑAS DE MERCADO LIBRE - VERSIÓN SIMPLIFICADA")
    print(f"# Solo extrae resúmenes de IA (más rápido y eficiente)")
    print(f"{'#'*100}\n")
    
    # Obtener archivo JSON de productos
    if len(sys.argv) < 2:
        print("❌ Error: Debes especificar un archivo JSON de productos")
        print("\n❓ Uso:")
        print("  python analizar_resenias_ia.py <archivo_productos.json> [cantidad_opcional]")
        print("\n📝 Ejemplos:")
        print("  python analizar_resenias_ia.py productos_auriculares_20241104.json")
        print("  python analizar_resenias_ia.py productos_auriculares_20241104.json 10")
        sys.exit(1)
    
    ARCHIVO_PRODUCTOS = sys.argv[1]
    
    if not ARCHIVO_PRODUCTOS:
        print("❌ No se especificó ningún archivo")
        sys.exit(1)
    
    # Configuración de análisis
    MAX_PRODUCTOS = None  # Por defecto: analizar TODOS los productos
    DELAY_ENTRE_PETICIONES = 2  # segundos
    
    # Detectar si hay argumentos adicionales para límite
    if len(sys.argv) > 2:
        limite_arg = sys.argv[2]
        if limite_arg.isdigit():
            MAX_PRODUCTOS = int(limite_arg)
            print(f"\n📊 Analizando {MAX_PRODUCTOS} productos...")
        else:
            print(f"\n⚠️  Argumento '{limite_arg}' no válido, analizando todos los productos...")
    else:
        print(f"\n📊 Analizando TODOS los productos del archivo...")
    
    try:
        # Analizar productos
        resultados, producto_buscado = analizar_productos_desde_json(
            ARCHIVO_PRODUCTOS,
            max_productos=MAX_PRODUCTOS,
            delay=DELAY_ENTRE_PETICIONES
        )
        
        # Mostrar resumen
        mostrar_resumen_analisis(resultados, producto_buscado)
        
        # Guardar resultados
        archivo_salida = guardar_resultados(resultados, producto_buscado)
        
        print(f"\n{'='*100}")
        print(f"✅ ANÁLISIS COMPLETADO EXITOSAMENTE!")
        print(f"{'='*100}\n")
        
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el archivo '{ARCHIVO_PRODUCTOS}'")
        print("   Asegúrate de que el archivo existe y el nombre es correcto")
    except json.JSONDecodeError:
        print(f"\n❌ Error: El archivo '{ARCHIVO_PRODUCTOS}' no es un JSON válido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
