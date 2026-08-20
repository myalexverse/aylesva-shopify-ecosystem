"""
Script para eliminar colecciones innecesarias, duplicadas y ambiguas de Shopify.
Total estimado: ~56 colecciones.
"""
import json
import time
import requests
import urllib3
from dotenv import load_dotenv
import os

urllib3.disable_warnings()
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", os.getenv("SHOPIFY_ACCESS_TOKEN", ""))
SHOP_NAME = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
API_VERSION = os.getenv("API_VERSION", "2025-01")
BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# === LISTA COMPLETA DE HANDLES A ELIMINAR ===

# No prioritarias - Nicho/bajo margen
NO_PRIORITARIAS = [
    "pijamas-y-ropa-de-dormir-mujer",
    "pijamas-y-ropa-de-dormir-hombre",
    "overoles-y-monos-mujer",
    "pantuflas-hombre",
    "pantuflas-y-chanclas",
    "plataformas",
    "zapatos-de-trabajo",
    "bodies",
    "fajas-y-moldeadores",
    "medias-y-calcetas",
    "brasieres-y-bras",
    "panties-y-calzones",
    "pijamas-y-lenceria",
    "calzoncillos-y-boxers",
    "medias-y-calcetines-hombre",
    "pijamas-hombre",
    "cuidado-del-cabello-hombre",
    "instrumentos-musicales-artesanales",
    "ropa-de-lactancia",
    "fajas-postparto",
    "frontpage",
    "on-sale",
]

# Electrónicos - departamento completo vacío
ELECTRONICOS = [
    "telefonos",
    "telefonos-y-comunicacion",
    "computadoras",
    "computadoras-y-laptops",
    "audio-y-video",
    "audio-y-sonido",
    "television-y-video",
    "fotografia-y-video",
    "videojuegos",
    "electrodomesticos",
    "gadgets",
    "redes-e-internet",
    "energia-y-carga",
    "seguridad-electronica",
]

# Vehículos - departamento completo vacío
VEHICULOS = [
    "automoviles",
    "motocicletas",
    "vehiculos-trabajo",
    "vehiculos-de-carga-y-trabajo",
    "refacciones",
    "accesorios-y-refacciones",
    "vehiculos-recreativos",
    "transporte-publico-y-comercial",
]

# Duplicadas - el handle menos descriptivo de cada par
DUPLICADAS = [
    "recamara",           # conservar recamara-y-ropa-de-cama
    "jardin",             # conservar jardin-y-exterior
    "productos-organicos",# conservar productos-organicos-y-naturales
    "reposteria",         # conservar reposteria-y-panaderia
    "regalos-gourmet",    # conservar canastas-y-regalos-gourmet
    "ofertas",            # on-sale ya eliminada; saldos y 2x1 se conservan
]

# Ambiguas - propósito confuso o redundante
AMBIGUAS = [
    "mayoreo",                    # debería ser página, no colección
    "ropa-interior-y-lenceria",   # Level 2 vacía + todos Level 3 eliminados
    "ropa-interior-hombre",       # Level 2 vacía + todos Level 3 eliminados
    "ropa-interior-nino",         # vacía
    "ropa-interior-nina",         # vacía
    "belleza-y-cuidado-personal", # Level 2 vacía, solo maquillaje tiene prods
]

ALL_TO_DELETE = NO_PRIORITARIAS + ELECTRONICOS + VEHICULOS + DUPLICADAS + AMBIGUAS

def log(msg):
    print(msg, flush=True)

def api_request(method, url, retries=3, **kwargs):
    for attempt in range(retries):
        try:
            r = requests.request(method, url, headers=HEADERS, verify=False, timeout=30, **kwargs)
            return r
        except Exception as e:
            if attempt < retries - 1:
                wait = (attempt + 1) * 3
                log(f"    ⏳ Reintentando en {wait}s... ({e})")
                time.sleep(wait)
            else:
                log(f"    ❌ Error después de {retries} intentos: {e}")
                return None

def get_all_collections():
    """Fetch all custom and smart collections"""
    all_collections = []
    
    for endpoint in ["custom_collections", "smart_collections"]:
        url = f"{BASE_URL}/{endpoint}.json?limit=250"
        page = 1
        while url:
            log(f"  Obteniendo {endpoint} página {page}...")
            r = api_request("GET", url)
            if not r or r.status_code != 200:
                log(f"  Error obteniendo {endpoint}: {r.status_code if r else 'sin respuesta'}")
                break
            
            data = r.json()
            items = data.get(endpoint, [])
            for item in items:
                item['_type'] = endpoint
            all_collections.extend(items)
            log(f"  Obtenidos {len(items)} ({endpoint})")
            
            # Pagination
            link_header = r.headers.get('Link', '')
            if 'rel="next"' in link_header:
                parts = link_header.split(',')
                for part in parts:
                    if 'rel="next"' in part:
                        url = part.split('<')[1].split('>')[0]
                        page += 1
                        break
            else:
                url = None
            
            time.sleep(0.5)
    
    return all_collections

def delete_collection(collection_id, collection_type, handle):
    """Delete a collection by ID"""
    if collection_type == "custom_collections":
        url = f"{BASE_URL}/custom_collections/{collection_id}.json"
    else:
        url = f"{BASE_URL}/smart_collections/{collection_id}.json"
    
    r = api_request("DELETE", url)
    if r and r.status_code in [200, 204]:
        return True
    elif r:
        log(f"    ❌ Error {r.status_code}: {r.text[:200]}")
        return False
    return False

def main():
    log("=" * 80)
    log("ELIMINACIÓN DE COLECCIONES INNECESARIAS - AYLESVA")
    log("=" * 80)
    log(f"\nTotal de handles a eliminar: {len(ALL_TO_DELETE)}")
    log(f"  - No prioritarias: {len(NO_PRIORITARIAS)}")
    log(f"  - Electrónicos: {len(ELECTRONICOS)}")
    log(f"  - Vehículos: {len(VEHICULOS)}")
    log(f"  - Duplicadas: {len(DUPLICADAS)}")
    log(f"  - Ambiguas: {len(AMBIGUAS)}")
    
    # Step 1: Fetch all collections
    log("\n📋 Paso 1: Obteniendo todas las colecciones de Shopify...")
    all_collections = get_all_collections()
    log(f"  Total obtenidas: {len(all_collections)}")
    
    # Step 2: Map handles to collections
    handle_map = {}
    for c in all_collections:
        handle_map[c['handle']] = c
    
    # Step 3: Find matches
    to_delete = []
    not_found = []
    
    for handle in ALL_TO_DELETE:
        if handle in handle_map:
            to_delete.append(handle_map[handle])
        else:
            not_found.append(handle)
    
    log(f"\n🎯 Paso 2: Colecciones encontradas para eliminar: {len(to_delete)}")
    if not_found:
        log(f"⚠️  Handles no encontrados en Shopify: {len(not_found)}")
        for h in not_found:
            log(f"    - {h}")
    
    # Step 4: Delete
    log(f"\n🗑️  Paso 3: Eliminando {len(to_delete)} colecciones...")
    deleted = 0
    failed = 0
    
    for i, c in enumerate(to_delete):
        handle = c['handle']
        cid = c['id']
        ctype = c['_type']
        
        log(f"  {i+1}/{len(to_delete)} Eliminando {handle} (ID: {cid}, tipo: {ctype})...")
        
        success = delete_collection(cid, ctype, handle)
        if success:
            log(f"    ✅ Eliminada: {handle}")
            deleted += 1
        else:
            log(f"    ❌ Falló: {handle}")
            failed += 1
        
        time.sleep(0.5)  # Rate limit
    
    # Summary
    log("\n" + "=" * 80)
    log("RESUMEN")
    log("=" * 80)
    log(f"  ✅ Eliminadas exitosamente: {deleted}")
    log(f"  ❌ Fallidas: {failed}")
    log(f"  ⚠️  No encontradas: {len(not_found)}")
    log(f"  📊 Colecciones restantes: {len(all_collections) - deleted}")
    
    # Save results
    results = {
        "deleted": deleted,
        "failed": failed,
        "not_found": not_found,
        "handles_deleted": [c['handle'] for c in to_delete if c['handle'] not in [f['handle'] for f in to_delete if False]],
        "total_before": len(all_collections),
        "total_after": len(all_collections) - deleted
    }
    with open("deletion_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"\n💾 Resultados guardados en deletion_results.json")

if __name__ == "__main__":
    main()
