# SISTEMA RAG - Información Empresarial

## ¿Qué hace?

El sistema lee **automáticamente** cualquier documento que coloques en la carpeta `4. INFORMACION EMPRESA/` y usa su contenido como contexto para generar respuestas más realistas con la IA.

## Tipos de archivos soportados

- ✅ **PDF** (.pdf)
- ✅ **Word** (.docx)
- ✅ **Excel** (.xlsx)
- ✅ **Texto plano** (.txt)

## Cómo usar

### 1. Coloca archivos en la carpeta

```
4. INFORMACION EMPRESA/
├── Ficha_RUC.pdf
├── Alcance_SIG.docx
├── Lista_Proyectos.xlsx
└── cualquier_otro_archivo.txt
```

**No importa el nombre de los archivos**, el sistema lee TODO lo que encuentre.

### 2. Ejecuta el script

```bash
python3 inyectar_word.py
```

### 3. La IA usa automáticamente esa información

**Ejemplo de lo que genera:**

**SIN información adicional:**
```
"La empresa auditada demuestra cumplimiento de la cláusula 6.1..."
```

**CON** información adicional:
```
"ICOCERT SAC (RUC: 20613997025), bajo la dirección del Gerente General 
Edson Pérez López, demuestra cumplimiento de la cláusula 6.1. Se evidenció 
en el proyecto de certificación ISO 9001 para ORPIZA que..."
```

## Ventajas

- ✅ **Automático**: Solo dejas archivos y funciona
- ✅ **Flexible**: Archivos con cualquier nombre
- ✅ **Realista**: La IA menciona proyectos, personas, datos reales
- ✅ **Coherente**: Todo cuadra con la información de la empresa

## Recomendaciones

### Archivos útiles:

1. **Ficha RUC** (PDF/Word):
   - Nombre, RUC, gerente, actividad económica

2. **Alcance del Sistema** (Word/PDF):
   - A qué se dedica la empresa
   - Qué servicios presta

3. **Lista de Proyectos/Obras** (Excel):
   - Proyectos ejecutados
   - Clientes atendidos

4. **Organigrama** (PDF):
   - Estructura organizacional
   - Nombres de jefes/responsables

5. **Manual de Calidad/SST** (PDF/Word):
   - Políticas, objetivos
   - Procesos principales

### Límite de contenido:

- Gemini 2.0 tiene límite de ~32,000 tokens de entrada
- Aproximadamente **20-30 páginas de texto**
- Si tienes documentos muy largos, el sistema los incluirá pero pueden cortarse

### Entre auditorías:

**IMPORTANTE**: Limpia la carpeta antes de cada auditoría nueva o la información se mezclará.

```bash
# Borrar archivos anteriores
rm -f "4. INFORMACION EMPRESA"/*

# O mueve a una subcarpeta
mv "4. INFORMACION EMPRESA"/*.* "4. INFORMACION EMPRESA/ARCHIVO_EMPRESA_ANTERIOR/"
```

## Prueba

Ejecuta:
```bash
python3 lector_informacion.py
```

Verás el contenido extraído de todos los archivos.
