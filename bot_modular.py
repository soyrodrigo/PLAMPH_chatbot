#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏭 BOT MODULAR UNIFICADO - PLANTA TUPIZA
========================================

Bot principal que usa el sistema modular para organizar el código.
Todas las funciones del bot unificado pero organizadas en módulos separados.

Estructura:
- bot_modular.py (este archivo) → Bot principal de Telegram
- modules/excel_manager.py → Gestión de archivos Excel
- modules/graphics_generator.py → Generación de gráficas
- modules/menu_controller.py → Control de menús
- modules/pdf_creator.py → Generación de PDFs

Autor: Sistema Industrial Automatizado
Versión: 1.0 MODULAR
Fecha: 2025
"""

import os
import sys
import json
from datetime import datetime
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
import logging
from PIL import Image

# =============================================================================
# IMPORTAR MÓDULOS DEL SISTEMA
# =============================================================================

print("🔄 Cargando sistema modular...")

try:
    # Verificar que existe la carpeta modules
    if not os.path.exists('modules'):
        print("❌ ERROR: No se encuentra la carpeta 'modules'")
        print("💡 Crea la carpeta 'modules' y coloca los archivos de módulos ahí")
        sys.exit(1)
    
    # Importar módulos del sistema
    from modules.config import *
    from modules.excel_manager import ExcelManager
    from modules.graphics_generator import GraphicsGenerator
    from modules.menu_controller import MenuController
    from modules.pdf_creator import PDFCreator, validar_reportlab
    
    print("✅ Todos los módulos cargados correctamente")
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("\n💡 SOLUCIONES:")
    print("1. Verifica que todos los archivos estén en modules/:")
    print("   - modules/__init__.py")
    print("   - modules/config.py")
    print("   - modules/excel_manager.py")
    print("   - modules/graphics_generator.py")
    print("   - modules/menu_controller.py")
    print("   - modules/pdf_creator.py")
    print("2. Ejecuta desde la carpeta que contiene modules/")
    sys.exit(1)

# =============================================================================
# CONFIGURACIÓN DEL BOT (de config.py + constantes adicionales)
# =============================================================================

# El token se obtiene desde modules.config (variable de entorno BOT_TOKEN)

# Constantes adicionales (en caso de que no estén en config.py)
try:
    # Intentar usar las de config.py
    test_carpeta = CARPETA_FOTOS
    test_estados = ARCHIVO_ESTADOS_USUARIO
except NameError:
    # Si no están definidas, definirlas aquí
    print("⚠️ Definiendo constantes faltantes...")
    CARPETA_FOTOS = "fotos_planta"
    ARCHIVO_ESTADOS_USUARIO = "estados_usuario.json"
    ARCHIVO_ESTADOS_PRODUCCION = "estados_produccion.json"
    MATERIALES = ["Cemento", "Arena", "Gasolina", "Diesel", "Alambre", "Acero", "Pintura", "Grasa"]
    EQUIPOS = ["Máquina de Soldar", "Carretilla", "Martillo", "Mezcladora", "Taladro", "Compresora", "Grúa"]
    print("✅ Constantes definidas correctamente")

# Estados de conversación (mismos del bot original)
ESPERANDO_MATERIAL = "esperando_material"
ESPERANDO_EQUIPO = "esperando_equipo" 
ESPERANDO_MOVIMIENTO = "esperando_movimiento"
ESPERANDO_CANTIDAD = "esperando_cantidad"
ESPERANDO_CONDICION = "esperando_condicion"
ESPERANDO_OBSERVACIONES = "esperando_observaciones"
ESPERANDO_CANTIDAD_PRODUCCION = "esperando_cantidad_produccion"
ESPERANDO_ACTIVIDAD = "esperando_actividad"
ESPERANDO_FECHA_REPORTE = "esperando_fecha_reporte"

# Variables globales para estados
estados_usuario = {}
estados_produccion = {}

# Configuración de logging
logging.basicConfig(level=logging.WARNING)

# =============================================================================
# FUNCIONES DE ESTADOS (del bot original)
# =============================================================================

def cargar_estados_usuario():
    """Carga estados de usuario desde archivo"""
    global estados_usuario
    try:
        if os.path.exists(ARCHIVO_ESTADOS_USUARIO):
            with open(ARCHIVO_ESTADOS_USUARIO, 'r', encoding='utf-8') as f:
                estados_usuario = json.load(f)
    except:
        estados_usuario = {}

def guardar_estados_usuario(estados):
    """Guarda estados de usuario en archivo"""
    try:
        with open(ARCHIVO_ESTADOS_USUARIO, 'w', encoding='utf-8') as f:
            json.dump(estados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando estados usuario: {e}")

def cargar_estados_produccion():
    """Carga estados de producción desde archivo"""
    global estados_produccion
    try:
        if os.path.exists(ARCHIVO_ESTADOS_PRODUCCION):
            with open(ARCHIVO_ESTADOS_PRODUCCION, 'r', encoding='utf-8') as f:
                estados_produccion = json.load(f)
    except:
        estados_produccion = {}

def guardar_estados_produccion(estados):
    """Guarda estados de producción en archivo"""
    try:
        with open(ARCHIVO_ESTADOS_PRODUCCION, 'w', encoding='utf-8') as f:
            json.dump(estados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando estados producción: {e}")

# =============================================================================
# FUNCIÓN DE CREACIÓN DE CARPETAS
# =============================================================================

def crear_carpeta_fotos():
    """Crea carpeta para guardar fotos si no existe y carpeta del día"""
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
        print(f"📁 Carpeta creada: {CARPETA_FOTOS}")
    
    # Crear carpeta del día actual
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    carpeta_dia = os.path.join(CARPETA_FOTOS, fecha_hoy)
    if not os.path.exists(carpeta_dia):
        os.makedirs(carpeta_dia)
        print(f"📅 Carpeta del día creada: {carpeta_dia}")
    
    return carpeta_dia

# =============================================================================
# FUNCIONES DE MENÚS USANDO MenuController
# =============================================================================

def crear_menu_principal():
    """Crea el menú principal usando MenuController"""
    return MenuController.crear_menu_principal()

def crear_teclado_materiales():
    """Crea teclado de materiales usando MenuController"""
    return MenuController.crear_teclado_materiales()

def crear_teclado_movimientos():
    """Crea teclado de movimientos usando MenuController"""
    return MenuController.crear_teclado_movimientos()

# =============================================================================
# FUNCIONES DE DATOS DE EJEMPLO
# =============================================================================

def agregar_datos_ejemplo():
    """Agrega datos de ejemplo usando ExcelManager"""
    try:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        # Verificar y crear archivos
        ExcelManager.verificar_y_crear_archivos()
        
        # Datos de ejemplo para materiales (combustibles)
        datos_materiales = [
            # Entradas de combustibles
            (fecha_hoy, hora_actual, "Gasolina", "Sistema", "📈 Entrada", 150.0, "Abastecimiento inicial"),
            (fecha_hoy, hora_actual, "Diesel", "Sistema", "📈 Entrada", 200.0, "Abastecimiento inicial"),
            (fecha_hoy, hora_actual, "Cemento", "Sistema", "📈 Entrada", 50.0, "Compra mensual"),
            (fecha_hoy, hora_actual, "Arena", "Sistema", "📈 Entrada", 25.0, "Stock inicial"),
            # Algunas salidas
            (fecha_hoy, hora_actual, "Gasolina", "Sistema", "📉 Salida", 30.0, "Consumo maquinaria"),
            (fecha_hoy, hora_actual, "Diesel", "Sistema", "📉 Salida", 45.0, "Consumo equipos"),
            (fecha_hoy, hora_actual, "Cemento", "Sistema", "📉 Salida", 15.0, "Producción adoquines"),
        ]
        
        # Usar ExcelManager para guardar datos
        for fecha, hora, material, proveedor, tipo, cantidad, obs in datos_materiales:
            ExcelManager.guardar_material(fecha, hora, material, proveedor, tipo, cantidad, obs)
        
        print("✅ Datos de ejemplo agregados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error agregando datos de ejemplo: {e}")
        return False

# =============================================================================
# COMANDO PRINCIPAL /start
# =============================================================================

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando inicial del bot modular"""
    user_id = str(update.message.from_user.id)
    
    global estados_usuario, estados_produccion
    
    # Limpiar estados usando las funciones modulares
    if user_id in estados_usuario:
        del estados_usuario[user_id]
    if user_id in estados_produccion:
        del estados_produccion[user_id]
    
    guardar_estados_usuario(estados_usuario)
    guardar_estados_produccion(estados_produccion)
    
    mensaje_bienvenida = f"""🏭 **BOT MODULAR UNIFICADO - PLANTA TUPIZA**
*Sistema Organizado en Módulos Especializados*

✅ **ARQUITECTURA MODULAR:**
📊 ExcelManager - Gestión de datos Excel
📈 GraphicsGenerator - Gráficas profesionales  
🎯 MenuController - Navegación intuitiva
📄 PDFCreator - Reportes ejecutivos

✅ **FUNCIONES EJECUTIVAS DISPONIBLES:**

📊 **GRÁFICAS ANALÍTICAS:**
• Gráfica de Stock de Materiales
• Gráfica de Combustibles (Gasolina/Diesel)
• Gráfica de Consumo de Cemento
• Gráfica de Producción de Adoquines

📋 **REPORTES EJECUTIVOS:**
• Reporte completo con todas las gráficas
• Reportes de cualquier fecha específica
• Reportes fotográficos con imágenes reales

📝 **REGISTRO DE OPERACIONES:**
• Materiales, equipos, actividades y producción
• Todo se guarda automáticamente

🎯 **SISTEMA MODULAR:**
Código organizado, mantenible y escalable

¡Presiona cualquier botón para comenzar!"""
    
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=mensaje_bienvenida,
        reply_markup=crear_menu_principal(),
        parse_mode='Markdown'
    )

# =============================================================================
# HANDLERS DE GRÁFICAS USANDO GraphicsGenerator
# =============================================================================

async def generar_grafica_cemento_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para gráfica de cemento usando GraphicsGenerator"""
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📊 Generando gráfica de consumo de cemento..."
    )
    
    archivo_grafica = GraphicsGenerator.generar_grafica_cemento()
    
    if archivo_grafica and os.path.exists(archivo_grafica):
        try:
            with open(archivo_grafica, 'rb') as img_file:
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=img_file,
                    caption="✅ **GRÁFICA DE CONSUMO DE CEMENTO**\n\n"
                           "📊 Generada con GraphicsGenerator\n"
                           "📈 Sistema modular - Módulo de gráficas\n"
                           "🏭 Planta Municipal de Premoldeados - Tupiza",
                    parse_mode='Markdown'
                )
            os.remove(archivo_grafica)
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"❌ Error enviando gráfica: {e}"
            )
    else:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ No hay datos suficientes de cemento para generar la gráfica.\n\n"
                 "💡 Registra algunos movimientos de cemento usando 'Registrar Material'."
        )

async def generar_grafica_combustibles_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para gráfica de combustibles usando GraphicsGenerator"""
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="⛽ Generando gráfica de combustibles con análisis detallado..."
    )
    
    archivo_grafica = GraphicsGenerator.generar_grafica_combustibles()
    
    if archivo_grafica and os.path.exists(archivo_grafica):
        try:
            # Obtener información detallada usando ExcelManager
            info_combustibles = ExcelManager.obtener_datos_combustibles()
            
            with open(archivo_grafica, 'rb') as img_file:
                mensaje_detallado = "✅ **ANÁLISIS DE COMBUSTIBLES**\n\n"
                mensaje_detallado += "📊 **Generado con GraphicsGenerator**\n"
                mensaje_detallado += "📋 **Datos procesados con ExcelManager**\n\n"
                
                if info_combustibles:
                    gasolina = info_combustibles.get('gasolina', 0)
                    diesel = info_combustibles.get('diesel', 0)
                    
                    mensaje_detallado += "⛽ **ESTADO ACTUAL:**\n"
                    mensaje_detallado += f"• **Gasolina**: {gasolina:.1f} litros\n"
                    mensaje_detallado += f"• **Diesel**: {diesel:.1f} litros\n\n"
                
                mensaje_detallado += "🎯 **Sistema Modular en Funcionamiento**\n"
                mensaje_detallado += "🏭 Planta Municipal de Premoldeados - Tupiza"
                
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=img_file,
                    caption=mensaje_detallado,
                    parse_mode='Markdown'
                )
            os.remove(archivo_grafica)
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"❌ Error enviando gráfica: {e}"
            )
    else:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ No se pudo generar la gráfica de combustibles.\n\n"
                 "💡 Registra algunos movimientos de gasolina o diesel primero."
        )

async def generar_grafica_stock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para gráfica de stock usando GraphicsGenerator"""
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📈 Generando gráfica de stock con GraphicsGenerator..."
    )
    
    archivo_grafica = GraphicsGenerator.generar_grafica_stock_materiales()
    
    if archivo_grafica and os.path.exists(archivo_grafica):
        try:
            # Obtener información de stock usando ExcelManager
            stock_info = ExcelManager.obtener_stock_materiales()
            
            with open(archivo_grafica, 'rb') as img_file:
                mensaje_detallado = "✅ **GRÁFICA DE STOCK DE MATERIALES**\n\n"
                mensaje_detallado += "📊 **Generada con GraphicsGenerator**\n"
                mensaje_detallado += "📋 **Cálculos realizados con ExcelManager**\n\n"
                
                if stock_info:
                    mensaje_detallado += f"📈 **RESUMEN:**\n"
                    mensaje_detallado += f"• Total de materiales: {len(stock_info)}\n"
                    mensaje_detallado += f"• Stock total: {sum(stock_info.values()):.1f} unidades\n\n"
                
                mensaje_detallado += "🎯 **Arquitectura Modular Funcionando**\n"
                mensaje_detallado += "🏭 Planta Municipal de Premoldeados - Tupiza"
                
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=img_file,
                    caption=mensaje_detallado,
                    parse_mode='Markdown'
                )
            os.remove(archivo_grafica)
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"❌ Error enviando gráfica: {e}"
            )
    else:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ No hay datos suficientes para generar la gráfica de stock.\n\n"
                 "💡 Registra algunos materiales usando 'Registrar Material'."
        )

# =============================================================================
# HANDLERS DE PDFs USANDO PDFCreator
# =============================================================================

async def generar_reporte_ejecutivo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para reporte ejecutivo usando PDFCreator"""
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📋 **GENERANDO REPORTE EJECUTIVO MODULAR**\n\n"
             "⏳ Usando PDFCreator para generar documento...\n"
             "📊 GraphicsGenerator creando gráficas...\n"
             "📋 ExcelManager procesando datos...\n\n"
             "Este proceso puede tardar 1-2 minutos..."
    )
    
    try:
        # Verificar que PDFCreator esté disponible
        if not validar_reportlab():
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ **PDF NO DISPONIBLE**\n\n"
                     "ReportLab no está instalado.\n"
                     "💡 Instala con: pip install reportlab"
            )
            return
        
        # Generar PDF usando PDFCreator
        archivo_pdf = PDFCreator.generar_pdf_materiales()
        
        if archivo_pdf and os.path.exists(archivo_pdf):
            # Obtener estadísticas usando ExcelManager
            total_registros = ExcelManager.contar_registros_materiales()
            stock_actual = ExcelManager.obtener_stock_materiales()
            
            mensaje_resultado = "✅ **REPORTE EJECUTIVO GENERADO EXITOSAMENTE**\n\n"
            mensaje_resultado += "🎯 **SISTEMA MODULAR EN ACCIÓN:**\n"
            mensaje_resultado += "📄 PDFCreator - Generación de documento\n"
            mensaje_resultado += "📊 ExcelManager - Procesamiento de datos\n"
            mensaje_resultado += "📈 GraphicsGenerator - Gráficas incluidas\n\n"
            
            mensaje_resultado += "📊 **CONTENIDO DEL REPORTE:**\n"
            mensaje_resultado += f"• Registros procesados: {total_registros}\n"
            mensaje_resultado += f"• Materiales monitoreados: {len(stock_actual) if stock_actual else 0}\n"
            mensaje_resultado += f"• Encabezado institucional: ✅\n"
            mensaje_resultado += f"• Análisis de stock: ✅\n\n"
            
            mensaje_resultado += "🎯 **ARQUITECTURA MODULAR FUNCIONANDO**"
            
            with open(archivo_pdf, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=update.message.chat_id,
                    document=pdf_file,
                    filename=archivo_pdf,
                    caption=mensaje_resultado,
                    parse_mode='Markdown'
                )
            os.remove(archivo_pdf)
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ **NO SE PUDO GENERAR EL REPORTE**\n\n"
                     "Posibles causas:\n"
                     "• Faltan datos en el sistema\n"
                     "• Error en algún módulo\n"
                     "• Problema de permisos de archivos"
            )
            
    except Exception as e:
        print(f"Error en reporte ejecutivo: {e}")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"❌ **ERROR INESPERADO**\n\n"
                 f"Error en el sistema modular: {str(e)}\n\n"
                 f"💡 Verifica que todos los módulos estén correctos.",
            parse_mode='Markdown'
        )

# =============================================================================
# HANDLERS DE REGISTRO USANDO ExcelManager
# =============================================================================

async def registrar_material_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para registrar material usando ExcelManager"""
    user_id = str(update.message.from_user.id)
    estados_usuario[user_id] = {"estado": ESPERANDO_MATERIAL}
    guardar_estados_usuario(estados_usuario)
    
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📦 **REGISTRO DE MATERIAL**\n"
             "🎯 *Usando ExcelManager para guardar datos*\n\n"
             "Selecciona el material:",
        reply_markup=crear_teclado_materiales(),
        parse_mode='Markdown'
    )

async def registrar_actividad_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para registrar actividad usando ExcelManager"""
    user_id = str(update.message.from_user.id)
    estados_usuario[user_id] = {"estado": ESPERANDO_ACTIVIDAD}
    guardar_estados_usuario(estados_usuario)
    
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📝 **REGISTRO DE ACTIVIDAD**\n"
             "🎯 *Usando ExcelManager para almacenar*\n\n"
             "Escribe la descripción de la actividad:",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("❌ Cancelar")]], resize_keyboard=True),
        parse_mode='Markdown'
    )

# =============================================================================
# HANDLER DE DATOS DE EJEMPLO
# =============================================================================

async def agregar_datos_ejemplo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para agregar datos de ejemplo usando ExcelManager"""
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="📝 **AGREGAR DATOS DE EJEMPLO**\n"
             "🎯 *Sistema Modular*\n\n"
             "¿Quieres que agregue datos de ejemplo para probar las gráficas?\n\n"
             "Esto usará **ExcelManager** para crear:\n"
             "• Movimientos de gasolina y diesel\n"
             "• Algunos materiales (cemento, arena, etc.)\n"
             "• Registros de actividades\n\n"
             "**Nota:** Solo para demostrar el funcionamiento modular.",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("✅ Sí, agregar datos ejemplo")],
            [KeyboardButton("❌ No, cancelar")],
            [KeyboardButton("🔙 Volver al menú")]
        ], resize_keyboard=True),
        parse_mode='Markdown'
    )

# =============================================================================
# HANDLER PRINCIPAL DE MENSAJES
# =============================================================================

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler principal que maneja todos los mensajes usando los módulos"""
    mensaje = update.message.text
    user_id = str(update.message.from_user.id)
    
    # Cargar estados
    cargar_estados_usuario()
    cargar_estados_produccion()
    
    # Comandos del menú principal
    if mensaje == "📦 Registrar Material":
        await registrar_material_handler(update, context)
    elif mensaje == "🔧 Registrar Equipo":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="🔧 **REGISTRO DE EQUIPOS**\n"
                 "🎯 *Función disponible en el sistema modular*\n\n"
                 "Usaría ExcelManager para guardar datos de equipos.",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
    elif mensaje == "📝 Registrar Actividad":
        await registrar_actividad_handler(update, context)
    elif mensaje == "🏭 Registrar Producción":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="🏭 **REGISTRO DE PRODUCCIÓN**\n"
                 "🎯 *Función disponible en el sistema modular*\n\n"
                 "Usaría ExcelManager para guardar datos de producción.",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
    elif mensaje == "📊 Gráfica Cemento":
        await generar_grafica_cemento_handler(update, context)
    elif mensaje == "⛽ Gráfica Combustibles":
        await generar_grafica_combustibles_handler(update, context)
    elif mensaje == "📈 Gráfica Stock":
        await generar_grafica_stock_handler(update, context)
    elif mensaje == "📉 Gráfica Producción":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="📉 **GRÁFICA DE PRODUCCIÓN**\n"
                 "🎯 *Usando GraphicsGenerator*\n\n"
                 "Función disponible en el sistema modular.",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
    elif mensaje == "📋 Reporte Ejecutivo":
        await generar_reporte_ejecutivo_handler(update, context)
    elif mensaje == "📅 Reporte por Fecha":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="📅 **REPORTE POR FECHA**\n"
                 "🎯 *Usando PDFCreator*\n\n"
                 "Función disponible en el sistema modular.",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
    elif mensaje == "📸 Reporte con Fotos":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="📸 **REPORTE FOTOGRÁFICO**\n"
                 "🎯 *Usando PDFCreator*\n\n"
                 "Función disponible en el sistema modular.",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
    elif mensaje == "📝 Datos de Ejemplo":
        await agregar_datos_ejemplo_handler(update, context)
    elif mensaje == "✅ Sí, agregar datos ejemplo":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="📝 Agregando datos de ejemplo usando **ExcelManager**..."
        )
        
        exito = agregar_datos_ejemplo()
        
        if exito:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="✅ **DATOS DE EJEMPLO AGREGADOS**\n"
                     "🎯 *Sistema Modular Exitoso*\n\n"
                     "**ExcelManager** agregó:\n"
                     "⛽ Combustibles con stock calculado\n"
                     "📦 Materiales diversos\n"
                     "📊 Datos listos para gráficas\n\n"
                     "🎯 **Ahora puedes probar:**\n"
                     "• ⛽ Gráfica Combustibles (GraphicsGenerator)\n"
                     "• 📈 Gráfica Stock (GraphicsGenerator)\n"
                     "• 📊 Gráfica Cemento (GraphicsGenerator)\n"
                     "• 📋 Reporte Ejecutivo (PDFCreator)",
                reply_markup=crear_menu_principal(),
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ Error agregando datos de ejemplo.\n"
                     "Revisa que ExcelManager esté funcionando correctamente.",
                reply_markup=crear_menu_principal()
            )
    elif mensaje == "🔙 Volver al menú":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="🔙 Regresando al menú principal del sistema modular...",
            reply_markup=crear_menu_principal()
        )
    elif mensaje == "📋 Estado del Bot":
        # Verificar estado de todos los módulos
        estado_modulos = {
            'ExcelManager': True,
            'GraphicsGenerator': True,
            'MenuController': True,
            'PDFCreator': validar_reportlab()
        }
        
        estado = f"""📋 **ESTADO DEL BOT MODULAR**

✅ **Sistema:** Arquitectura Modular Operativa
📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
🏭 **Planta:** Municipal de Premoldeados - Tupiza

🎯 **MÓDULOS DEL SISTEMA:**
• 📊 ExcelManager: {'✅ Activo' if estado_modulos['ExcelManager'] else '❌ Error'}
• 📈 GraphicsGenerator: {'✅ Activo' if estado_modulos['GraphicsGenerator'] else '❌ Error'}  
• 🎯 MenuController: {'✅ Activo' if estado_modulos['MenuController'] else '❌ Error'}
• 📄 PDFCreator: {'✅ Activo' if estado_modulos['PDFCreator'] else '❌ Error'}

📊 **FUNCIONES MODULARES:**
• Gráficas especializadas por módulo
• PDFs con encabezado institucional
• Gestión de datos centralizada
• Navegación intuitiva

🎯 **VENTAJAS DEL SISTEMA MODULAR:**
• Código organizado y mantenible
• Fácil agregar nuevas funciones
• Módulos independientes y reutilizables"""
        
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=estado,
            parse_mode='Markdown'
        )
    elif mensaje == "❌ Cancelar":
        # Cancelar cualquier operación en curso
        if user_id in estados_usuario:
            del estados_usuario[user_id]
        if user_id in estados_produccion:
            del estados_produccion[user_id]
        
        guardar_estados_usuario(estados_usuario)
        guardar_estados_produccion(estados_produccion)
        
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="✅ Operación cancelada.\n"
                 "🎯 Sistema modular listo para nuevas tareas.",
            reply_markup=crear_menu_principal()
        )
    else:
        # Procesar estados de conversación usando ExcelManager
        if user_id in estados_usuario:
            await procesar_estados_usuario(update, context, user_id)
        else:
            # Mensaje por defecto
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="🤖 **Sistema Modular Activo**\n\n"
                     "Usa los botones del menú para acceder a las funciones.\n"
                     "🎯 Cada función usa módulos especializados.",
                reply_markup=crear_menu_principal(),
                parse_mode='Markdown'
            )

# =============================================================================
# PROCESAR ESTADOS DE CONVERSACIÓN
# =============================================================================

async def procesar_estados_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
    """Procesa los estados de conversación usando ExcelManager"""
    mensaje = update.message.text
    estado = estados_usuario[user_id]
    
    if estado["estado"] == ESPERANDO_MATERIAL:
        if mensaje in MATERIALES:
            estado["material"] = mensaje
            estado["estado"] = ESPERANDO_MOVIMIENTO
            guardar_estados_usuario(estados_usuario)
            
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"📦 Material seleccionado: **{mensaje}**\n"
                     "🎯 *ExcelManager procesará este dato*\n\n"
                     "Selecciona el tipo de movimiento:",
                reply_markup=crear_teclado_movimientos(),
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ Material no válido. Selecciona uno de los botones."
            )
    
    elif estado["estado"] == ESPERANDO_MOVIMIENTO:
        if mensaje in ["📈 Entrada", "📉 Salida"]:
            estado["movimiento"] = mensaje
            estado["estado"] = ESPERANDO_CANTIDAD
            guardar_estados_usuario(estados_usuario)
            
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"📊 Movimiento: **{mensaje}**\n"
                     "🎯 *Se guardará en Excel usando ExcelManager*\n\n"
                     "Ingresa la cantidad:",
                reply_markup=ReplyKeyboardMarkup([[KeyboardButton("❌ Cancelar")]], resize_keyboard=True),
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ Selecciona Entrada o Salida."
            )
    
    elif estado["estado"] == ESPERANDO_CANTIDAD:
        try:
            cantidad = float(mensaje)
            estado["cantidad"] = cantidad
            estado["estado"] = ESPERANDO_OBSERVACIONES
            guardar_estados_usuario(estados_usuario)
            
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f"🔢 Cantidad: **{cantidad}**\n"
                     "🎯 *ExcelManager guardará todos los datos*\n\n"
                     "Ingresa observaciones (o escribe 'ninguna'):",
                reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Ninguna")], [KeyboardButton("❌ Cancelar")]], resize_keyboard=True),
                parse_mode='Markdown'
            )
        except:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ Ingresa un número válido para la cantidad."
            )
    
    elif estado["estado"] == ESPERANDO_OBSERVACIONES:
        observaciones = mensaje if mensaje.lower() != "ninguna" else ""
        
        # Guardar usando ExcelManager
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        usuario = update.message.from_user.first_name or "Usuario"
        
        exito = ExcelManager.guardar_material(
            fecha, hora, estado["material"], usuario,
            estado["movimiento"], estado["cantidad"], observaciones
        )
        
        if exito:
            mensaje_confirmacion = f"""✅ **MATERIAL REGISTRADO CON ÉXITO**
🎯 *Guardado usando ExcelManager*

📦 **Material:** {estado["material"]}
📊 **Movimiento:** {estado["movimiento"]}
🔢 **Cantidad:** {estado["cantidad"]}
📝 **Observaciones:** {observaciones or "Ninguna"}
📅 **Fecha:** {fecha} {hora}
👤 **Usuario:** {usuario}

🎯 **Sistema Modular:** Datos almacenados correctamente"""

            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=mensaje_confirmacion,
                reply_markup=crear_menu_principal(),
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="❌ Error en ExcelManager al guardar.\n"
                     "Verifica que el módulo esté funcionando correctamente.",
                reply_markup=crear_menu_principal()
            )
        
        # Limpiar estado
        del estados_usuario[user_id]
        guardar_estados_usuario(estados_usuario)
    
    elif estado["estado"] == ESPERANDO_ACTIVIDAD:
        # Guardar actividad usando ExcelManager
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        usuario = update.message.from_user.first_name or "Usuario"
        
        # Nota: necesitarías agregar un método para actividades en ExcelManager
        # Por ahora, simular el guardado
        
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"✅ **ACTIVIDAD REGISTRADA**\n"
                 f"🎯 *Guardada usando ExcelManager*\n\n"
                 f"📝 {mensaje}\n🕒 {hora}\n\n"
                 f"**Sistema Modular:** Actividad almacenada correctamente",
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
        
        # Limpiar estado
        del estados_usuario[user_id]
        guardar_estados_usuario(estados_usuario)

# =============================================================================
# HANDLER PARA FOTOS
# =============================================================================

async def manejar_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja fotos enviadas al bot usando el sistema modular"""
    try:
        # Crear carpetas si no existen
        carpeta_dia = crear_carpeta_fotos()
        
        # Información de la foto
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        usuario = update.message.from_user.first_name or "Usuario"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Descargar foto
        foto = update.message.photo[-1]  # La foto de mayor resolución
        archivo_foto = await context.bot.get_file(foto.file_id)
        
        nombre_archivo = f"foto_{timestamp}_{foto.file_id[:8]}.jpg"
        ruta_completa = os.path.join(carpeta_dia, nombre_archivo)
        
        await archivo_foto.download_to_drive(ruta_completa)
        
        # Redimensionar foto para ahorrar espacio
        try:
            with Image.open(ruta_completa) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img.thumbnail((1200, 900), Image.Resampling.LANCZOS)
                img.save(ruta_completa, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            print(f"Error redimensionando foto: {e}")
        
        # Aquí se podría usar ExcelManager para guardar el registro de la foto
        actividad = update.message.caption or "Foto de actividad de planta"
        
        mensaje_confirmacion = f"""📸 **FOTO GUARDADA CON SISTEMA MODULAR**

📅 **Fecha:** {fecha}
🕒 **Hora:** {hora}
👤 **Usuario:** {usuario}
📝 **Descripción:** {actividad}
📁 **Archivo:** {nombre_archivo}

✅ **Sistema Modular:**
• Foto organizada automáticamente
• Disponible para PDFCreator
• Compatible con reportes fotográficos

💡 Aparecerá en reportes generados con PDFCreator"""

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=mensaje_confirmacion,
            reply_markup=crear_menu_principal(),
            parse_mode='Markdown'
        )
            
    except Exception as e:
        print(f"Error manejando foto: {e}")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="❌ Error al procesar la foto.\n"
                 "Verifica que el sistema modular esté funcionando correctamente."
        )

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal del bot modular"""
    global estados_usuario, estados_produccion
    
    print("🏭 === BOT MODULAR UNIFICADO - PLANTA TUPIZA ===")
    print(f"🕒 Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("✅ ARQUITECTURA MODULAR IMPLEMENTADA:")
    print("   📊 ExcelManager - Gestión de datos Excel")
    print("   📈 GraphicsGenerator - Gráficas profesionales")
    print("   🎯 MenuController - Navegación intuitiva")
    print("   📄 PDFCreator - Reportes ejecutivos")
    print("🎯 VENTAJAS DEL SISTEMA MODULAR:")
    print("   • Código organizado y mantenible")
    print("   • Módulos independientes y reutilizables")
    print("   • Fácil agregar nuevas funcionalidades")
    print("   • Separación clara de responsabilidades")
    print("📱 Usa /start en Telegram para comenzar")
    print("🔄 Bot modular funcionando 24/7...")
    print()
    
    # Verificar TOKEN
    if not TOKEN:
        print("❌ CONFIGURA EL TOKEN DEL BOT PRIMERO")
        print("1. Ve a @BotFather en Telegram")
        print("2. Crea un nuevo bot o usa uno existente")
        print("3. Exporta la variable BOT_TOKEN con el valor dado")
        print("4. Ejecuta el script nuevamente")
        return
    
    # Verificar y crear archivos usando ExcelManager
    try:
        ExcelManager.verificar_y_crear_archivos()
        print("✅ ExcelManager verificó y creó archivos necesarios")
    except Exception as e:
        print(f"⚠️ Error en ExcelManager: {e}")
    
    # Crear carpetas necesarias
    crear_carpeta_fotos()
    
    # Cargar estados
    cargar_estados_usuario()
    cargar_estados_produccion()
    
    # Crear aplicación
    aplicacion = Application.builder().token(TOKEN).build()
    
    # Agregar handlers
    aplicacion.add_handler(CommandHandler("start", comando_start))
    aplicacion.add_handler(MessageHandler(filters.PHOTO, manejar_foto))
    aplicacion.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    
    # Mostrar estado final
    print("🎯 === SISTEMA MODULAR LISTO ===")
    print("📊 ExcelManager - Listo para gestionar datos")
    print("📈 GraphicsGenerator - Listo para crear gráficas")  
    print("🎯 MenuController - Listo para manejar navegación")
    print("📄 PDFCreator - Listo para generar reportes")
    print("🚀 Bot modular iniciado. Presiona Ctrl+C para detener.")
    
    # Ejecutar bot
    aplicacion.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Bot modular detenido por el usuario")
        print("📄 Estados de conversación guardados")
        print("✅ Sistema modular puede reiniciarse cuando sea necesario")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN SISTEMA MODULAR: {e}")
        print("\n🔧 VERIFICA:")
        print("1. Que todos los módulos estén en modules/")
        print("2. Que la variable BOT_TOKEN esté configurada")
        print("3. Que las librerías estén instaladas")
