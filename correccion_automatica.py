#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORRECCIÓN AUTOMÁTICA - GRÁFICA CEMENTO
========================================
Este script corrige automáticamente el problema con la gráfica de cemento
"""

import os
import shutil
from datetime import datetime

def crear_backup():
    """Crea backup del archivo original"""
    archivo_original = "modules/graphics_generator.py"
    
    if os.path.exists(archivo_original):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"modules/graphics_generator_backup_{timestamp}.py"
        shutil.copy2(archivo_original, backup_name)
        print(f"✅ Backup creado: {backup_name}")
        return backup_name
    return None

def corregir_graphics_generator():
    """Corrige el archivo graphics_generator.py"""
    
    print("🔧 === CORRECCIÓN AUTOMÁTICA GRÁFICA CEMENTO ===")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 55)
    
    archivo_graphics = "modules/graphics_generator.py"
    
    if not os.path.exists(archivo_graphics):
        print(f"❌ No se encuentra: {archivo_graphics}")
        print("💡 Verifica que tengas la estructura de módulos correcta")
        return False
    
    # Crear backup
    print("\n1️⃣ CREANDO BACKUP...")
    backup = crear_backup()
    
    # Leer archivo actual
    print("\n2️⃣ LEYENDO ARCHIVO ACTUAL...")
    with open(archivo_graphics, 'r', encoding='utf-8') as f:
        contenido_actual = f.read()
    
    print(f"   📄 Archivo leído: {len(contenido_actual)} caracteres")
    
    # Verificar si ya está corregido
    if "_buscar_cemento_flexible" in contenido_actual:
        print("   ✅ El archivo ya parece estar corregido")
        print("   💡 Ejecuta el diagnóstico para verificar")
        return True
    
    # Preparar código corregido
    print("\n3️⃣ APLICANDO CORRECCIÓN...")
    
    codigo_nuevo_cemento = '''
    @staticmethod
    def generar_grafica_cemento():
        """Genera gráfica específica de consumo de cemento por día - VERSIÓN CORREGIDA"""
        
        if not GRAFICOS_DISPONIBLES or not os.path.exists(ARCHIVO_EXCEL_MATERIALES):
            print("❌ No hay archivo de materiales o matplotlib no disponible")
            return None
        
        try:
            # Buscar datos de cemento con búsqueda flexible
            datos_cemento = GraphicsGenerator._buscar_cemento_flexible()
            
            if not datos_cemento:
                print("❌ No hay datos de cemento para generar gráfica")
                return None
            
            print(f"\\n📊 === GENERANDO GRÁFICA DE CEMENTO ===")
            print(f"Datos a graficar: {len(datos_cemento)} registros")
            
            # Agrupar por fecha
            from collections import defaultdict
            consumo_por_fecha = defaultdict(float)
            
            for dato in datos_cemento:
                fecha = dato['fecha']
                cantidad = dato['cantidad']
                consumo_por_fecha[fecha] += cantidad
                print(f"   📅 {fecha}: +{cantidad} bolsas")
            
            # Preparar datos para la gráfica
            fechas = list(consumo_por_fecha.keys())
            cantidades = list(consumo_por_fecha.values())
            
            print(f"\\n📈 DATOS AGRUPADOS POR FECHA:")
            for fecha, total in consumo_por_fecha.items():
                print(f"   📅 {fecha}: {total} bolsas")
            
            # Crear gráfica
            plt.figure(figsize=(12, 8))
            
            # Configurar colores y estilo
            plt.style.use('default')
            color_principal = '#2E86AB'
            
            # Crear gráfica de barras
            bars = plt.bar(fechas, cantidades, color=color_principal, alpha=0.8, width=0.6)
            
            # Personalizar gráfica
            plt.title('📊 CONSUMO DIARIO DE CEMENTO\\\\n🏭 Planta Municipal de Premoldeados - Tupiza', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Fecha', fontsize=14, fontweight='bold')
            plt.ylabel('Cemento Consumido (bolsas)', fontsize=14, fontweight='bold')
            
            # Rotar etiquetas de fechas
            plt.xticks(rotation=45, ha='right')
            
            # Agregar valores encima de las barras
            for bar, cantidad in zip(bars, cantidades):
                altura = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., altura + max(cantidades)*0.01,
                        f'{cantidad:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            # Grid para mejor lectura
            plt.grid(True, alpha=0.3, axis='y', linestyle='--')
            
            # Información adicional
            total_consumo = sum(cantidades)
            promedio_diario = total_consumo / len(cantidades) if cantidades else 0
            
            plt.figtext(0.02, 0.02, 
                       f'Total consumido: {total_consumo:.0f} bolsas | Promedio diario: {promedio_diario:.1f} bolsas', 
                       fontsize=10, style='italic')
            
            # Ajustar diseño
            plt.tight_layout()
            
            # Guardar gráfica
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"graficas/consumo_cemento_{timestamp}.png"
            
            # Crear directorio si no existe
            os.makedirs("graficas", exist_ok=True)
            
            plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✅ Gráfica generada: {nombre_archivo}")
            
            if os.path.exists(nombre_archivo):
                tamaño = os.path.getsize(nombre_archivo) / 1024
                print(f"📏 Tamaño del archivo: {tamaño:.1f} KB")
                
            return nombre_archivo
            
        except Exception as e:
            print(f"❌ Error generando gráfica: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def _buscar_cemento_flexible():
        """Busca datos de cemento de forma flexible - BÚSQUEDA MEJORADA"""
        
        try:
            libro = openpyxl.load_workbook(ARCHIVO_EXCEL_MATERIALES)
            hoja = libro.active
            
            print(f"🔍 Buscando datos de cemento en {hoja.max_row} filas...")
            
            datos_cemento = []
            
            # Variantes de cemento a buscar (insensible a mayúsculas)
            variantes_cemento = ['cemento', 'cement', 'cimento']
            
            # Variantes de salida a buscar
            variantes_salida = ['salida', 'sal', 'consumo', 'uso', 'gasto', 'out', '📉']
            
            for row in range(2, hoja.max_row + 1):  # Empezar desde fila 2
                try:
                    # Leer todas las celdas de la fila
                    valores_fila = []
                    for col in range(1, hoja.max_column + 1):
                        valor = hoja.cell(row=row, column=col).value
                        valores_fila.append(str(valor).strip() if valor else "")
                    
                    # Buscar cemento en cualquier columna
                    material_encontrado = False
                    for valor in valores_fila:
                        if any(variante in valor.lower() for variante in variantes_cemento):
                            material_encontrado = True
                            break
                    
                    if not material_encontrado:
                        continue
                    
                    # Buscar movimiento de salida
                    movimiento_salida = False
                    for valor in valores_fila:
                        if any(variante in valor.lower() for variante in variantes_salida):
                            movimiento_salida = True
                            break
                    
                    if not movimiento_salida:
                        continue
                    
                    # Buscar cantidad (número válido)
                    cantidad = None
                    for valor in valores_fila:
                        try:
                            # Intentar convertir a número
                            cantidad_num = float(str(valor).replace(",", "."))
                            if cantidad_num > 0:  # Solo cantidades positivas
                                cantidad = cantidad_num
                                break
                        except:
                            continue
                    
                    if cantidad is None:
                        continue
                    
                    # Buscar fecha
                    fecha = None
                    for valor in valores_fila:
                        if "/" in str(valor) and len(str(valor)) >= 8:  # Formato de fecha
                            fecha = str(valor)
                            break
                    
                    if not fecha:
                        fecha = datetime.now().strftime("%d/%m/%Y")  # Fecha actual si no encuentra
                    
                    # Agregar dato válido
                    datos_cemento.append({
                        'fecha': fecha,
                        'cantidad': cantidad,
                        'fila': row
                    })
                    
                    print(f"✅ Cemento encontrado - Fila {row}: {fecha} = {cantidad} bolsas")
                    
                except Exception as e:
                    print(f"⚠️ Error procesando fila {row}: {e}")
                    continue
            
            print(f"\\n📊 RESULTADO: {len(datos_cemento)} registros de cemento encontrados")
            
            return datos_cemento
            
        except Exception as e:
            print(f"❌ Error buscando cemento: {e}")
            return []
'''
    
    # Buscar y reemplazar la función actual
    import re
    
    # Patrón para encontrar la función generar_grafica_cemento actual
    patron_funcion = r'@staticmethod\s+def generar_grafica_cemento\(.*?\):.*?(?=@staticmethod|\Z)'
    
    if re.search(patron_funcion, contenido_actual, re.DOTALL):
        # Reemplazar función existente
        contenido_nuevo = re.sub(patron_funcion, codigo_nuevo_cemento.strip(), contenido_actual, flags=re.DOTALL)
    else:
        # Agregar al final de la clase
        contenido_nuevo = contenido_actual + codigo_nuevo_cemento
    
    # Escribir archivo corregido
    print("\n4️⃣ ESCRIBIENDO ARCHIVO CORREGIDO...")
    with open(archivo_graphics, 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)
    
    print("   ✅ Archivo actualizado")
    
    print("\n🎉 === CORRECCIÓN COMPLETADA ===")
    print("✅ El método generar_grafica_cemento() ha sido corregido")
    print("✅ Se agregó el método _buscar_cemento_flexible()")
    print("💡 Ejecuta el diagnóstico para verificar la corrección")
    
    if backup:
        print(f"🔄 Backup disponible en: {backup}")
    
    return True

if __name__ == "__main__":
    exito = corregir_graphics_generator()
    if exito:
        print("\\n🚀 ¡Corrección aplicada exitosamente!")
        print("💡 Próximo paso: Ejecuta el diagnóstico para verificar")
    else:
        print("\\n❌ Hubo problemas aplicando la corrección")
        print("💡 Revisa manualmente el archivo graphics_generator.py")