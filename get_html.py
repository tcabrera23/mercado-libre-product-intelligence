import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import io

# Configurar encoding UTF-8 para Windows (solo cuando se ejecuta directamente)
if __name__ == "__main__" and sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def obtener_html_mercadolibre(producto, solo_resultados=True):
    """
    Obtiene el HTML de Mercado Libre para un producto específico
    
    Args:
        producto (str): Nombre del producto a buscar (ej: "auriculares", "celulares samsung")
        solo_resultados (bool): Si es True, retorna solo la sección de resultados.
                                Si es False, retorna el HTML completo.
    
    Returns:
        tuple: (soup_completo, seccion_resultados) o (soup_completo, None) si no encuentra resultados
    """
    
    # Headers para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }
    # Nota: No incluimos Accept-Encoding para que requests lo maneje automáticamente
    
    # Formatear el producto para la URL (reemplazar espacios con guiones)celulares-samsung
    producto_formateado = urllib.parse.quote(producto.replace(' ', '-'))
    url = f"https://listado.mercadolibre.com.ar/{producto_formateado}"
    
    print(f"🔍 Buscando: {producto}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Error: No se pudo obtener la página (Status: {response.status_code})")
            return None, None
        
        print(f"📊 Content Length: {len(response.text):,} caracteres")
        print(f"🔤 Encoding: {response.encoding}")
        
        # Parsear el HTML completo
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if solo_resultados:
            # Buscar la sección específica de resultados
            seccion_resultados = soup.find('section', class_='ui-search-results')
            
            if seccion_resultados:
                # Contar productos encontrados
                productos = seccion_resultados.find_all('li', class_='ui-search-layout__item')
                print(f"✨ Encontrados: {len(productos)} productos")
                return soup, seccion_resultados
            else:
                print("⚠️ No se encontró la sección de resultados")
                return soup, None
        else:
            return soup, soup
            
    except requests.exceptions.Timeout:
        print("❌ Error: La solicitud excedió el tiempo de espera")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None, None


# Ejemplo de uso
if __name__ == "__main__":
    # Puedes cambiar el producto aquí
    producto = "ipad"
    
    soup_completo, seccion_resultados = obtener_html_mercadolibre(producto, solo_resultados=True)
    
    if seccion_resultados:
        print("\n" + "="*80)
        print("HTML DE LA SECCIÓN DE RESULTADOS:")
        print("="*80)
        print(seccion_resultados.prettify()[:10000])  # Mostrar solo los primeros 2000 caracteres
        print("\n... (HTML truncado para visualización) ...")
    elif soup_completo:
        print("\n⚠️ No se pudo extraer la sección específica, pero se obtuvo el HTML completo")
    else:
        print("\n❌ No se pudo obtener el HTML")