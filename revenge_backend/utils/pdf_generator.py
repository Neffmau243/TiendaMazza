"""
Generador de PDFs para Reportes
Utiliza reportlab para crear documentos PDF
"""

from io import BytesIO
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  WARNING: reportlab no está instalado. Instala con: pip install reportlab")


class PDFGenerator:
    """Generador de reportes en PDF"""
    
    @staticmethod
    def _check_reportlab():
        """Verifica si reportlab está disponible"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab no está instalado. Ejecuta: pip install reportlab")
    
    @staticmethod
    def generar_reporte_ventas(datos, fecha_inicio=None, fecha_fin=None):
        """
        Genera PDF de reporte de ventas
        
        Args:
            datos (dict): Datos del reporte
            fecha_inicio (str): Fecha inicio
            fecha_fin (str): Fecha fin
            
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        PDFGenerator._check_reportlab()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Título
        elements.append(Paragraph("REPORTE DE VENTAS", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Período
        if fecha_inicio and fecha_fin:
            periodo = f"Período: {fecha_inicio} al {fecha_fin}"
        else:
            periodo = "Período: Todas las ventas"
        elements.append(Paragraph(periodo, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Resumen
        elements.append(Paragraph("Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Total de Ventas', str(resumen.get('total_ventas', 0))],
            ['Total Ingresos', f"${resumen.get('monto_total', 0):,.2f}"],
            ['Ticket Promedio', f"${resumen.get('promedio_venta', 0):,.2f}"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Productos más vendidos
        if 'productos_mas_vendidos' in datos and datos['productos_mas_vendidos']:
            elements.append(Paragraph("Productos Más Vendidos", heading_style))
            
            productos_data = [['Producto', 'Cantidad', 'Total']]
            for producto in datos['productos_mas_vendidos'][:10]:
                productos_data.append([
                    producto.get('producto', ''),
                    str(producto.get('cantidad', 0)),
                    f"${producto.get('total', 0):,.2f}"
                ])
            
            productos_table = Table(productos_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(productos_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.5*inch))
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Generado el: {fecha_generacion}", styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_reporte_compras(datos, fecha_inicio=None, fecha_fin=None):
        """
        Genera PDF de reporte de compras
        
        Args:
            datos (dict): Datos del reporte
            fecha_inicio (str): Fecha inicio
            fecha_fin (str): Fecha fin
            
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        PDFGenerator._check_reportlab()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Título
        elements.append(Paragraph("REPORTE DE COMPRAS", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Período
        if fecha_inicio and fecha_fin:
            periodo = f"Período: {fecha_inicio} al {fecha_fin}"
        else:
            periodo = "Período: Todas las compras"
        elements.append(Paragraph(periodo, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Resumen
        elements.append(Paragraph("Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Total de Compras', str(resumen.get('total_compras', 0))],
            ['Total Gastos', f"${resumen.get('monto_total', 0):,.2f}"],
            ['Promedio por Compra', f"${resumen.get('promedio_compra', 0):,.2f}"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Compras por proveedor
        if 'compras_por_proveedor' in datos and datos['compras_por_proveedor']:
            elements.append(Paragraph("Compras por Proveedor", heading_style))
            
            proveedores_data = [['Proveedor', 'Cantidad', 'Total']]
            for proveedor in datos['compras_por_proveedor']:
                proveedores_data.append([
                    proveedor.get('proveedor', ''),
                    str(proveedor.get('cantidad', 0)),
                    f"${proveedor.get('total', 0):,.2f}"
                ])
            
            proveedores_table = Table(proveedores_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
            proveedores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(proveedores_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.5*inch))
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Generado el: {fecha_generacion}", styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generar_reporte_inventario(datos):
        """
        Genera PDF de reporte de inventario
        
        Args:
            datos (dict): Datos del reporte
            
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        PDFGenerator._check_reportlab()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Título
        elements.append(Paragraph("REPORTE DE INVENTARIO", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Resumen
        elements.append(Paragraph("Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Total Productos', str(resumen.get('total_productos', 0))],
            ['Valor Inventario', f"${resumen.get('valor_inventario', 0):,.2f}"],
            ['Stock Bajo', str(resumen.get('productos_stock_bajo', 0))],
            ['Sin Stock', str(resumen.get('productos_sin_stock', 0))]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Productos con stock bajo
        if 'productos_stock_bajo' in datos and datos['productos_stock_bajo']:
            elements.append(Paragraph("⚠️ Productos con Stock Bajo", heading_style))
            
            stock_data = [['Código', 'Producto', 'Stock', 'Mínimo']]
            for producto in datos['productos_stock_bajo']:
                stock_data.append([
                    producto.get('codigo_barras', ''),
                    producto.get('nombre', ''),
                    str(producto.get('stock_actual', 0)),
                    str(producto.get('stock_minimo', 0))
                ])
            
            stock_table = Table(stock_data, colWidths=[1.2*inch, 3*inch, 0.9*inch, 0.9*inch])
            stock_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(stock_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.5*inch))
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Generado el: {fecha_generacion}", styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
