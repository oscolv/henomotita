# henomotita.mx

Sitio web de referencia para el control y prevención del heno motita (*Tillandsia recurvata*) en el Valle del Mezquital, Hidalgo, México.

## Estructura

```
index.html        Sitio completo (una sola página, todas las secciones)
_headers          Cabeceras de seguridad para Cloudflare Pages
_redirects        Redirecciones URL para Cloudflare Pages
```

## Antes de publicar — pasos obligatorios

### 1. Conectar el formulario de contacto

En `index.html`, busca esta línea (aprox. línea 2016):

```js
var FORM_ENDPOINT = 'https://formsubmit.co/ajax/REEMPLAZA_CON_TU_CORREO@dominio.com';
```

Reemplaza `REEMPLAZA_CON_TU_CORREO@dominio.com` con el correo donde quieres recibir las inscripciones a brigadas. Ejemplo:

```js
var FORM_ENDPOINT = 'https://formsubmit.co/ajax/henomotita@correo.com';
```

La primera vez que alguien llene el formulario, FormSubmit te enviará un correo de verificación. Cuando lo confirmes, todos los envíos futuros llegarán automáticamente. No se necesita cuenta ni configuración adicional.

### 2. Despliegue en Cloudflare Pages

1. Sube este repositorio a GitHub (cuenta gratuita)
2. Entra a [pages.cloudflare.com](https://pages.cloudflare.com)
3. Clic en **Create a project** → **Connect to Git**
4. Selecciona este repositorio
5. Configuración de build:
   - **Framework preset**: None
   - **Build command**: (vacío — no requiere compilación)
   - **Build output directory**: `/` (barra diagonal solamente)
6. Clic en **Save and Deploy**

### 3. Conectar el dominio henomotita.mx

En el panel de Cloudflare Pages (después del despliegue):

1. Ve a tu proyecto → **Custom domains**
2. Clic en **Set up a custom domain**
3. Escribe `henomotita.mx`
4. Cloudflare te dará los registros DNS para configurar en NIC México

En NIC México (panel de administración del dominio):
- Cambiar los **nameservers** a los que te indique Cloudflare, o
- Agregar los registros CNAME que Cloudflare especifique

### 4. Despliegue automático

Una vez conectado, cada vez que hagas `git push` al repositorio, Cloudflare Pages desplegará automáticamente los cambios en 1–2 minutos.

## Contenido científico

El contenido está basado en artículos científicos revisados por pares, documentos de CONAFOR, INIFAP, y estudios de la UTTT (Universidad Tecnológica Tula-Tepeji). Las referencias se listan en la sección "Referencias" del sitio.

## Licencia

Contenido de libre acceso para uso educativo y de divulgación científica.
