#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 GRAPHICS GENERATOR - VERSIÓN CORREGIDA
==========================================

Módulo para generar gráficas del Sistema Industrial Unificado
Versión corregida que soluciona el error de f-string línea 229

Autor: Sistema Industrial Automatizado
Versión: 1.1 CORREGIDA
Fecha: 2025
"""

import os
import sys
from datetime import datetime, timedelta
import openpyxl

# Importar configuración
try:
    from .config import *
except ImportError:
    # Si falla la importación relativa, usar absoluta
    try:
        from modules.config import *
    except ImportError:
        # Configuración básica de respaldo
        ARCHIVO_EXCEL_MATERIALES = "datos/inventario_materiales.xlsx"
        ARCHIVO_EXCEL_EQUIPOS = "datos/inventario_equipos.xlsx"
        ARCHIVO_EXCEL_PRODUCCION = "datos/registro_produccion.xlsx"

# Verificar matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # Usar backend no interactivo
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Patch
    GRAFICOS_DISPONIBLES = True
    print("✅ Matplotlib cargado para gráficos")
except ImportError:
    GRAFICOS_DISPONIBLES = False
    print("⚠️ Matplotlib no disponible - gráficas deshabilitadas")

class GraphicsGenerator:
    """Generador de gráficas para el sistema industrial"""
    
    @staticmethod
    def verificar_matplotlib():
        """Verifica si matplotlib está disponible"""
        return GRAFICOS_DISPONIBLES
    
    @staticmethod
    def generar_grafica_combustibles():
        """Genera gráfica de stock de combustibles"""
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return None
        
        try:
            # Verificar si existe el archivo
            if not os.path.exists(ARCHIVO_EXCEL_EQUIPOS):
                print("❌ No se encuentra archivo de equipos")
                return None
            
            # Leer datos del Excel
            libro = openpyxl.load_workbook(ARCHIVO_EXCEL_EQUIPOS)
            hoja = libro.active
            
            print(f"📊 Leyendo archivo con {hoja.max_row} filas")
            
            # Extraer movimientos de combustible
            movimientos_gasolina = []
            movimientos_diesel = []
            
            for row in range(5, hoja.max_row + 1):
                try:
                    fecha = hoja.cell(row=row, column=1).value
                    equipo = hoja.cell(row=row, column=3).value
                    combustible = hoja.cell(row=row, column=4).value
                    movimiento = hoja.cell(row=row, column=5).value
                    cantidad = hoja.cell(row=row, column=6).value
                    
                    if combustible and cantidad:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                        
                        if "gasolina" in str(combustible).lower():
                            if "entrada" in str(movimiento).lower():
                                movimientos_gasolina.append((fecha, cantidad_num))
                            elif "salida" in str(movimiento).lower():
                                movimientos_gasolina.append((fecha, -cantidad_num))
                        
                        elif "diesel" in str(combustible).lower():
                            if "entrada" in str(movimiento).lower():
                                movimientos_diesel.append((fecha, cantidad_num))
                            elif "salida" in str(movimiento).lower():
                                movimientos_diesel.append((fecha, -cantidad_num))
                                
                except Exception as e:
                    continue
            
            print(f"🔍 Movimientos gasolina: {len(movimientos_gasolina)}")
            print(f"🔍 Movimientos diesel: {len(movimientos_diesel)}")
            
            # Si no hay datos reales, usar datos de ejemplo
            if not movimientos_gasolina and not movimientos_diesel:
                print("📊 No hay datos reales, usando datos de ejemplo")
                fechas_ejemplo = [
                    (datetime.now() - timedelta(days=6)).strftime("%d/%m/%Y"),
                    (datetime.now() - timedelta(days=5)).strftime("%d/%m/%Y"),
                    (datetime.now() - timedelta(days=4)).strftime("%d/%m/%Y"),
                    (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y"),
                    (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y"),
                    (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y"),
                    datetime.now().strftime("%d/%m/%Y")
                ]
                stock_gasolina = [150, 120, 100, 80, 60, 40, 20]
                stock_diesel = [200, 180, 160, 140, 120, 100, 80]
            else:
                # Procesar datos reales
                fechas_ejemplo = []
                stock_gasolina = []
                stock_diesel = []
                
                # Generar fechas de la última semana
                for i in range(7):
                    fecha = (datetime.now() - timedelta(days=6-i)).strftime("%d/%m/%Y")
                    fechas_ejemplo.append(fecha)
                    
                    # Calcular stock acumulado para cada fecha
                    acum_gasolina = 0
                    acum_diesel = 0
                    
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
            # Importar ExcelManager
            try:
                from .excel_manager import ExcelManager
            except ImportError:
                from modules.excel_manager import ExcelManager
            
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
        """Genera gráfica específica de consumo de cemento - VERSIÓN CORREGIDA"""
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
                
                # CORRECCIÓN: Búsqueda más flexible de cemento
                if material and "cemento" in str(material).lower():
                    # CORRECCIÓN: Manejo seguro de fecha
                    if isinstance(fecha, datetime):
                        fecha_str = fecha.strftime("%d/%m/%Y")
                    else:
                        fecha_str = str(fecha) if fecha else datetime.now().strftime("%d/%m/%Y")
                    
                    if fecha_str not in movimientos_cemento:
                        movimientos_cemento[fecha_str] = 0
                    
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                        
                        # CORRECCIÓN: Solo contar salidas (consumo)
                        if movimiento and "salida" in str(movimiento).lower():
                            movimientos_cemento[fecha_str] += cantidad_num
                            
                    except (ValueError, TypeError):
                        continue
            
            # Verificar si hay datos
            if not movimientos_cemento or all(v == 0 for v in movimientos_cemento.values()):
                print("❌ No hay datos de consumo de cemento")
                return None
            
            # Preparar datos para gráfica
            fechas = list(movimientos_cemento.keys())
            cantidades = list(movimientos_cemento.values())
            
            # Filtrar solo fechas con consumo > 0
            datos_filtrados = [(f, c) for f, c in zip(fechas, cantidades) if c > 0]
            
            if not datos_filtrados:
                print("❌ No hay consumo registrado de cemento")
                return None
            
            fechas_filtradas, cantidades_filtradas = zip(*datos_filtrados)
            
            # Crear gráfica
            plt.figure(figsize=(12, 8))
            
            barras = plt.bar(range(len(fechas_filtradas)), cantidades_filtradas, 
                           color='#8E44AD', alpha=0.8, edgecolor='black', linewidth=1)
            
            plt.title('🏗️ CONSUMO DIARIO DE CEMENTO\nPlanta Premoldeados Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Bolsas Consumidas', fontsize=12)
            
            # CORRECCIÓN: Manejo seguro de labels de fecha
            plt.xticks(range(len(fechas_filtradas)), fechas_filtradas, rotation=45)
            plt.grid(True, alpha=0.3, linestyle='--')
            
            # Agregar valores en las barras
            for i, (barra, cantidad) in enumerate(zip(barras, cantidades_filtradas)):
                plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + max(cantidades_filtradas)*0.01,
                        f'{cantidad:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            # Información adicional
            total_consumo = sum(cantidades_filtradas)
            promedio_diario = total_consumo / len(cantidades_filtradas)
            
            # CORRECCIÓN: F-string arreglado - era aquí el problema línea 229
            info_text = f'Total consumido: {total_consumo:.0f} bolsas | Promedio diario: {promedio_diario:.1f} bolsas'
            plt.figtext(0.02, 0.02, info_text, fontsize=10, style='italic')
            
            plt.tight_layout()
            
            nombre_grafica = f"cemento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_grafica, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return nombre_grafica
            
        except Exception as e:
            print(f"Error generando gráfica cemento: {e}")
            return None
    
    @staticmethod
    def generar_todas_las_graficas():
        """Genera todas las gráficas disponibles"""
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return []
        
        graficas_generadas = []
        
        print("📊 Generando todas las gráficas...")
        
        # Gráfica de combustibles
        try:
            grafica1 = GraphicsGenerator.generar_grafica_combustibles()
            if grafica1:
                graficas_generadas.append(grafica1)
                print(f"✅ Combustibles: {grafica1}")
        except Exception as e:
            print(f"❌ Error en gráfica combustibles: {e}")
        
        # Gráfica de stock de materiales
        try:
            grafica2 = GraphicsGenerator.generar_grafica_stock_materiales()
            if grafica2:
                graficas_generadas.append(grafica2)
                print(f"✅ Stock materiales: {grafica2}")
        except Exception as e:
            print(f"❌ Error en gráfica stock: {e}")
        
        # Gráfica de cemento
        try:
            grafica3 = GraphicsGenerator.generar_grafica_cemento()
            if grafica3:
                graficas_generadas.append(grafica3)
                print(f"✅ Cemento: {grafica3}")
        except Exception as e:
            print(f"❌ Error en gráfica cemento: {e}")
        
        print(f"📈 Total gráficas generadas: {len(graficas_generadas)}")
        return graficas_generadas
    
    @staticmethod
    def limpiar_graficas_antiguas(dias=7):
        """Limpia gráficas más antiguas que X días"""
        try:
            import glob
            import time
            
            archivos_graficas = glob.glob("*.png")
            eliminados = 0
            
            for archivo in archivos_graficas:
                if os.path.getctime(archivo) < time.time() - (dias * 24 * 60 * 60):
                    os.remove(archivo)
                    eliminados += 1
            
            print(f"🧹 Limpieza completada: {eliminados} archivos eliminados")
            return eliminados
            
        except Exception as e:
            print(f"❌ Error en limpieza: {e}")
            return 0

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def probar_graphics_generator():
    """Prueba todas las funciones del generador de gráficas"""
    print("🧪 === PRUEBA DE GRAPHICS GENERATOR ===")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if not GraphicsGenerator.verificar_matplotlib():
        print("❌ Matplotlib no disponible - no se pueden generar gráficas")
        return False
    
    # Probar cada función
    funciones = [
        ("Combustibles", GraphicsGenerator.generar_grafica_combustibles),
        ("Stock Materiales", GraphicsGenerator.generar_grafica_stock_materiales),
        ("Cemento", GraphicsGenerator.generar_grafica_cemento)
    ]
    
    resultados = []
    
    for nombre, funcion in funciones:
        try:
            print(f"\n📊 Probando gráfica de {nombre}...")
            resultado = funcion()
            
            if resultado:
                print(f"   ✅ Generada: {resultado}")
                resultados.append(resultado)
            else:
                print(f"   ⚠️ No se generó (normal si no hay datos)")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📈 Resumen: {len(resultados)}/{len(funciones)} gráficas generadas")
    
    # Limpiar archivos de prueba
    for archivo in resultados:
        try:
            if os.path.exists(archivo):
                os.remove(archivo)
        except:
            pass
    
    return len(resultados) > 0

if __name__ == "__main__":
    probar_graphics_generator()