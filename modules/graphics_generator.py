"""
📈 modules/graphics_generator.py - GENERACIÓN DE GRÁFICAS
"""

# Importaciones para gráficos (exactamente como las tienes)
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import MaxNLocator
    import numpy as np
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True
    GRAFICOS_DISPONIBLES = True
    print("✅ Matplotlib cargado para gráficos")
except ImportError:
    GRAFICOS_DISPONIBLES = False
    print("⚠️ Matplotlib no disponible - gráficos deshabilitados")

import openpyxl
from datetime import datetime
import os
from .config import *
from .excel_manager import ExcelManager

class GraphicsGenerator:
    """
    Generador de gráficas
    CONTIENE EXACTAMENTE TU LÓGICA ACTUAL DE GRÁFICAS, SOLO ORGANIZADA
    """
    
    @staticmethod
    def generar_grafica_combustibles():
        """Genera gráfica de combustibles - EXACTAMENTE TU LÓGICA ACTUAL"""
        if not GRAFICOS_DISPONIBLES or not os.path.exists(ARCHIVO_EXCEL_MATERIALES):
            print("❌ No hay archivo de materiales o matplotlib no disponible")
            return None
        
        try:
            libro = openpyxl.load_workbook(ARCHIVO_EXCEL_MATERIALES)
            hoja = libro.active
            
            print(f"📊 Leyendo archivo con {hoja.max_row} filas")
            
            movimientos_gasolina = []
            movimientos_diesel = []
            
            # Buscar datos de forma más flexible (exactamente como lo tienes)
            for row in range(5, hoja.max_row + 1):
                material = hoja.cell(row=row, column=3).value
                fecha = hoja.cell(row=row, column=1).value
                movimiento = hoja.cell(row=row, column=5).value
                cantidad = hoja.cell(row=row, column=6).value
                
                if material and movimiento and cantidad:
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                        
                        if "gasolina" in str(material).lower():
                            signo = 1 if "📈" in str(movimiento) or "entrada" in str(movimiento).lower() else -1
                            movimientos_gasolina.append((fecha, cantidad_num * signo))
                        
                        elif "diesel" in str(material).lower():
                            signo = 1 if "📈" in str(movimiento) or "entrada" in str(movimiento).lower() else -1
                            movimientos_diesel.append((fecha, cantidad_num * signo))
                            
                    except (ValueError, TypeError):
                        continue
            
            print(f"🔍 Movimientos gasolina: {len(movimientos_gasolina)}")
            print(f"🔍 Movimientos diesel: {len(movimientos_diesel)}")
            
            # Si no hay datos, usar valores por defecto
            if not movimientos_gasolina and not movimientos_diesel:
                print("📊 No hay datos reales, usando datos de ejemplo")
                fechas_ejemplo = [datetime.now().strftime("%d/%m/%Y")]
                stock_gasolina = [40.0]
                stock_diesel = [70.0]
            else:
                # Calcular stock acumulado
                fechas_ejemplo = []
                stock_gasolina = []
                stock_diesel = []
                
                todas_fechas = set()
                for fecha, _ in movimientos_gasolina + movimientos_diesel:
                    if fecha:
                        todas_fechas.add(str(fecha))
                
                todas_fechas = sorted(list(todas_fechas))
                
                acum_gasolina = 0
                acum_diesel = 0
                
                for fecha in todas_fechas:
                    fechas_ejemplo.append(fecha)
                    
                    # Sumar movimientos de esta fecha
                    for f, cantidad in movimientos_gasolina:
                        if str(f) == fecha:
                            acum_gasolina += cantidad
                    
                    for f, cantidad in movimientos_diesel:
                        if str(f) == fecha:
                            acum_diesel += cantidad
                    
                    stock_gasolina.append(max(0, acum_gasolina))
                    stock_diesel.append(max(0, acum_diesel))
            
            # Crear gráfica
            plt.figure(figsize=(12, 8))
            
            x_pos = range(len(fechas_ejemplo))
            
            plt.bar([x - 0.2 for x in x_pos], stock_gasolina, 0.4, 
                   label='Gasolina', color='#FF6B6B', alpha=0.8)
            plt.bar([x + 0.2 for x in x_pos], stock_diesel, 0.4, 
                   label='Diesel', color='#4ECDC4', alpha=0.8)
            
            plt.title('📊 STOCK DE COMBUSTIBLES\nPlanta Premoldeados Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Cantidad (Litros)', fontsize=12)
            
            plt.xticks(x_pos, fechas_ejemplo, rotation=45)
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Agregar valores en las barras
            for i, (g, d) in enumerate(zip(stock_gasolina, stock_diesel)):
                plt.text(i - 0.2, g + 1, f'{g:.1f}L', ha='center', va='bottom', fontsize=9)
                plt.text(i + 0.2, d + 1, f'{d:.1f}L', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            
            nombre_grafica = f"combustibles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return nombre_grafica
            
        except Exception as e:
            print(f"Error generando gráfica combustibles: {e}")
            return None
    
    @staticmethod
    def generar_grafica_stock_materiales():
        """Genera gráfica de stock actual de materiales"""
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return None
        
        try:
            stock = ExcelManager.obtener_stock_materiales()
            
            if not stock:
                print("❌ No hay datos de stock para graficar")
                return None
            
            # Preparar datos
            materiales = list(stock.keys())
            cantidades = list(stock.values())
            
            # Colores según nivel de stock
            colores = []
            for cantidad in cantidades:
                if cantidad > 50:
                    colores.append('#2ECC71')  # Verde - Óptimo
                elif cantidad > 10:
                    colores.append('#F39C12')  # Naranja - Bajo
                else:
                    colores.append('#E74C3C')  # Rojo - Crítico
            
            # Crear gráfica
            plt.figure(figsize=(12, 8))
            
            barras = plt.bar(materiales, cantidades, color=colores, alpha=0.8)
            
            plt.title('📦 STOCK ACTUAL DE MATERIALES\nPlanta Premoldeados Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Material', fontsize=12)
            plt.ylabel('Cantidad', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Agregar valores en las barras
            for barra, cantidad in zip(barras, cantidades):
                plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1,
                        f'{cantidad:.1f}', ha='center', va='bottom', fontsize=10)
            
            # Leyenda de colores
            from matplotlib.patches import Patch
            leyenda = [
                Patch(color='#2ECC71', label='Óptimo (>50)'),
                Patch(color='#F39C12', label='Bajo (10-50)'),
                Patch(color='#E74C3C', label='Crítico (<10)')
            ]
            plt.legend(handles=leyenda, loc='upper right')
            
            plt.tight_layout()
            
            nombre_grafica = f"stock_materiales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return nombre_grafica
            
        except Exception as e:
            print(f"Error generando gráfica stock: {e}")
            return None
    
    @staticmethod
    def generar_grafica_cemento():
        """Genera gráfica específica de consumo de cemento"""
        if not GRAFICOS_DISPONIBLES:
            return None
        
        try:
            # Obtener movimientos de cemento
            if not os.path.exists(ARCHIVO_EXCEL_MATERIALES):
                return None
            
            libro = openpyxl.load_workbook(ARCHIVO_EXCEL_MATERIALES)
            hoja = libro.active
            
            movimientos_cemento = {}
            
            for row in range(5, hoja.max_row + 1):
                material = hoja.cell(row=row, column=3).value
                fecha = hoja.cell(row=row, column=1).value
                movimiento = hoja.cell(row=row, column=5).value
                cantidad = hoja.cell(row=row, column=6).value
                
                if material and "cemento" in str(material).lower():
                    fecha_str = str(fecha) if fecha else datetime.now().strftime("%d/%m/%Y")
                    
                    if fecha_str not in movimientos_cemento:
                        movimientos_cemento[fecha_str] = 0
                    
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                        if "📉" in str(movimiento) or "salida" in str(movimiento).lower():
                            movimientos_cemento[fecha_str] += cantidad_num
                    except (ValueError, TypeError):
                        continue
            
            if not movimientos_cemento:
                print("⚠️ No hay datos de cemento suficientes")
                return None
            
            # Crear gráfica
            fechas = list(movimientos_cemento.keys())
            consumos = list(movimientos_cemento.values())
            
            plt.figure(figsize=(12, 6))
            plt.plot(fechas, consumos, marker='o', linewidth=2, markersize=6, color='#8B4513')
            plt.fill_between(fechas, consumos, alpha=0.3, color='#D2B48C')
            
            plt.title('🏗️ CONSUMO DIARIO DE CEMENTO\nPlanta Premoldeados Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Cantidad Consumida (Kg)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Agregar valores
            for fecha, consumo in zip(fechas, consumos):
                plt.annotate(f'{consumo:.1f}', (fecha, consumo), 
                           textcoords="offset points", xytext=(0,10), ha='center')
            
            plt.tight_layout()
            
            nombre_grafica = f"cemento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return nombre_grafica
            
        except Exception as e:
            print(f"Error generando gráfica cemento: {e}")
            return None
    
    @staticmethod
    def generar_grafica_produccion():
        """Genera gráfica de producción de adoquines"""
        if not GRAFICOS_DISPONIBLES:
            return None
        
        try:
            if not os.path.exists(ARCHIVO_EXCEL_PRODUCCION):
                print("⚠️ No existe archivo de producción")
                return None
            
            libro = openpyxl.load_workbook(ARCHIVO_EXCEL_PRODUCCION)
            hoja = libro.active
            
            produccion_diaria = {}
            
            for row in range(5, hoja.max_row + 1):
                fecha = hoja.cell(row=row, column=1).value
                producto = hoja.cell(row=row, column=3).value
                cantidad = hoja.cell(row=row, column=4).value
                
                if fecha and cantidad:
                    fecha_str = str(fecha)
                    
                    if fecha_str not in produccion_diaria:
                        produccion_diaria[fecha_str] = 0
                    
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                        produccion_diaria[fecha_str] += cantidad_num
                    except (ValueError, TypeError):
                        continue
            
            if not produccion_diaria:
                print("⚠️ No hay datos de producción")
                return None
            
            # Crear gráfica
            fechas = list(produccion_diaria.keys())
            producciones = list(produccion_diaria.values())
            
            plt.figure(figsize=(12, 6))
            plt.bar(fechas, producciones, color='#FF9500', alpha=0.8)
            
            plt.title('🔨 PRODUCCIÓN DIARIA DE ADOQUINES\nPlanta Premoldeados Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Cantidad Producida (Adoquines)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            plt.tight_layout()
            
            nombre_grafica = f"produccion_adoquines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return nombre_grafica
            
        except Exception as e:
            print(f"Error generando gráfica producción: {e}")
            return None
    
    @staticmethod
    def obtener_info_combustibles_detallada():
        """Obtiene información detallada de combustibles - EXACTAMENTE TU LÓGICA ACTUAL"""
        # Reutilizar lógica del ExcelManager
        datos = ExcelManager.obtener_datos_combustibles()
        
        if not datos:
            # Devolver datos de ejemplo en caso de error (exactamente como lo tienes)
            return {
                'gasolina': 40.0,
                'diesel': 70.0
            }
        
        return datos