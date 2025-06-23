"""
⚙️ modules/config.py - CONFIGURACIÓN GENERAL DEL SISTEMA
"""

import os
from datetime import datetime

# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

VERSION = "1.0.0"
NOMBRE_SISTEMA = "Sistema Industrial Unificado"
ENTIDAD = "Gobierno Autónomo Municipal de Tupiza"
UBICACION = "Planta Municipal de Premoldeados"

# ============================================================================
# CONFIGURACIÓN DE ARCHIVOS
# ============================================================================

# Directorio base para datos
DIRECTORIO_DATOS = "datos"

# Crear directorio si no existe
if not os.path.exists(DIRECTORIO_DATOS):
    os.makedirs(DIRECTORIO_DATOS)
    print(f"📁 Directorio creado: {DIRECTORIO_DATOS}")

# Archivos Excel principales
ARCHIVO_EXCEL_MATERIALES = os.path.join(DIRECTORIO_DATOS, "inventario_materiales.xlsx")
ARCHIVO_EXCEL_EQUIPOS = os.path.join(DIRECTORIO_DATOS, "inventario_equipos.xlsx") 
ARCHIVO_EXCEL_PRODUCCION = os.path.join(DIRECTORIO_DATOS, "registro_produccion.xlsx")

# Configuración de gráficas
DIRECTORIO_GRAFICAS = "graficas"
if not os.path.exists(DIRECTORIO_GRAFICAS):
    os.makedirs(DIRECTORIO_GRAFICAS)

# Configuración de reportes
DIRECTORIO_REPORTES = "reportes"
if not os.path.exists(DIRECTORIO_REPORTES):
    os.makedirs(DIRECTORIO_REPORTES)

# ============================================================================
# CONFIGURACIÓN DE TELEGRAM (OPCIONAL)
# ============================================================================

# Se lee desde la variable de entorno BOT_TOKEN para evitar exponerlo en el código
TOKEN = os.getenv("BOT_TOKEN", "")

# ============================================================================
# CONFIGURACIÓN DE MATERIALES
# ============================================================================

# Tipos de materiales reconocidos
MATERIALES_VALIDOS = [
    "Cemento",
    "Arena",
    "Grava", 
    "Hierro",
    "Agua",
    "Aditivos",
    "Gasolina",
    "Diesel",
    "Aceite",
    "Otros"
]

# Tipos de movimientos
TIPOS_MOVIMIENTO = [
    "📈 Entrada",
    "📉 Salida"
]

# Estados de materiales
ESTADOS_STOCK = {
    "critico": 10,      # Menos de 10 unidades
    "bajo": 50,         # Entre 10 y 50 unidades
    "optimo": 51        # Más de 50 unidades
}

def obtener_info_sistema():
    """Retorna información completa del sistema"""
    return {
        "version": VERSION,
        "nombre": NOMBRE_SISTEMA,
        "entidad": ENTIDAD,
        "ubicacion": UBICACION,
        "fecha_inicio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "archivos": {
            "materiales": ARCHIVO_EXCEL_MATERIALES,
            "equipos": ARCHIVO_EXCEL_EQUIPOS,
            "produccion": ARCHIVO_EXCEL_PRODUCCION
        }
    }