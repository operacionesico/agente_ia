"""
Procesador adaptado para Streamlit - Trabaja con archivos en memoria
Soporta Word (.docx) y Excel (.xlsx)
"""

import io
import tempfile
import os
import shutil
from docx import Document
from docx.shared import Inches
import openpyxl
from openpyxl.drawing.image import Image
from datetime import datetime
import re

from gemini_client import GeminiClient
from config_auditoria import generar_contexto_base

# Configuración
IMAGENES_DIR = '5. IMAGENES'  # Ruta relativa para Streamlit


def procesar_documentos_streamlit(data_file, plantillas, docs_empresa=None, progress_callback=None):
    """
    Procesa documentos usando archivos en memoria (UploadedFile de Streamlit).
    Soporta plantillas Word (.docx) y Excel (.xlsx).
    
    Args:
        data_file: UploadedFile con DATA.xlsx
        plantillas: Lista de UploadedFile con plantillas .docx o .xlsx
        docs_empresa: Lista de UploadedFile con documentos empresa (opcional)
        progress_callback: Función callback(progress, mensaje) para actualizar UI
    
    Returns:
        Lista de diccionarios {'nombre': str, 'contenido': bytes}
    """
    
    def update_progress(percent, message):
        if progress_callback:
            progress_callback(percent, message)
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    
    try:
        update_progress(15, "Leyendo datos del Excel...")
        
        # 1. Leer datos del Excel
        datos_estaticos, datos_ia, normas = leer_datos_excel_memoria(data_file)
        
        update_progress(25, "Inicializando cliente IA...")
        
        # 2. Inicializar cliente Gemini
        cliente_gemini = GeminiClient()
        
        update_progress(30, "Procesando información empresarial...")
        
        # 3. Procesar documentos empresa (RAG)
        contexto_empresa = ""
        if docs_empresa:
            contexto_empresa = procesar_docs_empresa_memoria(docs_empresa, temp_dir)
        
        update_progress(35, "Generando contexto base...")
        
        # 4. Generar contexto base
        contexto_sistema = generar_contexto_base(normas, datos_estaticos, None, contexto_empresa)
        
        # 5. Procesar cada plantilla (Word o Excel)
        documentos_generados = []
        num_plantillas = len(plantillas)
        
        for idx, plantilla_file in enumerate(plantillas):
            progress_inicio = 40 + (idx * 50 // num_plantillas)
            progress_fin = 40 + ((idx + 1) * 50 // num_plantillas)
            
            update_progress(progress_inicio, f"Procesando plantilla {idx+1}/{num_plantillas}: {plantilla_file.name}...")
            
            # Detectar tipo de archivo y procesar
            es_excel = plantilla_file.name.endswith('.xlsx')
            
            if es_excel:
                doc_generado = procesar_plantilla_excel_memoria(
                    plantilla_file,
                    datos_estaticos,
                    datos_ia,
                    cliente_gemini,
                    contexto_sistema,
                    lambda p: update_progress(progress_inicio + int((progress_fin - progress_inicio) * p / 100), 
                                             f"Procesando {plantilla_file.name}... {p}%")
                )
            else:
                doc_generado = procesar_plantilla_word_memoria(
                    plantilla_file,
                    datos_estaticos,
                    datos_ia,
                    cliente_gemini,
                    contexto_sistema,
                    lambda p: update_progress(progress_inicio + int((progress_fin - progress_inicio) * p / 100), 
                                             f"Procesando {plantilla_file.name}... {p}%")
                )
            
            # Generar nombre de salida
            nombre_salida = plantilla_file.name.replace('_', '').strip()
            
            # Guardar en memoria
            output_buffer = io.BytesIO()
            doc_generado.save(output_buffer)
            output_buffer.seek(0)
            
            documentos_generados.append({
                'nombre': nombre_salida,
                'contenido': output_buffer.getvalue()
            })
            
            update_progress(progress_fin, f"Completado: {nombre_salida}")
        
        update_progress(95, "Finalizando...")
        
        return documentos_generados
        
    finally:
        # Limpiar directorio temporal
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


def leer_datos_excel_memoria(excel_file):
    """Lee datos del Excel desde un UploadedFile."""
    
    # Cargar workbook desde bytes
    wb = openpyxl.load_workbook(io.BytesIO(excel_file.read()), data_only=True)
    ws = wb.active
    
    datos_estaticos = {}
    datos_ia = {}
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        
        campo = str(row[0]).strip()
        valor = row[1] if row[1] is not None else ""
        campo_generado = str(row[2]).strip() if len(row) > 2 and row[2] else ""
        
        if campo_generado.startswith("{{IA:"):
            datos_ia[campo] = valor
        else:
            datos_estaticos[campo] = valor
    
    # Detectar normas
    normas = []
    for campo, valor in datos_estaticos.items():
        if 'NORMA' in campo.upper() and valor:
            normas.append(str(valor))
    
    wb.close()
    
    return datos_estaticos, datos_ia, normas


def procesar_docs_empresa_memoria(docs_files, temp_dir):
    """Procesa documentos de empresa desde UploadedFiles."""
    
    contexto = "\n\n═══════════════════════════════════════════════════════════════════════\n"
    contexto += "INFORMACIÓN ADICIONAL DE LA EMPRESA:\n"
    contexto += "═══════════════════════════════════════════════════════════════════════\n\n"
    
    for doc_file in docs_files:
        # Guardar temporalmente
        temp_path = os.path.join(temp_dir, doc_file.name)
        with open(temp_path, 'wb') as f:
            f.write(doc_file.read())
        
        # Leer contenido según tipo
        try:
            if doc_file.name.endswith('.txt'):
                with open(temp_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
            elif doc_file.name.endswith('.docx'):
                doc = Document(temp_path)
                contenido = '\n'.join([p.text for p in doc.paragraphs])
            else:
                contenido = f"[Documento: {doc_file.name}]"
            
            contexto += f"--- {doc_file.name} ---\n{contenido[:2000]}\n\n"
        except:
            pass
    
    return contexto


def procesar_plantilla_word_memoria(plantilla_file, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, progress_callback=None):
    """Procesa una plantilla Word desde UploadedFile."""
    
    # Cargar documento desde bytes
    doc = Document(io.BytesIO(plantilla_file.read()))
    
    # Memoria acumulativa
    memoria_respuestas = []
    
    total_parrafos = len(doc.paragraphs)
    
    # Procesar párrafos
    for idx, parrafo in enumerate(doc.paragraphs):
        if progress_callback:
            progress_callback(int((idx / total_parrafos) * 100))
        
        procesar_parrafo_streamlit(parrafo, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, memoria_respuestas)
    
    # Procesar tablas
    for tabla in doc.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                for parrafo in celda.paragraphs:
                    procesar_parrafo_streamlit(parrafo, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, memoria_respuestas)
    
    return doc


def procesar_plantilla_excel_memoria(plantilla_file, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, progress_callback=None):
    """Procesa una plantilla Excel desde UploadedFile."""
    
    # Cargar workbook desde bytes
    wb = openpyxl.load_workbook(io.BytesIO(plantilla_file.read()))
    
    # Memoria acumulativa
    memoria_respuestas = []
    
    # Contar total de celdas para progreso
    total_celdas = sum(len(list(ws.iter_rows())) for ws in wb.worksheets)
    celdas_procesadas = 0
    
    # Procesar todas las hojas
    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for celda in row:
                procesar_celda_streamlit(celda, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, memoria_respuestas)
                
                celdas_procesadas += 1
                if progress_callback and total_celdas > 0:
                    progress_callback(int((celdas_procesadas / total_celdas) * 100))
    
    return wb


def procesar_parrafo_streamlit(parrafo, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, memoria_respuestas):
    """Procesa un párrafo individual de Word."""
    
    texto = parrafo.text
    cambios = False
    
    # 1. Reemplazar etiquetas estáticas
    for campo, valor in datos_estaticos.items():
        etiqueta = f"{{{{{campo}}}}}"
        if etiqueta in texto:
            texto = texto.replace(etiqueta, str(valor))
            cambios = True
    
    # 2. Procesar etiquetas IA
    etiquetas_ia = re.findall(r'\{\{IA:([^}]+)\}\}', texto)
    
    for nombre_prompt in etiquetas_ia:
        if nombre_prompt in datos_ia:
            prompt = datos_ia[nombre_prompt]
            
            # Agregar memoria
            contexto_con_memoria = contexto_sistema
            if memoria_respuestas:
                contexto_con_memoria += "\n\n" + "="*80 + "\n"
                contexto_con_memoria += "RESPUESTAS GENERADAS PREVIAMENTE (mantén coherencia con estos datos):\n"
                contexto_con_memoria += "="*80 + "\n\n"
                # Solo últimas 15
                contexto_con_memoria += "\n\n".join(memoria_respuestas[-15:])
            
            respuesta = cliente_gemini.generar_texto(prompt, datos_estaticos, contexto_con_memoria)
            
            # Guardar en memoria
            memoria_respuestas.append(f"[{nombre_prompt}]\n{respuesta}")
            
            texto = texto.replace(f"{{{{IA:{nombre_prompt}}}}}", respuesta)
            cambios = True
    
    # 3. Limpiar formato
    if cambios:
        texto = re.sub(r',\s*,', ',', texto)
        texto = re.sub(r'\s+,', ',', texto)
        texto = re.sub(r',\s*\.', '.', texto)
        texto = re.sub(r'\s{2,}', ' ', texto)
        
        parrafo.text = texto.strip()


def procesar_celda_streamlit(celda, datos_estaticos, datos_ia, cliente_gemini, contexto_sistema, memoria_respuestas):
    """Procesa una celda individual de Excel."""
    
    if celda.value is None or not isinstance(celda.value, str):
        return
    
    texto = str(celda.value)
    cambios = False
    
    # 1. Reemplazar etiquetas estáticas
    for campo, valor in datos_estaticos.items():
        etiqueta = f"{{{{{campo}}}}}"
        if etiqueta in texto:
            texto = texto.replace(etiqueta, str(valor))
            cambios = True
    
    # 2. Procesar etiquetas IA
    etiquetas_ia = re.findall(r'\{\{IA:([^}]+)\}\}', texto)
    
    for nombre_prompt in etiquetas_ia:
        if nombre_prompt in datos_ia:
            prompt = datos_ia[nombre_prompt]
            
            # Agregar memoria
            contexto_con_memoria = contexto_sistema
            if memoria_respuestas:
                contexto_con_memoria += "\n\n" + "="*80 + "\n"
                contexto_con_memoria += "RESPUESTAS GENERADAS PREVIAMENTE (mantén coherencia con estos datos):\n"
                contexto_con_memoria += "="*80 + "\n\n"
                # Solo últimas 15
                contexto_con_memoria += "\n\n".join(memoria_respuestas[-15:])
            
            respuesta = cliente_gemini.generar_texto(prompt, datos_estaticos, contexto_con_memoria)
            
            # Guardar en memoria
            memoria_respuestas.append(f"[{nombre_prompt}]\n{respuesta}")
            
            texto = texto.replace(f"{{{{IA:{nombre_prompt}}}}}", respuesta)
            cambios = True
    
    # 3. Limpiar formato
    if cambios:
        texto = re.sub(r',\s*,', ',', texto)
        texto = re.sub(r'\s+,', ',', texto)
        texto = re.sub(r',\s*\.', '.', texto)
        texto = re.sub(r'\s{2,}', ' ', texto)
        
        celda.value = texto.strip()
