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
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#555555'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        # 🧾 1. ENCABEZADO
        elements.append(Paragraph("REVENGE POS", title_style))
        elements.append(Paragraph("🧾 REPORTE DE VENTAS", title_style))
        
        # Período y fecha de generación
        if fecha_inicio and fecha_fin:
            periodo = f"Período: Del {fecha_inicio} al {fecha_fin}"
        else:
            periodo = "Período: Todas las ventas"
        elements.append(Paragraph(periodo, subtitle_style))
        
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Fecha de generación: {fecha_generacion}", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # 📊 2. RESUMEN GENERAL (INDICADORES CLAVE)
        elements.append(Paragraph("📊 Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Total de Ventas (S/)', f"S/ {resumen.get('monto_total', 0):,.2f}"],
            ['Número de Transacciones', str(resumen.get('total_ventas', 0))],
            ['Ticket Promedio', f"S/ {resumen.get('promedio_venta', 0):,.2f}"],
            ['Venta Mínima', f"S/ {resumen.get('venta_minima', 0):,.2f}"],
            ['Venta Máxima', f"S/ {resumen.get('venta_maxima', 0):,.2f}"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3.5*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # 🛍️ 3. DETALLE DE VENTAS POR PRODUCTO
        if 'productos_mas_vendidos' in datos and datos['productos_mas_vendidos']:
            elements.append(Paragraph("🛍️ Detalle de Ventas por Producto", heading_style))
            
            productos_data = [['Código', 'Producto', 'Categoría', 'Cant.', 'P. Unit.', 'Total', '% Part.']]
            for producto in datos['productos_mas_vendidos']:
                productos_data.append([
                    producto.get('codigo', '')[:10],
                    producto.get('producto', '')[:25],
                    producto.get('categoria', '')[:15],
                    str(producto.get('cantidad', 0)),
                    f"S/ {producto.get('precio_unitario', 0):.2f}",
                    f"S/ {producto.get('total', 0):,.2f}",
                    f"{producto.get('porcentaje', 0):.1f}%"
                ])
            
            productos_table = Table(productos_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 0.5*inch, 0.8*inch, 1*inch, 0.6*inch])
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(productos_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # 👥 4. DETALLE POR VENDEDOR/CAJERO
        if 'ventas_por_cajero' in datos and datos['ventas_por_cajero']:
            elements.append(Paragraph("👥 Detalle por Vendedor/Cajero", heading_style))
            
            cajeros_data = [['Vendedor', 'Ventas Totales', 'Nº Trans.', 'Ticket Prom.', '% del Total']]
            for cajero in datos['ventas_por_cajero']:
                cajeros_data.append([
                    cajero.get('cajero', ''),
                    f"S/ {cajero.get('total', 0):,.2f}",
                    str(cajero.get('cantidad', 0)),
                    f"S/ {cajero.get('ticket_promedio', 0):,.2f}",
                    f"{cajero.get('porcentaje', 0):.1f}%"
                ])
            
            cajeros_table = Table(cajeros_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.3*inch, 1*inch])
            cajeros_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(cajeros_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # 🗓️ 5. VENTAS POR DÍA
        if 'ventas_por_dia' in datos and datos['ventas_por_dia']:
            elements.append(Paragraph("🗓️ Ventas por Día", heading_style))
            
            dias_data = [['Fecha', 'Ventas Totales', 'Nº Transacciones']]
            for dia in datos['ventas_por_dia']:
                dias_data.append([
                    dia.get('fecha', ''),
                    f"S/ {dia.get('total', 0):,.2f}",
                    str(dia.get('cantidad', 0))
                ])
            
            dias_table = Table(dias_data, colWidths=[2.5*inch, 2.5*inch, 1.8*inch])
            dias_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(dias_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # 💰 7. MÉTODOS DE PAGO
        if 'ventas_por_metodo_pago' in datos and datos['ventas_por_metodo_pago']:
            elements.append(Paragraph("💰 Métodos de Pago", heading_style))
            
            metodos_data = [['Método', 'Ventas Totales', '%']]
            for metodo in datos['ventas_por_metodo_pago']:
                metodos_data.append([
                    metodo.get('metodo', ''),
                    f"S/ {metodo.get('total', 0):,.2f}",
                    f"{metodo.get('porcentaje', 0):.1f}%"
                ])
            
            metodos_table = Table(metodos_data, colWidths=[2.5*inch, 2.5*inch, 1.8*inch])
            metodos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(metodos_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"Reporte generado por REVENGE POS - {fecha_generacion}", footer_style))
        
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
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#555555'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        # 🧾 1. ENCABEZADO
        elements.append(Paragraph("REVENGE POS", title_style))
        elements.append(Paragraph("📦 REPORTE DE COMPRAS", title_style))
        
        # Período y fecha de generación
        if fecha_inicio and fecha_fin:
            periodo = f"Período: Del {fecha_inicio} al {fecha_fin}"
        else:
            periodo = "Período: Todas las compras"
        elements.append(Paragraph(periodo, subtitle_style))
        
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Fecha de generación: {fecha_generacion}", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # 📊 2. RESUMEN GENERAL
        elements.append(Paragraph("📊 Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Total de Compras (S/)', f"S/ {resumen.get('monto_total', 0):,.2f}"],
            ['Número de Transacciones', str(resumen.get('total_compras', 0))],
            ['Promedio por Compra', f"S/ {resumen.get('promedio_compra', 0):,.2f}"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3.5*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # 📦 3. DETALLE DE COMPRAS POR PRODUCTO
        if 'productos_mas_comprados' in datos and datos['productos_mas_comprados']:
            elements.append(Paragraph("📦 Detalle de Compras por Producto", heading_style))
            
            productos_data = [['Código', 'Producto', 'Categoría', 'Cant.', 'P. Unit.', 'Total', '% Part.']]
            for producto in datos['productos_mas_comprados']:
                productos_data.append([
                    producto.get('codigo', '')[:10],
                    producto.get('producto', '')[:25],
                    producto.get('categoria', '')[:15],
                    str(producto.get('cantidad', 0)),
                    f"S/ {producto.get('precio_unitario', 0):.2f}",
                    f"S/ {producto.get('total', 0):,.2f}",
                    f"{producto.get('porcentaje', 0):.1f}%"
                ])
            
            productos_table = Table(productos_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 0.5*inch, 0.8*inch, 1*inch, 0.6*inch])
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(productos_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # 🏢 4. COMPRAS POR PROVEEDOR
        if 'compras_por_proveedor' in datos and datos['compras_por_proveedor']:
            elements.append(Paragraph("🏢 Compras por Proveedor", heading_style))
            
            proveedores_data = [['Proveedor', 'Nº Compras', 'Total', '% del Total']]
            for proveedor in datos['compras_por_proveedor']:
                proveedores_data.append([
                    proveedor.get('proveedor', ''),
                    str(proveedor.get('cantidad', 0)),
                    f"S/ {proveedor.get('total', 0):,.2f}",
                    f"{proveedor.get('porcentaje', 0):.1f}%"
                ])
            
            proveedores_table = Table(proveedores_data, colWidths=[2.5*inch, 1.3*inch, 1.8*inch, 1.2*inch])
            proveedores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(proveedores_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # 🗓️ 5. COMPRAS POR DÍA
        if 'compras_por_dia' in datos and datos['compras_por_dia']:
            elements.append(Paragraph("🗓️ Compras por Día", heading_style))
            
            dias_data = [['Fecha', 'Total Compras', 'Nº Transacciones']]
            for dia in datos['compras_por_dia']:
                dias_data.append([
                    dia.get('fecha', ''),
                    f"S/ {dia.get('total', 0):,.2f}",
                    str(dia.get('cantidad', 0))
                ])
            
            dias_table = Table(dias_data, colWidths=[2.5*inch, 2.5*inch, 1.8*inch])
            dias_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(dias_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"Reporte generado por REVENGE POS - {fecha_generacion}", footer_style))
        
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
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#555555'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        )
        
        # 🧾 1. ENCABEZADO
        elements.append(Paragraph("REVENGE POS", title_style))
        elements.append(Paragraph("📦 REPORTE DE INVENTARIO", title_style))
        
        fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Fecha de generación: {fecha_generacion}", subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # 📊 2. RESUMEN GENERAL
        elements.append(Paragraph("📊 Resumen General", heading_style))
        
        resumen = datos.get('resumen', {})
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Total de Productos', str(resumen.get('total_productos', 0))],
            ['Valor del Inventario', f"S/ {resumen.get('valor_inventario', 0):,.2f}"],
            ['Valor Potencial de Venta', f"S/ {resumen.get('valor_venta_potencial', 0):,.2f}"],
            ['⚠️ Productos con Stock Bajo', str(resumen.get('productos_stock_bajo', 0))],
            ['❌ Productos Sin Stock', str(resumen.get('productos_sin_stock', 0))]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3.5*inch, 3*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # 📂 3. INVENTARIO POR CATEGORÍA
        if 'productos_por_categoria' in datos and datos['productos_por_categoria']:
            elements.append(Paragraph("📂 Inventario por Categoría", heading_style))
            
            categorias_data = [['Categoría', 'Cant. Productos', 'Stock Total', 'Valor']]
            for categoria in datos['productos_por_categoria']:
                categorias_data.append([
                    categoria.get('categoria', ''),
                    str(categoria.get('cantidad', 0)),
                    str(categoria.get('stock_total', 0)),
                    f"S/ {categoria.get('valor', 0):,.2f}"
                ])
            
            categorias_table = Table(categorias_data, colWidths=[2.5*inch, 1.5*inch, 1.3*inch, 1.5*inch])
            categorias_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            
            elements.append(categorias_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # ⚠️ 4. PRODUCTOS CON STOCK BAJO
        if 'productos_stock_bajo' in datos and datos['productos_stock_bajo']:
            elements.append(Paragraph("⚠️ Productos con Stock Bajo (Requieren Reabastecimiento)", heading_style))
            
            stock_data = [['Código', 'Producto', 'Categoría', 'Stock', 'Mínimo']]
            for producto in datos['productos_stock_bajo'][:15]:  # Limitar a 15 productos
                stock_data.append([
                    producto.get('codigo_barras', '')[:12],
                    producto.get('nombre', '')[:30],
                    producto.get('categoria', '')[:15],
                    str(producto.get('stock_actual', 0)),
                    str(producto.get('stock_minimo', 0))
                ])
            
            stock_table = Table(stock_data, colWidths=[1*inch, 2.5*inch, 1.3*inch, 0.7*inch, 0.7*inch])
            stock_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fff3cd')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6)
            ]))
            
            elements.append(stock_table)
            elements.append(Spacer(1, 0.25*inch))
        
        # ❌ 5. PRODUCTOS SIN STOCK
        if 'productos_sin_stock' in datos and datos['productos_sin_stock']:
            elements.append(Paragraph("❌ Productos Sin Stock (Urgente)", heading_style))
            
            sin_stock_data = [['Código', 'Producto', 'Categoría']]
            for producto in datos['productos_sin_stock'][:15]:  # Limitar a 15 productos
                sin_stock_data.append([
                    producto.get('codigo_barras', '')[:12],
                    producto.get('nombre', '')[:35],
                    producto.get('categoria', '')[:20]
                ])
            
            sin_stock_table = Table(sin_stock_data, colWidths=[1.2*inch, 3.5*inch, 2.1*inch])
            sin_stock_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8d7da')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6)
            ]))
            
            elements.append(sin_stock_table)
        
        # Pie de página
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(f"Reporte generado por REVENGE POS - {fecha_generacion}", footer_style))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
