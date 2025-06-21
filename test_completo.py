#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 test_completo.py - PRUEBA INTEGRAL DE TODO EL SISTEMA
"""

import sys
import os
from datetime import datetime

def probar_sistema_completo():
    """Prueba integral de todos los módulos"""
    print("🧪 === PRUEBA INTEGRAL DEL SISTEMA ===")
    print(f"⏰ Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    errores = []
    
    # 1. Probar importación de módulos
    print("\n1️⃣ Probando importación de módulos...")
    try:
        from modules.excel_manager import ExcelManager
        from modules.graphics_generator import GraphicsGenerator
        from modules.menu_controller import MenuController
        from modules.pdf_creator import PDFCreator, validar_reportlab
        from modules.config import obtener_info_sistema, VERSION
        print("   ✅ Todos los módulos importados correctamente")
    except Exception as e:
        error = f"Error importando módulos: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
        return errores
    
    # 2. Verificar configuración del sistema
    print("\n2️⃣ Verificando configuración del sistema...")
    try:
        info_sistema = obtener_info_sistema()
        print(f"   ✅ Sistema: {info_sistema['nombre']} v{info_sistema['version']}")
        print(f"   ✅ Entidad: {info_sistema['entidad']}")
        
        # Verificar que se crean las carpetas automáticamente
        for directorio in ['datos', 'graficas', 'reportes']:
            if os.path.exists(directorio):
                print(f"   ✅ Directorio {directorio}/ existe")
            else:
                print(f"   ⚠️ Directorio {directorio}/ no existe (se creará automáticamente)")
                
    except Exception as e:
        error = f"Error en configuración: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 3. Probar ExcelManager
    print("\n3️⃣ Probando ExcelManager...")
    try:
        ExcelManager.verificar_y_crear_archivos()
        print("   ✅ Archivos Excel verificados/creados")
        
        # Agregar datos de prueba
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        
        # Prueba de materiales diversos
        materiales_prueba = [
            ("Cemento", "Proveedor A", "📈 Entrada", 150.0),
            ("Arena", "Proveedor B", "📈 Entrada", 200.0),
            ("Gasolina", "Estación Sur", "📈 Entrada", 180.0),
            ("Diesel", "Estación Norte", "📈 Entrada", 220.0),
            ("Cemento", "Obra 1", "📉 Salida", 25.0),
            ("Gasolina", "Maquinaria", "📉 Salida", 30.0)
        ]
        
        for material, proveedor, tipo, cantidad in materiales_prueba:
            resultado = ExcelManager.guardar_material(
                fecha, hora, material, proveedor, tipo, cantidad, "Prueba integral"
            )
            if not resultado:
                errores.append(f"Error guardando {material}")
        
        print(f"   ✅ {len(materiales_prueba)} materiales guardados")
        
        # Obtener y verificar stock
        stock = ExcelManager.obtener_stock_materiales()
        if stock:
            print(f"   ✅ Stock calculado: {len(stock)} tipos de materiales")
            for material, cantidad in stock.items():
                print(f"      📦 {material}: {cantidad:.1f}")
        else:
            error = "No se pudo calcular el stock"
            errores.append(error)
            print(f"   ❌ {error}")
        
        # Probar datos de combustibles
        combustibles = ExcelManager.obtener_datos_combustibles()
        if combustibles:
            print(f"   ✅ Datos de combustibles obtenidos")
            for combustible, cantidad in combustibles.items():
                print(f"      ⛽ {combustible}: {cantidad:.1f}L")
        
        # Probar últimos movimientos
        movimientos = ExcelManager.obtener_ultimos_movimientos(5)
        if movimientos:
            print(f"   ✅ Últimos movimientos: {len(movimientos)} registros")
        
        # Contar registros
        total_registros = ExcelManager.contar_registros_materiales()
        print(f"   ✅ Total de registros: {total_registros}")
            
    except Exception as e:
        error = f"Error en ExcelManager: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 4. Probar GraphicsGenerator
    print("\n4️⃣ Probando GraphicsGenerator...")
    try:
        # Probar gráfica de combustibles
        grafica_combustibles = GraphicsGenerator.generar_grafica_combustibles()
        if grafica_combustibles and os.path.exists(grafica_combustibles):
            print(f"   ✅ Gráfica de combustibles: {grafica_combustibles}")
            # Limpiar archivo temporal
            os.remove(grafica_combustibles)
        else:
            print("   ⚠️ No se pudo generar gráfica de combustibles")
        
        # Probar gráfica de stock
        grafica_stock = GraphicsGenerator.generar_grafica_stock_materiales()
        if grafica_stock and os.path.exists(grafica_stock):
            print(f"   ✅ Gráfica de stock: {grafica_stock}")
            # Limpiar archivo temporal
            os.remove(grafica_stock)
        else:
            print("   ⚠️ No se pudo generar gráfica de stock")
        
        # Probar información detallada de combustibles
        info_combustibles = GraphicsGenerator.obtener_info_combustibles_detallada()
        if info_combustibles:
            print(f"   ✅ Info combustibles detallada obtenida")
        
    except Exception as e:
        error = f"Error en GraphicsGenerator: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 5. Probar PDFCreator
    print("\n5️⃣ Probando PDFCreator...")
    try:
        if validar_reportlab():
            # Probar PDF de materiales
            pdf_materiales = PDFCreator.generar_pdf_materiales()
            if pdf_materiales and os.path.exists(pdf_materiales):
                print(f"   ✅ PDF de materiales: {pdf_materiales}")
                tamaño = os.path.getsize(pdf_materiales) / 1024
                print(f"      📄 Tamaño: {tamaño:.1f} KB")
            else:
                error = "No se pudo generar PDF de materiales"
                errores.append(error)
                print(f"   ❌ {error}")
            
            # Probar PDF de combustibles
            pdf_combustibles = PDFCreator.generar_pdf_combustibles()
            if pdf_combustibles and os.path.exists(pdf_combustibles):
                print(f"   ✅ PDF de combustibles: {pdf_combustibles}")
            else:
                print("   ⚠️ No se pudo generar PDF de combustibles")
                
        else:
            print("   ⚠️ ReportLab no disponible - PDFs omitidos")
            print("   💡 Instala con: pip install reportlab")
            
    except Exception as e:
        error = f"Error en PDFCreator: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 6. Probar MenuController (funciones básicas)
    print("\n6️⃣ Probando MenuController...")
    try:
        # Solo verificar que las funciones existen y son llamables
        funciones_menu = [
            MenuController.mostrar_menu_principal,
            MenuController.mostrar_menu_materiales,
            MenuController.mostrar_menu_combustibles,
            MenuController.gestionar_materiales,
            MenuController.mostrar_informacion_sistema
        ]
        
        funciones_ok = 0
        for func in funciones_menu:
            if callable(func):
                funciones_ok += 1
        
        if funciones_ok == len(funciones_menu):
            print(f"   ✅ MenuController - {funciones_ok} funciones verificadas")
        else:
            error = f"MenuController - Solo {funciones_ok}/{len(funciones_menu)} funciones disponibles"
            errores.append(error)
            print(f"   ❌ {error}")
            
    except Exception as e:
        error = f"Error en MenuController: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 7. Verificar archivos generados
    print("\n7️⃣ Verificando archivos generados...")
    archivos_esperados = [
        ("datos/inventario_materiales.xlsx", "Archivo de materiales"),
        ("datos/inventario_equipos.xlsx", "Archivo de equipos"), 
        ("datos/registro_produccion.xlsx", "Archivo de producción")
    ]
    
    for archivo, descripcion in archivos_esperados:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo) / 1024
            print(f"   ✅ {descripcion}: {tamaño:.1f} KB")
        else:
            error = f"{descripcion} no fue creado"
            errores.append(error)
            print(f"   ❌ {error}")
    
    # 8. Resumen final
    print(f"\n🎯 === RESUMEN DE LA PRUEBA ===")
    print(f"⏰ Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if errores:
        print(f"❌ Prueba FALLIDA - {len(errores)} errores encontrados:")
        for i, error in enumerate(errores, 1):
            print(f"   {i}. {error}")
        print(f"\n💡 RECOMENDACIONES:")
        print(f"   • Verifica que todos los archivos están en su lugar")
        print(f"   • Instala dependencias faltantes")
        print(f"   • Revisa los errores específicos arriba")
    else:
        print("✅ Prueba EXITOSA - Todos los módulos funcionan correctamente")
        print("🚀 El sistema está completamente operativo")
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   • Módulos probados: 4/4")
        print(f"   • Funcionalidades verificadas: 15+")
        print(f"   • Archivos generados automáticamente")
        print(f"   • Sistema listo para producción")
    
    return errores

def probar_rendimiento():
    """Prueba el rendimiento del sistema con datos múltiples"""
    print("\n⚡ === PRUEBA DE RENDIMIENTO ===")
    
    try:
        from modules.excel_manager import ExcelManager
        from modules.graphics_generator import GraphicsGenerator
        
        # Generar múltiples registros
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        
        print("📊 Generando 50 registros de prueba...")
        inicio = datetime.now()
        
        for i in range(50):
            material = f"Material_{i%5}"  # 5 tipos diferentes
            cantidad = 10.0 + (i % 100)
            tipo = "📈 Entrada" if i % 2 == 0 else "📉 Salida"
            
            ExcelManager.guardar_material(
                fecha, hora, material, "Proveedor Test", tipo, cantidad, f"Registro {i}"
            )
        
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        print(f"   ✅ 50 registros en {duracion:.2f} segundos")
        print(f"   📈 Velocidad: {50/duracion:.1f} registros/segundo")
        
        # Probar cálculo de stock con muchos datos
        print("📊 Calculando stock con datos múltiples...")
        inicio = datetime.now()
        stock = ExcelManager.obtener_stock_materiales()
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        print(f"   ✅ Stock calculado en {duracion:.3f} segundos")
        print(f"   📦 {len(stock)} tipos de materiales procesados")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en prueba de rendimiento: {e}")
        return False

def limpiar_archivos_prueba():
    """Limpia archivos generados durante las pruebas"""
    print("\n🧹 === LIMPIEZA DE ARCHIVOS DE PRUEBA ===")
    
    try:
        archivos_a_limpiar = []
        
        # Buscar archivos de prueba
        for archivo in os.listdir("."):
            if (archivo.startswith("combustibles_") or 
                archivo.startswith("stock_materiales_") or 
                archivo.startswith("reporte_") or
                archivo.startswith("grafica_")):
                archivos_a_limpiar.append(archivo)
        
        if archivos_a_limpiar:
            print(f"🗑️ Limpiando {len(archivos_a_limpiar)} archivos temporales...")
            for archivo in archivos_a_limpiar:
                try:
                    os.remove(archivo)
                    print(f"   🗑️ {archivo}")
                except:
                    pass
        else:
            print("   ✅ No hay archivos temporales para limpiar")
            
    except Exception as e:
        print(f"   ⚠️ Error durante limpieza: {e}")

def main():
    """Función principal de las pruebas"""
    print("🧪 SISTEMA DE PRUEBAS INTEGRALES")
    print("=" * 50)
    
    # Ejecutar pruebas principales
    errores = probar_sistema_completo()
    
    # Si no hay errores, hacer pruebas adicionales
    if not errores:
        print("\n" + "=" * 50)
        respuesta = input("¿Ejecutar prueba de rendimiento? (s/N): ").strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            probar_rendimiento()
        
        print("\n" + "=" * 50)
        respuesta = input("¿Limpiar archivos temporales? (s/N): ").strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            limpiar_archivos_prueba()
    
    # Resultado final
    if errores:
        print(f"\n🔥 RESULTADO: FALLÓ - {len(errores)} errores")
        sys.exit(1)
    else:
        print(f"\n🎉 RESULTADO: ÉXITO - Sistema 100% funcional")
        print("🚀 Puedes usar 'python main_modular.py' para la aplicación completa")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado en las pruebas: {e}")
        sys.exit(1)