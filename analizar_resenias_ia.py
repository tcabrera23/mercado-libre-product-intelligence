"""
Script para analizar reseñas de productos de Mercado Libre

Este script:
1. Lee los JSON de productos generados por buscar_productos_ml.py
2. Extrae el "Resumen de opiniones generado por IA" de cada producto
3. Extrae el top 5 de opiniones con 1 estrella
4. Genera un JSON con los resultados
"""

from bs4 import BeautifulSoup
import requests
import json
import time
import sys
import io
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


def extraer_resumen_ia_y_opiniones_1_estrella(url_producto, producto_id):
    """
    Extrae el resumen de IA y las opiniones de 1 estrella de un producto
    
    Args:
        url_producto: URL del producto en Mercado Libre
        producto_id: ID único del producto
        
    Returns:
        dict: Contiene resumen_ia y lista de opiniones_1_estrella
    """
    resultado = {
        'resumen_ia': None,
        'opiniones_1_estrella': []
    }
    
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
        
        # ===== EXTRAER RESUMEN DE IA =====
        # Selector CSS: #reviews_capability_v3 > div > section > div > div:nth-child(2) > div.ui-review-capability-filter > div.ui-review-capability-filter__comments > div.ui-review-capability__summary > div.ui-review-capability__summary__plain_text > p
        
        # Intentar con el ID específico
        reviews_section = soup.find('div', id='reviews_capability_v3')
        
        if reviews_section:
            # Buscar el párrafo con el resumen de IA
            resumen_container = reviews_section.find('div', class_='ui-review-capability__summary__plain_text')
            
            if resumen_container:
                resumen_p = resumen_container.find('p')
                if resumen_p:
                    resultado['resumen_ia'] = resumen_p.get_text().strip()
                    print(f"  ✅ Resumen de IA encontrado ({len(resultado['resumen_ia'])} caracteres)")
                else:
                    print(f"  ⚠️  No se encontró el elemento <p> del resumen de IA")
            else:
                print(f"  ⚠️  No se encontró el contenedor del resumen de IA")
        else:
            print(f"  ⚠️  No se encontró la sección de reviews")
        
        # ===== EXTRAER OPINIONES DE 1 ESTRELLA =====
        # Buscar todos los artículos de opiniones
        articulos_opiniones = soup.find_all('article', class_='ui-review-capability-comments__comment')
        
        opiniones_1_estrella = []
        
        for articulo in articulos_opiniones:
            try:
                # Extraer calificación (contar estrellas activas)
                rating_container = articulo.find('div', class_='ui-review-capability-comments__comment__rating')
                calificacion = 0
                
                if rating_container:
                    # Contar SVGs con la clase que indica estrella activa
                    estrellas_activas = rating_container.find_all('svg')
                    
                    # Determinar calificación basándose en las clases o estructura
                    # Mercado Libre usa diferentes estructuras, intentemos contar las estrellas "filled"
                    for estrella in estrellas_activas:
                        # Si tiene una clase que indica que está llena, contarla
                        clases = estrella.get('class', [])
                        if 'ui-review-capability-comments__comment__rating__star' in clases:
                            calificacion += 1
                
                # Solo procesar si es calificación de 1 estrella
                if calificacion == 1:
                    # Extraer fecha
                    fecha_element = articulo.find('span', class_='ui-review-capability-comments__comment__date')
                    fecha = fecha_element.text.strip() if fecha_element else "Fecha no disponible"
                    
                    # Extraer contenido de la opinión
                    contenido_element = articulo.find('p', class_='ui-review-capability-comments__comment__content')
                    contenido = contenido_element.text.strip() if contenido_element else "Contenido no disponible"
                    
                    # Extraer cantidad de "Es útil"
                    util_element = articulo.find('p', class_='ui-review-capability-valorizations__button-like__text')
                    util_count = util_element.text.strip() if util_element else "0"
                    
                    # Verificar si hay imágenes en la reseña
                    tiene_imagenes = bool(articulo.find('div', class_='ui-review-capability-comments__comment__carousel'))
                    
                    opinion = {
                        'calificacion': calificacion,
                        'fecha': fecha,
                        'contenido': contenido,
                        'util_count': util_count,
                        'tiene_imagenes': tiene_imagenes
                    }
                    
                    opiniones_1_estrella.append(opinion)
                    
                    # Limitar a top 5
                    if len(opiniones_1_estrella) >= 5:
                        break
                        
            except Exception as e:
                print(f"    ⚠️  Error procesando opinión: {e}")
                continue
        
        resultado['opiniones_1_estrella'] = opiniones_1_estrella
        print(f"  ✅ {len(opiniones_1_estrella)} opiniones de 1 estrella encontradas")
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error al acceder al producto {producto_id}: {e}")
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
    
    return resultado


def analizar_productos_desde_json(productos_json_path, max_productos=None, delay=3):
    """
    Analiza productos desde un archivo JSON generado por buscar_productos_ml.py
    
    Args:
        productos_json_path: Ruta al archivo JSON de productos
        max_productos: Cantidad máxima de productos a analizar (None para todos)
        delay: Segundos de espera entre peticiones
        
    Returns:
        list: Lista de resultados con análisis de cada producto
    """
    # Cargar productos desde el JSON
    print(f"📂 Cargando productos desde: {productos_json_path}")
    
    with open(productos_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # El JSON tiene estructura con metadata
    productos = data.get('productos', [])
    producto_buscado = data.get('producto_buscado', 'desconocido')
    
    print(f"✅ Archivo cargado: {len(productos)} productos encontrados")
    print(f"📦 Producto buscado: {producto_buscado}")
    
    # Limitar cantidad de productos si se especifica
    if max_productos:
        productos = productos[:max_productos]
        print(f"⚠️  Limitando análisis a {max_productos} productos")
    
    resultados = []
    
    print(f"\n{'='*100}")
    print(f"🔍 INICIANDO ANÁLISIS DE RESEÑAS CON IA")
    print(f"{'='*100}")
    print(f"⏰ Delay entre peticiones: {delay} segundos\n")
    
    for i, producto in enumerate(productos, 1):
        producto_id = producto['id']
        titulo = producto['titulo']
        link = producto['link']
        calificacion = producto.get('calificacion', 0)
        
        print(f"\n[{i}/{len(productos)}] 🔎 Analizando: {producto_id}")
        print(f"   📱 Producto: {titulo[:70]}...")
        print(f"   ⭐ Calificación: {calificacion}")
        
        if link == "No disponible":
            print("   ⚠️  Sin link disponible, saltando...")
            continue
        
        # Extraer resumen de IA y opiniones de 1 estrella
        analisis = extraer_resumen_ia_y_opiniones_1_estrella(link, producto_id)
        
        # Crear resultado para este producto
        resultado_producto = {
            'producto_id': producto_id,
            'producto_titulo': titulo,
            'producto_link': link,
            'producto_calificacion': calificacion,
            'producto_precio': producto.get('precio_actual', 'No disponible'),
            'resumen_ia': analisis['resumen_ia'],
            'opiniones_1_estrella': analisis['opiniones_1_estrella'],
            'total_opiniones_1_estrella': len(analisis['opiniones_1_estrella']),
            'timestamp_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        resultados.append(resultado_producto)
        
        # Delay para no sobrecargar el servidor
        if i < len(productos):
            print(f"   ⏳ Esperando {delay} segundos...")
            time.sleep(delay)
    
    return resultados, producto_buscado


def mostrar_resumen_analisis(resultados, producto_buscado):
    """
    Muestra un resumen del análisis de reseñas
    """
    print(f"\n{'='*100}")
    print(f"📊 RESUMEN DEL ANÁLISIS DE RESEÑAS")
    print(f"{'='*100}\n")
    
    total_con_resumen_ia = sum(1 for r in resultados if r['resumen_ia'])
    total_opiniones_1_estrella = sum(r['total_opiniones_1_estrella'] for r in resultados)
    
    print(f"🔍 Producto analizado: {producto_buscado}")
    print(f"📦 Productos procesados: {len(resultados)}")
    print(f"🤖 Productos con resumen de IA: {total_con_resumen_ia}/{len(resultados)}")
    print(f"⭐ Total de opiniones de 1 estrella: {total_opiniones_1_estrella}")
    print(f"📅 Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📋 Detalle por producto:")
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{i}. {resultado['producto_titulo'][:60]}...")
        print(f"   ID: {resultado['producto_id']}")
        print(f"   Calificación: {resultado['producto_calificacion']}")
        print(f"   Resumen IA: {'✅ Disponible' if resultado['resumen_ia'] else '❌ No disponible'}")
        print(f"   Opiniones 1★: {resultado['total_opiniones_1_estrella']}")
        
        # Mostrar preview del resumen de IA
        if resultado['resumen_ia']:
            preview = resultado['resumen_ia'][:100]
            print(f"   Preview: \"{preview}...\"")
        
        # Mostrar ejemplo de opinión de 1 estrella
        if resultado['opiniones_1_estrella']:
            primera_opinion = resultado['opiniones_1_estrella'][0]['contenido'][:80]
            print(f"   Opinión 1★: \"{primera_opinion}...\"")


def guardar_resultados(resultados, producto_buscado):
    """
    Guarda los resultados en un archivo JSON
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"analisis_resenias_{producto_buscado.replace(' ', '_')}_{timestamp}.json"
    
    # Preparar datos para guardar
    datos_salida = {
        'producto_analizado': producto_buscado,
        'fecha_analisis': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_productos': len(resultados),
        'total_con_resumen_ia': sum(1 for r in resultados if r['resumen_ia']),
        'total_opiniones_1_estrella': sum(r['total_opiniones_1_estrella'] for r in resultados),
        'productos': resultados
    }
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos_salida, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {nombre_archivo}")
    return nombre_archivo


if __name__ == "__main__":
    print("\n" + "="*100)
    print("🤖 ANÁLISIS DE RESEÑAS CON IA - MERCADO LIBRE")
    print("="*100 + "\n")
    
    # Configuración
    if len(sys.argv) > 1:
        # Usar argumento de línea de comandos
        ARCHIVO_PRODUCTOS = sys.argv[1]
    else:
        # Modo interactivo
        print("📝 Este script analiza las reseñas de productos extraídos por buscar_productos_ml.py")
        print("\nEjemplos de archivos:")
        print("  • productos_ipad_20251104_210247.json")
        print("  • productos_auriculares_20251104_202812.json")
        print()
        ARCHIVO_PRODUCTOS = input("📂 Ingresa el nombre del archivo JSON de productos ► ").strip()
        
        if not ARCHIVO_PRODUCTOS:
            print("❌ No ingresaste ningún archivo")
            sys.exit(1)
    
    # Configuración de análisis
    MAX_PRODUCTOS = None  # None para analizar todos, o número para limitar
    DELAY_ENTRE_PETICIONES = 3  # segundos (más conservador para no ser bloqueado)
    
    # Preguntar si quiere limitar productos
    print(f"\n¿Cuántos productos deseas analizar? (Enter para todos)")
    limite = input("Cantidad (o Enter para todos) ► ").strip()
    if limite.isdigit():
        MAX_PRODUCTOS = int(limite)
    
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

