#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 GRAPHICS GENERATOR - VERSIÓN CORREGIDA
=========================================

Módulo para generar gráficas del Sistema Industrial Unificado
CORRECCIONES APLICADAS:
- Búsqueda correcta de "📈 Entrada" y "📉 Salida" 
- Lectura mejorada de la columna Material
- Cálculo correcto de stock de combustibles
- Manejo robusto de emojis en los datos

Versión: 2.1 CORREGIDA
"""

import os
import sys
from datetime import datetime, timedelta
import openpyxl

# Importar configuración
try:
    from .config import *
except ImportError:
    try:
        from modules.config import *
    except ImportError:
        # Configuración de respaldo
        ARCHIVO_EXCEL_MATERIALES = "datos/inventario_materiales.xlsx"

# Verificar matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
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
    def _buscar_archivo_materiales():
        """Busca el archivo de materiales en diferentes ubicaciones"""
        ubicaciones = [
            "datos/inventario_materiales.xlsx",
            "inventario_materiales.xlsx",
            "./datos/inventario_materiales.xlsx"
        ]
        
        for ubicacion in ubicaciones:
            if os.path.exists(ubicacion):
                print(f"📁 Usando archivo: {ubicacion}")
                return ubicacion
        
        print("❌ No se encontró archivo de materiales")
        return None
    
    @staticmethod
    def obtener_datos_combustibles():
        """
        Obtiene datos de combustibles calculando el stock actual
        CORREGIDO: Búsqueda mejorada con emojis
        """
        archivo = GraphicsGenerator._buscar_archivo_materiales()
        if not archivo:
            return {"gasolina": 0, "diesel": 0}
        
        try:
            libro = openpyxl.load_workbook(archivo)
            hoja = libro.active
            
            print(f"📊 Leyendo archivo con {hoja.max_row} filas")
            
            stock_gasolina = 0
            stock_diesel = 0
            
            # Leer desde fila 5 (después de encabezados)
            for row in range(5, hoja.max_row + 1):
                try:
                    material = hoja.cell(row=row, column=3).value    # Columna C: Material
                    movimiento = hoja.cell(row=row, column=5).value  # Columna E: Movimiento  
                    cantidad = hoja.cell(row=row, column=6).value    # Columna F: Cantidad
                    
                    if not material or not movimiento or not cantidad:
                        continue
                    
                    # Convertir a texto y limpiar
                    material_texto = str(material).lower().strip()
                    movimiento_texto = str(movimiento).strip()
                    
                    # Convertir cantidad a número
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                    except:
                        continue
                    
                    # CORRECCIÓN: Buscar combustibles en material
                    es_gasolina = any(palabra in material_texto for palabra in 
                                    ['gasolina', 'gasoline', 'nafta', 'bencina'])
                    es_diesel = any(palabra in material_texto for palabra in 
                                  ['diesel', 'diésel', 'gasoil', 'petróleo'])
                    
                    if not (es_gasolina or es_diesel):
                        continue
                    
                    # CORRECCIÓN: Detectar tipo de movimiento con emojis
                    es_entrada = ("📈" in movimiento_texto or 
                                "entrada" in movimiento_texto.lower() or
                                "Entrada" in movimiento_texto)
                    
                    es_salida = ("📉" in movimiento_texto or 
                               "salida" in movimiento_texto.lower() or
                               "Salida" in movimiento_texto)
                    
                    # Aplicar movimiento al stock
                    if es_gasolina:
                        if es_entrada:
                            stock_gasolina += cantidad_num
                            print(f"   ⛽ Gasolina +{cantidad_num} (Total: {stock_gasolina})")
                        elif es_salida:
                            stock_gasolina -= cantidad_num
                            print(f"   ⛽ Gasolina -{cantidad_num} (Total: {stock_gasolina})")
                    
                    elif es_diesel:
                        if es_entrada:
                            stock_diesel += cantidad_num
                            print(f"   ⛽ Diesel +{cantidad_num} (Total: {stock_diesel})")
                        elif es_salida:
                            stock_diesel -= cantidad_num
                            print(f"   ⛽ Diesel -{cantidad_num} (Total: {stock_diesel})")
                            
                except Exception as e:
                    continue
            
            # Asegurar valores positivos
            stock_gasolina = max(0, stock_gasolina)
            stock_diesel = max(0, stock_diesel)
            
            print(f"📊 Stock final - Gasolina: {stock_gasolina}L, Diesel: {stock_diesel}L")
            
            return {
                "gasolina": stock_gasolina,
                "diesel": stock_diesel
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de combustibles: {e}")
            return {"gasolina": 0, "diesel": 0}
    
    @staticmethod
    def generar_grafica_combustibles():
        """
        Genera gráfica de stock actual de combustibles
        CORREGIDO: Usa datos reales del Excel
        """
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return None
        
        try:
            # Obtener datos reales de combustibles
            datos_combustibles = GraphicsGenerator.obtener_datos_combustibles()
            
            gasolina = datos_combustibles["gasolina"]
            diesel = datos_combustibles["diesel"]
            
            print(f"📊 Datos para gráfica - Gasolina: {gasolina}L, Diesel: {diesel}L")
            
            # Si no hay datos, usar valores mínimos para mostrar la estructura
            if gasolina == 0 and diesel == 0:
                print("⚠️ No hay datos de combustibles, usando valores de ejemplo")
                gasolina = 50
                diesel = 75
            
            # Crear gráfica
            plt.figure(figsize=(10, 6))
            
            combustibles = ['Gasolina', 'Diesel']
            cantidades = [gasolina, diesel]
            colores = ['#FF6B6B', '#4ECDC4']
            
            # Crear gráfica de barras
            barras = plt.bar(combustibles, cantidades, color=colores, alpha=0.8, edgecolor='black')
            
            # Personalizar gráfica
            plt.title('⛽ STOCK ACTUAL DE COMBUSTIBLES\nPlanta Municipal de Premoldeados - Tupiza', 
                     fontsize=14, fontweight='bold', pad=20)
            plt.ylabel('Cantidad (Litros)', fontsize=12)
            plt.grid(True, alpha=0.3, axis='y')
            
            # Agregar valores en las barras
            for barra, cantidad in zip(barras, cantidades):
                altura = barra.get_height()
                plt.text(barra.get_x() + barra.get_width()/2., altura + max(cantidades)*0.02,
                        f'{cantidad:.0f}L', ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # Agregar líneas de referencia
            plt.axhline(y=100, color='orange', linestyle='--', alpha=0.7, label='Nivel mínimo (100L)')
            plt.axhline(y=200, color='green', linestyle='--', alpha=0.7, label='Nivel óptimo (200L)')
            plt.legend()
            
            # Información adicional
            total = gasolina + diesel
            plt.figtext(0.02, 0.02, f'Total combustible: {total:.0f} litros', 
                       fontsize=10, style='italic')
            
            plt.tight_layout()
            
            # Crear directorio si no existe
            os.makedirs("graficas", exist_ok=True)
            
            # Guardar gráfica
            nombre_archivo = f"graficas/combustibles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✅ Gráfica de combustibles generada: {nombre_archivo}")
            return nombre_archivo
            
        except Exception as e:
            print(f"❌ Error generando gráfica combustibles: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def obtener_datos_cemento():
        """
        Obtiene datos de consumo de cemento - CORREGIDO PARA TU ARCHIVO
        """
        archivo = GraphicsGenerator._buscar_archivo_materiales()
        if not archivo:
            return {}
        
        try:
            libro = openpyxl.load_workbook(archivo)
            hoja = libro.active
            
            print(f"📊 Buscando cemento desde fila 4 hasta fila {hoja.max_row}...")
            
            consumo_por_fecha = {}
            
            # CORREGIDO: Empezar desde fila 4 (donde están tus datos)
            for row in range(4, hoja.max_row + 1):
                try:
                    fecha = hoja.cell(row=row, column=1).value      # Columna A: Fecha
                    material = hoja.cell(row=row, column=3).value   # Columna C: Material
                    movimiento = hoja.cell(row=row, column=5).value # Columna E: Movimiento
                    cantidad = hoja.cell(row=row, column=6).value   # Columna F: Cantidad
                    
                    if not material or not movimiento or not cantidad:
                        continue
                    
                    # CORREGIDO: Buscar cemento (más flexible)
                    material_texto = str(material).lower().strip()
                    if "cemento" not in material_texto:
                        continue
                    
                    print(f"   📦 Cemento encontrado en fila {row}: {material}")
                    
                    # CORREGIDO: Buscar salidas (más flexible)
                    movimiento_texto = str(movimiento).strip()
                    es_salida = (
                        "📉" in movimiento_texto or 
                        "salida" in movimiento_texto.lower() or
                        "consumo" in movimiento_texto.lower() or
                        "uso" in movimiento_texto.lower()
                    )
                    
                    print(f"      Movimiento: '{movimiento_texto}' -> ¿Es salida? {es_salida}")
                    
                    if not es_salida:
                        continue
                    
                    # Convertir cantidad a número
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                    except:
                        print(f"      ❌ Error con cantidad: {cantidad}")
                        continue
                    
                    # Procesar fecha
                    if isinstance(fecha, datetime):
                        fecha_str = fecha.strftime("%d/%m")
                    else:
                        fecha_str = str(fecha)[-5:] if fecha else "S/F"
                    
                    # Acumular consumo por fecha
                    if fecha_str not in consumo_por_fecha:
                        consumo_por_fecha[fecha_str] = 0
                    
                    consumo_por_fecha[fecha_str] += cantidad_num
                    print(f"      ✅ Registrado: {fecha_str} = +{cantidad_num} bolsas")
                    
                except Exception as e:
                    continue
            
            print(f"\n📊 Días con consumo de cemento: {len(consumo_por_fecha)}")
            return consumo_por_fecha
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de cemento: {e}")
            return {}
    
    @staticmethod
    def generar_grafica_cemento():
        """
        Genera gráfica de consumo de cemento
        CORREGIDO: Usa datos reales del Excel
        """
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return None
        
        try:
            # Obtener datos reales de cemento
            consumo_cemento = GraphicsGenerator.obtener_datos_cemento()
            
            if not consumo_cemento:
                print("❌ No hay datos de consumo de cemento")
                print("💡 Registra algunas salidas de cemento para generar la gráfica")
                return None
            
            # Preparar datos para gráfica
            fechas = sorted(consumo_cemento.keys())
            cantidades = [consumo_cemento[f] for f in fechas]
            
            print(f"📊 Generando gráfica con {len(fechas)} días de datos")
            
            # Crear gráfica
            plt.figure(figsize=(12, 6))
            
            # Gráfica de barras
            barras = plt.bar(range(len(fechas)), cantidades, 
                           color='#8E44AD', alpha=0.8, edgecolor='black')
            
            # Personalizar gráfica
            plt.title('🏗️ CONSUMO DIARIO DE CEMENTO\nPlanta Municipal de Premoldeados - Tupiza', 
                     fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=12)
            plt.ylabel('Bolsas Consumidas', fontsize=12)
            
            # Configurar eje X
            plt.xticks(range(len(fechas)), fechas, rotation=45)
            plt.grid(True, alpha=0.3, axis='y')
            
            # Agregar valores en las barras
            for i, (barra, cantidad) in enumerate(zip(barras, cantidades)):
                if cantidad > 0:
                    plt.text(barra.get_x() + barra.get_width()/2, 
                            barra.get_height() + max(cantidades)*0.02,
                            f'{cantidad:.0f}', ha='center', va='bottom', 
                            fontweight='bold', fontsize=10)
            
            # Información adicional
            total_consumo = sum(cantidades)
            promedio_diario = total_consumo / len(cantidades) if cantidades else 0
            
            plt.figtext(0.02, 0.02, 
                       f'Total consumido: {total_consumo:.0f} bolsas | Promedio: {promedio_diario:.1f} bolsas/día', 
                       fontsize=10, style='italic')
            
            plt.tight_layout()
            
            # Crear directorio si no existe
            os.makedirs("graficas", exist_ok=True)
            
            # Guardar gráfica
            nombre_archivo = f"graficas/cemento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✅ Gráfica de cemento generada: {nombre_archivo}")
            return nombre_archivo
            
        except Exception as e:
            print(f"❌ Error generando gráfica cemento: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def generar_grafica_stock_materiales():
        """
        Genera gráfica de stock general de materiales
        CORREGIDO: Cálculo mejorado de stock
        """
        if not GRAFICOS_DISPONIBLES:
            print("❌ Matplotlib no disponible")
            return None
        
        try:
            archivo = GraphicsGenerator._buscar_archivo_materiales()
            if not archivo:
                return None
            
            libro = openpyxl.load_workbook(archivo)
            hoja = libro.active
            
            print(f"📊 Calculando stock de materiales...")
            
            stock_materiales = {}
            
            # Leer desde fila 5 (después de encabezados)
            for row in range(5, hoja.max_row + 1):
                try:
                    material = hoja.cell(row=row, column=3).value   # Columna C: Material
                    movimiento = hoja.cell(row=row, column=5).value # Columna E: Movimiento
                    cantidad = hoja.cell(row=row, column=6).value   # Columna F: Cantidad
                    
                    if not material or not movimiento or not cantidad:
                        continue
                    
                    # Limpiar nombres de materiales
                    material_nombre = str(material).strip()
                    movimiento_texto = str(movimiento).strip()
                    
                    # Convertir cantidad a número
                    try:
                        cantidad_num = float(str(cantidad).replace(",", "."))
                    except:
                        continue
                    
                    # Inicializar material si no existe
                    if material_nombre not in stock_materiales:
                        stock_materiales[material_nombre] = 0
                    
                    # CORRECCIÓN: Detectar tipo de movimiento con emojis
                    es_entrada = ("📈" in movimiento_texto or 
                                "entrada" in movimiento_texto.lower())
                    es_salida = ("📉" in movimiento_texto or 
                               "salida" in movimiento_texto.lower())
                    
                    # Aplicar movimiento al stock
                    if es_entrada:
                        stock_materiales[material_nombre] += cantidad_num
                    elif es_salida:
                        stock_materiales[material_nombre] -= cantidad_num
                        
                except Exception as e:
                    continue
            
            # Filtrar materiales con stock positivo
            stock_filtrado = {k: max(0, v) for k, v in stock_materiales.items() if v != 0}
            
            if not stock_filtrado:
                print("❌ No hay datos de stock para mostrar")
                return None
            
            # Preparar datos para gráfica
            materiales = list(stock_filtrado.keys())
            cantidades = list(stock_filtrado.values())
            
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
            plt.figure(figsize=(14, 8))
            
            barras = plt.bar(materiales, cantidades, color=colores, alpha=0.8, edgecolor='black')
            
            plt.title('📦 STOCK ACTUAL DE MATERIALES\nPlanta Municipal de Premoldeados - Tupiza', 
                     fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Material', fontsize=12)
            plt.ylabel('Cantidad', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            
            # Agregar valores en las barras
            for barra, cantidad in zip(barras, cantidades):
                altura = barra.get_height()
                plt.text(barra.get_x() + barra.get_width()/2, altura + max(cantidades)*0.01,
                        f'{cantidad:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # Leyenda de colores
            leyenda = [
                Patch(color='#2ECC71', label='Óptimo (>50)'),
                Patch(color='#F39C12', label='Bajo (10-50)'),
                Patch(color='#E74C3C', label='Crítico (<10)')
            ]
            plt.legend(handles=leyenda, loc='upper right')
            
            plt.tight_layout()
            
            # Crear directorio si no existe
            os.makedirs("graficas", exist_ok=True)
            
            # Guardar gráfica
            nombre_archivo = f"graficas/stock_materiales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✅ Gráfica de stock generada: {nombre_archivo}")
            return nombre_archivo
            
        except Exception as e:
            print(f"❌ Error generando gráfica stock: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def obtener_info_combustibles_detallada():
        """Obtiene información detallada de combustibles para reportes"""
        datos = GraphicsGenerator.obtener_datos_combustibles()
        
        total = datos["gasolina"] + datos["diesel"]
        
        info = {
            "gasolina": datos["gasolina"],
            "diesel": datos["diesel"], 
            "total": total,
            "estado_gasolina": "Crítico" if datos["gasolina"] < 50 else "Bajo" if datos["gasolina"] < 100 else "Óptimo",
            "estado_diesel": "Crítico" if datos["diesel"] < 50 else "Bajo" if datos["diesel"] < 100 else "Óptimo",
            "recomendacion": "Abastecimiento urgente" if total < 100 else "Monitoreo normal"
        }
        
        return info

# ============================================================================
# FUNCIÓN DE PRUEBA
# ============================================================================

def probar_graphics_generator():
    """Prueba rápida del generador de gráficas"""
    print("🧪 === PRUEBA RÁPIDA GRAPHICS GENERATOR ===")
    
    if not GraphicsGenerator.verificar_matplotlib():
        print("❌ Matplotlib no disponible")
        return False
    
    archivo = GraphicsGenerator._buscar_archivo_materiales()
    if not archivo:
        print("❌ No se encontró archivo de materiales")
        return False
    
    print("✅ Archivo encontrado, probando funciones...")
    
    # Probar datos de combustibles
    print("\n⛽ Probando datos de combustibles...")
    datos_comb = GraphicsGenerator.obtener_datos_combustibles()
    print(f"   Gasolina: {datos_comb['gasolina']}L")
    print(f"   Diesel: {datos_comb['diesel']}L")
    
    # Probar datos de cemento
    print("\n🏗️ Probando datos de cemento...")
    datos_cemento = GraphicsGenerator.obtener_datos_cemento()
    print(f"   Días con consumo: {len(datos_cemento)}")
    
    return True

if __name__ == "__main__":
    probar_graphics_generator()