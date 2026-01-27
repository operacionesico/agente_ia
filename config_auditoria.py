"""
Configuración global para generación de contenido de auditoría.
Define el contexto base que se aplica a TODAS las generaciones de IA.
"""

import os

# Leer prompt desde archivo externo
def cargar_prompt_sistema():
    """Lee el prompt del sistema desde el archivo prompt.txt"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_prompt = os.path.join(base_dir, 'prompt.txt')
    
    try:
        with open(ruta_prompt, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️  Archivo prompt.txt no encontrado, usando prompt por defecto")
        return """
Eres un auditor experto en sistemas de gestión ISO.

NORMAS AUDITADAS: {NORMAS_AUDITADAS}
EMPRESA: {EMPRESA}
RUC: {RUC}

Genera contenido profesional y específico para auditorías.
"""

# Cargar prompt al iniciar
CONTEXTO_SISTEMA = cargar_prompt_sistema()


def formatear_procesos(datos_estaticos):
    """
    Extrae y formatea la información de procesos y personal desde datos_estaticos.
    
    Args:
        datos_estaticos: Diccionario con todos los datos del Excel
    
    Returns:
        String formateado con la lista de procesos y personal
    """
    procesos_texto = "\n\n═══════════════════════════════════════════════════════════════════════\n"
    procesos_texto += "PERSONAL DE LA EMPRESA (USAR ESTOS NOMBRES REALES):\n\n"
    procesos_texto += "IMPORTANTE: SOLO usa estos nombres reales en las entrevistas. NO inventes nombres.\n\n"
    
    # Detectar cuántos procesos hay (buscar PROCESO_1, PROCESO_2, etc.)
    num_proceso = 1
    procesos_encontrados = []
    
    while f'PROCESO_{num_proceso}' in datos_estaticos:
        proceso = datos_estaticos.get(f'PROCESO_{num_proceso}', '')
        responsable = datos_estaticos.get(f'RESPONSABLE_PROC{num_proceso}', '')
        nombre = datos_estaticos.get(f'NOMBRE_RESP{num_proceso}', '')
        tipo = datos_estaticos.get(f'TIPOPROC_{num_proceso}', '')
        cantidad = datos_estaticos.get(f'CANTPROC_{num_proceso}', '')
        
        # Solo agregar si hay información
        if proceso or responsable or nombre:
            procesos_encontrados.append({
                'num': num_proceso,
                'proceso': proceso,
                'responsable': responsable,
                'nombre': nombre,
                'tipo': tipo,
                'cantidad': cantidad
            })
        
        num_proceso += 1
    
    # Formatear procesos encontrados
    for proc in procesos_encontrados:
        procesos_texto += f"{proc['num']}. {proc['proceso']}\n"
        if proc['responsable']:
            procesos_texto += f"   - Cargo: {proc['responsable']}\n"
        if proc['nombre']:
            procesos_texto += f"   - Nombre: {proc['nombre']}\n"
        if proc['tipo']:
            procesos_texto += f"   - Tipo: {proc['tipo']}\n"
        if proc['cantidad']:
            procesos_texto += f"   - Personal: {proc['cantidad']} persona(s)\n"
        procesos_texto += "\n"
    
    if procesos_encontrados:
        procesos_texto += "═══════════════════════════════════════════════════════════════════════\n"
        return procesos_texto
    else:
        return ""

def generar_contexto_base(normas, datos_estaticos, catalogo_documentos=None, contexto_empresa=None):
    """
    Genera el contexto base personalizado para esta ejecución.
    
    Args:
        normas: Lista de normas (ej: ["ISO 9001:2015", "ISO 45001:2018"])
        datos_estaticos: Diccionario con datos de la empresa
        catalogo_documentos: String con el catálogo formateado de documentos del SIG
        contexto_empresa: String con información adicional de la empresa (RAG)
    
    Returns:
        String con el contexto formateado
    """
    normas_texto = "\n   - ".join(normas) if normas else "No especificadas"
    
    contexto = CONTEXTO_SISTEMA.format(
        NORMAS_AUDITADAS=normas_texto,
        EMPRESA=datos_estaticos.get('EMPRESA', 'No especificada'),
        RUC=datos_estaticos.get('RUC', 'No especificado')
    )
    
    # Agregar catálogo de documentos si existe
    if catalogo_documentos:
        contexto += catalogo_documentos
    
    # Agregar información empresarial si existe
    if contexto_empresa:
        contexto += contexto_empresa
        
    # Agregar SERVICIO AUDITADO ESPECÍFICO (Prioridad Alta)
    servicio_auditado = datos_estaticos.get('SERVICIO_1')
    if servicio_auditado:
        contexto += f"\n\n═══════════════════════════════════════════════════════════════════════\n"
        contexto += f"SERVICIO / PROYECTO AUDITADO (FOCO PRINCIPAL):\n"
        contexto += f"Todas las evidencias y muestreos deben enfocarse en:\n"
        contexto += f"👉 {servicio_auditado}\n"
        contexto += f"═══════════════════════════════════════════════════════════════════════\n"
    
    # Agregar información de procesos y personal
    procesos_info = formatear_procesos(datos_estaticos)
    if procesos_info:
        contexto += procesos_info
    
    return contexto