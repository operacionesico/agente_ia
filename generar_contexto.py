"""
Script para generar SOLO el archivo CONTEXTO_IA.txt
sin procesar documentos Word.

Úsalo para revisar qué se enviará a la IA antes de ejecutar el proceso completo.
"""

import os
import glob
from datetime import datetime
import openpyxl
from config_auditoria import generar_contexto_base
from lector_informacion import leer_informacion_empresa

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '1. Data')
INYECTADO_DIR = os.path.join(BASE_DIR, '3. Inyectado')

def leer_datos_excel():
    """Lee datos del Excel (solo lo necesario para contexto)"""
    archivos_excel = glob.glob(os.path.join(DATA_DIR, '*.xlsx'))
    
    if not archivos_excel:
        print(f"❌ No se encontró ningún archivo Excel en '{DATA_DIR}'")
        return None, None
    
    archivo_excel = archivos_excel[0]
    print(f"📄 Leyendo datos desde: {os.path.basename(archivo_excel)}")
    
    wb = openpyxl.load_workbook(archivo_excel, data_only=True)
    ws = wb.active
    
    datos_estaticos = {}
    
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not row[0]: continue
        
        campo = str(row[0]).strip()
        valor = row[1] if row[1] is not None else ""
        campo_generado = str(row[2]).strip() if len(row) > 2 and row[2] else ""
        
        # Solo procesar etiquetas estáticas
        if not campo_generado.startswith("{{IA:"):
            datos_estaticos[campo] = valor
    
    # Detectar normas
    normas = []
    for campo, valor in datos_estaticos.items():
        if 'NORMA' in campo.upper() and valor:
            normas.append(str(valor))
    
    wb.close()
    return datos_estaticos, normas

def main():
    print("="*80)
    print("GENERADOR DE CONTEXTO IA - MODO REVISIÓN")
    print("="*80)
    
    # 1. Leer datos
    datos_estaticos, normas = leer_datos_excel()
    if not datos_estaticos:
        return
    
    print(f"✅ Datos cargados: {len(datos_estaticos)} variables")
    
    # 2. Leer información adicional de la empresa
    contexto_empresa = leer_informacion_empresa()
    
    # 3. Generar contexto global
    contexto_sistema = generar_contexto_base(normas, datos_estaticos, None, contexto_empresa)
    
    if normas:
        print(f"📋 Normas detectadas: {', '.join(normas)}")
    
    # 4. Guardar en archivo TXT
    if not os.path.exists(INYECTADO_DIR):
        os.makedirs(INYECTADO_DIR)
    
    ruta_contexto = os.path.join(INYECTADO_DIR, 'CONTEXTO_IA.txt')
    
    with open(ruta_contexto, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CONTEXTO COMPLETO QUE SE ENVIARÁ A LA IA\n")
        f.write(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        f.write(contexto_sistema)
        f.write("\n\n" + "="*80 + "\n")
        f.write("FIN DEL CONTEXTO\n")
        f.write("="*80 + "\n")
    
    print(f"\n✅ Contexto guardado en: 3. Inyectado/CONTEXTO_IA.txt")
    print(f"📏 Tamaño: {len(contexto_sistema)} caracteres")
    print(f"📊 Tokens aprox: {len(contexto_sistema) // 4}")
    print("\nPuedes revisar el archivo antes de ejecutar inyectar_word.py")

if __name__ == "__main__":
    main()
