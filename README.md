# Sistema de Generación de Documentos de Auditoría con IA

Sistema automatizado para generar documentos de auditoría ISO utilizando plantillas Word/Excel y contenido generado por IA (Gemini).

## Características

- ✅ Inyección de datos estáticos desde Excel
- ✅ Generación de contenido con IA (Gemini 2.5 Flash)
- ✅ Sistema de memoria acumulativa para coherencia
- ✅ RAG con documentos empresariales
- ✅ Catálogo automático de documentos del SIG
- ✅ Filtrado inteligente de servicios auditados
- ✅ Formato optimizado (90 palabras, muestreo detallado)

## Estructura del Proyecto

```
agente_ia/
├── 1. Data/              # Archivos Excel con datos (no versionado)
├── 2. Plantilla/         # Plantillas Word
├── 3. Inyectado/         # Documentos generados (no versionado)
├── 4. INFORMACION EMPRESA/ # Docs para RAG (no versionado)
├── 5. IMAGENES/          # Imágenes para insertar (no versionado)
├── inyectar_word.py      # Script principal
├── gemini_client.py      # Cliente Gemini API
├── config_auditoria.py   # Configuración de prompts
├── lector_informacion.py # Sistema RAG
├── prompt.txt            # Prompt principal de la IA
└── .env                  # API keys (no versionado)
```

## Instalación

```bash
# Instalar dependencias
pip install python-docx openpyxl google-generativeai python-dotenv

# Configurar API key de Gemini
echo "GEMINI_API_KEY=tu_clave_aqui" > .env
```

## Uso

```bash
python3 inyectar_word.py
```

## Configuración

- **Excel de datos**: Colocar en `1. Data/`
- **Plantillas**: Colocar en `2. Plantilla/`
- **Servicio auditado**: Definir variable `SERVICIO_1` en Excel

## Notas

- Los datos sensibles están protegidos por `.gitignore`
- El sistema usa Gemini 2.5 Flash para velocidad óptima
- Memoria limitada a 15 respuestas para eficiencia
