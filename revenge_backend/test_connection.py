"""
Script para probar la conexión a la base de datos
Ejecutar: python test_connection.py
"""

from config.database import Database

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("="*60)
    print("🔍 PROBANDO CONEXIÓN A LA BASE DE DATOS")
    print("="*60)
    
    try:
        # Test básico de conexión
        if Database.test_connection():
            print("✅ Conexión exitosa!")
            
            # Probar algunas queries
            print("\n📊 Probando queries básicas...")
            
            # Contar estados
            with Database.get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM estados")
                result = cursor.fetchone()
                print(f"   - Estados en BD: {result['total']}")
                
                cursor.execute("SELECT COUNT(*) as total FROM roles")
                result = cursor.fetchone()
                print(f"   - Roles en BD: {result['total']}")
                
                cursor.execute("SELECT COUNT(*) as total FROM usuarios")
                result = cursor.fetchone()
                print(f"   - Usuarios en BD: {result['total']}")
                
                cursor.execute("SELECT COUNT(*) as total FROM metodos_pago")
                result = cursor.fetchone()
                print(f"   - Métodos de pago en BD: {result['total']}")
            
            print("\n✅ ¡Todas las pruebas pasaron correctamente!")
            print("\n🚀 Puedes ejecutar el servidor con: python app.py")
            
        else:
            print("❌ Error en la conexión")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Verifica:")
        print("   1. MySQL está corriendo")
        print("   2. La base de datos 'mazza' existe")
        print("   3. Las credenciales en .env son correctas")
        print("   4. El usuario tiene permisos")
    
    print("="*60)


if __name__ == '__main__':
    test_database_connection()
