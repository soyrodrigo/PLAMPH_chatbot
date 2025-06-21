#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 test_simple.py - PRUEBA SIMPLE PARA VERIFICAR QUE TODO FUNCIONA
"""

import sys
from datetime import datetime

def probar_modulos():
    """Prueba que todos los módulos se puedan importar"""
    print("🧪 === PRUEBA SIMPLE DE MÓDULOS ===")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # 1. Probar importaciones
    print("\n1️⃣ Probando importaciones...")
    try:
        from modules.config import VERSION, NOMBRE_SISTEMA
        print("   ✅ config.py importado")
        
        from modules.excel_manager import ExcelManager
        print("   ✅ excel_manager.py importado")
        
        from modules.graphics_generator import GraphicsGenerator
        print("   ✅ graphics_generator.py importado")
        
        # Verificar que menu_controller.py y pdf_creator.py existan
        # (Los crearemos en los siguientes pasos)
        try:
            from modules.menu_controller import MenuController
            print("   ✅ menu_controller.py importado")
        except ImportError:
            print("   ⚠️ menu_controller.py no encontrado (crear después)")
        
        try:
            from modules.pdf_creator import PDFCreator
            print("   ✅ pdf_creator.py importado")
        except ImportError:
            print("   ⚠️ pdf_creator.py no encontrado (crear después)")
        
    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False
    
    # 2. Probar funciones básicas
    print("\n2️⃣ Probando funciones básicas...")
    try:
        # Crear archivos Excel
        ExcelManager.verificar_y_crear_archivos()
        print("   ✅ Archivos Excel verificados/creados")
        
        # Agregar dato de prueba
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        
        resultado = ExcelManager.guardar_material(
            fecha, hora, "Cemento", "Prueba", "📈 Entrada", 50.0, "Test"
        )
        
        if resultado:
            print("   ✅ Guardado de material funciona")
        else:
            print("   ❌ Error guardando material")
        
        # Obtener stock
        stock = ExcelManager.obtener_stock_materiales()
        if stock:
            print(f"   ✅ Stock obtenido: {len(stock)} materiales")
        else:
            print("   ⚠️ No hay stock (normal en primera ejecución)")
        
    except Exception as e:
        print(f"   ❌ Error en funciones: {e}")
        return False
    
    # 3. Probar gráficas (si matplotlib está disponible)
    print("\n3️⃣ Probando gráficas...")
    try:
        grafica = GraphicsGenerator.generar_grafica_combustibles()
        if grafica:
            print(f"   ✅ Gráfica generada: {grafica}")
            # Limpiar archivo temporal
            import os
            if os.path.exists(grafica):
                os.remove(grafica)
        else:
            print("   ⚠️ No se pudo generar gráfica (normal si falta matplotlib)")
    except Exception as e:
        print(f"   ⚠️ Error en gráficas: {e}")
    
    print("\n✅ === PRUEBA COMPLETADA ===")
    print("🎯 Los módulos básicos funcionan correctamente")
    print("💡 Ahora puedes crear los módulos restantes")
    
    return True

if __name__ == "__main__":
    exito = probar_modulos()
    if exito:
        print("\n🚀 ¡Sistema listo para continuar!")
    else:
        print("\n❌ Hay problemas que resolver")
        sys.exit(1)