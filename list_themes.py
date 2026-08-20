"""
Lista todos los temas disponibles en la tienda para encontrar uno de prueba
o crear uno nuevo vacío.
"""
import os
import requests
import urllib3
from dotenv import load_dotenv

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

session = requests.Session()
session.headers.update(HEADERS)

r = session.get(f"{BASE_URL}/themes.json", verify=False)
if r.status_code == 200:
    themes = r.json().get('themes', [])
    print(f"{'='*70}")
    print(f"  TEMAS EN LA TIENDA ({len(themes)} total)")
    print(f"{'='*70}")
    for t in themes:
        role = t.get('role', 'unknown')
        status = "🟢 EN VIVO" if role == 'main' else "⚪ No publicado"
        print(f"  {status}  ID: {t['id']}  |  {t['name']}")
        print(f"           Role: {role}  |  Created: {t.get('created_at', 'N/A')[:10]}")
        print()
else:
    print(f"Error: {r.status_code} - {r.text}")
