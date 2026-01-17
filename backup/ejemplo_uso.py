"""
Ejemplos de uso del sistema de búsqueda de productos de Mercado Libre

Este archivo muestra diferentes formas de usar las funciones del proyecto
"""

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

from buscar_productos_ml import buscar_producto_mercadolibre, extraer_productos_con_id, guardar_productos
from get_html import obtener_html_mercadolibre
import json


# ============================================================================
# EJEMPLO 1: Búsqueda simple
# ============================================================================
def ejemplo_busqueda_simple():
    """Ejemplo básico: buscar un producto y ver los resultados"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Búsqueda Simple")
    print("="*80)
    
    productos = buscar_producto_mercadolibre("auriculares")
    
    if productos:
        print(f"\n✅ Se encontraron {len(productos)} productos")
        print(f"   Primer producto: {productos[0]['titulo']}")
    

# ============================================================================
# EJEMPLO 2: Búsqueda de múltiples productos
# ============================================================================
def ejemplo_busqueda_multiple():
    """Buscar varios productos en secuencia"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Búsqueda Múltiple")
    print("="*80)
    
    productos_a_buscar = ["celulares samsung", "notebook", "smart tv"]
    
    resultados = {}
    
    for producto in productos_a_buscar:
        print(f"\n🔍 Buscando: {producto}")
        productos = buscar_producto_mercadolibre(producto)
        resultados[producto] = len(productos)
        
        # Importante: agregar delay entre búsquedas
        import time
        time.sleep(3)  # Esperar 3 segundos entre búsquedas
    
    print("\n" + "-"*80)
    print("📊 RESUMEN:")
    for producto, cantidad in resultados.items():
        print(f"   {producto}: {cantidad} productos encontrados")


# ============================================================================
# EJEMPLO 3: Análisis de precios
# ============================================================================
def ejemplo_analisis_precios():
    """Analizar precios de productos"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Análisis de Precios")
    print("="*80)
    
    productos = buscar_producto_mercadolibre("notebook gaming")
    
    if not productos:
        print("❌ No se encontraron productos")
        return
    
    # Extraer precios (convertir string a número)
    precios = []
    for prod in productos:
        precio_str = prod['precio_actual'].replace('$', '').replace('.', '').replace(',', '')
        try:
            precio = int(precio_str)
            precios.append(precio)
        except:
            continue
    
    if precios:
        print(f"\n💰 Análisis de precios:")
        print(f"   Productos analizados: {len(precios)}")
        print(f"   Precio más bajo: ${min(precios):,}")
        print(f"   Precio más alto: ${max(precios):,}")
        print(f"   Precio promedio: ${sum(precios)//len(precios):,}")


# ============================================================================
# EJEMPLO 4: Filtrar productos con descuento y envío gratis
# ============================================================================
def ejemplo_filtrar_descuentos():
    """Encontrar solo productos con descuento y envío gratis"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Productos con Descuento y Envío Gratis")
    print("="*80)
    
    productos = buscar_producto_mercadolibre("auriculares")
    
    if not productos:
        print("❌ No se encontraron productos")
        return
    
    # Filtrar productos con descuento
    con_descuento = [p for p in productos if p['descuento']]
    
    # Filtrar productos con envío gratis
    con_envio_gratis = [p for p in productos if p['envio_gratis']]
    
    # Filtrar productos con ambos
    combo = [p for p in productos if p['descuento'] and p['envio_gratis']]
    
    print(f"\n📊 Resultados:")
    print(f"   🎉 Con descuento: {len(con_descuento)}/{len(productos)}")
    print(f"   🚚 Con envío gratis: {len(con_envio_gratis)}/{len(productos)}")
    print(f"   ✨ Con ambos: {len(combo)}/{len(productos)}")
    
    # Mostrar los 5 mejores descuentos con envío gratis
    print("\n🏆 Top 5 ofertas (descuento + envío gratis):")
    for i, prod in enumerate(combo[:5], 1):
        print(f"\n{i}. {prod['titulo'][:60]}...")
        print(f"   💰 {prod['precio_actual']} (antes: {prod['precio_anterior']})")
        print(f"   🎯 {prod['descuento']}")
        print(f"   🚚 Envío gratis: ✅")


# ============================================================================
# EJEMPLO 5: Productos con mejor calificación
# ============================================================================
def ejemplo_mejor_calificacion():
    """Encontrar productos mejor calificados"""
    print("\n" + "="*80)
    print("EJEMPLO 5: Productos Mejor Calificados")
    print("="*80)
    
    productos = buscar_producto_mercadolibre("auriculares bluetooth")
    
    if not productos:
        print("❌ No se encontraron productos")
        return
    
    # Filtrar productos con calificación
    productos_calificados = []
    for p in productos:
        if p['calificacion'] is not None:
            productos_calificados.append((p['calificacion'], p))
    
    # Ordenar por calificación (mayor a menor)
    productos_calificados.sort(reverse=True, key=lambda x: x[0])
    
    print(f"\n⭐ Top 5 productos mejor calificados:")
    for i, (rating, prod) in enumerate(productos_calificados[:5], 1):
        print(f"\n{i}. {prod['titulo'][:60]}...")
        print(f"   ⭐ {rating} estrellas")
        print(f"   💰 {prod['precio_actual']}")
        print(f"   📦 {prod['vendidos']}")


# ============================================================================
# EJEMPLO 6: Usar solo la función de HTML (más control)
# ============================================================================
def ejemplo_uso_avanzado():
    """Uso avanzado: obtener HTML y procesarlo manualmente"""
    print("\n" + "="*80)
    print("EJEMPLO 6: Uso Avanzado (más control)")
    print("="*80)
    
    # Obtener solo el HTML
    soup_completo, seccion_resultados = obtener_html_mercadolibre(
        "notebook", 
        solo_resultados=True
    )
    
    if seccion_resultados:
        # Extraer productos
        productos = extraer_productos_con_id(seccion_resultados)
        
        # Hacer tu propio procesamiento
        print(f"\n🔧 Procesamiento personalizado:")
        print(f"   Total de productos: {len(productos)}")
        
        # Ejemplo: contar cuántos tienen envío gratis
        envio_gratis = sum(1 for p in productos if p['envio_gratis'])
        print(f"   Con envío gratis: {envio_gratis}")
        
        # Productos mejor calificados
        con_calificacion = sum(1 for p in productos if p['calificacion'] is not None)
        print(f"   Con calificación: {con_calificacion}")
        
        # Guardar con nombre personalizado
        archivo = guardar_productos(productos, "notebook_custom")
        print(f"   Guardado en: {archivo}")


# ============================================================================
# EJEMPLO 7: Comparar productos por precio/calidad
# ============================================================================
def ejemplo_comparacion_precio_calidad():
    """Encontrar productos con mejor relación precio/calidad"""
    print("\n" + "="*80)
    print("EJEMPLO 7: Mejor Relación Precio/Calidad")
    print("="*80)
    
    productos = buscar_producto_mercadolibre("auriculares")
    
    if not productos:
        print("❌ No se encontraron productos")
        return
    
    # Calcular score precio/calidad
    productos_score = []
    for p in productos:
        try:
            # Extraer precio
            precio_str = p['precio_actual'].replace('$', '').replace('.', '').replace(',', '')
            precio = int(precio_str)
            
            # Extraer calificación
            if p['calificacion'] is not None:
                rating = p['calificacion']
                
                # Score simple: rating / (precio / 10000)
                # Productos más baratos con mejor rating tendrán score más alto
                score = rating / (precio / 10000)
                productos_score.append((score, p))
        except:
            continue
    
    # Ordenar por score
    productos_score.sort(reverse=True, key=lambda x: x[0])
    
    print(f"\n🎯 Top 5 mejor relación precio/calidad:")
    for i, (score, prod) in enumerate(productos_score[:5], 1):
        print(f"\n{i}. {prod['titulo'][:60]}...")
        print(f"   Score: {score:.2f}")
        print(f"   ⭐ {prod['calificacion']} estrellas")
        print(f"   💰 {prod['precio_actual']}")


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================
def main():
    """Menú principal para ejecutar ejemplos"""
    print("\n" + "="*80)
    print("🎓 EJEMPLOS DE USO - SCRAPER DE MERCADO LIBRE")
    print("="*80)
    print("\nSelecciona un ejemplo:")
    print("  1. Búsqueda simple")
    print("  2. Búsqueda múltiple (varios productos)")
    print("  3. Análisis de precios")
    print("  4. Productos con descuento")
    print("  5. Productos mejor calificados")
    print("  6. Uso avanzado (más control)")
    print("  7. Mejor relación precio/calidad")
    print("  8. Ejecutar todos los ejemplos")
    print("  0. Salir")
    
    try:
        opcion = input("\n👉 Opción: ").strip()
        
        if opcion == "1":
            ejemplo_busqueda_simple()
        elif opcion == "2":
            ejemplo_busqueda_multiple()
        elif opcion == "3":
            ejemplo_analisis_precios()
        elif opcion == "4":
            ejemplo_filtrar_descuentos()
        elif opcion == "5":
            ejemplo_mejor_calificacion()
        elif opcion == "6":
            ejemplo_uso_avanzado()
        elif opcion == "7":
            ejemplo_comparacion_precio_calidad()
        elif opcion == "8":
            print("\n⚠️ NOTA: Esto hará múltiples requests. Toma unos minutos...")
            input("Presiona ENTER para continuar o CTRL+C para cancelar")
            ejemplo_busqueda_simple()
            ejemplo_analisis_precios()
            ejemplo_filtrar_descuentos()
            ejemplo_mejor_calificacion()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            return
        else:
            print("\n❌ Opción inválida")
    
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

