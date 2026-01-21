# Memoria del Proyecto - Agente IA
## Información Personal
- **Nombre del usuario**: Edson
- **Perfil**: Ingeniero de Sistemas, Ingeniero Civil y Auditor
- **Contexto**: Retomando programación después de 13 años sin programar
- **Objetivo**: Maximizar habilidades como desarrollador
## Contexto General del Proyecto

### Problema a Resolver
Edson trabaja como auditor de Sistemas Integrados de Gestión ISO (9001, 14001, 45001, 37001).

**Volumen de trabajo:**
- Realiza ~50 auditorías por mes
- Cada auditoría requiere llenar 15 documentos (Word/Excel)

**Sistema actual (parcialmente implementado):**
- Excel maestro con variables y valores (ej: <<Empresa>>, <<RUC>>)
- Plantillas Word/Excel con etiquetas <<Variable>>
- Script Python que inyecta datos del Excel en las plantillas
- ✅ Funciona bien para datos estáticos

**Desafíos NO resueltos:**

1. **Lógica Condicional Compleja:**
   - Documentos varían según cantidad de normas solicitadas (1 a 4)
   - Cláusulas específicas por norma (aparecen en unas, no en otras)
   - Campos que deben mostrarse/ocultarse/bloquearse según contexto
   - Múltiples combinaciones posibles de normas

2. **Generación de Texto Natural con IA:**
   - Respuestas que parezcan escritas por humano
   - Variación entre auditorías (nunca idénticas)
   - Contextualizadas por norma y tipo de hallazgo
   - Etiquetas especiales que invocan IA para generar contenido

### Solución Elegida
**Sistema de Agentes IA Especializados (Opción 3)**

**Razón de la elección:**
- Aprendizaje profundo que servirá para otros proyectos
- Máxima automatización del proceso
- Generación de textos humanizados y variados
- Prioriza conocimiento sobre costo inicial

## Decisiones Técnicas

### Stack Tecnológico (Fase 1 - MVP)
- **Python:** 3.12.8
- **API de IA:** Gemini API (Google) - Plan gratuito
- **Procesamiento Documentos:** python-docx, openpyxl
- **Almacenamiento Prompts:** Excel (columnas adicionales)

### Formato de Etiquetas (CONFIRMADO POR EDSON)
**Etiquetas Estáticas:**
- Formato: `{{CAMPO}}` (doble llave)
- Ejemplo: `{{EMPRESA}}`, `{{RUC}}`, `{{DIRECCION}}`
- Reemplazo: Valor directo del Excel (Columna B)

**Etiquetas IA:**
- Formato: `{{IA:NOMBRE_PROMPT}}` (doble llave con prefijo IA:)
- Ejemplo: `{{IA:Hallazgo_9001}}`, `{{IA:Conclusion_General}}`
- Reemplazo: Texto generado por Gemini API usando el prompt de Columna E

### Estructura Excel Simplificada (3 columnas)
| Columna | Contenido | Ejemplo |
|---------|-----------|---------|
| A | Campo | EMPRESA, Saludo_Prueba |
| B | Valor | "Acme Corp" (estático) o "Escribe un saludo..." (prompt IA) |
| C | Campo Generado | {{EMPRESA}} o {{IA:Saludo_Prueba}} |

**Detección automática:**
- Si Campo Generado empieza con `{{IA:` → Valor = prompt para IA
- Si no → Valor = dato estático

### Arquitectura Simplificada (Fase 1)
1. **Lector Excel:** Lee datos y prompts
2. **Procesador Etiquetas:** Diferencia STATIC vs IA
3. **Cliente Gemini:** Envía prompts y recibe respuestas
4. **Generador Documentos:** Reemplaza etiquetas en plantillas

## Reglas de Generación IA (Contexto Global)
- Máximo 200 palabras por respuesta
- Concisión obligatoria: sin palabreo innecesario
- Al mencionar documentos del SIG incluir: Nombre, Código, Versión, Fecha
- Redacción en 3era persona (perspectiva de auditor)
- Sin listas, viñetas o numerales
- **EVIDENCIAS CONCRETAS**: Incluir ejemplos específicos de hallazgos (riesgos, oportunidades, datos reales)

## Aprendizajes Clave
- Sistema de contexto global permite mantener coherencia en todas las generaciones
- Detección automática de normas desde Excel (campos NORMA1, NORMA2, etc.)
- Arquitectura modular: config_auditoria.py centraliza comportamiento de IA

## Notas Importantes
- Costo actual: ~$0.0038 USD por auditoría con 60 prompts
- Tiempo de procesamiento: 2-5 segundos por prompt (secuencial)
- Con 50 prompts: ~3-4 minutos por auditoría
