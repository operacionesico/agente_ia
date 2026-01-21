"""
Script de prueba para verificar que Gemini API funciona correctamente.
"""

from gemini_client import GeminiClient


def main():
    print("=" * 60)
    print("PRUEBA DE GEMINI API")
    print("=" * 60)
    
    try:
        # Inicializar cliente
        print("\n1. Inicializando cliente Gemini...")
        client = GeminiClient()
        print("   ✅ Cliente inicializado correctamente")
        
        # Prueba 1: Generación simple
        print("\n2. Prueba de generación simple...")
        prompt1 = "Escribe un saludo profesional breve de máximo 20 palabras."
        resultado1 = client.generar_texto(prompt1)
        print(f"   Prompt: {prompt1}")
        print(f"   Respuesta: {resultado1}")
        
        # Prueba 2: Generación con contexto
        print("\n3. Prueba de generación con contexto...")
        prompt2 = "Escribe un saludo para la empresa {{EMPRESA}} con RUC {{RUC}}."
        contexto = {
            'EMPRESA': 'INVERSIONES & CONTRATISTAS ORPIZA E.I.R.L.',
            'RUC': '20613997025'
        }
        resultado2 = client.generar_texto(prompt2, contexto)
        print(f"   Prompt: {prompt2}")
        print(f"   Contexto: {contexto}")
        print(f"   Respuesta: {resultado2}")
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS EXITOSAS")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nVerifica que:")
        print("1. Tienes el archivo .env con tu GEMINI_API_KEY")
        print("2. La API key es válida")
        print("3. Tienes conexión a internet")


if __name__ == "__main__":
    main()