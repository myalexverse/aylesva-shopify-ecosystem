# Handoff para Claude Code — Sección Shopify "Aylesva China"

> Instrucciones para que Claude Code suba esta sección a la tienda Shopify del usuario.
> El usuario habla español; puedes responderle en español.

## Qué es esto

`sections/aylesva-china.liquid` es una **sección de Shopify de producción, ya terminada y validada** (NO es un prototipo a reescribir). Incluye su bloque `{% schema %}` completo con settings, blocks y un `preset` por defecto. Solo hay que colocarla en el tema y publicarla.

- Liquid + HTML + CSS + JS mínimo, todo autocontenido en un único archivo.
- Estilos con scope `#aylesva-{{ section.id }}` → no choca con el resto del tema.
- Fuente Manrope vía Google Fonts (cargada dentro de la sección).
- Compatible con **Translate & Adapt** (todo el texto vive en settings/blocks).

## Tarea

Instalar el archivo `sections/aylesva-china.liquid` en el tema Shopify del usuario y dejarlo disponible en el Theme Customizer como sección **"Aylesva China"**.

## Opción 1 — Shopify CLI (recomendada para deploy)

Requisitos: Node 18+, Shopify CLI (`npm i -g @shopify/cli @shopify/theme`) y acceso a la tienda.

```bash
# 1. Clonar/descargar el tema vivo a una carpeta local
shopify theme pull --store TIENDA.myshopify.com   # p.ej. aylesva.myshopify.com

# 2. Copiar la sección dentro del tema
cp sections/aylesva-china.liquid <carpeta-del-tema>/sections/aylesva-china.liquid

# 3. Previsualizar en local antes de publicar
shopify theme dev --store TIENDA.myshopify.com
#   -> abre la preview, añade la sección desde "Add section → Aylesva China"

# 4. Subir SOLO ese archivo a un tema (sin sobreescribir todo el tema)
shopify theme push --only sections/aylesva-china.liquid --store TIENDA.myshopify.com
#   Recomendado: pushear primero a un tema NO publicado (development/duplicate) y revisar.
```

Notas:
- `shopify theme push` sin `--only` sube todo el directorio; usa `--only` para tocar solo esta sección.
- Para no arriesgar el tema en vivo: `shopify theme push --unpublished` crea un tema nuevo donde probar, luego se publica desde el admin.

## Opción 2 — Sin CLI (editor de código del admin)

1. Shopify admin → **Online Store → Themes → ⋯ → Edit code**.
2. Carpeta **Sections** → **Add a new section** → nombre `aylesva-china`.
3. Borrar el contenido generado y pegar el de `sections/aylesva-china.liquid`. **Save**.

## Cómo usarla después de instalarla

- Theme Customizer → **Add section → "Aylesva China"**.
- Aparece con todo el contenido por defecto (logo de texto, imágenes placeholder de Unsplash, 5 tarjetas, 4 pasos, banner, 8 oportunidades, formulario, disclaimer).
- Todo es editable: logo (imagen/ancho 100–300px/alineación/toggle en hero), colores, títulos, descripciones, botones, imágenes (subida **o** URL externa), bloques repetibles (trust, imágenes del collage, tarjetas, pasos, oportunidades).

## Detalles importantes

- **Botones de tarjeta**: por defecto dicen "Request Information" y hacen scroll suave a la sección del formulario. Si en el editor se rellena "Button link", ese enlace tiene prioridad; dejarlo vacío mantiene el scroll al formulario.
- **Formulario**: usa el formulario de contacto nativo de Shopify (`{% form 'contact' %}`). La subida de imagen del producto NO se adjunta por correo de forma nativa en Shopify. Si el cliente necesita adjuntos, usar el setting **"Custom form embed code"** con un servicio externo (Typeform, HubSpot, etc.) — ese embed reemplaza el formulario nativo.
- **Colores de marca**: Navy `#0B1F3A`, Rojo `#D62828`, Gris claro `#F7F8FA`, Blanco `#FFFFFF` (editables como settings).

## Archivos en este paquete

- `sections/aylesva-china.liquid` — la sección lista para subir.
