"""
Listar todas las páginas de Shopify con sus IDs, títulos, handles y template_suffixes
"""
import requests
import urllib3
urllib3.disable_warnings()
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()

r = session.get(f"{BASE_URL}/pages.json?limit=50")
if r.status_code == 200:
    pages = r.json().get("pages", [])
    print("✅ Páginas registradas en Shopify:")
    for page in pages:
        print(f"   ID: {page['id']} - Title: '{page['title']}' - Handle: '{page['handle']}' - Template: '{page['template_suffix']}'")
else:
    print(f"❌ Error: {r.status_code} - {r.text}")
