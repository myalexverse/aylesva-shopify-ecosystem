"""
Descargar sections/aylesva-recursos.liquid de Shopify e imprimir las líneas del Hero CTA
"""
import requests
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, HEADERS, THEME_ID

url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]=sections/aylesva-recursos.liquid"
r = requests.get(url, headers=HEADERS, verify=False, timeout=30)

if r.status_code == 200:
    data = r.json()
    value = data["asset"]["value"]
    lines = value.split("\n")
    print("✅ Líneas descargadas de Shopify:")
    for idx in range(230, 260):
        if idx < len(lines):
            print(f"{idx+1}: {lines[idx]}")
else:
    print(f"❌ Error al descargar: {r.status_code} - {r.text}")
