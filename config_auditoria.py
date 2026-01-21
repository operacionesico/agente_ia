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
    
    return contexto