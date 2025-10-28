"""
Script de Prueba para Reportes
Verifica que los reportes funcionen correctamente con la BD corregida
"""

import sys
sys.path.append('.')

from revenge_backend.models.reporte_model import ReporteModel
from datetime import datetime, timedelta

def test_reporte_ventas():
    """Prueba el reporte de ventas"""
    print("\n" + "="*60)
    print("🧪 PROBANDO REPORTE DE VENTAS")
    print("="*60)
    
    try:
        # Últimos 7 días
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n📅 Período: {fecha_inicio} a {fecha_fin}")
        
        resultado = ReporteModel.reporte_ventas(fecha_inicio, fecha_fin)
        
        print("\n✅ RESUMEN:")
        print(f"   - Total ventas: {resultado['resumen']['total_ventas']}")
        print(f"   - Monto total: S/. {resultado['resumen']['monto_total']:.2f}")
        print(f"   - Promedio: S/. {resultado['resumen']['promedio_venta']:.2f}")
        
        print("\n📊 PRODUCTOS MÁS VENDIDOS:")
        for i, prod in enumerate(resultado['productos_mas_vendidos'][:5], 1):
            print(f"   {i}. {prod['producto']}: {prod['cantidad']} unidades (S/. {prod['total']:.2f})")
        
        print("\n💳 VENTAS POR MÉTODO DE PAGO:")
        for metodo in resultado['ventas_por_metodo_pago']:
            print(f"   - {metodo['metodo']}: {metodo['cantidad']} ventas (S/. {metodo['total']:.2f})")
        
        print("\n👤 VENTAS POR CAJERO:")
        for cajero in resultado['ventas_por_cajero']:
            print(f"   - {cajero['cajero']}: {cajero['cantidad']} ventas (S/. {cajero['total']:.2f})")
        
        print("\n✅ ¡Reporte de ventas OK!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reporte_inventario():
    """Prueba el reporte de inventario"""
    print("\n" + "="*60)
    print("🧪 PROBANDO REPORTE DE INVENTARIO")
    print("="*60)
    
    try:
        resultado = ReporteModel.reporte_inventario()
        
        print("\n✅ RESUMEN:")
        print(f"   - Total productos: {resultado['resumen']['total_productos']}")
        print(f"   - Valor inventario: S/. {resultado['resumen']['valor_inventario']:.2f}")
        print(f"   - Valor venta potencial: S/. {resultado['resumen']['valor_venta_potencial']:.2f}")
        print(f"   - Productos con stock bajo: {resultado['resumen']['productos_stock_bajo']}")
        print(f"   - Productos sin stock: {resultado['resumen']['productos_sin_stock']}")
        
        print("\n📦 PRODUCTOS POR CATEGORÍA:")
        for cat in resultado['productos_por_categoria']:
            print(f"   - {cat['categoria']}: {cat['cantidad']} productos, {cat['stock_total']} unidades (S/. {cat['valor']:.2f})")
        
        if resultado['productos_stock_bajo']:
            print("\n⚠️  PRODUCTOS CON STOCK BAJO:")
            for prod in resultado['productos_stock_bajo'][:5]:
                print(f"   - {prod['nombre']}: {prod['stock_actual']} / {prod['stock_minimo']} mínimo")
        
        if resultado['productos_sin_stock']:
            print("\n🚨 PRODUCTOS SIN STOCK:")
            for prod in resultado['productos_sin_stock'][:5]:
                print(f"   - {prod['nombre']} ({prod['categoria']})")
        
        print("\n✅ ¡Reporte de inventario OK!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reporte_compras():
    """Prueba el reporte de compras"""
    print("\n" + "="*60)
    print("🧪 PROBANDO REPORTE DE COMPRAS")
    print("="*60)
    
    try:
        # Últimos 30 días
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n📅 Período: {fecha_inicio} a {fecha_fin}")
        
        resultado = ReporteModel.reporte_compras(fecha_inicio, fecha_fin)
        
        print("\n✅ RESUMEN:")
        print(f"   - Total compras: {resultado['resumen']['total_compras']}")
        print(f"   - Monto total: S/. {resultado['resumen']['monto_total']:.2f}")
        print(f"   - Promedio: S/. {resultado['resumen']['promedio_compra']:.2f}")
        
        print("\n🏢 COMPRAS POR PROVEEDOR:")
        for prov in resultado['compras_por_proveedor']:
            print(f"   - {prov['proveedor']}: {prov['cantidad']} compras (S/. {prov['total']:.2f})")
        
        print("\n📦 PRODUCTOS MÁS COMPRADOS:")
        for prod in resultado['productos_mas_comprados'][:5]:
            print(f"   - {prod['producto']}: {prod['cantidad']} unidades (S/. {prod['total']:.2f})")
        
        print("\n✅ ¡Reporte de compras OK!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INICIANDO PRUEBAS DE REPORTES")
    print("="*60)
    
    resultados = {
        'ventas': test_reporte_ventas(),
        'inventario': test_reporte_inventario(),
        'compras': test_reporte_compras()
    }
    
    print("\n" + "="*60)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"   Reporte de Ventas: {'✅ PASS' if resultados['ventas'] else '❌ FAIL'}")
    print(f"   Reporte de Inventario: {'✅ PASS' if resultados['inventario'] else '❌ FAIL'}")
    print(f"   Reporte de Compras: {'✅ PASS' if resultados['compras'] else '❌ FAIL'}")
    
    if all(resultados.values()):
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
    
    print("="*60 + "\n")
