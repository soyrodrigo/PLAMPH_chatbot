#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 MÓDULOS DEL SISTEMA INDUSTRIAL UNIFICADO
===========================================

Paquete de módulos para la gestión de la Planta de Premoldeados de Tupiza.

Módulos disponibles:
- config: Configuraciones del sistema
- excel_manager: Gestión de archivos Excel
- graphics_generator: Generación de gráficas
- menu_controller: Control de menús
- pdf_creator: Generación de reportes PDF

Autor: Sistema Industrial Automatizado
Versión: 1.0
"""

# Información del paquete
__version__ = "1.0.0"
__author__ = "Sistema Industrial Automatizado"
__description__ = "Módulos para el Sistema Industrial Unificado - Planta Tupiza"

# Imports opcionales (no obligatorios)
try:
    from . import config
except ImportError:
    pass

try:
    from . import excel_manager
except ImportError:
    pass

try:
    from . import graphics_generator
except ImportError:
    pass

# Lista de módulos exportables
__all__ = [
    'config',
    'excel_manager', 
    'graphics_generator',
    'menu_controller',
    'pdf_creator'
]