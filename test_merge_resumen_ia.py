#!/usr/bin/env python3
"""
Script de prueba para verificar el merge de resumen_ia
Testea que el JOIN entre productos y análisis funcione correctamente
"""

import json
import pandas as pd
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_merge_resumen_ia():
    """Prueba el merge entre productos y análisis"""
    print("=" * 60)
    print("🧪 TEST: Merge de resumen_ia")
    print("=" * 60)
    
    # Cargar JSONs
    print("\n1️⃣ Cargando JSONs...")
    
    try:
        with open('productos_auriculares_bluetooth_20251104_212857.json', 'r', encoding='utf-8') as f:
            data_productos = json.load(f)
        print("✅ JSON de productos cargado")
    except FileNotFoundError:
        print("❌ Archivo de productos no encontrado")
        return False
    
    try:
        with open('analisis_resenias_auriculares_bluetooth_20251104_213319.json', 'r', encoding='utf-8') as f:
            data_analisis = json.load(f)
        print("✅ JSON de análisis cargado")
    except FileNotFoundError:
        print("❌ Archivo de análisis no encontrado")
        return False
    
    # Crear DataFrames
    print("\n2️⃣ Creando DataFrames...")
    df_productos = pd.DataFrame(data_productos.get('productos', []))
    df_analisis = pd.DataFrame(data_analisis.get('productos', []))
    
    print(f"   - Productos: {len(df_productos)} filas")
    print(f"   - Análisis: {len(df_analisis)} filas")
    print(f"   - Columnas productos: {list(df_productos.columns)[:5]}...")
    print(f"   - Columnas análisis: {list(df_analisis.columns)[:5]}...")
    
    # Verificar campos clave
    print("\n3️⃣ Verificando campos clave...")
    if 'id' not in df_productos.columns:
        print("❌ Campo 'id' no encontrado en productos")
        return False
    else:
        print("✅ Campo 'id' existe en productos")
    
    if 'producto_id' not in df_analisis.columns:
        print("❌ Campo 'producto_id' no encontrado en análisis")
        return False
    else:
        print("✅ Campo 'producto_id' existe en análisis")
    
    # Test con id específico: fc48da47
    print("\n4️⃣ Testeando con id 'fc48da47'...")
    test_id = "fc48da47"
    
    # Buscar en productos
    producto_test = df_productos[df_productos['id'] == test_id]
    if len(producto_test) > 0:
        print(f"✅ Producto encontrado:")
        print(f"   - ID: {producto_test.iloc[0]['id']}")
        print(f"   - Título: {producto_test.iloc[0]['titulo'][:50]}...")
    else:
        print(f"❌ Producto con id '{test_id}' no encontrado")
        return False
    
    # Buscar en análisis
    analisis_test = df_analisis[df_analisis['producto_id'] == test_id]
    if len(analisis_test) > 0:
        print(f"✅ Análisis encontrado:")
        print(f"   - ID: {analisis_test.iloc[0]['producto_id']}")
        print(f"   - Resumen IA: {analisis_test.iloc[0]['resumen_ia'][:80]}...")
    else:
        print(f"❌ Análisis con producto_id '{test_id}' no encontrado")
        return False
    
    # Realizar merge
    print("\n5️⃣ Realizando merge...")
    df_merged = df_productos.merge(
        df_analisis[['producto_id', 'resumen_ia', 'opiniones_1_estrella']],
        left_on='id',
        right_on='producto_id',
        how='left'
    )
    
    print(f"   - Filas después del merge: {len(df_merged)}")
    print(f"   - Columnas después del merge: {len(df_merged.columns)}")
    
    # Verificar que resumen_ia existe
    if 'resumen_ia' in df_merged.columns:
        print("✅ Columna 'resumen_ia' existe después del merge")
    else:
        print("❌ Columna 'resumen_ia' NO existe después del merge")
        print(f"   Columnas disponibles: {list(df_merged.columns)}")
        return False
    
    # Verificar el producto de prueba
    print("\n6️⃣ Verificando resultado del merge para 'fc48da47'...")
    producto_merged = df_merged[df_merged['id'] == test_id]
    
    if len(producto_merged) > 0:
        resumen = producto_merged.iloc[0].get('resumen_ia', None)
        
        if resumen and resumen != "Sin análisis disponible":
            print(f"✅ Resumen IA encontrado:")
            print(f"   {resumen[:150]}...")
        elif resumen == "Sin análisis disponible":
            print("⚠️ Resumen IA es 'Sin análisis disponible'")
        else:
            print("❌ Resumen IA es None o no existe")
            return False
    else:
        print(f"❌ Producto '{test_id}' no encontrado después del merge")
        return False
    
    # Estadísticas finales
    print("\n7️⃣ Estadísticas del merge...")
    total_con_resumen = df_merged['resumen_ia'].notna().sum()
    total_sin_resumen = df_merged['resumen_ia'].isna().sum()
    
    print(f"   - Total productos: {len(df_merged)}")
    print(f"   - Con resumen IA: {total_con_resumen}")
    print(f"   - Sin resumen IA: {total_sin_resumen}")
    print(f"   - % con resumen: {(total_con_resumen/len(df_merged)*100):.1f}%")
    
    # Verificar algunos más
    print("\n8️⃣ Verificando primeros 5 productos...")
    for idx, row in df_merged.head(5).iterrows():
        resumen = row.get('resumen_ia', None)
        tiene_resumen = "✅" if (resumen and resumen != "Sin análisis disponible") else "❌"
        print(f"   {tiene_resumen} {row['id']}: {row['titulo'][:40]}...")
    
    print("\n" + "=" * 60)
    print("🎉 TEST COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        exito = test_merge_resumen_ia()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

