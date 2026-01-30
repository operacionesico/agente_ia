"""
Configuración global para generación de contenido de auditoría.
Define el contexto base que se aplica a TODAS las generaciones de IA.
"""

import os

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
    
    num_proceso = 1
    procesos_encontrados = []
    
    while f'PROCESO_{num_proceso}' in datos_estaticos:
        proceso = datos_estaticos.get(f'PROCESO_{num_proceso}', '')
        responsable = datos_estaticos.get(f'RESPONSABLE_PROC{num_proceso}', '')
        nombre = datos_estaticos.get(f'NOMBRE_RESP{num_proceso}', '')
        tipo = datos_estaticos.get(f'TIPOPROC_{num_proceso}', '')
        cantidad = datos_estaticos.get(f'CANTPROC_{num_proceso}', '')
        
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

def extraer_catalogo_documentos_sig(datos_estaticos):
    """
    Extrae todos los documentos del SIG desde campos DOC_* en datos_estaticos.
    
    Args:
        datos_estaticos: Diccionario con todos los campos de DATA.xlsx
    
    Returns:
        String con catálogo formateado de documentos del SIG
    """
    documentos_sig = []
    
    # Extraer solo campos que empiezan con DOC_ y tienen valor
    for campo, valor in sorted(datos_estaticos.items()):
        if campo.startswith('DOC_') and valor and str(valor).strip():
            documentos_sig.append(str(valor).strip())
    
    if not documentos_sig:
        return ""
    
    # Formatear catálogo destacado
    catalogo = "\n\n" + "="*70 + "\n"
    catalogo += "📋 DOCUMENTOS DEL SIG DISPONIBLES PARA CITAR\n"
    catalogo += "="*70 + "\n\n"
    catalogo += f"Total de documentos registrados: {len(documentos_sig)}\n\n"
    
    for i, doc in enumerate(documentos_sig, 1):
        catalogo += f"{i}. {doc}\n"
    
    catalogo += "\n" + "="*70 + "\n"
    catalogo += "⚠️  IMPORTANTE: Cita estos documentos con su código y versión exacta\n"
    catalogo += "cuando generes evidencias de auditoría.\n"
    catalogo += "="*70 + "\n"
    
    return catalogo

def generar_contexto_base(normas, datos_estaticos, catalogo_documentos=None, contexto_empresa=None):
    """
    Genera el contexto base personalizado para esta ejecución.
    
    Args:
        normas: Lista de normas (ej: ["ISO 9001:2015", "ISO 45001:2018"])
        datos_estaticos: Diccionario con datos de la empresa
        catalogo_documentos: DEPRECATED - Se ignora, se usa extraer_catalogo_documentos_sig()
        contexto_empresa: String con información adicional de la empresa (RAG)
    
    Returns:
        String con el contexto formateado
    """
    normas_texto = "\n   - ".join(normas) if normas else "No especificadas"
    
    # 1. Template base con normas
    contexto = CONTEXTO_SISTEMA.format(
        NORMAS_AUDITADAS=normas_texto,
        EMPRESA=datos_estaticos.get('EMPRESA', 'No especificada'),
        RUC=datos_estaticos.get('RUC', 'No especificado')
    )
    
    # 2. Catálogo de documentos del SIG (destacado)
    catalogo_sig = extraer_catalogo_documentos_sig(datos_estaticos)
    if catalogo_sig:
        contexto += catalogo_sig
    
    # 3. Alcance del SIG (destacado - MUY IMPORTANTE)
    alcance_texto = extraer_alcance(datos_estaticos)
    if alcance_texto:
        contexto += alcance_texto
    
    # 4. Personal y Procesos (destacado)
    procesos_info = formatear_procesos(datos_estaticos)
    if procesos_info:
        contexto += procesos_info
    
    # 4.5. Función de Cumplimiento (SOLO si se audita ISO 37001)
    funcion_cumplimiento = extraer_funcion_cumplimiento(datos_estaticos, normas)
    if funcion_cumplimiento:
        contexto += funcion_cumplimiento
    
    # 5. Servicio/Proyecto principal (destacado - foco de muestreo)
    servicio_principal = extraer_servicio_principal(datos_estaticos)
    if servicio_principal:
        contexto += servicio_principal
    
    # 6. Datos básicos de la empresa (limpios, sin DOC_* ni etiquetas)
    datos_limpios = formatear_datos_empresa_limpios(datos_estaticos)
    if datos_limpios:
        contexto += datos_limpios
    
    # 7. Contexto empresa (RAG) si existe
    if contexto_empresa:
        contexto += "\n\n" + "="*70 + "\n"
        contexto += "📄 INFORMACIÓN ADICIONAL DE DOCUMENTOS EMPRESA\n"
        contexto += "="*70 + "\n"
        contexto += contexto_empresa
    
    return contexto
def extraer_alcance(datos_estaticos):
    """
    Extrae y destaca el ALCANCE del sistema de gestión.
    
    Args:
        datos_estaticos: Diccionario con todos los campos de DATA.xlsx
    
    Returns:
        String con alcance formateado y destacado
    """
    alcance = datos_estaticos.get('ALCANCE', '')
    if not alcance or not str(alcance).strip():
        return ""
    
    texto = "\n\n" + "="*70 + "\n"
    texto += "🎯 ALCANCE DEL SISTEMA DE GESTIÓN\n"
    texto += "="*70 + "\n\n"
    texto += f"{alcance}\n\n"
    texto += "="*70 + "\n"
    
    return texto

def extraer_servicio_principal(datos_estaticos):
    """
    Extrae SERVICIO_1 como foco principal de muestreo y lista otros servicios.
    
    Args:
        datos_estaticos: Diccionario con todos los campos de DATA.xlsx
    
    Returns:
        String con servicio principal destacado
    """
    servicio_1 = datos_estaticos.get('SERVICIO_1', '')
    if not servicio_1 or not str(servicio_1).strip():
        return ""
    
    texto = "\n\n" + "="*70 + "\n"
    texto += "🎯 SERVICIO/PROYECTO AUDITADO (FOCO PRINCIPAL DE MUESTREO)\n"
    texto += "="*70 + "\n\n"
    texto += f"{servicio_1}\n\n"
    texto += "IMPORTANTE: Todas las evidencias operativas y de control deben\n"
    texto += "referirse principalmente a este proyecto/servicio.\n"
    
    # Agregar otros servicios (contexto adicional)
    otros_servicios = []
    for i in range(2, 7):
        serv = datos_estaticos.get(f'SERVICIO_{i}', '')
        if serv and str(serv).strip():
            otros_servicios.append(f"- {serv}")
    
    if otros_servicios:
        texto += "\nOtros servicios ejecutados (para contexto):\n"
        texto += "\n".join(otros_servicios) + "\n"
    
    texto += "="*70 + "\n"
    
    return texto

def formatear_datos_empresa_limpios(datos_estaticos):
    """
    Formatea datos básicos de la empresa sin etiquetas, DOC_*, NORMA*, etc.
    Solo extrae valores relevantes de columna B.
    
    Args:
        datos_estaticos: Diccionario con todos los campos de DATA.xlsx
    
    Returns:
        String con datos limpios formateados
    """
    # Campos a excluir completamente
    campos_excluir_prefijos = ['DOC_', 'NORMA', 'PROCESO_', 'SERVICIO_', 
                               'RESPONSABLE_PROC', 'NOMBRE_RESP', 'TIPOPROC', 
                               'CANTPROC', 'CLAUSULA', 'FC_', 'FUNCION_CUMPLIMIENTO']
    
    campos_excluir_exactos = ['ALCANCE', 'PROMPTS IA', 'AL', 'A1', 'A2']
    
    datos_relevantes = []
    
    for campo, valor in sorted(datos_estaticos.items()):
        # Excluir por prefijo
        if any(campo.startswith(excl) or excl in campo for excl in campos_excluir_prefijos):
            continue
        
        # Excluir exactos
        if campo in campos_excluir_exactos:
            continue
        
        # Solo incluir valores no vacíos
        if valor and str(valor).strip():
            datos_relevantes.append(f"{campo}: {valor}")
    
    if not datos_relevantes:
        return ""
    
    texto = "\n\n" + "="*70 + "\n"
    texto += "📊 INFORMACIÓN GENERAL DE LA EMPRESA\n"
    texto += "="*70 + "\n\n"
    texto += "\n".join(datos_relevantes) + "\n\n"
    texto += "="*70 + "\n"
    
    return texto

def extraer_funcion_cumplimiento(datos_estaticos, normas):
    """
    Extrae y destaca el puesto de Función de Cumplimiento (Oficial de Cumplimiento)
    SOLO si ISO 37001 está entre las normas auditadas.
    
    Args:
        datos_estaticos: Diccionario con todos los campos de DATA.xlsx
        normas: Lista de normas auditadas
    
    Returns:
        String con Oficial de Cumplimiento destacado, o cadena vacía
    """
    # Verificar si ISO 37001 está siendo auditada
    hay_iso_37001 = any('37001' in str(norma) for norma in normas)
    
    if not hay_iso_37001:
        return ""
    
    # Extraer datos del Oficial de Cumplimiento
    nombre = datos_estaticos.get('FUNCION_CUMPLIMIENTO', '')
    profesion = datos_estaticos.get('FC_PROFESION', '')
    experiencia = datos_estaticos.get('FC_EXPERIENCIA', '')
    universidad = datos_estaticos.get('FC_UNIVERSIDAD', '')
    
    if not nombre or not str(nombre).strip():
        return ""
    
    texto = "\n\n" + "="*70 + "\n"
    texto += "⚖️  FUNCIÓN DE CUMPLIMIENTO ANTISOBORNO (ISO 37001)\n"
    texto += "="*70 + "\n\n"
    texto += f"Oficial de Cumplimiento: {nombre}\n"
    
    if profesion and str(profesion).strip():
        texto += f"Profesión: {profesion}\n"
    
    if experiencia and str(experiencia).strip():
        texto += f"Experiencia: {experiencia}\n"
    
    if universidad and str(universidad).strip():
        texto += f"Formación: {universidad}\n"
    
    texto += "\n⚠️  IMPORTANTE: Esta persona es clave para responder preguntas\n"
    texto += "relacionadas con el Sistema de Gestión Antisoborno (ISO 37001).\n"
    texto += "DEBE ser entrevistada en cláusulas críticas de antisoborno.\n"
    texto += "\n" + "="*70 + "\n"
    
    return texto
