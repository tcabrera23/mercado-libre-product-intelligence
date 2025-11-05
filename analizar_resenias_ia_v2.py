"""
Script para analizar reseñas de productos de Mercado Libre v2

Mejoras v2:
- Filtrado dinámico de opiniones de 1 estrella usando Selenium
- Mejor extracción de reseñas
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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


def configurar_driver():
    """
    Configura el driver de Selenium con opciones optimizadas
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Modo sin interfaz gráfica
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Error al configurar Selenium: {e}")
        print("💡 Asegúrate de tener ChromeDriver instalado")
        print("   Descarga: https://chromedriver.chromium.org/")
        return None


def extraer_resumen_ia_y_opiniones_1_estrella(driver, url_producto, producto_id):
    """
    Extrae el resumen de IA y las opiniones de 1 estrella usando Selenium
    """
    resultado = {
        'resumen_ia': None,
        'opiniones_1_estrella': []
    }
    
    try:
        # Navegar a la página del producto
        driver.get(url_producto)
        time.sleep(2)  # Esperar a que cargue
        
        # ===== EXTRAER RESUMEN DE IA =====
        try:
            resumen_element = driver.find_element(By.CSS_SELECTOR, 
                "#reviews_capability_v3 .ui-review-capability__summary__plain_text p")
            resultado['resumen_ia'] = resumen_element.text.strip()
            print(f"  ✅ Resumen de IA encontrado ({len(resultado['resumen_ia'])} caracteres)")
        except Exception as e:
            print(f"  ⚠️  No se encontró el resumen de IA")
        
        # ===== FILTRAR Y EXTRAER OPINIONES DE 1 ESTRELLA =====
        try:
            # Hacer scroll hacia la sección de reseñas
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            # Hacer clic en el filtro de 1 estrella usando JavaScript
            try:
                filter_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#dropdown-option-rating-1"))
                )
                driver.execute_script("arguments[0].click();", filter_button)
                print(f"  🔍 Filtro de 1 estrella aplicado")
                time.sleep(3)  # Esperar a que carguen las reseñas filtradas
            except Exception as e:
                print(f"  ⚠️  No se pudo aplicar filtro de 1 estrella, extrayendo todas")
            
            # Extraer opiniones
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            articulos_opiniones = soup.find_all('article', class_='ui-review-capability-comments__comment')
            
            opiniones_encontradas = 0
            for articulo in articulos_opiniones:
                if opiniones_encontradas >= 5:
                    break
                
                try:
                    # Extraer calificación
                    rating_container = articulo.find('div', class_='ui-review-capability-comments__comment__rating')
                    calificacion = 0
                    
                    if rating_container:
                        estrellas = rating_container.find_all('svg')
                        calificacion = len([s for s in estrellas if 'ui-review-capability-comments__comment__rating__star' in s.get('class', [])])
                    
                    # Solo tomar si es 1 estrella
                    if calificacion == 1:
                        # Extraer fecha
                        fecha_element = articulo.find('span', class_='ui-review-capability-comments__comment__date')
                        fecha = fecha_element.text.strip() if fecha_element else "Fecha no disponible"
                        
                        # Extraer contenido
                        contenido_element = articulo.find('p', class_='ui-review-capability-comments__comment__content')
                        contenido = contenido_element.text.strip() if contenido_element else "Contenido no disponible"
                        
                        # Extraer útil count
                        util_element = articulo.find('p', class_='ui-review-capability-valorizations__button-like__text')
                        util_count = util_element.text.strip() if util_element else "0"
                        
                        # Verificar imágenes
                        tiene_imagenes = bool(articulo.find('div', class_='ui-review-capability-comments__comment__carousel'))
                        
                        opinion = {
                            'calificacion': calificacion,
                            'fecha': fecha,
                            'contenido': contenido,
                            'util_count': util_count,
                            'tiene_imagenes': tiene_imagenes
                        }
                        
                        resultado['opiniones_1_estrella'].append(opinion)
                        opiniones_encontradas += 1
                        
                except Exception as e:
                    print(f"    ⚠️  Error procesando opinión: {e}")
                    continue
            
            print(f"  ✅ {len(resultado['opiniones_1_estrella'])} opiniones de 1 estrella encontradas")
            
        except Exception as e:
            print(f"  ⚠️  Error al extraer opiniones: {e}")
        
    except Exception as e:
        print(f"  ❌ Error al procesar producto: {e}")
    
    return resultado


def analizar_productos_desde_json(productos_json_path, max_productos=None, delay=3):
    """
    Analiza productos desde un archivo JSON usando Selenium
    """
    # Configurar Selenium
    driver = configurar_driver()
    if not driver:
        return [], None
    
    try:
        # Cargar productos
        print(f"📂 Cargando productos desde: {productos_json_path}")
        
        with open(productos_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        productos = data.get('productos', [])
        producto_buscado = data.get('producto_buscado', 'desconocido')
        
        print(f"✅ Archivo cargado: {len(productos)} productos encontrados")
        print(f"📦 Producto buscado: {producto_buscado}")
        
        if max_productos:
            productos = productos[:max_productos]
            print(f"⚠️  Limitando análisis a {max_productos} productos")
        
        resultados = []
        
        print(f"\n{'='*100}")
        print(f"🔍 INICIANDO ANÁLISIS DE RESEÑAS CON IA (Selenium v2)")
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
            
            if link == "No disponible" or not link:
                print("   ⚠️  Sin link disponible, saltando...")
                continue
            
            # Extraer con Selenium
            analisis = extraer_resumen_ia_y_opiniones_1_estrella(driver, link, producto_id)
            
            # Crear resultado
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
            
            # Delay
            if i < len(productos):
                print(f"   ⏳ Esperando {delay} segundos...")
                time.sleep(delay)
        
        return resultados, producto_buscado
        
    finally:
        # Cerrar driver
        driver.quit()
        print("\n🔒 Driver de Selenium cerrado")


def mostrar_resumen_analisis(resultados, producto_buscado):
    """
    Muestra un resumen del análisis
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
        print(f"   Resumen IA: {'✅' if resultado['resumen_ia'] else '❌'}")
        print(f"   Opiniones 1★: {resultado['total_opiniones_1_estrella']}")


def guardar_resultados(resultados, producto_buscado):
    """
    Guarda los resultados en JSON
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"analisis_resenias_{producto_buscado.replace(' ', '_')}_{timestamp}.json"
    
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
    print("🤖 ANÁLISIS DE RESEÑAS CON IA v2 (Selenium) - MERCADO LIBRE")
    print("="*100 + "\n")
    
    print("⚠️  NOTA: Este script requiere ChromeDriver instalado")
    print("   Descarga: https://chromedriver.chromium.org/\n")
    
    # Configuración
    if len(sys.argv) > 1:
        ARCHIVO_PRODUCTOS = sys.argv[1]
    else:
        print("📝 Ingresa el archivo JSON de productos")
        ARCHIVO_PRODUCTOS = input("📂 Archivo ► ").strip()
        
        if not ARCHIVO_PRODUCTOS:
            print("❌ No ingresaste ningún archivo")
            sys.exit(1)
    
    print(f"\n¿Cuántos productos deseas analizar? (Enter para todos)")
    limite = input("Cantidad ► ").strip()
    MAX_PRODUCTOS = int(limite) if limite.isdigit() else None
    
    DELAY_ENTRE_PETICIONES = 3
    
    try:
        resultados, producto_buscado = analizar_productos_desde_json(
            ARCHIVO_PRODUCTOS,
            max_productos=MAX_PRODUCTOS,
            delay=DELAY_ENTRE_PETICIONES
        )
        
        if resultados:
            mostrar_resumen_analisis(resultados, producto_buscado)
            guardar_resultados(resultados, producto_buscado)
            
            print(f"\n{'='*100}")
            print(f"✅ ANÁLISIS COMPLETADO!")
            print(f"{'='*100}\n")
        else:
            print("\n❌ No se pudieron analizar productos")
        
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el archivo '{ARCHIVO_PRODUCTOS}'")
    except json.JSONDecodeError:
        print(f"\n❌ Error: El archivo no es un JSON válido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

