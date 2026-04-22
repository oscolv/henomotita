# henomotita.mx

Sitio web de referencia para el control y prevención del heno motita (*Tillandsia recurvata*) en el Valle del Mezquital, Hidalgo, México.

## Estructura del proyecto

```
index.html                    Sitio completo (una sola página, diez secciones)
ZRE.png                       Mapa oficial de la Zona de Restauración Ecológica (DOF 26/09/2024)
gen_taller.py                 Generador de PDF para talleres de capacitación (ReportLab)
taller-01-heno-motita.pdf     Taller 1: Primera campaña de control (30 min, 5 módulos + ZRE)
wrangler.toml                 Configuración de Cloudflare Workers
_headers                      Cabeceras de seguridad (CSP, X-Frame-Options, etc.)
_redirects                    Redirecciones URL para Cloudflare Pages
.github/workflows/deploy.yml  Despliegue automático vía GitHub Actions
```

## Secciones del sitio

| Sección | Contenido |
|---------|-----------|
| Inicio | Presentación y llamada a la acción |
| ¿Qué es? | Biología de *T. recurvata*, rol dual epífito/parásito |
| El problema | Escala del daño, hospederos afectados, dispersión |
| Decreto ZRE | Zona de Restauración Ecológica Presa Endhó (DOF 26/09/2024) |
| Métodos de control | Protocolos mecánico, químico y combinado |
| Prevención | Manejo integrado, ventana óptima enero–abril |
| Errores comunes | Mitos y errores que hacen fracasar una campaña |
| Preguntas frecuentes | FAQ para brigadistas y ciudadanos |
| Únete | Formulario de inscripción a brigadas de control |
| Referencias | Fuentes científicas e institucionales |

## Despliegue

El sitio se despliega automáticamente en Cloudflare Workers cada vez que se hace `git push` a la rama `main`, usando el workflow `.github/workflows/deploy.yml`.

**Requisito:** el secreto `CLOUDFLARE_API_TOKEN` debe estar configurado en GitHub → Settings → Secrets and variables → Actions.

Para despliegue manual desde terminal:

```bash
npx wrangler deploy
```

## Formulario de contacto

El formulario usa [FormSubmit.co](https://formsubmit.co) sin backend propio. El endpoint está configurado en `index.html`:

```js
var FORM_ENDPOINT = 'https://formsubmit.co/ajax/...';
```

La primera vez que alguien envía el formulario, FormSubmit envía un correo de verificación al destinatario. Una vez confirmado, los envíos llegan automáticamente. No se requiere cuenta ni servidor.

## Talleres de capacitación

El archivo `gen_taller.py` genera PDFs de talleres usando [ReportLab](https://www.reportlab.com/). Requiere Python 3 y el paquete `reportlab`:

```bash
pip install reportlab
python3 gen_taller.py
```

Genera `taller-01-heno-motita.pdf` con 6 páginas:
- Portada con tabla de módulos
- Módulo 1: El problema (qué es y cuándo es dañino)
- Módulo 2: Evaluar la infestación
- Módulo 3: Métodos de control (mecánico, bicarbonato, poda)
- Módulo 4: Errores comunes
- Módulo 5: Plan de acción / organizar la brigada
- Módulo ZRE: Decreto federal y alcance de la Zona de Restauración Ecológica

## Marco normativo

El sitio incluye una sección dedicada al **Decreto de Zona de Restauración Ecológica de la Presa Endhó** (DOF 26/09/2024), que declara 36,637 ha del Valle del Mezquital como ZRE y nombra explícitamente al heno motita como especie invasora de control obligatorio en 8 municipios:

Atitalaquia · Atotonilco de Tula · Tepeji del Río · Tepetitlán · Tezontepec de Aldama · Tlahuelilpan · Tlaxcoapan · Tula de Allende

## Fuentes científicas

El contenido está basado en artículos revisados por pares, documentos de CONAFOR, INIFAP, SEMARNAT y estudios de la Universidad Tecnológica Tula-Tepeji (UTTT), la UNAM y la UAEH. Las referencias completas se listan en la sección "Referencias" del sitio.

## Licencia

Contenido de libre acceso para uso educativo y de divulgación científica.
