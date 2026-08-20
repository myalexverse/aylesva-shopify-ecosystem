"""
Descargar sections/aylesva-recursos.liquid de Shopify para verificar su contenido
"""
import os
import requests
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, HEADERS, THEME_ID

url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]=sections/aylesva-recursos.liquid"
r = requests.get(url, headers=HEADERS, verify=False, timeout=30)

if r.status_code == 200:
    data = r.json()
    value = data["asset"]["value"]
    print("✅ Sección descargada del servidor de Shopify.")
    print(f"   Tamaño: {len(value)} bytes")
    # Verificar si contiene rc-fadeup
    if "rc-fadeup" in value:
        print("   🔍 CONTIENE 'rc-fadeup' en la sección en Shopify.")
    else:
        print("   ❌ NO CONTIENE 'rc-fadeup' en la sección en Shopify.")
        
    if "rc-sim-container" in value:
        print("   🔍 CONTIENE 'rc-sim-container' en la sección en Shopify.")
    else:
        print("   ❌ NO CONTIENE 'rc-sim-container' en la sección en Shopify.")
else:
    print(f"❌ Error al descargar: {r.status_code} - {r.text}")
