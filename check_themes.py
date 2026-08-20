"""
Listar todos los temas de la tienda para verificar cuál es el publicado (main)
"""
import requests
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, HEADERS, THEME_ID

url = f"{BASE_URL}/themes.json"
r = requests.get(url, headers=HEADERS, verify=False, timeout=30)

if r.status_code == 200:
    themes = r.json().get("themes", [])
    print("✅ Temas en Shopify:")
    for theme in themes:
        role_str = f" [PUBLICADO/LIVE]" if theme["role"] == "main" else ""
        active_str = f" [NUESTRO THEME_ID CONFIGURADO]" if str(theme["id"]) == str(THEME_ID) else ""
        print(f"   ID: {theme['id']} - Name: '{theme['name']}' - Role: '{theme['role']}'{role_str}{active_str}")
else:
    print(f"❌ Error: {r.status_code} - {r.text}")
