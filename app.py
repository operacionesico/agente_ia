"""
Aplicación Web Streamlit para Generación de Documentos de Auditoría con IA
"""

import streamlit as st
import io
import zipfile
from datetime import datetime
import tempfile
import os
import shutil

# Configurar página
st.set_page_config(
    page_title="Generador de Documentos de Auditoría IA",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📋 Generador de Documentos de Auditoría con IA")
st.markdown("---")

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    ### Cómo usar:
    1. **Sube el archivo DATA.xlsx** con los datos de la auditoría
    2. **Sube las plantillas Word** que deseas procesar
    3. **(Opcional)** Sube documentos de la empresa para contexto
    4. **Haz clic en Generar** y espera
    5. **Descarga** los documentos generados
    
    ### Tecnología:
    - 🤖 Gemini 2.5 Flash
    - 📝 Procesamiento inteligente
    - 🔒 Datos seguros
    """)
    
    st.markdown("---")
    st.caption(f"Versión 1.0 | {datetime.now().year}")

# Inicializar session state
if 'documentos_generados' not in st.session_state:
    st.session_state.documentos_generados = None
if 'procesamiento_completo' not in st.session_state:
    st.session_state.procesamiento_completo = False

# Layout en columnas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Paso 1: Datos de Auditoría")
    data_file = st.file_uploader(
        "Sube el archivo DATA.xlsx",
        type=['xlsx'],
        help="Archivo Excel con los datos estáticos y prompts de IA"
    )
    
    if data_file:
        st.success(f"✅ Archivo cargado: {data_file.name}")

with col2:
    st.header("📄 Paso 2: Plantillas Word")
    plantillas = st.file_uploader(
        "Sube las plantillas (.docx)",
        type=['docx'],
        accept_multiple_files=True,
        help="Puedes subir múltiples plantillas a la vez"
    )
    
    if plantillas:
        st.success(f"✅ {len(plantillas)} plantilla(s) cargada(s)")
        with st.expander("Ver plantillas"):
            for p in plantillas:
                st.write(f"- {p.name}")

st.markdown("---")

st.header("🏢 Paso 3: Información de la Empresa (Opcional)")
docs_empresa = st.file_uploader(
    "Sube documentos de contexto empresarial",
    type=['pdf', 'docx', 'txt', 'xlsx'],
    accept_multiple_files=True,
    help="Estos documentos se usarán para generar contenido más específico (RAG)"
)

if docs_empresa:
    st.info(f"📁 {len(docs_empresa)} documento(s) de empresa cargado(s)")

st.markdown("---")

# Botón de procesamiento
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    procesar_btn = st.button(
        "🚀 Generar Documentos",
        type="primary",
        use_container_width=True,
        disabled=not (data_file and plantillas)
    )

if not (data_file and plantillas):
    st.warning("⚠️ Debes subir al menos el archivo DATA.xlsx y una plantilla para continuar")

# Procesamiento
if procesar_btn:
    try:
        # Importar procesador
        from procesador_streamlit import procesar_documentos_streamlit
        
        with st.spinner("🔄 Procesando documentos con IA... Esto puede tomar varios minutos."):
            # Crear barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Procesar
            status_text.text("Inicializando...")
            progress_bar.progress(10)
            
            documentos_generados = procesar_documentos_streamlit(
                data_file=data_file,
                plantillas=plantillas,
                docs_empresa=docs_empresa,
                progress_callback=lambda p, msg: (progress_bar.progress(p), status_text.text(msg))
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Procesamiento completado!")
            
            # Guardar en session state
            st.session_state.documentos_generados = documentos_generados
            st.session_state.procesamiento_completo = True
            
        st.success("✅ ¡Documentos generados exitosamente!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.exception(e)

# Mostrar resultados
if st.session_state.procesamiento_completo and st.session_state.documentos_generados:
    st.markdown("---")
    st.header("📥 Descargar Documentos Generados")
    
    documentos = st.session_state.documentos_generados
    
    # Crear ZIP con todos los documentos
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for doc in documentos:
            zip_file.writestr(doc['nombre'], doc['contenido'])
    
    zip_buffer.seek(0)
    
    # Botón para descargar todo
    col_zip1, col_zip2, col_zip3 = st.columns([1, 2, 1])
    with col_zip2:
        st.download_button(
            label="📦 Descargar Todos (ZIP)",
            data=zip_buffer,
            file_name=f"documentos_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )
    
    st.markdown("### Documentos Individuales")
    
    # Mostrar cada documento
    for i, doc in enumerate(documentos):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{i+1}.** {doc['nombre']}")
        
        with col2:
            st.download_button(
                label="⬇️ Descargar",
                data=doc['contenido'],
                file_name=doc['nombre'],
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"download_{i}"
            )
    
    # Botón para limpiar y procesar nuevos documentos
    st.markdown("---")
    if st.button("🔄 Procesar Nuevos Documentos"):
        st.session_state.documentos_generados = None
        st.session_state.procesamiento_completo = False
        st.rerun()

# Footer
st.markdown("---")
st.caption("🤖 Powered by Gemini AI | Desarrollado para auditorías ISO")
