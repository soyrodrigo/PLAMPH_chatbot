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
        
        print(f"\n📊 === GENERANDO GRÁFICA DE CEMENTO ===")
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
        
        print(f"\n📈 DATOS AGRUPADOS POR FECHA:")
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
        plt.title('📊 CONSUMO DIARIO DE CEMENTO\n🏭 Planta Municipal de Premoldeados - Tupiza', 
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
        
        print(f"\n📊 RESULTADO: {len(datos_cemento)} registros de cemento encontrados")
        
        return datos_cemento
        
    except Exception as e:
        print(f"❌ Error buscando cemento: {e}")
        return []