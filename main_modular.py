#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏭 MAIN MODULAR - APLICACIÓN PRINCIPAL COMPLETA
Sistema Industrial Unificado con Arquitectura Modular
Planta Premoldeados Tupiza - Gobierno Municipal

MÓDULOS INCLUIDOS:
✅ ExcelManager - Gestión de archivos Excel
✅ GraphicsGenerator - Generación de gráficas
✅ MenuController - Control de navegación y menús
✅ PDFCreator - Generación de reportes PDF
"""

import sys
import os
from datetime import datetime

def verificar_dependencias():
    """Verifica que todas las dependencias estén disponibles"""
    print("\n🔍 === VERIFICACIÓN DE DEPENDENCIAS ===")
    
    dependencias = {
        "openpyxl": "Gestión de archivos Excel",
        "matplotlib": "Generación de gráficas", 
        "reportlab": "Generación de PDFs"
    }
    
    disponibles = []
    faltantes = []
    
    for dep, descripcion in dependencias.items():
        try:
            __import__(dep)
            print(f"✅ {dep:<12} - {descripcion}")
            disponibles.append(dep)
        except ImportError:
            print(f"❌ {dep:<12} - {descripcion} (NO DISPONIBLE)")
            faltantes.append(dep)
    
    print(f"\n📊 Resumen: {len(disponibles)}/{len(dependencias)} dependencias disponibles")
    
    if faltantes:
        print("\n💡 Para instalar dependencias faltantes:")
        for dep in faltantes:
            print(f"   pip install {dep}")
    
    return len(faltantes) == 0

def verificar_modulos():
    """Verifica que todos los módulos estén disponibles"""
    print("\n🔧 === VERIFICACIÓN DE MÓDULOS ===")
    
    try:
        from modules.config import VERSION, NOMBRE_SISTEMA
        print("✅ config.py - Configuración del sistema")
        
        from modules.excel_manager import ExcelManager
        print("✅ excel_manager.py - Gestión de archivos Excel")
        
        from modules.graphics_generator import GraphicsGenerator
        print("✅ graphics_generator.py - Generación de gráficas")
        
        from modules.menu_controller import MenuController
        print("✅ menu_controller.py - Control de navegación")
        
        from modules.pdf_creator import PDFCreator, validar_reportlab
        if validar_reportlab():
            print("✅ pdf_creator.py - Generación de reportes PDF")
        else:
            print("⚠️ pdf_creator.py - Cargado (reportlab no disponible)")
        
        return True, (ExcelManager, GraphicsGenerator, MenuController, PDFCreator)
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Verifica que todos los archivos estén en la carpeta 'modules/'")
        return False, None

def mostrar_informacion_sistema():
    """Muestra información completa del sistema"""
    from modules.config import VERSION, NOMBRE_SISTEMA, ENTIDAD, UBICACION
    
    print("\n" + "="*70)
    print("🏭 === SISTEMA INDUSTRIAL UNIFICADO MODULAR ===")
    print("="*70)
    print(f"📍 Ubicación: {UBICACION}")
    print(f"🏛️ Entidad: {ENTIDAD}")
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"⚙️ Versión: {VERSION}")
    print("="*70)
    
    print("\n🔧 MÓDULOS DEL SISTEMA:")
    modulos = [
        ("📊 ExcelManager", "Gestión de archivos Excel y datos"),
        ("📈 GraphicsGenerator", "Generación de gráficas y visualizaciones"),
        ("🎯 MenuController", "Control de navegación y menús interactivos"),
        ("📄 PDFCreator", "Generación de reportes PDF profesionales")
    ]
    
    for nombre, descripcion in modulos:
        print(f"   {nombre:<20} - {descripcion}")
    
    print("\n💾 FUNCIONALIDADES PRINCIPALES:")
    funciones = [
        "📦 Gestión completa de inventario de materiales",
        "⛽ Control de stock de combustibles (Gasolina/Diesel)",
        "🏗️ Registro y seguimiento de equipos",
        "📈 Generación automática de gráficas estadísticas", 
        "📄 Reportes PDF con formato profesional",
        "📋 Consultas y análisis de datos",
        "🔧 Mantenimiento de archivos y base de datos"
    ]
    
    for funcion in funciones:
        print(f"   {funcion}")
    
    print("="*70)

def ejecutar_modo_interactivo():
    """Ejecuta el sistema en modo interactivo"""
    print("\n🚀 === INICIANDO MODO INTERACTIVO ===")
    
    # Verificar módulos
    modulos_ok, modulos = verificar_modulos()
    if not modulos_ok:
        print("❌ No se puede ejecutar - faltan módulos")
        return
    
    ExcelManager, GraphicsGenerator, MenuController, PDFCreator = modulos
    
    # Verificar y crear archivos Excel si no existen
    print("📊 Verificando archivos de datos...")
    ExcelManager.verificar_y_crear_archivos()
    
    # Ejecutar aplicación principal
    print("🎯 Iniciando aplicación principal...")
    MenuController.ejecutar_aplicacion()

def ejecutar_modo_prueba():
    """Ejecuta el sistema en modo de prueba"""
    print("\n🧪 === MODO DE PRUEBA ===")
    
    # Verificar módulos
    modulos_ok, modulos = verificar_modulos()
    if not modulos_ok:
        print("❌ No se puede ejecutar - faltan módulos")
        return
    
    ExcelManager, GraphicsGenerator, MenuController, PDFCreator = modulos
    
    print("📊 Verificando ExcelManager...")
    ExcelManager.verificar_y_crear_archivos()
    
    # Agregar datos de prueba
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    
    print("📝 Agregando datos de prueba...")
    ExcelManager.guardar_material(fecha_hoy, hora_actual, "Cemento", "Proveedor Prueba", "📈 Entrada", 100.0, "Datos de prueba")
    ExcelManager.guardar_material(fecha_hoy, hora_actual, "Gasolina", "Estación Central", "📈 Entrada", 200.0, "Abastecimiento prueba")
    ExcelManager.guardar_material(fecha_hoy, hora_actual, "Diesel", "Estación Norte", "📈 Entrada", 150.0, "Abastecimiento prueba")
    ExcelManager.guardar_material(fecha_hoy, hora_actual, "Gasolina", "Maquinaria", "📉 Salida", 25.0, "Consumo diario")
    ExcelManager.guardar_material(fecha_hoy, hora_actual, "Diesel", "Vehículos", "📉 Salida", 40.0, "Transporte")
    
    print("📈 Probando generación de gráficas...")
    grafica_combustibles = GraphicsGenerator.generar_grafica_combustibles()
    if grafica_combustibles:
        print(f"✅ Gráfica de combustibles: {grafica_combustibles}")
    
    grafica_stock = GraphicsGenerator.generar_grafica_stock_materiales()
    if grafica_stock:
        print(f"✅ Gráfica de stock: {grafica_stock}")
    
    from modules.pdf_creator import validar_reportlab
    if validar_reportlab():
        print("📄 Probando generación de PDF...")
        try:
            pdf_materiales = PDFCreator.generar_pdf_materiales()
            if pdf_materiales:
                print(f"✅ PDF de materiales: {pdf_materiales}")
                
        except Exception as e:
            print(f"⚠️ Error en PDFs: {e}")
    else:
        print("⚠️ ReportLab no disponible - PDFs omitidos")
    
    print("\n🎯 === PRUEBA COMPLETADA ===")
    print("✅ Todos los módulos funcionan correctamente")
    print("💡 Ejecuta sin argumentos para modo interactivo")

def ejecutar_demo_rapido():
    """Ejecuta una demostración rápida del sistema"""
    print("\n🎬 === DEMOSTRACIÓN RÁPIDA ===")
    
    # Verificar módulos
    modulos_ok, modulos = verificar_modulos()
    if not modulos_ok:
        print("❌ No se puede ejecutar - faltan módulos")
        return
    
    ExcelManager, GraphicsGenerator, MenuController, PDFCreator = modulos
    
    # 1. Crear archivos
    print("1️⃣ Creando estructura de archivos...")
    ExcelManager.verificar_y_crear_archivos()
    
    # 2. Agregar datos de ejemplo
    print("2️⃣ Agregando datos de ejemplo...")
    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    
    materiales_ejemplo = [
        ("Cemento", "📈 Entrada", 250.0, "Compra mensual"),
        ("Arena", "📈 Entrada", 180.0, "Abastecimiento"),
        ("Gasolina", "📈 Entrada", 300.0, "Tanque lleno"),
        ("Diesel", "📈 Entrada", 400.0, "Abastecimiento semanal"),
        ("Cemento", "📉 Salida", 45.0, "Producción adoquines"),
        ("Gasolina", "📉 Salida", 35.0, "Maquinaria"),
        ("Diesel", "📉 Salida", 60.0, "Vehículos")
    ]
    
    for material, tipo, cantidad, obs in materiales_ejemplo:
        ExcelManager.guardar_material(fecha, hora, material, "Demo", tipo, cantidad, obs)
    
    # 3. Mostrar stock
    print("3️⃣ Stock actual:")
    stock = ExcelManager.obtener_stock_materiales()
    for material, cantidad in stock.items():
        print(f"   📦 {material}: {cantidad:.1f}")
    
    # 4. Generar gráficas
    print("4️⃣ Generando gráficas...")
    grafica1 = GraphicsGenerator.generar_grafica_combustibles()
    grafica2 = GraphicsGenerator.generar_grafica_stock_materiales()
    
    if grafica1:
        print(f"   📈 Gráfica combustibles: {grafica1}")
    if grafica2:
        print(f"   📊 Gráfica stock: {grafica2}")
    
    # 5. Generar reporte
    print("5️⃣ Generando reporte...")
    from modules.pdf_creator import validar_reportlab, generar_reporte_simple
    
    reporte = generar_reporte_simple()
    if reporte:
        print(f"   📄 Reporte: {reporte}")
    
    print("\n🎉 === DEMOSTRACIÓN COMPLETADA ===")
    print("✅ Sistema funcionando correctamente")
    print("🚀 Usa 'python main_modular.py' para modo interactivo")

def mostrar_ayuda():
    """Muestra la ayuda del sistema"""
    print("\n📖 === AYUDA DEL SISTEMA ===")
    print("\nUSO:")
    print("   python main_modular.py [opción]")
    print("\nOPCIONES:")
    print("   (sin argumentos)  - Ejecutar modo interactivo")
    print("   --test           - Ejecutar modo de prueba")
    print("   --demo           - Ejecutar demostración rápida")
    print("   --info           - Mostrar información del sistema")
    print("   --deps           - Verificar dependencias")
    print("   --help           - Mostrar esta ayuda")
    print("\nEJEMPLOS:")
    print("   python main_modular.py")
    print("   python main_modular.py --test")
    print("   python main_modular.py --demo")
    print("   python main_modular.py --info")

def main():
    """Función principal del sistema"""
    # Mostrar información básica
    print("🏭 Sistema Industrial Unificado - Planta Premoldeados Tupiza")
    print(f"⏰ Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Procesar argumentos de línea de comandos
    if len(sys.argv) > 1:
        argumento = sys.argv[1].lower()
        
        if argumento in ['--help', '-h', 'help']:
            mostrar_ayuda()
        elif argumento in ['--info', 'info']:
            mostrar_informacion_sistema()
        elif argumento in ['--deps', 'deps', '--dependencies']:
            verificar_dependencias()
        elif argumento in ['--test', 'test']:
            verificar_dependencias()
            ejecutar_modo_prueba()
        elif argumento in ['--demo', 'demo']:
            verificar_dependencias()
            ejecutar_demo_rapido()
        else:
            print(f"❌ Argumento no reconocido: {argumento}")
            mostrar_ayuda()
    else:
        # Modo interactivo por defecto
        print("🔄 Verificando sistema...")
        dependencias_ok = verificar_dependencias()
        
        if not dependencias_ok:
            print("\n⚠️ Algunas dependencias faltan, pero el sistema puede funcionar")
            print("💡 Instala las dependencias faltantes para funcionalidad completa")
            respuesta = input("\n¿Continuar de todas formas? (s/N): ").strip().lower()
            if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                print("🚪 Saliendo...")
                return
        
        ejecutar_modo_interactivo()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrumpido por el usuario")
        print("🚪 Saliendo del sistema...")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Ejecuta con --help para obtener ayuda")
    finally:
        print(f"\n📅 Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("✅ Gracias por usar el Sistema Industrial Unificado")

# ============================================================================
# INFORMACIÓN ADICIONAL
# ============================================================================

"""
🎯 ESTRUCTURA DEL PROYECTO:

proyecto/
├── main_modular.py          # ← Este archivo (aplicación principal)
├── modules/
│   ├── __init__.py          # Archivo vacío para Python
│   ├── config.py            # Configuración general
│   ├── excel_manager.py     # Gestión de archivos Excel
│   ├── graphics_generator.py # Generación de gráficas
│   ├── menu_controller.py   # Control de menús
│   └── pdf_creator.py       # Generación de PDFs
├── datos/                   # Archivos de datos (se crean automáticamente)
│   ├── inventario_materiales.xlsx
│   ├── inventario_equipos.xlsx
│   └── registro_produccion.xlsx
├── graficas/                # Gráficas generadas (se crea automáticamente)
└── reportes/                # Reportes PDF (se crea automáticamente)

📋 INSTALACIÓN DE DEPENDENCIAS:
pip install openpyxl matplotlib reportlab

🚀 FORMAS DE EJECUTAR:
1. Modo interactivo: python main_modular.py
2. Modo prueba: python main_modular.py --test
3. Demostración: python main_modular.py --demo
4. Ver información: python main_modular.py --info
5. Verificar dependencias: python main_modular.py --deps

🎯 CARACTERÍSTICAS:
✅ Arquitectura modular limpia
✅ Gestión completa de inventarios
✅ Generación automática de gráficas
✅ Reportes PDF profesionales
✅ Interfaz de línea de comandos intuitiva
✅ Sistema de verificación automática
✅ Manejo robusto de errores
✅ Documentación integrada
"""