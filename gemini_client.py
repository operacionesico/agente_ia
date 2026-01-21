"""
Cliente para interactuar con Gemini API.
Maneja la generación de texto mediante IA.
"""

from google import genai
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
        # Intentar cargar desde Streamlit secrets primero
        api_key = None
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
                api_key = st.secrets['GEMINI_API_KEY']
        except:
            pass
        
        # Si no está en Streamlit, cargar desde .env
        if not api_key:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY no encontrada. "
                "Configúrala en .env o en Streamlit secrets"
            )
        
        # Configurar cliente Gemini
        self.client = genai.Client(api_key=api_key)
    
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
        # Reemplazar variables en el prompt con valores del contexto
        if contexto:
            for key, value in contexto.items():
                # Buscar {{KEY}} y reemplazar con el valor
                placeholder = f"{{{{{key}}}}}"
                prompt = prompt.replace(placeholder, str(value))
        
        # Construir prompt completo con contexto sistema
        if contexto_sistema:
            prompt_completo = f"{contexto_sistema}\n\n---\n\nTAREA ESPECÍFICA:\n{prompt}"
        else:
            prompt_completo = prompt
        
        try:
            # Generar contenido con Gemini usando el modelo actualizado
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_completo
            )
            return response.text
        
        except Exception as e:
            # Si hay error, retornar mensaje descriptivo
            return f"[ERROR IA: {str(e)}]"


# Función de prueba (solo para verificar que funciona)
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