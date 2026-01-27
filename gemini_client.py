"""
Cliente para interactuar con Gemini API.
Maneja la generación de texto mediante IA.
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

class GeminiClient:
    """
    Cliente para generar texto usando Gemini API de Google.
    
    Funcionalidades:
    - Configuración automática desde archivo .env
    - Generación de texto con contexto dinámico
    - Manejo de errores
    """
    
    def __init__(self):
        """
        Inicializa el cliente Gemini.
        Lee la API key desde el archivo .env
        """
        api_key = None
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                api_key = st.secrets['GEMINI_API_KEY']
        except:
            pass
        
        if not api_key:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY no encontrada. "
                "Configúrala en .env o en Streamlit secrets"
            )
        
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generar_texto(self, prompt: str, contexto: dict = None, contexto_sistema: str = None) -> str:
        """
        Genera texto usando Gemini API con contexto global de auditoría.
        
        Args:
            prompt: Texto del prompt específico que describe qué generar
            contexto: Diccionario con variables para reemplazar en el prompt
                     Ejemplo: {'EMPRESA': 'Acme Corp', 'RUC': '12345'}
            contexto_sistema: Contexto base que se añade a TODOS los prompts
                            (instrucciones globales, normas, restricciones)
        
        Returns:
            Texto generado por la IA
        
        Ejemplo:
            >>> client = GeminiClient()
            >>> prompt = "Escribe un saludo para {{EMPRESA}}"
            >>> contexto = {'EMPRESA': 'Acme Corp'}
            >>> resultado = client.generar_texto(prompt, contexto)
            >>> print(resultado)
            "Buenos días, Acme Corp..."
        """
        if contexto:
            for key, value in contexto.items():
                placeholder = f"{{{{{key}}}}}"
                prompt = prompt.replace(placeholder, str(value))
        
        if contexto_sistema:
            prompt_completo = f"{contexto_sistema}\n\n---\n\nTAREA ESPECÍFICA:\n{prompt}"
        else:
            prompt_completo = prompt
        
        try:
            response = self.model.generate_content(prompt_completo)
            return response.text
        
        except Exception as e:
            return f"[ERROR IA: {str(e)}]"

if __name__ == "__main__":
    print("Probando GeminiClient...")
    
    try:
        client = GeminiClient()
        resultado = client.generar_texto(
            "Escribe un saludo profesional breve de máximo 20 palabras."
        )
        print(f"\n✅ Prueba exitosa!\n\nRespuesta de Gemini:\n{resultado}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")