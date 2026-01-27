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

st.set_page_config(
    page_title="Generador de Documentos de Auditoría IA",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📋 Generador de Documentos de Auditoría con IA")
st.markdown("---")

with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    ### Cómo usar:
    1. **Sube el archivo DATA.xlsx** con los datos de la auditoría
    2. **Sube las plantillas Word y/o Excel** que deseas procesar
    3. **(Opcional)** Sube documentos de la empresa para contexto
    4. **Haz clic en Generar** y espera
    5. **Descarga** los documentos generados
    
    ### Tecnología:
    - 🤖 Gemini
    - 📝 Procesamiento inteligente
    - 🔒 Datos seguros
    """)
    
    st.markdown("---")
    st.caption(f"Versión 1.1 | {datetime.now().year}")

if 'documentos_generados' not in st.session_state:
    st.session_state.documentos_generados = None
if 'procesamiento_completo' not in st.session_state:
    st.session_state.procesamiento_completo = False

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
    st.header("📄 Paso 2: Plantillas Word/Excel")
    plantillas = st.file_uploader(
        "Sube las plantillas (.docx o .xlsx)",
        type=['docx', 'xlsx'],
        accept_multiple_files=True,
        help="Puedes subir plantillas Word y Excel al mismo tiempo"
    )
    
    if plantillas:
        plantillas_word = [p for p in plantillas if p.name.endswith('.docx')]
        plantillas_excel = [p for p in plantillas if p.name.endswith('.xlsx')]
        
        st.success(f"✅ {len(plantillas)} plantilla(s) cargada(s)")
        with st.expander("Ver plantillas"):
            if plantillas_word:
                st.write("**📝 Word:**")
                for p in plantillas_word:
                    st.write(f"- {p.name}")
            if plantillas_excel:
                st.write("**📊 Excel:**")
                for p in plantillas_excel:
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

if procesar_btn:
    try:
        from procesador_streamlit import procesar_documentos_streamlit
        
        with st.spinner("🔄 Procesando documentos con IA... Esto puede tomar varios minutos."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
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
            
            st.session_state.documentos_generados = documentos_generados
            st.session_state.procesamiento_completo = True
            
        st.success("✅ ¡Documentos generados exitosamente!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.exception(e)

if st.session_state.procesamiento_completo and st.session_state.documentos_generados:
    st.markdown("---")
    st.header("📥 Descargar Documentos Generados")
    
    documentos = st.session_state.documentos_generados
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for doc in documentos:
            zip_file.writestr(doc['nombre'], doc['contenido'])
    
    zip_buffer.seek(0)
    
    col_zip1, col_zip2, col_zip3 = st.columns([1, 2, 1])
    with col_zip2:
        st.download_button(
            label="📦 Descargar Todos (ZIP)",
            data=zip_buffer,
            file_name=f"documentos_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            use_container_width=True
        )
    
    docs_principales = [d for d in documentos if d.get('tipo') == 'documento']
    docs_contexto = [d for d in documentos if d.get('tipo') == 'contexto']
    docs_memoria = [d for d in documentos if d.get('tipo') == 'memoria']
    
    if docs_principales:
        st.markdown("### 📄 Documentos Procesados")
        
        for i, doc in enumerate(docs_principales):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{i+1}.** {doc['nombre']}")
            
            with col2:
                if doc['nombre'].endswith('.xlsx'):
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                else:
                    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                
                st.download_button(
                    label="⬇️ Descargar",
                    data=doc['contenido'],
                    file_name=doc['nombre'],
                    mime=mime_type,
                    key=f"download_doc_{i}"
                )
    
    if docs_contexto:
        st.markdown("### 📋 Archivos de Contexto IA")
        st.caption("Contexto enviado a la IA para generar las respuestas")
        
        for i, doc in enumerate(docs_contexto):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**📝** {doc['nombre']}")
            
            with col2:
                st.download_button(
                    label="⬇️ Descargar",
                    data=doc['contenido'],
                    file_name=doc['nombre'],
                    mime="text/plain",
                    key=f"download_ctx_{i}"
                )
    
    if docs_memoria:
        st.markdown("### 🧠 Archivos de Memoria IA")
        st.caption("Registro de todas las respuestas generadas por la IA")
        
        for i, doc in enumerate(docs_memoria):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**💾** {doc['nombre']}")
            
            with col2:
                st.download_button(
                    label="⬇️ Descargar",
                    data=doc['contenido'],
                    file_name=doc['nombre'],
                    mime="text/plain",
                    key=f"download_mem_{i}"
                )
    
    st.markdown("---")
    if st.button("🔄 Procesar Nuevos Documentos"):
        st.session_state.documentos_generados = None
        st.session_state.procesamiento_completo = False
        st.rerun()

st.markdown("---")
st.caption("🤖 Powered by Gemini AI | Desarrollado para auditorías ISO")
