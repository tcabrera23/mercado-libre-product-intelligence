"""
Script para buscar y extraer productos de Mercado Libre de forma dinámica

Este script permite buscar cualquier producto en Mercado Libre Argentina,
extraer su información y guardarla en un archivo JSON.
"""

from bs4 import BeautifulSoup
import json
import uuid
from datetime import datetime
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except Exception:
        pass  # Si falla, continuar sin emojis

# Importar la función para obtener HTML de Mercado Libre
from get_html import obtener_html_mercadolibre


def extraer_productos_con_id(html_section):
    """
    Extrae los productos de una sección HTML de Mercado Libre y les asigna un ID único
    
    Args:
        html_section: Objeto BeautifulSoup con la sección de resultados
        
    Returns:
        list: Lista de diccionarios con la información de cada producto
    """
    productos = []
    
    product_items = html_section.find_all('li', class_='ui-search-layout__item')
    
    print(f"\n📦 Procesando {len(product_items)} productos...")
    
    for i, item in enumerate(product_items, 1):
        try:
            # Generar ID único para el producto
            producto_id = str(uuid.uuid4())[:8]
            
            # Título
            title_element = item.find('a', class_='poly-component__title')
            titulo = title_element.text.strip() if title_element else "No disponible"
            
            # Link
            link = title_element.get('href') if title_element else "No disponible"
            
            # Precio actual
            price_current = item.find('div', class_='poly-price__current')
            precio = "No disponible"
            if price_current:
                price_fraction = price_current.find('span', class_='andes-money-amount__fraction')
                if price_fraction:
                    precio = f"${price_fraction.text.strip()}"
            
            # Precio anterior (si hay descuento)
            price_previous = item.find('s', class_='andes-money-amount--previous')
            precio_anterior = ""
            if price_previous:
                prev_fraction = price_previous.find('span', class_='andes-money-amount__fraction')
                if prev_fraction:
                    precio_anterior = f"${prev_fraction.text.strip()}"
            
            # Descuento
            discount_element = item.find('span', class_='poly-price__disc_label')
            descuento = discount_element.text.strip() if discount_element else ""
            
            # Si no hay precio anterior, usar el precio actual y descuento 0%
            if not precio_anterior and precio != "No disponible":
                precio_anterior = precio
                descuento = "0%"
            
            # Envío gratis (convertir a boolean)
            shipping_div = item.find('div', class_='poly-component__shipping')
            envio_gratis = False
            if shipping_div:
                shipping_text = shipping_div.get_text().lower()
                envio_gratis = 'gratis' in shipping_text
            
            # Calificación y vendidos (ambos están en span.poly-phrase-label)
            calificacion = None
            vendidos = None
            
            # Buscar todos los elementos poly-phrase-label
            phrase_labels = item.find_all('span', class_='poly-phrase-label')
            for label in phrase_labels:
                text = label.get_text().strip()
                
                # Si contiene "vendidos", es el campo de vendidos
                if 'vendidos' in text.lower():
                    # Limpiar el texto (quitar el "|" inicial si existe)
                    vendidos = text.replace('|', '').strip()
                # Si es un número (calificación), guardarlo
                else:
                    try:
                        # Intentar convertir a float para verificar que es una calificación
                        rating_value = float(text)
                        calificacion = rating_value
                    except ValueError:
                        continue
            
            # Completar campos null con valores por defecto
            if calificacion is None:
                calificacion = 0.0
            
            if vendidos is None:
                vendidos = "Sin ventas"
            
            # Imagen
            img_element = item.find('img')
            imagen = img_element.get('src', 'No disponible') if img_element else "No disponible"
            
            # Crear diccionario del producto
            producto = {
                'id': producto_id,
                'titulo': titulo,
                'link': link,
                'precio_actual': precio,
                'precio_anterior': precio_anterior,
                'descuento': descuento,
                'calificacion': calificacion,  # float o None
                'vendidos': vendidos,  # texto como "+25 vendidos"
                'imagen': imagen,
                'envio_gratis': envio_gratis  # boolean
            }
            
            productos.append(producto)
            
            # Mostrar progreso cada 10 productos
            if i % 10 == 0:
                print(f"  ✓ Procesados {i}/{len(product_items)} productos...")
            
        except Exception as e:
            print(f"  ⚠️ Error procesando producto {i}: {e}")
            continue
    
    print(f"✅ Total de productos extraídos: {len(productos)}")
    return productos


def guardar_productos(productos, nombre_producto):
    """
    Guarda los productos en un archivo JSON
    
    Args:
        productos: Lista de productos
        nombre_producto: Nombre del producto buscado (para el nombre del archivo)
    """
    if not productos:
        print("❌ No hay productos para guardar")
        return None
    
    # Crear nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"productos_{nombre_producto.replace(' ', '_')}_{timestamp}.json"
    
    # Preparar datos para guardar
    datos = {
        'producto_buscado': nombre_producto,
        'fecha_busqueda': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_productos': len(productos),
        'productos': productos
    }
    
    # Guardar en JSON
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Archivo guardado exitosamente: {nombre_archivo}")
        return nombre_archivo
    except Exception as e:
        print(f"\n❌ Error al guardar archivo: {e}")
        return None


def mostrar_resumen_productos(productos, limite=5):
    """
    Muestra un resumen de los primeros productos encontrados
    
    Args:
        productos: Lista de productos
        limite: Cantidad de productos a mostrar
    """
    if not productos:
        print("\n❌ No hay productos para mostrar")
        return
    
    print(f"\n{'='*100}")
    print(f"📋 RESUMEN DE LOS PRIMEROS {min(limite, len(productos))} PRODUCTOS:")
    print(f"{'='*100}\n")
    
    for i, prod in enumerate(productos[:limite], 1):
        print(f"{i}. {prod['titulo'][:80]}...")
        print(f"   💰 Precio: {prod['precio_actual']}", end="")
        if prod['precio_anterior']:
            print(f" (antes: {prod['precio_anterior']}) - {prod['descuento']}", end="")
        print()
        
        # Mostrar calificación y vendidos
        calificacion_str = f"{prod['calificacion']}" if prod['calificacion'] and prod['calificacion'] > 0 else "Sin calificación"
        print(f"   ⭐ {calificacion_str} | {prod['vendidos']}")
        
        # Mostrar envío gratis
        envio_str = "✅ Envío gratis" if prod['envio_gratis'] else "❌ Sin envío gratis"
        print(f"   🚚 {envio_str}")
        
        print(f"   🔗 {prod['link'][:80]}...")
        print()


def buscar_producto_mercadolibre(nombre_producto):
    """
    Función principal que busca un producto en Mercado Libre
    
    Args:
        nombre_producto: Nombre del producto a buscar
        
    Returns:
        list: Lista de productos encontrados
    """
    print("\n" + "="*100)
    print("🛒 BUSCADOR DE PRODUCTOS - MERCADO LIBRE ARGENTINA")
    print("="*100 + "\n")
    
    # Obtener HTML de Mercado Libre
    soup_completo, seccion_resultados = obtener_html_mercadolibre(
        nombre_producto, 
        solo_resultados=True
    )
    
    if not seccion_resultados:
        print("\n❌ No se pudieron obtener resultados. Verifica:")
        print("   • Tu conexión a internet")
        print("   • Que el producto exista en Mercado Libre Argentina")
        print("   • Que no estés siendo bloqueado por anti-scraping")
        return []
    
    # Extraer productos
    print("\n" + "-"*100)
    productos = extraer_productos_con_id(seccion_resultados)
    
    if productos:
        # Mostrar resumen
        mostrar_resumen_productos(productos, limite=5)
        
        # Guardar en JSON
        archivo = guardar_productos(productos, nombre_producto)
        
        if archivo:
            print(f"\n✨ Proceso completado exitosamente!")
            print(f"   Total de productos: {len(productos)}")
            print(f"   Archivo: {archivo}")
    else:
        print("\n❌ No se encontraron productos")
    
    return productos


if __name__ == "__main__":
    # Verificar si se pasó un argumento
    if len(sys.argv) > 1:
        # Usar el argumento de línea de comandos
        producto = ' '.join(sys.argv[1:])
    else:
        # Modo interactivo
        print("\n" + "="*100)
        print("🛒 BUSCADOR DE PRODUCTOS - MERCADO LIBRE ARGENTINA")
        print("="*100)
        print("\nEjemplos de búsquedas:")
        print("  • auriculares")
        print("  • celulares samsung")
        print("  • notebook gaming")
        print("  • zapatillas nike")
        print()
        producto = input("¿Qué producto deseas buscar? ► ").strip()
        
        if not producto:
            print("❌ No ingresaste ningún producto")
            sys.exit(1)
    
    # Buscar el producto
    resultados = buscar_producto_mercadolibre(producto)
    
    print("\n" + "="*100)
    print("🎯 Búsqueda finalizada")
    print("="*100 + "\n")

