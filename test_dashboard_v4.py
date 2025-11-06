#!/usr/bin/env python3
"""
Script de prueba para verificar el Dashboard v4.1
Verifica que todos los componentes funcionen correctamente
"""

import json
import os
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_archivos_json():
    """Verifica que existan archivos JSON de productos y análisis"""
    print("🔍 Verificando archivos JSON...")
    
    archivos_productos = [f for f in os.listdir('.') if f.startswith('productos_') and f.endswith('.json')]
    archivos_analisis = [f for f in os.listdir('.') if f.startswith('analisis_resenias_') and f.endswith('.json')]
    
    if not archivos_productos:
        print("❌ No se encontraron archivos de productos")
        print("💡 Ejecuta: python buscar_productos_ml.py 'producto'")
        return False
    
    print(f"✅ Encontrados {len(archivos_productos)} archivos de productos:")
    for f in archivos_productos:
        print(f"   - {f}")
    
    if archivos_analisis:
        print(f"✅ Encontrados {len(archivos_analisis)} archivos de análisis:")
        for f in archivos_analisis:
            print(f"   - {f}")
    else:
        print("⚠️ No se encontraron archivos de análisis de reseñas")
        print("💡 Ejecuta: python analizar_resenias_ia.py")
    
    return True


def test_estructura_json():
    """Verifica la estructura de los JSONs para el JOIN"""
    print("\n🔍 Verificando estructura de JSONs...")
    
    archivos_productos = [f for f in os.listdir('.') if f.startswith('productos_') and f.endswith('.json')]
    archivos_analisis = [f for f in os.listdir('.') if f.startswith('analisis_resenias_') and f.endswith('.json')]
    
    if archivos_productos:
        with open(archivos_productos[0], 'r', encoding='utf-8') as f:
            data_productos = json.load(f)
            productos = data_productos.get('productos', [])
            if productos:
                primer_producto = productos[0]
                print(f"✅ Estructura de productos OK:")
                print(f"   - Campo ID: '{primer_producto.get('id', 'NO ENCONTRADO')}'")
                print(f"   - Campos disponibles: {list(primer_producto.keys())}")
    
    if archivos_analisis:
        with open(archivos_analisis[0], 'r', encoding='utf-8') as f:
            data_analisis = json.load(f)
            productos_analisis = data_analisis.get('productos', [])
            if productos_analisis:
                primer_analisis = productos_analisis[0]
                print(f"✅ Estructura de análisis OK:")
                print(f"   - Campo ID: '{primer_analisis.get('producto_id', 'NO ENCONTRADO')}'")
                print(f"   - Tiene resumen_ia: {bool(primer_analisis.get('resumen_ia'))}")
                print(f"   - Campos disponibles: {list(primer_analisis.keys())}")
    
    return True


def test_groq_api_key():
    """Verifica la configuración de la API key de Groq"""
    print("\n🔍 Verificando API Key de Groq...")
    
    # Verificar en variables de entorno
    api_key = os.getenv("GROQ_API_KEY")
    
    if api_key:
        print(f"✅ API Key encontrada en variable de entorno")
        print(f"   - Primeros 10 caracteres: {api_key[:10]}...")
        return True
    else:
        print("⚠️ GROQ_API_KEY no encontrada en variables de entorno")
        print("💡 El chatbot estará deshabilitado")
        print("📝 Para habilitarlo:")
        print("   Windows: set GROQ_API_KEY=tu_api_key_aqui")
        print("   Linux/Mac: export GROQ_API_KEY=tu_api_key_aqui")
        return False


def test_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'plotly': 'Plotly',
        'groq': 'Groq',
        'openpyxl': 'Openpyxl'
    }
    
    todas_ok = True
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {nombre} instalado")
        except ImportError:
            print(f"❌ {nombre} NO instalado")
            todas_ok = False
    
    if not todas_ok:
        print("\n💡 Instala las dependencias faltantes:")
        print("   pip install -r requirements.txt")
    
    return todas_ok


def main():
    print("=" * 60)
    print("🧪 TEST DASHBOARD v4.1 - Verificación de Sistema")
    print("=" * 60)
    
    tests = [
        ("Archivos JSON", test_archivos_json),
        ("Estructura JSON", test_estructura_json),
        ("Dependencias Python", test_dependencias),
        ("Groq API Key", test_groq_api_key),
    ]
    
    resultados = []
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error en test '{nombre}': {e}")
            resultados.append((nombre, False))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    for nombre, resultado in resultados:
        status = "✅ OK" if resultado else "❌ FAIL"
        print(f"{status} - {nombre}")
    
    total_ok = sum(1 for _, r in resultados if r)
    print(f"\nTests exitosos: {total_ok}/{len(resultados)}")
    
    if total_ok == len(resultados):
        print("\n🎉 ¡Todo listo! Puedes ejecutar el dashboard:")
        print("   streamlit run dashboard_productos_v4.py")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los mensajes arriba.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

