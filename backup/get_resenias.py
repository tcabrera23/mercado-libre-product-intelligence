from bs4 import BeautifulSoup
import requests
import json
import time

def extraer_opiniones_de_producto(url_producto, producto_id):
    """
    Extrae las opiniones destacadas de la página de un producto
    """
    opiniones = []
    
    try:
        # Headers para simular un navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Hacer la petición a la página del producto
        response = requests.get(url_producto, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar la sección de opiniones destacadas
        seccion_opiniones = soup.find('div', class_='ui-review-capability-comments')
        
        if not seccion_opiniones:
            print(f"  ⚠️  No se encontró sección de opiniones para {producto_id}")
            return opiniones
        
        # Encontrar todos los artículos de opiniones
        articulos_opiniones = seccion_opiniones.find_all('article', class_='ui-review-capability-comments__comment')
        
        for i, articulo in enumerate(articulos_opiniones, 1):
            try:
                # Extraer calificación (contar estrellas)
                rating_container = articulo.find('div', class_='ui-review-capability-comments__comment__rating')
                calificacion = 0
                if rating_container:
                    estrellas = rating_container.find_all('svg', class_='ui-review-capability-comments__comment__rating__star')
                    calificacion = len(estrellas)
                
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
                tiene_imagenes = bool(articulo.find('div', class_='ui-review-capability-comments__comment__carousel--secondary'))
                
                opinion = {
                    'opinion_id': f"{producto_id}_op{i}",
                    'calificacion': calificacion,
                    'fecha': fecha,
                    'contenido': contenido,
                    'util_count': util_count,
                    'tiene_imagenes': tiene_imagenes
                }
                
                opiniones.append(opinion)
                
            except Exception as e:
                print(f"    Error procesando opinión {i}: {e}")
                continue
        
        print(f"  ✅ {len(opiniones)} opiniones encontradas")
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error al acceder al producto {producto_id}: {e}")
    except Exception as e:
        print(f"  ❌ Error inesperado al procesar opiniones de {producto_id}: {e}")
    
    return opiniones

def extraer_resenas_por_producto(productos_json_path, max_productos=None, delay=2):
    """
    Extrae reseñas para cada producto del archivo JSON
    """
    # Cargar productos desde el JSON
    with open(productos_json_path, 'r', encoding='utf-8') as f:
        productos = json.load(f)
    
    # Limitar cantidad de productos si se especifica
    if max_productos:
        productos = productos[:max_productos]
    
    resultados = []
    
    print(f"📝 Iniciando extracción de reseñas para {len(productos)} productos...")
    print(f"⏰ Delay entre peticiones: {delay} segundos")
    print("-" * 80)
    
    for i, producto in enumerate(productos, 1):
        producto_id = producto['id']
        titulo = producto['titulo']
        link = producto['link']
        
        print(f"\n[{i}/{len(productos)}] Procesando: {producto_id}")
        print(f"   Producto: {titulo[:60]}...")
        
        if link == "No disponible":
            print("   ⚠️  Sin link disponible, saltando...")
            continue
        
        # Extraer opiniones del producto
        opiniones = extraer_opiniones_de_producto(link, producto_id)
        
        # Crear resultado para este producto
        resultado_producto = {
            'producto_id': producto_id,
            'producto_numero': producto['numero'],
            'producto_titulo': titulo,
            'producto_link': link,
            'total_opiniones_encontradas': len(opiniones),
            'opiniones': opiniones,
            'timestamp_extraccion': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        resultados.append(resultado_producto)
        
        # Delay para no sobrecargar el servidor
        if i < len(productos):  # No esperar después del último producto
            print(f"   ⏳ Esperando {delay} segundos...")
            time.sleep(delay)
    
    return resultados

def mostrar_resumen_resenas(resultados):
    """
    Muestra un resumen de las reseñas extraídas
    """
    print(f"\n{'='*80}")
    print(f"RESUMEN DE EXTRACCIÓN DE RESEÑAS")
    print(f"{'='*80}")
    
    total_opiniones = sum(resultado['total_opiniones_encontradas'] for resultado in resultados)
    
    print(f"📊 Productos procesados: {len(resultados)}")
    print(f"💬 Total de opiniones extraídas: {total_opiniones}")
    print(f"📅 Fecha de extracción: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📋 Detalle por producto:")
    for resultado in resultados:
        print(f"  - {resultado['producto_id']}: {resultado['total_opiniones_encontradas']} opiniones")
        
        # Mostrar algunas opiniones de ejemplo
        if resultado['opiniones']:
            print(f"    Ejemplo: '{resultado['opiniones'][0]['contenido'][:80]}...'")

# USO DEL SCRIPT 2
if __name__ == "__main__":
    # Configuración
    ARCHIVO_PRODUCTOS = 'productos_con_id.json'
    MAX_PRODUCTOS = 3  # None para procesar todos, o un número para limitar
    DELAY_ENTRE_PETICIONES = 2  # segundos
    
    print("🚀 INICIANDO EXTRACCIÓN DE RESEÑAS")
    print("=" * 50)
    
    # Extraer reseñas
    resultados_resenas = extraer_resenas_por_producto(
        ARCHIVO_PRODUCTOS, 
        max_productos=MAX_PRODUCTOS, 
        delay=DELAY_ENTRE_PETICIONES
    )
    
    # Mostrar resumen
    mostrar_resumen_resenas(resultados_resenas)
    
    # Guardar resultados en JSON
    nombre_archivo_salida = f"resenas_productos_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultados_resenas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ EXTRACCIÓN COMPLETADA!")
    print(f"💾 Resultados guardados en: {nombre_archivo_salida}")