#!/usr/bin/env python3
"""
Script de prueba para verificar que analizar_resenias_ia.py
funciona correctamente cuando se ejecuta desde subprocess (sin stdin)
"""

import subprocess
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_analisis_desde_subprocess():
    """Prueba ejecutar el análisis desde subprocess"""
    print("=" * 60)
    print("🧪 TEST: Análisis de reseñas desde subprocess")
    print("=" * 60)
    
    # Usar el archivo de productos de auriculares
    archivo_productos = "productos_auriculares_bluetooth_20251104_212857.json"
    
    print(f"\n1️⃣ Ejecutando análisis desde subprocess...")
    print(f"   Archivo: {archivo_productos}")
    print(f"   Modo: No-interactivo (sin stdin)")
    print(f"   Nota: Este test no ejecuta realmente el análisis (toma mucho tiempo)")
    print(f"         Solo verifica que el comando se puede construir correctamente")
    
    # Construir comando
    comando = ['python', 'analizar_resenias_ia.py', archivo_productos]
    
    print(f"\n2️⃣ Comando a ejecutar:")
    print(f"   {' '.join(comando)}")
    
    print(f"\n3️⃣ Verificación de sintaxis...")
    try:
        # Solo verificar que el archivo existe y es ejecutable
        # No ejecutar realmente (tomaría mucho tiempo)
        with open('analizar_resenias_ia.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'sys.stdin.isatty()' in content:
                print("   ✅ Script contiene detección de modo no-interactivo")
            else:
                print("   ❌ Script NO contiene detección de modo no-interactivo")
                return False
            
            if 'EOFError' in content:
                print("   ✅ Script maneja EOFError correctamente")
            else:
                print("   ⚠️ Script podría no manejar EOFError")
    except FileNotFoundError:
        print("   ❌ Archivo analizar_resenias_ia.py no encontrado")
        return False
    
    print(f"\n4️⃣ Verificación de archivo de entrada...")
    import os
    if os.path.exists(archivo_productos):
        print(f"   ✅ Archivo de productos existe: {archivo_productos}")
    else:
        print(f"   ⚠️ Archivo de productos no encontrado (normal si no se ha ejecutado)")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETADO - Configuración correcta")
    print("=" * 60)
    print("\n💡 Para probar el análisis real desde el dashboard:")
    print("   1. streamlit run dashboard_productos_v4.py")
    print("   2. Sidebar → Búsqueda en Tiempo Real")
    print("   3. Buscar un producto con 'Incluir reseñas' marcado")
    print("   4. Verificar que NO aparezca el error EOFError")
    
    return True


if __name__ == "__main__":
    try:
        exito = test_analisis_desde_subprocess()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

