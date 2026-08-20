"""
=============================================================
Transferir imágenes de Global States: aylesva.COM → aylesva.MX
=============================================================
1. Descarga imágenes del CDN público de aylesva.com
2. Las sube al Files de aylesva.mx via GraphQL stagedUploads
3. Actualiza page.globalstates.json con las nuevas refs
4. Empuja el template al tema activo
=============================================================
"""
import os
import sys
import json
import time
import mimetypes
import requests
import urllib3
from pathlib import Path
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

# ── Credenciales aylesva.MX ──────────────────────────────
SHOP       = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
TOKEN      = os.getenv("ACCESS_TOKEN")
API_VER    = os.getenv("API_VERSION", "2025-01")
THEME_ID   = os.getenv("THEME_ID", "172455165975")
REST_BASE  = f"https://{SHOP}/admin/api/{API_VER}"
GQL_URL    = f"https://{SHOP}/admin/api/{API_VER}/graphql.json"
HEADERS    = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# ── Directorio temporal para imágenes ────────────────────
DL_DIR = Path(__file__).parent / "globalstates_images"
DL_DIR.mkdir(exist_ok=True)

# ── Imágenes a transferir ────────────────────────────────
# (nombre_local, URL_publica_aylesva_com, uso)
IMAGES = [
    ("heroimage.png",        "https://www.aylesva.com/cdn/shop/files/heroimage.png",        "hero_image"),
    ("mapofmexico.jpg",      "https://www.aylesva.com/cdn/shop/files/mapofmexico.jpg",      "map_image"),
    # Paradise Bay
    ("paradisebay1.png",     "https://www.aylesva.com/cdn/shop/files/paradisebay1.png",     "paradise_img1"),
    ("paradisebay2.png",     "https://www.aylesva.com/cdn/shop/files/paradisebay2.png",     "paradise_img2"),
    ("paradisebay3.png",     "https://www.aylesva.com/cdn/shop/files/paradisebay3.png",     "paradise_img3"),
    ("paradisebay4.png",     "https://www.aylesva.com/cdn/shop/files/paradisebay4.png",     "paradise_img4"),
    # Torre 40
    ("foorplantorre40.jpg",  "https://www.aylesva.com/cdn/shop/files/foorplantorre40.jpg",  "torre40_floorplan"),
    ("ameneties.png",        "https://www.aylesva.com/cdn/shop/files/ameneties.png",        "torre40_amenities"),
    ("en_construcion.png",   "https://www.aylesva.com/cdn/shop/files/en_construcion.png",   "torre40_construction"),
    ("torre40gallery.png",   "https://www.aylesva.com/cdn/shop/files/torre40gallery.png",   "torre40_gallery"),
    # Altarena
    ("altarema1.png",        "https://www.aylesva.com/cdn/shop/files/altarema1.png",        "altarena_img1"),
    ("Altarena2.png",        "https://www.aylesva.com/cdn/shop/files/Altarena2.png",        "altarena_img2"),
    ("altarena3.webp",       "https://www.aylesva.com/cdn/shop/files/altarena3.webp",       "altarena_img3"),
    ("altanera5.jpg",        "https://www.aylesva.com/cdn/shop/files/altanera5.jpg",        "altarena_img4"),
]

# ══════════════════════════════════════════════════════════
# PASO 1 — Descargar imágenes del CDN público
# ══════════════════════════════════════════════════════════
def download_images():
    print("\n" + "="*60)
    print("PASO 1: Descargando imágenes de aylesva.com...")
    print("="*60)
    for fname, url, usage in IMAGES:
        dest = DL_DIR / fname
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"  ✅ Ya existe: {fname} ({dest.stat().st_size:,} bytes)")
            continue
        print(f"  ⬇ Descargando {fname}...", end=" ", flush=True)
        try:
            r = requests.get(url, verify=False, timeout=60, headers={
                "User-Agent": "Mozilla/5.0"
            })
            if r.status_code == 200 and len(r.content) > 500:
                dest.write_bytes(r.content)
                print(f"✅ ({len(r.content):,} bytes)")
            else:
                print(f"❌ HTTP {r.status_code} ({len(r.content)} bytes)")
        except Exception as e:
            print(f"❌ Error: {e}")
    print()

# ══════════════════════════════════════════════════════════
# PASO 2 — Subir imágenes a aylesva.MX via GraphQL
# ══════════════════════════════════════════════════════════
def gql(query, variables=None):
    """Helper para ejecutar queries GraphQL."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(GQL_URL, json=payload, headers=HEADERS, verify=False, timeout=60)
    if r.status_code != 200:
        print(f"  ❌ GraphQL HTTP {r.status_code}: {r.text[:300]}")
        return None
    data = r.json()
    if "errors" in data:
        print(f"  ❌ GraphQL errors: {json.dumps(data['errors'], indent=2)[:500]}")
        return None
    return data.get("data")

def get_mime(fname):
    ext = Path(fname).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return mime_map.get(ext, "application/octet-stream")

def upload_images():
    print("\n" + "="*60)
    print("PASO 2: Subiendo imágenes a aylesva.mx...")
    print("="*60)
    
    uploaded = {}  # fname -> shopify://shop_images/fname
    
    for fname, _url, usage in IMAGES:
        local_path = DL_DIR / fname
        if not local_path.exists():
            print(f"  ⚠ Archivo no encontrado: {fname}, saltando...")
            continue
        
        file_size = local_path.stat().st_size
        mime = get_mime(fname)
        
        print(f"\n  📤 Subiendo {fname} ({file_size:,} bytes)...")
        
        # Paso 2a: Crear staged upload
        staged_query = """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters {
                name
                value
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        staged_vars = {
            "input": [{
                "resource": "FILE",
                "filename": fname,
                "mimeType": mime,
                "fileSize": str(file_size),
                "httpMethod": "POST"
            }]
        }
        
        data = gql(staged_query, staged_vars)
        if not data:
            print(f"    ❌ Error al crear staged upload para {fname}")
            continue
        
        staged = data.get("stagedUploadsCreate", {})
        user_errors = staged.get("userErrors", [])
        if user_errors:
            print(f"    ❌ Errores: {user_errors}")
            continue
        
        targets = staged.get("stagedTargets", [])
        if not targets:
            print(f"    ❌ No se obtuvo staged target")
            continue
        
        target = targets[0]
        upload_url = target["url"]
        resource_url = target["resourceUrl"]
        params = {p["name"]: p["value"] for p in target["parameters"]}
        
        print(f"    → Staged URL obtenido, subiendo archivo...")
        
        # Paso 2b: Subir el archivo
        with open(local_path, "rb") as fh:
            files_payload = {k: (None, v) for k, v in params.items()}
            files_payload["file"] = (fname, fh, mime)
            
            upload_r = requests.post(upload_url, files=files_payload, verify=False, timeout=120)
        
        if upload_r.status_code not in [200, 201, 204]:
            # Some staged uploads return XML with redirect
            if upload_r.status_code in [301, 302, 303]:
                print(f"    → Redirect {upload_r.status_code}, siguiendo...")
            else:
                print(f"    ❌ Upload HTTP {upload_r.status_code}: {upload_r.text[:200]}")
                continue
        
        print(f"    → Archivo subido, registrando en Shopify...")
        
        # Paso 2c: Registrar el archivo en Shopify
        file_create_query = """
        mutation fileCreate($files: [FileCreateInput!]!) {
          fileCreate(files: $files) {
            files {
              id
              alt
              createdAt
              ... on MediaImage {
                image {
                  url
                }
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        file_create_vars = {
            "files": [{
                "originalSource": resource_url,
                "contentType": "IMAGE",
                "alt": f"Global States - {usage}"
            }]
        }
        
        data = gql(file_create_query, file_create_vars)
        if not data:
            print(f"    ❌ Error al registrar archivo {fname}")
            continue
        
        fc = data.get("fileCreate", {})
        fc_errors = fc.get("userErrors", [])
        if fc_errors:
            print(f"    ❌ Errores: {fc_errors}")
            continue
        
        files_created = fc.get("files", [])
        if files_created:
            file_id = files_created[0].get("id", "")
            print(f"    ✅ Registrado: {file_id}")
            # La referencia para image_picker es shopify://shop_images/filename
            uploaded[fname] = f"shopify://shop_images/{fname}"
        
        # Pequeña pausa para no saturar la API
        time.sleep(0.5)
    
    return uploaded

# ══════════════════════════════════════════════════════════
# PASO 3 — Actualizar template page.globalstates.json
# ══════════════════════════════════════════════════════════
def update_template(uploaded):
    print("\n" + "="*60)
    print("PASO 3: Actualizando template page.globalstates.json...")
    print("="*60)
    
    template_path = Path(__file__).parent / "theme" / "templates" / "page.globalstates.json"
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    settings = template["sections"]["main"]["settings"]
    blocks = template["sections"]["main"]["blocks"]
    
    # Hero image
    if "heroimage.png" in uploaded:
        settings["hero_image"] = uploaded["heroimage.png"]
        print("  ✅ Hero image configurado")
    
    # Map image
    if "mapofmexico.jpg" in uploaded:
        settings["map_image"] = uploaded["mapofmexico.jpg"]
        print("  ✅ Map image configurado")
    
    # Paradise Bay images (block: proj_paradise_bay)
    pb = blocks.get("proj_paradise_bay", {}).get("settings", {})
    paradise_imgs = [
        ("paradisebay1.png", "image_1"),
        ("paradisebay2.png", "image_2"),
        ("paradisebay3.png", "image_3"),
        ("paradisebay4.png", "image_4"),
    ]
    for fname, key in paradise_imgs:
        if fname in uploaded:
            pb[key] = uploaded[fname]
            print(f"  ✅ Paradise Bay {key} configurado")
    
    # Torre 40 images (block: proj_torre_40)
    t40 = blocks.get("proj_torre_40", {}).get("settings", {})
    torre40_imgs = [
        ("foorplantorre40.jpg", "image_2"),
        ("ameneties.png", "image_3"),
        ("torre40gallery.png", "image_4"),
        ("en_construcion.png", "image_5"),
    ]
    for fname, key in torre40_imgs:
        if fname in uploaded:
            t40[key] = uploaded[fname]
            print(f"  ✅ Torre 40 {key} configurado")
    
    # Altarena images (block: proj_altarena)
    alt = blocks.get("proj_altarena", {}).get("settings", {})
    altarena_imgs = [
        ("altarema1.png", "image_1"),
        ("Altarena2.png", "image_2"),
        ("altarena3.webp", "image_3"),
        ("altanera5.jpg", "image_4"),
    ]
    for fname, key in altarena_imgs:
        if fname in uploaded:
            alt[key] = uploaded[fname]
            print(f"  ✅ Altarena {key} configurado")
    
    # Guardar template actualizado
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"\n  💾 Template guardado en: {template_path}")
    return template

# ══════════════════════════════════════════════════════════
# PASO 4 — Push template al tema activo de aylesva.MX
# ══════════════════════════════════════════════════════════
def push_template(template):
    print("\n" + "="*60)
    print("PASO 4: Subiendo template al tema de aylesva.mx...")
    print("="*60)
    
    url = f"{REST_BASE}/themes/{THEME_ID}/assets.json"
    payload = {
        "asset": {
            "key": "templates/page.globalstates.json",
            "value": json.dumps(template, indent=2, ensure_ascii=False)
        }
    }
    
    r = requests.put(url, json=payload, headers=HEADERS, verify=False, timeout=30)
    if r.status_code in [200, 201]:
        print(f"  ✅ Template subido exitosamente al tema {THEME_ID}")
        return True
    else:
        print(f"  ❌ Error HTTP {r.status_code}: {r.text[:300]}")
        return False

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    print("🏗  Transferencia Global States: aylesva.COM → aylesva.MX")
    print(f"   Tienda destino: {SHOP}")
    print(f"   Tema: {THEME_ID}")
    
    if not TOKEN:
        print("❌ No se encontró ACCESS_TOKEN en .env")
        sys.exit(1)
    
    # Paso 1
    download_images()
    
    # Paso 2
    uploaded = upload_images()
    print(f"\n  📊 {len(uploaded)}/{len(IMAGES)} imágenes subidas exitosamente")
    
    if not uploaded:
        print("❌ No se pudieron subir imágenes. Abortando.")
        sys.exit(1)
    
    # Paso 3
    template = update_template(uploaded)
    
    # Paso 4
    success = push_template(template)
    
    if success:
        print("\n" + "="*60)
        print("🎉 ¡COMPLETADO!")
        print("="*60)
        print("   Verifica la página en: https://aylesva.mx/pages/globalstates")
        print("   Compara con:           https://www.aylesva.com/pages/globalestates")
        print()
        print("   ⚠ PENDIENTE: Subir manualmente el video de Torre 40")
        print("     desde el admin de Shopify de aylesva.mx")
    else:
        print("\n❌ Hubo errores. Revisa los mensajes anteriores.")

if __name__ == "__main__":
    main()
