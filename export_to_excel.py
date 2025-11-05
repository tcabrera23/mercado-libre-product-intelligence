"""
Script para exportar JSON de productos a Excel con formato
"""

import pandas as pd
import json
import sys
import os
from datetime import datetime

# Configurar encoding para Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def clasificar_precio(precio_actual, promedio):
    """
    Clasifica productos por precio en categorías
    
    Args:
        precio_actual: Precio del producto (int)
        promedio: Precio promedio de todos los productos (float)
        
    Returns:
        str: "Económico", "Mediano" o "Caro"
    """
    umbral_economico = promedio * 0.9  # 10% por debajo del promedio
    umbral_caro = promedio * 1.1        # 10% por encima del promedio
    
    if precio_actual < umbral_economico:
        return "Económico"
    elif precio_actual > umbral_caro:
        return "Caro"
    else:
        return "Mediano"


def extraer_marca(titulo):
    """
    Intenta extraer la marca del título del producto
    """
    # Marcas comunes
    marcas_comunes = [
        'Samsung', 'Apple', 'Xiaomi', 'Motorola', 'iPhone', 'iPad',
        'Logitech', 'Redragon', 'HyperX', 'Razer', 'Corsair',
        'Sony', 'JBL', 'Harman', 'Bose', 'Audio-Technica',
        'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI',
        'Nike', 'Adidas', 'Puma', 'Reebok'
    ]
    
    titulo_upper = titulo.upper()
    for marca in marcas_comunes:
        if marca.upper() in titulo_upper:
            return marca
    
    # Si no se encuentra, intentar tomar la primera palabra
    primera_palabra = titulo.split()[0] if titulo.split() else "Sin marca"
    return primera_palabra


def limpiar_precio(precio_str):
    """
    Convierte string de precio a número
    Ej: "$25.109" -> 25109
    """
    try:
        # Remover $ y puntos
        precio_limpio = precio_str.replace('$', '').replace('.', '').replace(',', '')
        return int(precio_limpio)
    except:
        return 0


def json_to_excel(json_path, output_path=None):
    """
    Convierte JSON de productos a Excel con formato y categorización
    
    Args:
        json_path: Ruta al archivo JSON
        output_path: Ruta del archivo Excel de salida (opcional)
        
    Returns:
        str: Ruta del archivo Excel generado
    """
    print(f"\n{'='*80}")
    print(f"📊 EXPORT JSON → EXCEL")
    print(f"{'='*80}\n")
    
    # Cargar JSON
    print(f"📂 Cargando: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    productos = data.get('productos', [])
    producto_buscado = data.get('producto_buscado', 'productos')
    
    print(f"✅ {len(productos)} productos cargados")
    
    if not productos:
        print("❌ No hay productos para exportar")
        return None
    
    # Convertir a DataFrame
    df = pd.DataFrame(productos)
    
    # Agregar columnas calculadas
    print(f"\n🔧 Procesando datos...")
    
    # 1. Limpiar precios
    df['precio_numerico'] = df['precio_actual'].apply(limpiar_precio)
    df['precio_anterior_numerico'] = df['precio_anterior'].apply(limpiar_precio)
    
    # 2. Calcular descuento numérico
    df['descuento_porcentaje'] = df['descuento'].str.replace('%', '').str.replace(' OFF', '').str.strip()
    df['descuento_porcentaje'] = pd.to_numeric(df['descuento_porcentaje'], errors='coerce').fillna(0)
    
    # 3. Clasificar por precio
    promedio_precio = df['precio_numerico'].mean()
    df['categoria_precio'] = df['precio_numerico'].apply(
        lambda x: clasificar_precio(x, promedio_precio)
    )
    
    # 4. Extraer marca
    df['marca'] = df['titulo'].apply(extraer_marca)
    
    # 5. Convertir envio_gratis a texto
    df['envio_gratis_texto'] = df['envio_gratis'].apply(lambda x: 'Sí' if x else 'No')
    
    print(f"   ✅ Precios procesados (promedio: ${promedio_precio:,.0f})")
    print(f"   ✅ Categorías de precio asignadas")
    print(f"   ✅ Marcas extraídas")
    
    # Reordenar columnas para mejor visualización
    columnas_orden = [
        'id',
        'titulo',
        'marca',
        'precio_actual',
        'precio_numerico',
        'precio_anterior',
        'descuento',
        'descuento_porcentaje',
        'categoria_precio',
        'calificacion',
        'vendidos',
        'envio_gratis',
        'envio_gratis_texto',
        'link',
        'imagen'
    ]
    
    # Mantener solo columnas que existen
    columnas_orden = [col for col in columnas_orden if col in df.columns]
    df = df[columnas_orden]
    
    # Generar nombre de archivo si no se proporciona
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"productos_{producto_buscado.replace(' ', '_')}_{timestamp}.xlsx"
    
    # Exportar a Excel con formato
    print(f"\n💾 Guardando en Excel...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Productos', index=False)
        
        # Obtener el workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets['Productos']
        
        # Ajustar anchos de columna
        for idx, col in enumerate(df.columns, 1):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(str(col))
            )
            # Limitar a 50 caracteres max
            max_length = min(max_length, 50)
            worksheet.column_dimensions[chr(64 + idx)].width = max_length + 2
        
        # Agregar hoja de resumen
        resumen_data = {
            'Métrica': [
                'Total de Productos',
                'Precio Promedio',
                'Precio Mínimo',
                'Precio Máximo',
                'Productos Económicos',
                'Productos Medianos',
                'Productos Caros',
                'Con Envío Gratis',
                'Calificación Promedio',
                'Producto Buscado',
                'Fecha de Extracción'
            ],
            'Valor': [
                len(df),
                f"${df['precio_numerico'].mean():,.0f}",
                f"${df['precio_numerico'].min():,.0f}",
                f"${df['precio_numerico'].max():,.0f}",
                len(df[df['categoria_precio'] == 'Económico']),
                len(df[df['categoria_precio'] == 'Mediano']),
                len(df[df['categoria_precio'] == 'Caro']),
                len(df[df['envio_gratis'] == True]),
                f"{df['calificacion'].mean():.2f}",
                producto_buscado,
                data.get('fecha_busqueda', 'N/A')
            ]
        }
        
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
    
    print(f"✅ Archivo Excel creado: {output_path}")
    
    # Mostrar estadísticas
    print(f"\n📊 Estadísticas:")
    print(f"   Total productos: {len(df)}")
    print(f"   Precio promedio: ${df['precio_numerico'].mean():,.0f}")
    print(f"   Rango: ${df['precio_numerico'].min():,.0f} - ${df['precio_numerico'].max():,.0f}")
    print(f"\n📁 Categorías de precio:")
    print(f"   Económico: {len(df[df['categoria_precio'] == 'Económico'])} productos")
    print(f"   Mediano: {len(df[df['categoria_precio'] == 'Mediano'])} productos")
    print(f"   Caro: {len(df[df['categoria_precio'] == 'Caro'])} productos")
    
    return output_path


if __name__ == "__main__":
    print("\n" + "="*80)
    print("📊 EXPORTADOR DE JSON A EXCEL")
    print("="*80 + "\n")
    
    if len(sys.argv) > 1:
        archivo_json = sys.argv[1]
    else:
        print("Ejemplos de archivos:")
        print("  • productos_ipad_20251104_210247.json")
        print("  • productos_auriculares_20251104_202812.json")
        print()
        archivo_json = input("📂 Ingresa el archivo JSON ► ").strip()
        
        if not archivo_json:
            print("❌ No ingresaste ningún archivo")
            sys.exit(1)
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_json):
        print(f"❌ Error: El archivo '{archivo_json}' no existe")
        sys.exit(1)
    
    try:
        excel_path = json_to_excel(archivo_json)
        
        if excel_path:
            print(f"\n{'='*80}")
            print(f"✅ EXPORT COMPLETADO!")
            print(f"📁 Archivo: {excel_path}")
            print(f"{'='*80}\n")
            
            print("💡 Puedes abrir el archivo en Excel para ver:")
            print("   • Hoja 'Productos': Todos los productos con datos procesados")
            print("   • Hoja 'Resumen': Estadísticas generales")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

