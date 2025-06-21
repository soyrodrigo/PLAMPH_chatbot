# ============================================================================
# ARCHIVO: modules/__init__.py
# ============================================================================

"""
🏭 Sistema Industrial Unificado - Módulos
Planta Premoldeados Tupiza - Gobierno Municipal

Este paquete contiene todos los módulos del sistema:
- excel_manager: Gestión de archivos Excel
- graphics_generator: Generación de gráficas
- menu_controller: Control de navegación
- pdf_creator: Generación de reportes PDF
"""

__version__ = "1.0.0"
__author__ = "Sistema Industrial Tupiza"
__description__ = "Sistema de gestión industrial modular"

# Importaciones principales para facilitar el acceso
try:
    from .excel_manager import ExcelManager
    from .graphics_generator import GraphicsGenerator  
    from .menu_controller import MenuController
    from .pdf_creator import PDFCreator
    from .config import *
    
    __all__ = [
        'ExcelManager',
        'GraphicsGenerator', 
        'MenuController',
        'PDFCreator'
    ]
    
    print("✅ Módulos del sistema cargados correctamente")
    
except ImportError as e:
    print(f"⚠️ Error cargando algunos módulos: {e}")
    __all__ = []

# ============================================================================
# ARCHIVO: modules/config.py (ACTUALIZADO)
# ============================================================================

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

# TOKEN del bot de Telegram (opcional para modo bot)
TOKEN = "TU_TOKEN_AQUI"  # Cambiar por token real si se usa modo bot

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

# ============================================================================
# CONFIGURACIÓN DE EQUIPOS
# ============================================================================

TIPOS_EQUIPO = [
    "Mezcladora",
    "Vibrador",
    "Montacargas",
    "Vehículo",
    "Herramienta Manual",
    "Equipo Eléctrico",
    "Otros"
]

CONDICIONES_EQUIPO = [
    "Excelente",
    "Bueno", 
    "Regular",
    "Malo",
    "Fuera de Servicio"
]

# ============================================================================
# CONFIGURACIÓN DE REPORTES
# ============================================================================

# Configuración de PDFs
PDF_CONFIG = {
    "autor": ENTIDAD,
    "titulo_base": "Reporte del Sistema Industrial",
    "marca_agua": "GOBIERNO MUNICIPAL TUPIZA",
    "pie_pagina": f"Generado por {NOMBRE_SISTEMA}",
    "margenes": {
        "izquierdo": 72,
        "derecho": 72, 
        "superior": 72,
        "inferior": 72
    }
}

# ============================================================================
# CONFIGURACIÓN DE GRÁFICAS
# ============================================================================

GRAFICAS_CONFIG = {
    "formato": "png",
    "dpi": 300,
    "tamaño": (12, 8),
    "estilo": "seaborn-v0_8",
    "colores": {
        "primario": "#1f77b4",
        "secundario": "#ff7f0e", 
        "terciario": "#2ca02c",
        "peligro": "#d62728",
        "advertencia": "#ff9500"
    }
}

# ============================================================================
# CONFIGURACIÓN DE LOGS
# ============================================================================

LOG_CONFIG = {
    "archivo": os.path.join(DIRECTORIO_DATOS, "sistema.log"),
    "nivel": "INFO",
    "formato": "%(asctime)s - %(levelname)s - %(message)s",
    "max_tamaño": 10 * 1024 * 1024,  # 10 MB
    "backups": 5
}

# ============================================================================
# FUNCIONES DE CONFIGURACIÓN
# ============================================================================

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

def verificar_configuracion():
    """Verifica que la configuración sea válida"""
    errores = []
    
    # Verificar directorios
    directorios = [DIRECTORIO_DATOS, DIRECTORIO_GRAFICAS, DIRECTORIO_REPORTES]
    for directorio in directorios:
        if not os.path.exists(directorio):
            try:
                os.makedirs(directorio)
            except Exception as e:
                errores.append(f"No se pudo crear directorio {directorio}: {e}")
    
    # Verificar permisos de escritura
    for directorio in directorios:
        if os.path.exists(directorio) and not os.access(directorio, os.W_OK):
            errores.append(f"Sin permisos de escritura en {directorio}")
    
    return errores

def mostrar_configuracion():
    """Muestra la configuración actual del sistema"""
    print("\n⚙️ === CONFIGURACIÓN DEL SISTEMA ===")
    print(f"📊 Sistema: {NOMBRE_SISTEMA} v{VERSION}")
    print(f"🏛️ Entidad: {ENTIDAD}")
    print(f"📍 Ubicación: {UBICACION}")
    print(f"\n📁 Directorios:")
    print(f"   Datos: {DIRECTORIO_DATOS}")
    print(f"   Gráficas: {DIRECTORIO_GRAFICAS}")
    print(f"   Reportes: {DIRECTORIO_REPORTES}")
    print(f"\n📄 Archivos principales:")
    print(f"   Materiales: {os.path.basename(ARCHIVO_EXCEL_MATERIALES)}")
    print(f"   Equipos: {os.path.basename(ARCHIVO_EXCEL_EQUIPOS)}")
    print(f"   Producción: {os.path.basename(ARCHIVO_EXCEL_PRODUCCION)}")

# ============================================================================
# ARCHIVO: test_completo.py (PARA PROBAR TODO EL SISTEMA)
# ============================================================================

"""
🧪 test_completo.py - PRUEBA INTEGRAL DE TODO EL SISTEMA
"""

import sys
import os
from datetime import datetime

# Agregar modules al path
sys.path.append('modules')

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
        from modules.config import obtener_info_sistema, verificar_configuracion
        print("   ✅ Todos los módulos importados correctamente")
    except Exception as e:
        error = f"Error importando módulos: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
        return errores
    
    # 2. Verificar configuración
    print("\n2️⃣ Verificando configuración...")
    config_errores = verificar_configuracion()
    if config_errores:
        errores.extend(config_errores)
        for error in config_errores:
            print(f"   ❌ {error}")
    else:
        print("   ✅ Configuración válida")
    
    # 3. Probar ExcelManager
    print("\n3️⃣ Probando ExcelManager...")
    try:
        ExcelManager.verificar_y_crear_archivos()
        
        # Agregar datos de prueba
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        
        resultado = ExcelManager.guardar_material(
            fecha, hora, "Cemento", "Proveedor Test", "📈 Entrada", 100.0, "Prueba integral"
        )
        
        if resultado:
            print("   ✅ ExcelManager funcionando correctamente")
        else:
            error = "ExcelManager no pudo guardar datos"
            errores.append(error)
            print(f"   ❌ {error}")
            
    except Exception as e:
        error = f"Error en ExcelManager: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 4. Probar GraphicsGenerator
    print("\n4️⃣ Probando GraphicsGenerator...")
    try:
        grafica = GraphicsGenerator.generar_grafica_combustibles()
        if grafica and os.path.exists(grafica):
            print("   ✅ GraphicsGenerator funcionando correctamente")
            os.remove(grafica)  # Limpiar
        else:
            error = "GraphicsGenerator no pudo generar gráfica"
            errores.append(error)
            print(f"   ❌ {error}")
    except Exception as e:
        error = f"Error en GraphicsGenerator: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 5. Probar PDFCreator
    print("\n5️⃣ Probando PDFCreator...")
    try:
        if validar_reportlab():
            pdf = PDFCreator.generar_pdf_materiales()
            if pdf and os.path.exists(pdf):
                print("   ✅ PDFCreator funcionando correctamente")
                print(f"   📄 PDF generado: {pdf}")
            else:
                error = "PDFCreator no pudo generar PDF"
                errores.append(error)
                print(f"   ❌ {error}")
        else:
            print("   ⚠️ ReportLab no disponible - PDFCreator omitido")
    except Exception as e:
        error = f"Error en PDFCreator: {e}"
        errores.append(error)
        print(f"   ❌ {error}")
    
    # 6. Resumen final
    print(f"\n🎯 === RESUMEN DE LA PRUEBA ===")
    print(f"⏰ Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if errores:
        print(f"❌ Prueba FALLIDA - {len(errores)} errores encontrados:")
        for i, error in enumerate(errores, 1):
            print(f"   {i}. {error}")
    else:
        print("✅ Prueba EXITOSA - Todos los módulos funcionan correctamente")
        print("🚀 El sistema está listo para usar")
    
    return errores

if __name__ == "__main__":
    errores = probar_sistema_completo()
    sys.exit(len(errores))  # Salir con código de error si hay problemas

# ============================================================================
# ARCHIVO: README.md (DOCUMENTACIÓN)
# ============================================================================

"""
# 🏭 Sistema Industrial Unificado Modular

Sistema de gestión para la Planta Municipal de Premoldeados de Tupiza.

## 📋 Características

- ✅ **Gestión de Inventarios**: Control completo de materiales y combustibles
- ✅ **Visualización de Datos**: Gráficas automáticas con matplotlib
- ✅ **Reportes PDF**: Documentos profesionales con ReportLab
- ✅ **Arquitectura Modular**: Código organizado y mantenible
- ✅ **Interfaz Intuitiva**: Menús de consola fáciles de usar

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install openpyxl matplotlib reportlab
   ```
3. **Verificar estructura:**
   ```
   proyecto/
   ├── main_modular.py
   ├── modules/
   │   ├── __init__.py
   │   ├── config.py
   │   ├── excel_manager.py
   │   ├── graphics_generator.py
   │   ├── menu_controller.py
   │   └── pdf_creator.py
   └── test_completo.py
   ```

## 🎯 Uso

### Modo Interactivo (Recomendado)
```bash
python main_modular.py
```

### Modo de Prueba
```bash
python main_modular.py --test
```

### Verificar Sistema
```bash
python test_completo.py
```

## 📊 Módulos

### 1. ExcelManager
- Gestión de archivos Excel
- CRUD de materiales y equipos
- Cálculo de stock automático

### 2. GraphicsGenerator  
- Gráficas de combustibles
- Gráficas de stock de materiales
- Visualización de tendencias

### 3. MenuController
- Navegación por menús
- Interfaz de usuario
- Control de flujo

### 4. PDFCreator
- Reportes profesionales
- Marca de agua institucional
- Múltiples formatos de reporte

## 🔧 Configuración

Editar `modules/config.py` para personalizar:
- Rutas de archivos
- Configuración de gráficas
- Parámetros de reportes

## 📞 Soporte

Sistema desarrollado para el Gobierno Autónomo Municipal de Tupiza.
"""