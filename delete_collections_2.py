"""
Segundo pase: eliminar las 15 colecciones que no se encontraron en el primer intento.
Estas probablemente tienen handles ligeramente diferentes.
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

# Las 15 que no se encontraron
MISSING_HANDLES = [
    "frontpage",
    "on-sale",
    "telefonos",
    "computadoras",
    "audio-y-video",
    "gadgets",
    "vehiculos-trabajo",
    "refacciones",
    "recamara",
    "jardin",
    "productos-organicos",
    "reposteria",
    "regalos-gourmet",
    "ofertas",
    "mayoreo",
]

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
                return None

def search_collection_by_handle(handle):
    """Search for a collection by handle in both custom and smart collections"""
    # Try smart collections first
    url = f"{BASE_URL}/smart_collections.json?handle={handle}"
    r = api_request("GET", url)
    if r and r.status_code == 200:
        items = r.json().get('smart_collections', [])
        if items:
            return items[0]['id'], 'smart_collections'
    
    # Try custom collections
    url = f"{BASE_URL}/custom_collections.json?handle={handle}"
    r = api_request("GET", url)
    if r and r.status_code == 200:
        items = r.json().get('custom_collections', [])
        if items:
            return items[0]['id'], 'custom_collections'
    
    return None, None

def delete_collection(collection_id, collection_type):
    url = f"{BASE_URL}/{collection_type}/{collection_id}.json"
    r = api_request("DELETE", url)
    if r and r.status_code in [200, 204]:
        return True
    return False

def main():
    log("=" * 80)
    log("SEGUNDO PASE - ELIMINAR COLECCIONES FALTANTES")
    log("=" * 80)
    
    deleted = 0
    not_found = 0
    
    for i, handle in enumerate(MISSING_HANDLES):
        log(f"\n  {i+1}/{len(MISSING_HANDLES)} Buscando: {handle}...")
        
        cid, ctype = search_collection_by_handle(handle)
        
        if cid:
            log(f"    Encontrada: ID={cid}, tipo={ctype}")
            success = delete_collection(cid, ctype)
            if success:
                log(f"    ✅ Eliminada: {handle}")
                deleted += 1
            else:
                log(f"    ❌ Error al eliminar: {handle}")
        else:
            log(f"    ⚠️  No existe en Shopify: {handle}")
            not_found += 1
        
        time.sleep(0.5)
    
    log(f"\n{'='*80}")
    log("RESUMEN SEGUNDO PASE")
    log(f"{'='*80}")
    log(f"  ✅ Eliminadas: {deleted}")
    log(f"  ⚠️  No encontradas: {not_found}")
    log(f"\n  TOTAL ELIMINADAS EN AMBOS PASES: 41 + {deleted} = {41 + deleted}")

if __name__ == "__main__":
    main()
