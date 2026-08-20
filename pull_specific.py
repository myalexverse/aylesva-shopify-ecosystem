"""
Descarga solo los archivos específicos que necesitamos del tema de Shopify,
con timeouts más agresivos y retries.
"""
import os
import time
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", os.getenv("SHOPIFY_ACCESS_TOKEN", ""))
SHOP_NAME = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
API_VERSION = os.getenv("API_VERSION", "2025-01")
THEME_ID = os.getenv("THEME_ID", "172455165975")
BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def pull_asset(key, save_to):
    """Pull a single asset from Shopify"""
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]={key}"
    
    for attempt in range(5):
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=30)
            if r.status_code == 200:
                data = r.json().get('asset', {})
                if 'value' in data:
                    os.makedirs(os.path.dirname(save_to), exist_ok=True)
                    with open(save_to, 'w', encoding='utf-8') as f:
                        f.write(data['value'])
                    print(f"✅ Descargado: {key}")
                    return True
            elif r.status_code == 429:
                print(f"  Rate limited, esperando 3s...")
                time.sleep(3)
                continue
            else:
                print(f"❌ Error {r.status_code}: {key}")
                return False
        except Exception as e:
            wait = (attempt + 1) * 5
            print(f"  ⏳ Timeout, reintentando en {wait}s... (intento {attempt+1}/5)")
            time.sleep(wait)
    
    print(f"❌ No se pudo descargar {key} después de 5 intentos")
    return False

# Archivos que necesitamos descargar
files = [
    "templates/page.globalestates.json",
]

theme_dir = os.path.join(os.getcwd(), 'theme')

print("Descargando archivos del tema desde Shopify...")
for key in files:
    save_path = os.path.join(theme_dir, key)
    pull_asset(key, save_path)
    time.sleep(1)

print("\n✅ Descarga completa")
