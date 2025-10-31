"""
Modelo Venta
Estructura: Lista para registrar detalles de venta
"""

from config.database import Database
from datetime import datetime


class VentaModel:
    """Modelo para manejar ventas"""
    
    @staticmethod
    def crear(numero_boleta, cajero_id, subtotal, descuento, impuestos, 
              total, metodo_pago_id, observaciones=None):
        """Crea una nueva venta (cabecera)"""
        query = """
            INSERT INTO ventas (numero_boleta, cajero_id, subtotal, descuento,
                              impuestos, total, metodo_pago_id, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (numero_boleta, cajero_id, subtotal, descuento, 
                 impuestos, total, metodo_pago_id, observaciones)
        
        try:
            venta_id = Database.execute_query(query, params, commit=True)
            return venta_id
        except Exception as e:

            raise
    
    @staticmethod
    def obtener_por_id(venta_id):
        """Obtiene una venta con sus detalles"""
        query = """
            SELECT v.*, u.nombre as cajero_nombre, mp.nombre as metodo_pago_nombre
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            WHERE v.id = %s
        """
        venta = Database.execute_query(query, (venta_id,), fetch_one=True)
        
        if venta:
            # Obtener detalles
            venta['detalles'] = VentaModel.obtener_detalles(venta_id)
        
        return venta
    
    @staticmethod
    def obtener_por_numero_boleta(numero_boleta):
        """Obtiene una venta por número de boleta"""
        query = """
            SELECT v.*, u.nombre as cajero_nombre, mp.nombre as metodo_pago_nombre
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            WHERE v.numero_boleta = %s
        """
        venta = Database.execute_query(query, (numero_boleta,), fetch_one=True)
        
        if venta:
            venta['detalles'] = VentaModel.obtener_detalles(venta['id'])
        
        return venta
    
    @staticmethod
    def obtener_todas(limite=100, offset=0):
        """Obtiene todas las ventas con paginación"""
        query = """
            SELECT v.id, v.numero_boleta, v.cajero_id, u.nombre as cajero_nombre,
                   v.fecha, v.subtotal, v.descuento, v.impuestos, v.total,
                   mp.nombre as metodo_pago_nombre
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            ORDER BY v.fecha DESC
            LIMIT %s OFFSET %s
        """
        return Database.execute_query(query, (limite, offset), fetch_all=True)
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene ventas por rango de fechas"""
        query = """
            SELECT v.*, u.nombre as cajero_nombre, mp.nombre as metodo_pago_nombre,
                   (SELECT COALESCE(SUM(dv.cantidad), 0) FROM detalle_venta dv WHERE dv.venta_id = v.id) as total_productos
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            WHERE DATE(v.fecha) BETWEEN %s AND %s
            ORDER BY v.fecha DESC
        """
        return Database.execute_query(query, (fecha_inicio, fecha_fin), fetch_all=True)
    
    @staticmethod
    def obtener_por_cajero(cajero_id, fecha_inicio=None, fecha_fin=None):
        """Obtiene ventas de un cajero específico"""
        query = """
            SELECT v.*, u.nombre as cajero_nombre, mp.nombre as metodo_pago_nombre
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            WHERE v.cajero_id = %s
        """
        params = [cajero_id]
        
        if fecha_inicio and fecha_fin:
            query += " AND DATE(v.fecha) BETWEEN %s AND %s"
            params.extend([fecha_inicio, fecha_fin])
        
        query += " ORDER BY v.fecha DESC"
        
        return Database.execute_query(query, tuple(params), fetch_all=True)
    
    @staticmethod
    def obtener_detalles(venta_id):
        """Obtiene los detalles de una venta - Estructura de Lista"""
        query = """
            SELECT dv.*, p.nombre as producto_nombre, p.codigo_barras
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = %s
            ORDER BY dv.id
        """
        return Database.execute_query(query, (venta_id,), fetch_all=True)
    
    @staticmethod
    def obtener_resumen_dia(fecha=None):
        """Obtiene resumen de ventas del día"""
        if not fecha:
            fecha = datetime.now().strftime('%Y-%m-%d')
        
        query = """
            SELECT 
                COUNT(*) as total_ventas,
                SUM(total) as total_ingresos,
                SUM(descuento) as total_descuentos,
                AVG(total) as ticket_promedio
            FROM ventas
            WHERE DATE(fecha) = %s
        """
        return Database.execute_query(query, (fecha,), fetch_one=True)
    
    @staticmethod
    def obtener_productos_mas_vendidos(limite=10, fecha_inicio=None, fecha_fin=None):
        """Obtiene los productos más vendidos"""
        query = """
            SELECT p.id, p.nombre, p.codigo_barras,
                   SUM(dv.cantidad) as total_vendido,
                   SUM(dv.subtotal) as total_ingresos
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            INNER JOIN ventas v ON dv.venta_id = v.id
        """
        params = []
        
        if fecha_inicio and fecha_fin:
            query += " WHERE DATE(v.fecha) BETWEEN %s AND %s"
            params.extend([fecha_inicio, fecha_fin])
        
        query += """
            GROUP BY p.id, p.nombre, p.codigo_barras
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        params.append(limite)
        
        return Database.execute_query(query, tuple(params), fetch_all=True)
    
    @staticmethod
    def generar_numero_boleta():
        """Genera el siguiente número de boleta"""
        query = """
            SELECT numero_boleta FROM ventas 
            ORDER BY id DESC LIMIT 1
        """
        ultima_venta = Database.execute_query(query, fetch_one=True)
        
        if ultima_venta:
            ultimo_numero = ultima_venta['numero_boleta']
            # Extraer número (formato: B-00001)
            try:
                numero = int(ultimo_numero.split('-')[1])
                nuevo_numero = numero + 1
            except:
                nuevo_numero = 1
        else:
            nuevo_numero = 1
        
        return f"B-{nuevo_numero:05d}"
    
    @staticmethod
    def verificar_numero_boleta_existe(numero_boleta):
        """Verifica si un número de boleta ya existe"""
        query = "SELECT id FROM ventas WHERE numero_boleta = %s"
        resultado = Database.execute_query(query, (numero_boleta,), fetch_one=True)
        return resultado is not None
