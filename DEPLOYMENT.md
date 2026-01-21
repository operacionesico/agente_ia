# Deployment en Streamlit Cloud

## Pasos para Desplegar

### 1. Preparar Repositorio GitHub
✅ Ya completado - El código está en: `https://github.com/shell038/agente_ia.git`

### 2. Crear Cuenta en Streamlit Cloud
1. Ve a https://share.streamlit.io
2. Inicia sesión con tu cuenta de GitHub
3. Autoriza a Streamlit a acceder a tus repositorios

### 3. Desplegar la Aplicación
1. Click en "New app"
2. Selecciona:
   - **Repository:** `shell038/agente_ia`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click en "Advanced settings..."
4. En **Secrets**, agrega:
   ```toml
   GEMINI_API_KEY = "tu_api_key_de_gemini_aqui"
   ```
5. Click en "Deploy!"

### 4. Configurar Autenticación (Opcional)
Para restringir acceso a usuarios específicos:

1. En el dashboard de tu app, ve a "Settings" → "Sharing"
2. Selecciona "Restrict viewing to specific people"
3. Agrega los emails autorizados (máximo 10 usuarios)

### 5. URL de la Aplicación
Una vez desplegada, tu app estará disponible en:
```
https://[nombre-app].streamlit.app
```

## Prueba Local (Antes de Desplegar)

```bash
# Asegúrate de tener .env con GEMINI_API_KEY
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

## Actualizar la Aplicación

Cada vez que hagas `git push` a la rama `main`, Streamlit Cloud automáticamente redesplega la app.

## Solución de Problemas

### Error: "GEMINI_API_KEY not found"
- Verifica que agregaste el secret en Streamlit Cloud
- El nombre debe ser exactamente `GEMINI_API_KEY`

### Error: "Module not found"
- Verifica que `requirements.txt` esté actualizado
- Streamlit Cloud instala automáticamente las dependencias

### App muy lenta
- Considera actualizar a Streamlit Cloud Team ($20/mes)
- O migrar a Railway/Render para más recursos

## Límites del Plan Gratuito

- **RAM:** 1GB
- **CPU:** Compartida
- **Usuarios concurrentes:** ~3-5 procesando simultáneamente
- **Apps privadas:** 1
- **Apps públicas:** Ilimitadas

## Contacto

Si tienes problemas con el deployment, contacta al administrador del repositorio.
