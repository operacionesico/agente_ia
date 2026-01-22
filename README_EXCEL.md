# Procesador de Plantillas Excel con IA

## Descripción

Script para inyectar datos estáticos y contenido generado por IA en plantillas de Excel.

## Características

- ✅ Reemplazo de etiquetas estáticas `{{CAMPO}}`
- ✅ Generación de contenido con IA `{{IA:NOMBRE}}`
- ✅ Memoria acumulativa (últimas 15 respuestas)
- ✅ Sistema RAG con documentos empresariales
- ✅ Procesa múltiples hojas en un mismo archivo
- ✅ Guarda memoria de respuestas IA

## Uso

### Ejecución desde Consola

```bash
python3 inyectar_excel.py
```

### Estructura de Carpetas

```
agente_ia/
├── 1. Data/              # Excel con datos (DATA.xlsx)
├── 2. Plantilla/         # Plantillas Excel (_plantilla.xlsx)
├── 3. Inyectado/         # Excel generados
└── 4. INFORMACION EMPRESA/  # Docs para RAG (opcional)
```

## Formato de Etiquetas

### Etiquetas Estáticas

En cualquier celda de Excel:
```
{{EMPRESA}}
{{RUC}}
{{FECHA_AUDITORIA}}
```

### Etiquetas IA

En cualquier celda de Excel:
```
{{IA:HALLAZGO_9001}}
{{IA:CONCLUSION_GENERAL}}
{{IA:EVIDENCIA_CLAUSULA_4_1}}
```

## Configuración en DATA.xlsx

| Campo | Valor | Campo Generado |
|-------|-------|----------------|
| EMPRESA | ACME Corp | {{EMPRESA}} |
| RUC | 12345678 | {{RUC}} |
| HALLAZGO_9001 | Genera un hallazgo... | {{IA:HALLAZGO_9001}} |

## Salida

El script genera:
- **Excel procesados** en `3. Inyectado/`
- **MEMORIA_plantilla.txt** con historial de respuestas IA
- **CONTEXTO_IA_EXCEL.txt** con el prompt completo enviado a la IA

## Diferencias con inyectar_word.py

| Característica | Word | Excel |
|----------------|------|-------|
| Procesa | Párrafos y tablas | Celdas |
| Formato | Mantiene estilos Word | Mantiene formato Excel |
| Múltiples hojas | N/A | ✅ Sí |
| Fórmulas | N/A | Se preservan |

## Notas

- Las plantillas Excel deben empezar con `_` (ej: `_plantilla.xlsx`)
- El script ignora archivos temporales de Excel (`~$*.xlsx`)
- Las fórmulas de Excel se preservan si no contienen etiquetas
- El procesamiento es celda por celda, hoja por hoja

## Ejemplo de Uso

1. Crea `_checklist_auditoria.xlsx` en `2. Plantilla/`
2. En una celda escribe: `Empresa: {{EMPRESA}}`
3. En otra celda: `{{IA:HALLAZGO_9001}}`
4. Ejecuta: `python3 inyectar_excel.py`
5. Revisa el resultado en `3. Inyectado/checklist_auditoria.xlsx`

## Troubleshooting

**Error: "No se encontraron plantillas"**
- Verifica que los archivos estén en `2. Plantilla/`
- Asegúrate que sean `.xlsx`

**Error: "GEMINI_API_KEY no encontrada"**
- Configura tu API key en `.env`

**Las fórmulas no funcionan**
- Las fórmulas se preservan si no contienen etiquetas
- Si una celda tiene fórmula + etiqueta, se convierte a texto
