"""
Descargar templates/page.aylesva-recursos.json de Shopify para verificar su contenido
"""
import requests
import json
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, HEADERS, THEME_ID

url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]=templates/page.aylesva-recursos.json"
r = requests.get(url, headers=HEADERS, verify=False, timeout=30)

if r.status_code == 200:
    data = r.json()
    value = data["asset"]["value"]
    print("✅ Plantilla descargada de Shopify:")
    print(value)
else:
    print(f"❌ Error al descargar: {r.status_code} - {r.text}")
