#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 MENU CONTROLLER - CORREGIDO PARA BOT MODULAR
===============================================

Controla todos los menús y navegación del sistema.
COMPATIBLE CON BOT DE TELEGRAM.

Funciones corregidas para trabajar con bot_modular.py
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import os

# Importar configuración
try:
    from .config import MATERIALES, EQUIPOS, CONDICIONES
except ImportError:
    # Valores por defecto si no se puede importar
    MATERIALES = ["Cemento", "Arena", "Gasolina", "Diesel", "Alambre", "Acero", "Pintura", "Grasa"]
    EQUIPOS = ["Máquina de Soldar", "Carretilla", "Martillo", "Mezcladora", "Taladro", "Compresora", "Grúa"]
    CONDICIONES = ["Nuevo", "Muy Bueno", "Bueno", "Regular", "Malo", "Para Reparar"]

class MenuController:
    """Controlador de menús para el bot de Telegram"""
    
    @staticmethod
    def crear_menu_principal():
        """Crea el menú principal para el bot de Telegram"""
        keyboard = [
            [KeyboardButton("📦 Registrar Material"), KeyboardButton("🔧 Registrar Equipo")],
            [KeyboardButton("📝 Registrar Actividad"), KeyboardButton("🏭 Registrar Producción")],
            [KeyboardButton("📊 Gráfica Cemento"), KeyboardButton("⛽ Gráfica Combustibles")],
            [KeyboardButton("📈 Gráfica Stock"), KeyboardButton("📉 Gráfica Producción")],
            [KeyboardButton("📋 Reporte Ejecutivo"), KeyboardButton("📅 Reporte por Fecha")],
            [KeyboardButton("📸 Reporte con Fotos"), KeyboardButton("📝 Datos de Ejemplo")],
            [KeyboardButton("📋 Estado del Bot")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def crear_teclado_materiales():
        """Crea teclado con opciones de materiales para Telegram"""
        keyboard = []
        for i in range(0, len(MATERIALES), 2):
            row = []
            row.append(KeyboardButton(MATERIALES[i]))
            if i + 1 < len(MATERIALES):
                row.append(KeyboardButton(MATERIALES[i + 1]))
            keyboard.append(row)
        keyboard.append([KeyboardButton("❌ Cancelar")])
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    @staticmethod
    def crear_teclado_equipos():
        """Crea teclado con opciones de equipos para Telegram"""
        keyboard = []
        for i in range(0, len(EQUIPOS), 2):
            row = []
            row.append(KeyboardButton(EQUIPOS[i]))
            if i + 1 < len(EQUIPOS):
                row.append(KeyboardButton(EQUIPOS[i + 1]))
            keyboard.append(row)
        keyboard.append([KeyboardButton("❌ Cancelar")])
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    @staticmethod
    def crear_teclado_movimientos():
        """Crea teclado con opciones de movimientos para Telegram"""
        keyboard = [
            [KeyboardButton("📈 Entrada"), KeyboardButton("📉 Salida")],
            [KeyboardButton("❌ Cancelar")]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    @staticmethod
    def crear_teclado_condiciones():
        """Crea teclado con opciones de condiciones para Telegram"""
        keyboard = []
        for i in range(0, len(CONDICIONES), 2):
            row = []
            row.append(KeyboardButton(CONDICIONES[i]))
            if i + 1 < len(CONDICIONES):
                row.append(KeyboardButton(CONDICIONES[i + 1]))
            keyboard.append(row)
        keyboard.append([KeyboardButton("❌ Cancelar")])
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    @staticmethod
    def crear_menu_produccion():
        """Crea menú para tipos de producción"""
        keyboard = [
            [KeyboardButton("🧱 Adoquines Modelo I"), KeyboardButton("🧱 Adoquines Doble S")],
            [KeyboardButton("📦 Pallets Modelo I"), KeyboardButton("📦 Pallets Doble S")],
            [KeyboardButton("❌ Cancelar")]
        ]
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    @staticmethod
    def crear_menu_cancelar():
        """Crea menú simple con solo cancelar"""
        keyboard = [[KeyboardButton("❌ Cancelar")]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # ===============================================================
    # FUNCIONES ORIGINALES PARA COMPATIBILIDAD CON VERSIÓN ANTERIOR
    # ===============================================================
    
    @staticmethod
    def mostrar_menu_principal():
        """Muestra el menú principal (versión consola)"""
        print("\n🏭 === MENÚ PRINCIPAL ===")
        print("1. 📦 Gestión de Materiales")
        print("2. 🔧 Gestión de Equipos")
        print("3. 📊 Gráficas y Reportes")
        print("4. 📋 Consultas")
        print("5. ⚙️ Configuración")
        print("6. 🚪 Salir")
        print("=" * 30)
    
    @staticmethod
    def mostrar_menu_materiales():
        """Muestra el menú de materiales (versión consola)"""
        print("\n📦 === GESTIÓN DE MATERIALES ===")
        print("1. Registrar entrada de material")
        print("2. Registrar salida de material")
        print("3. Ver stock actual")
        print("4. Buscar material")
        print("5. 🔙 Volver al menú principal")
        print("=" * 35)
    
    @staticmethod
    def mostrar_menu_combustibles():
        """Muestra el menú de combustibles (versión consola)"""
        print("\n⛽ === GESTIÓN DE COMBUSTIBLES ===")
        print("1. Registrar entrada de gasolina")
        print("2. Registrar salida de gasolina")
        print("3. Registrar entrada de diesel")
        print("4. Registrar salida de diesel")
        print("5. Ver stock de combustibles")
        print("6. Generar gráfica de combustibles")
        print("7. 🔙 Volver")
        print("=" * 35)
    
    @staticmethod
    def gestionar_materiales():
        """Gestiona el flujo de materiales (versión consola)"""
        from .excel_manager import ExcelManager
        
        while True:
            MenuController.mostrar_menu_materiales()
            try:
                opcion = input("Selecciona una opción (1-5): ").strip()
                
                if opcion == "1":
                    MenuController._registrar_entrada_material()
                elif opcion == "2":
                    MenuController._registrar_salida_material()
                elif opcion == "3":
                    MenuController._mostrar_stock_actual()
                elif opcion == "4":
                    MenuController._buscar_material()
                elif opcion == "5":
                    break
                else:
                    print("❌ Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n🚪 Regresando al menú principal...")
                break
    
    @staticmethod
    def mostrar_informacion_sistema():
        """Muestra información del sistema"""
        from .config import VERSION, NOMBRE_SISTEMA, ENTIDAD
        
        print(f"\n📋 === INFORMACIÓN DEL SISTEMA ===")
        print(f"🏭 Sistema: {NOMBRE_SISTEMA}")
        print(f"🏛️ Entidad: {ENTIDAD}")
        print(f"⚙️ Versión: {VERSION}")
        print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 40)
    
    @staticmethod
    def ejecutar_aplicacion():
        """Ejecuta la aplicación principal en modo consola"""
        from .excel_manager import ExcelManager
        from .graphics_generator import GraphicsGenerator
        
        print("🚀 === APLICACIÓN PRINCIPAL ===")
        print("Sistema ejecutándose en modo consola...")
        
        # Verificar archivos
        ExcelManager.verificar_y_crear_archivos()
        
        while True:
            try:
                MenuController.mostrar_menu_principal()
                opcion = input("Selecciona una opción (1-6): ").strip()
                
                if opcion == "1":
                    MenuController.gestionar_materiales()
                elif opcion == "2":
                    print("🔧 Gestión de equipos - En desarrollo")
                elif opcion == "3":
                    MenuController._menu_graficas()
                elif opcion == "4":
                    MenuController._menu_consultas()
                elif opcion == "5":
                    MenuController.mostrar_informacion_sistema()
                elif opcion == "6":
                    print("🚪 Saliendo del sistema...")
                    break
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Aplicación interrumpida por el usuario")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
    
    # ===============================
    # MÉTODOS AUXILIARES PRIVADOS
    # ===============================
    
    @staticmethod
    def _registrar_entrada_material():
        """Registra entrada de material"""
        from .excel_manager import ExcelManager
        
        print("\n📦 === REGISTRAR ENTRADA DE MATERIAL ===")
        
        print("Materiales disponibles:")
        for i, material in enumerate(MATERIALES, 1):
            print(f"{i}. {material}")
        
        try:
            seleccion = int(input("Selecciona el material (número): ")) - 1
            if 0 <= seleccion < len(MATERIALES):
                material = MATERIALES[seleccion]
                cantidad = float(input("Cantidad: "))
                proveedor = input("Proveedor: ")
                observaciones = input("Observaciones (opcional): ")
                
                fecha = datetime.now().strftime("%d/%m/%Y")
                hora = datetime.now().strftime("%H:%M:%S")
                
                exito = ExcelManager.guardar_material(
                    fecha, hora, material, proveedor, "📈 Entrada", cantidad, observaciones
                )
                
                if exito:
                    print(f"✅ Entrada registrada: {cantidad} de {material}")
                else:
                    print("❌ Error al registrar entrada")
            else:
                print("❌ Selección no válida")
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Operación cancelada")
    
    @staticmethod
    def _registrar_salida_material():
        """Registra salida de material"""
        from .excel_manager import ExcelManager
        
        print("\n📦 === REGISTRAR SALIDA DE MATERIAL ===")
        
        print("Materiales disponibles:")
        for i, material in enumerate(MATERIALES, 1):
            print(f"{i}. {material}")
        
        try:
            seleccion = int(input("Selecciona el material (número): ")) - 1
            if 0 <= seleccion < len(MATERIALES):
                material = MATERIALES[seleccion]
                cantidad = float(input("Cantidad: "))
                destino = input("Destino/Uso: ")
                observaciones = input("Observaciones (opcional): ")
                
                fecha = datetime.now().strftime("%d/%m/%Y")
                hora = datetime.now().strftime("%H:%M:%S")
                
                exito = ExcelManager.guardar_material(
                    fecha, hora, material, destino, "📉 Salida", cantidad, observaciones
                )
                
                if exito:
                    print(f"✅ Salida registrada: {cantidad} de {material}")
                else:
                    print("❌ Error al registrar salida")
            else:
                print("❌ Selección no válida")
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Operación cancelada")
    
    @staticmethod
    def _mostrar_stock_actual():
        """Muestra el stock actual"""
        from .excel_manager import ExcelManager
        
        print("\n📊 === STOCK ACTUAL ===")
        
        stock = ExcelManager.obtener_stock_materiales()
        if stock:
            for material, cantidad in stock.items():
                print(f"📦 {material}: {cantidad:.1f}")
        else:
            print("📦 No hay datos de stock disponibles")
    
    @staticmethod
    def _buscar_material():
        """Busca un material específico"""
        from .excel_manager import ExcelManager
        
        material = input("Nombre del material a buscar: ").strip()
        if material:
            movimientos = ExcelManager.obtener_ultimos_movimientos(10)
            if movimientos:
                encontrados = [m for m in movimientos if material.lower() in str(m.get('material', '')).lower()]
                if encontrados:
                    print(f"📋 Últimos movimientos de {material}:")
                    for mov in encontrados:
                        print(f"  {mov.get('fecha')} - {mov.get('tipo')} - {mov.get('cantidad')}")
                else:
                    print(f"❌ No se encontraron movimientos de {material}")
            else:
                print("❌ No hay datos disponibles")
        else:
            print("❌ Nombre de material requerido")
    
    @staticmethod
    def _menu_graficas():
        """Menú de gráficas"""
        from .graphics_generator import GraphicsGenerator
        
        print("\n📊 === MENÚ DE GRÁFICAS ===")
        print("1. Gráfica de stock de materiales")
        print("2. Gráfica de combustibles")
        print("3. 🔙 Volver")
        
        try:
            opcion = input("Selecciona una opción (1-3): ").strip()
            
            if opcion == "1":
                grafica = GraphicsGenerator.generar_grafica_stock_materiales()
                if grafica:
                    print(f"✅ Gráfica generada: {grafica}")
                else:
                    print("❌ No se pudo generar la gráfica")
                    
            elif opcion == "2":
                grafica = GraphicsGenerator.generar_grafica_combustibles()
                if grafica:
                    print(f"✅ Gráfica generada: {grafica}")
                else:
                    print("❌ No se pudo generar la gráfica")
                    
        except (ValueError, KeyboardInterrupt):
            print("❌ Operación cancelada")
    
    @staticmethod
    def _menu_consultas():
        """Menú de consultas"""
        from .excel_manager import ExcelManager
        
        print("\n📋 === MENÚ DE CONSULTAS ===")
        print("1. Ver últimos movimientos")
        print("2. Ver datos de combustibles")
        print("3. Contar registros totales")
        print("4. 🔙 Volver")
        
        try:
            opcion = input("Selecciona una opción (1-4): ").strip()
            
            if opcion == "1":
                movimientos = ExcelManager.obtener_ultimos_movimientos(10)
                if movimientos:
                    print("📋 Últimos 10 movimientos:")
                    for mov in movimientos:
                        print(f"  {mov.get('fecha')} - {mov.get('material')} - {mov.get('tipo')} - {mov.get('cantidad')}")
                else:
                    print("❌ No hay movimientos disponibles")
                    
            elif opcion == "2":
                combustibles = ExcelManager.obtener_datos_combustibles()
                if combustibles:
                    print("⛽ Datos de combustibles:")
                    for combustible, cantidad in combustibles.items():
                        print(f"  {combustible}: {cantidad:.1f}L")
                else:
                    print("❌ No hay datos de combustibles")
                    
            elif opcion == "3":
                total = ExcelManager.contar_registros_materiales()
                print(f"📊 Total de registros: {total}")
                
        except (ValueError, KeyboardInterrupt):
            print("❌ Operación cancelada")

# ===================================================================
# FUNCIONES DE COMPATIBILIDAD PARA IMPORTACIÓN DIRECTA
# ===================================================================

def crear_menu_principal():
    """Función de compatibilidad"""
    return MenuController.crear_menu_principal()

def crear_teclado_materiales():
    """Función de compatibilidad"""
    return MenuController.crear_teclado_materiales()

def crear_teclado_movimientos():
    """Función de compatibilidad"""
    return MenuController.crear_teclado_movimientos()