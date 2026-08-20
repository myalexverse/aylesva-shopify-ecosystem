"""
Obtener los datos de la página Aylesva Recursos de Shopify para ver su template_suffix
"""
import requests
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()
page_id = 150855811095

r = session.get(f"{BASE_URL}/pages/{page_id}.json")
if r.status_code == 200:
    page = r.json().get("page", {})
    print("✅ Datos de la página en Shopify:")
    print(f"   ID: {page.get('id')}")
    print(f"   Title: '{page.get('title')}'")
    print(f"   Handle: '{page.get('handle')}'")
    print(f"   Template Suffix: '{page.get('template_suffix')}'")
else:
    print(f"❌ Error: {r.status_code} - {r.text}")
