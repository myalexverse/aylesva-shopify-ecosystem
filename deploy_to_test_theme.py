"""
Sube las secciones del redesign al tema de PRUEBAS (172862046231)
sin tocar el tema en vivo.
"""
import os
import sys
import time
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", os.getenv("SHOPIFY_ACCESS_TOKEN", ""))
SHOP_NAME = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
API_VERSION = os.getenv("API_VERSION", "2025-01")
TEST_THEME_ID = "172862046231"  # Tema "PRUEBAS"
BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

session = requests.Session()
session.headers.update(HEADERS)

def push_asset(asset_key, file_path):
    """Sube un archivo al tema de pruebas"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    payload = {"asset": {"key": asset_key, "value": content}}
    url = f"{BASE_URL}/themes/{TEST_THEME_ID}/assets.json"
    
    for attempt in range(3):
        r = session.put(url, json=payload, verify=False)
        if r.status_code in [200, 201]:
            print(f"  ✅ {asset_key}")
            return True
        elif r.status_code == 429:
            wait = 3 * (attempt + 1)
            print(f"  ⏳ Rate limited, esperando {wait}s...")
            time.sleep(wait)
        else:
            print(f"  ❌ Error {r.status_code}: {asset_key}")
            print(f"     {r.text[:300]}")
            return False
    return False

if __name__ == "__main__":
    theme_dir = os.path.join(os.getcwd(), 'theme')
    
    print(f"{'='*60}")
    print(f"  DEPLOY AL TEMA DE PRUEBAS (ID: {TEST_THEME_ID})")
    print(f"{'='*60}\n")
    
    # 1. Subir secciones nuevas
    new_sections = [
        "sections/ayl-home-hero-ecosystem.liquid",
        "sections/ayl-home-ecosystem.liquid",
        "sections/ayl-home-trust-logos.liquid",
        "sections/ayl-home-ecosystem-stats.liquid",
        "sections/ayl-home-solutions.liquid",
        "sections/ayl-home-timeline.liquid",
        "sections/ayl-home-testimonials.liquid",
        "sections/ayl-home-cta-ecosystem.liquid",
        "sections/header-ecosystem.liquid",
    ]
    
    print("── Subiendo 9 secciones nuevas ──")
    for asset_key in new_sections:
        file_path = os.path.join(theme_dir, asset_key)
        if os.path.exists(file_path):
            push_asset(asset_key, file_path)
        else:
            print(f"  ⚠️  No encontrado: {file_path}")
        time.sleep(0.5)
    
    # 2. Subir el nuevo index.json
    print("\n── Subiendo homepage template ──")
    redesign_index = os.path.join(theme_dir, 'templates', 'index.redesign.json')
    if os.path.exists(redesign_index):
        push_asset("templates/index.json", redesign_index)
    else:
        print(f"  ⚠️  No encontrado: {redesign_index}")
    time.sleep(0.5)
    
    # 3. Subir el nuevo header-group.json
    print("\n── Subiendo header group ──")
    redesign_header = os.path.join(theme_dir, 'sections', 'header-group.redesign.json')
    if os.path.exists(redesign_header):
        push_asset("sections/header-group.json", redesign_header)
    else:
        print(f"  ⚠️  No encontrado: {redesign_header}")
    
    print(f"\n{'='*60}")
    print(f"  ✅ DEPLOY COMPLETADO")
    print(f"{'='*60}")
    print(f"\n🔗 Preview URL (solo tú puedes verlo):")
    print(f"   https://{SHOP_NAME}/?preview_theme_id={TEST_THEME_ID}")
    print(f"\n📝 Editor de temas:")
    print(f"   https://{SHOP_NAME}/admin/themes/{TEST_THEME_ID}/editor")
    print(f"\n⚠️  El tema en vivo NO fue tocado.")
