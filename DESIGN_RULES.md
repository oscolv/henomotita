# DESIGN_RULES.md — henomotita.mx

> Este archivo es contexto obligatorio para cualquier prompt que modifique
> el frontend de henomotita.mx. Incluirlo en cada sesión de Claude Code
> con `--file DESIGN_RULES.md` o pegarlo al inicio del chat.

---

## 1. Identidad establecida — NO cambiar

El sitio ya tiene un sistema de diseño con personalidad. Estas decisiones están
tomadas y no se tocan:

| Elemento          | Valor                                                    |
|-------------------|----------------------------------------------------------|
| Paleta            | `--papel: #F5F1E8`, `--tinta: #1A1611`, `--caliza: #D4CFC4`, `--corteza: #6B5B47`, `--heno-seco: #B8965A`, `--mezquite-oscuro: #2F3E1F`, `--terracota: #A0541A` |
| Tipografía título | Source Serif 4 (serif editorial)                         |
| Tipografía cuerpo | Inter (sans-serif legible)                               |
| Tipografía código | JetBrains Mono (etiquetas, datos, labels)                |
| Bordes            | Siempre `border-radius: 0`. Sin esquinas redondeadas.    |
| Sombras           | Ninguna. Cero `box-shadow`.                              |
| Gradientes        | Ninguno.                                                 |
| Textura           | Solo la textura de papel sutil en `body::before`.        |
| Tono visual       | Guía de campo / cuaderno de naturalista / editorial seco |

**Si un prompt pide "modernizar", "refrescar" o "hacer más atractivo", la respuesta
es mejorar la composición y la jerarquía, NUNCA cambiar colores ni tipografías.**

---

## 2. Problemas actuales a corregir

Estos son los patrones que delatan al sitio como generado por IA. Cualquier
modificación debe reducirlos, no amplificarlos.

### 2.1 Sobre-sistematización de secciones

**Problema:** Todas las secciones siguen la misma estructura exacta:
`sh-eyebrow` → `h2` → `sh-lead` → `sh-rule` → contenido en grid.

**Regla:** Variar la entrada de cada sección. Alternativas válidas:
- Sección que abre directamente con contenido (sin eyebrow ni lead).
- Sección con título alineado a la derecha o en columna lateral.
- Sección que usa solo un bloque de texto corrido, sin grid.
- Sección donde el título está integrado al primer párrafo, no separado.

**Prohibido:** Que más de 2 secciones consecutivas tengan la misma estructura
de header.

### 2.2 Exceso de variantes de componente

**Problema:** Existen 12+ tipos de "caja con borde" (`field-card`, `error-card`,
`campaign-card`, `ficha-fuente`, `calendario-fenologico`, `nota-campo`,
`ficha-tecnica`, `stat-highlight`, `warning-box`, `tip-box`, `inset-box`,
`field-alert`). Un diseñador humano tendría 3 o 4.

**Regla:** Antes de crear un componente nuevo, verificar si alguno existente
sirve con una clase modificadora. Si no se puede resolver con los existentes,
justificar por escrito en un comentario CSS por qué el nuevo es necesario.

**Componentes base permitidos:**
- `.field-card` — bloque de contenido estándar (con variantes por border-top color)
- `.nota-campo` — aside informativo (border-left)
- `.field-alert` — advertencia importante (rojo)
- `.ficha-tecnica` — datos estructurados (border completo)

Todo lo demás debe derivar de estos cuatro.

### 2.3 CSS inflado y repetitivo

**Problema:** `font-family: 'JetBrains Mono', ui-monospace, monospace` aparece
~20 veces. Lo mismo con stacks tipográficos de Source Serif e Inter.

**Regla:** Usar clases utilitarias para tipografía:
```css
.mono  { font-family: 'JetBrains Mono', ui-monospace, monospace; }
.serif { font-family: 'Source Serif 4', Georgia, serif; }
.sans  { font-family: 'Inter', system-ui, sans-serif; }
```
Aplicarlas en HTML en lugar de repetir el stack en cada regla CSS.

Mismo principio para patrones recurrentes de labels:
```css
.label-upper {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
```

### 2.4 Exceso de etiquetas decorativas

**Problema:** Cada card tiene un eyebrow, cada sección un badge, cada bloque
un label en monospace uppercase. Todo está etiquetado.

**Regla:** Las etiquetas son para cuando aportan información que el lector
necesita (tipo de fuente en referencias, nivel de alerta, categoría). Si la
etiqueta solo dice lo que el título ya dice, eliminarla.

**Máximo:** 1 etiqueta decorativa por cada 3 componentes en pantalla.

### 2.5 Espaciado uniforme entre secciones

**Problema:** Todas las secciones usan el mismo padding (`4.5rem` desktop,
`2.75rem` mobile). El ritmo visual es monótono.

**Regla:** Variar el espaciado según la función de la sección:

| Tipo de sección              | Padding desktop | Padding mobile |
|------------------------------|-----------------|----------------|
| Hero / portada               | `6rem` a `8rem` | `3.5rem`       |
| Contenido denso (FAQ, tabs)  | `3.5rem`        | `2rem`         |
| Sección estándar             | `5rem`          | `3rem`         |
| CTA / Únete                  | `6rem`          | `4rem`         |
| Transición (dato destacado)  | `3rem`          | `2rem`         |

---

## 3. Reglas de composición

### Layout

- No todas las secciones necesitan un grid. El texto corrido con `max-width: 65ch`
  es una herramienta válida y subutilizada.
- Al menos una sección debe romper el contenedor de 1120px (full-bleed) para
  crear variación visual.
- Las imágenes no siempre van dentro de `<figure>` con caption. A veces una
  imagen a sangre completa comunica mejor.

### Tipografía

- Los títulos `h2` no necesitan ser todos del mismo tamaño. Un título corto
  puede ser más grande; uno largo, más pequeño. Usar `clamp()` con rangos
  diferentes.
- El texto corrido puede usar Source Serif 4 (no solo Inter). La serif en
  cuerpo refuerza el tono editorial.
- Evitar que más de 3 elementos visibles al mismo tiempo usen JetBrains Mono.
  El monospace es un acento, no el tono dominante.

### Color

- El `--terracota` es el color de acento. Usarlo con moderación: máximo 3
  elementos por pantalla visible.
- El `--mezquite-oscuro` funciona como "negro suave" para títulos y énfasis.
  No usarlo como fondo extenso (excepto en tabs y footer).
- Cuando una sección necesita contraste, usar `--papel-alt` como fondo, no
  inventar nuevos colores.

### Interacción

- Los hover effects actuales son correctos (cambio de color de borde, no
  transformaciones 3D ni sombras).
- No agregar animaciones de entrada (fade-in, slide-up) a más de 3 secciones.
  El `.reveal` actual es suficiente y debe usarse con moderación.
- Los estados `:focus-visible` deben existir en todo elemento interactivo.

---

## 4. Prohibiciones absolutas

Estas cosas NUNCA deben aparecer en el código, sin importar lo que pida el prompt:

1. `border-radius` mayor a `2px` en cualquier elemento.
2. `box-shadow` en cualquier componente (excepto `0 0 0 Xpx` para focus rings).
3. Gradientes de cualquier tipo (`linear-gradient`, `radial-gradient`).
4. Íconos de Lucide, Heroicons, o cualquier librería de íconos SVG genéricos.
   Los íconos actuales son emoji y deben seguir siéndolo, o ser SVGs custom.
5. Colores fuera de las CSS variables definidas en `:root`.
6. Fuentes distintas a Source Serif 4, Inter y JetBrains Mono.
7. Clases con nombres genéricos (`card`, `container`, `wrapper`, `section`
   sin prefijo contextual).
8. Más de 15 líneas de CSS nuevo sin eliminar al menos 10 líneas existentes.
9. Componentes que dupliquen la función de uno existente.
10. `!important` (excepto en los overrides de navegación móvil ya existentes).

---

## 5. Checklist antes de cada commit

Antes de aceptar código generado, verificar:

- [ ] ¿Alguna sección nueva repite la estructura eyebrow → h2 → lead → rule?
      Si sí, cambiar la estructura.
- [ ] ¿Se creó un componente CSS nuevo? ¿Puede resolverse con uno existente
      más una clase modificadora?
- [ ] ¿El CSS nuevo repite un stack tipográfico en lugar de usar `.mono`,
      `.serif` o `.sans`?
- [ ] ¿Hay más de 3 labels/badges/eyebrows visibles al mismo tiempo en
      cualquier viewport?
- [ ] ¿Todas las secciones tienen el mismo padding? Variar según la tabla
      de la sección 2.5.
- [ ] ¿Se agregaron sombras, gradientes o border-radius? Revertir.
- [ ] ¿El HTML resultante pasa el test de "¿esto lo haría un humano o solo
      un LLM"? Si todo está perfectamente simétrico y etiquetado, algo falta.

---

## 6. Cómo usar este archivo

### En Claude Code (terminal)
```bash
claude --file DESIGN_RULES.md "Agrega una sección de galería de fotos al sitio"
```

### En claude.ai (chat)
Pegar el contenido completo al inicio del prompt, seguido de la instrucción.

### En un system prompt de proyecto
Agregar como archivo de contexto del proyecto en Claude para que se aplique
automáticamente a cada conversación.

---

*Última actualización: mayo 2026*
*Sitio: henomotita.mx — Control y prevención del heno motita en el Valle del Mezquital*
