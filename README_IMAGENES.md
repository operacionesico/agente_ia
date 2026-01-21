# INSERCIÓN DE IMÁGENES EN DOCUMENTOS

## ✅ Funcionalidad Implementada

Ahora puedes insertar imágenes en tus documentos Word usando etiquetas.

## 📁 Estructura

```
5. IMAGENES/
├── firma_auditor.png
├── logo_empresa.png
└── cualquier_imagen.jpg
```

## 📝 Cómo Usar

### 1. Guardar imagen en carpeta
Coloca la imagen en `5. IMAGENES/`

### 2. Configurar en Excel

| Campo | Valor | Campo Generado |
|-------|-------|----------------|
| FIRMA_AUDITOR | firma_auditor.png | {{FIRMA_AUDITOR}} |

### 3. Usar en Word

**Insertar imagen en text:**
```
Auditor: {{AUDITOR_LIDER}}
Firma: {{IMG:FIRMA_AUDITOR}}
```

**En tabla:**
```
┌─────────────────┐
│ Nombre: Juan    │
│ {{IMG:FIRMA}}   │ ← Imagen aquí
└─────────────────┘
```

## ⚙️ Configuración

**Tamaño predeterminado:** 2 pulgadas de ancho
**Formatos soportados:** .png, .jpg, .jpeg, .gif, .bmp

## 📊 Ejemplo Completo

**Excel:**
```
AUDITOR_LIDER = "Juan Pérez"
FIRMA_AUDITOR = "firma_juan.png"
```

**Word:**
```
Auditor Líder: {{AUDITOR_LIDER}}
{{IMG:FIRMA_AUDITOR}}
```

**Resultado:**
```
Auditor Líder: Juan Pérez
[Imagen de firma insertada aquí]
```

## ⚠️  Importante

- El nombre del archivo debe coincidir exactamente (mayúsculas/minúsculas)
- La imagen debe estar en `5. IMAGENES/`
- Si la imagen no se encuentra, aparecerá una advertencia en la consola
