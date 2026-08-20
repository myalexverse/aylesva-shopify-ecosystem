"""Consultar los menús de navegación de Shopify buscando 'Saldos'"""
import json
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()

# Listar todos los menús
resp = session.get(f"{BASE_URL}/menus.json")
if resp.status_code == 200:
    menus = resp.json().get("menus", [])
    print(f"📋 Encontrados {len(menus)} menús\n")
    for menu in menus:
        print(f"  Menu: '{menu['title']}' (ID: {menu['id']}, handle: {menu.get('handle', 'N/A')})")
        # Buscar recursivamente items con "saldos"
        def search_items(items, depth=0):
            for item in items:
                prefix = "    " * (depth + 1)
                title = item.get("title", "")
                url = item.get("url", "")
                has_saldos = "saldo" in title.lower() or "saldo" in url.lower()
                marker = " ⚠️ SALDOS" if has_saldos else ""
                print(f"{prefix}- {title} → {url}{marker}")
                if item.get("items"):
                    search_items(item["items"], depth + 1)
        if menu.get("items"):
            search_items(menu["items"])
        print()
else:
    print(f"❌ Error: {resp.status_code} - {resp.text}")
    # Intentar con la API de Online Store
    print("\nIntentando con pages...")
    resp2 = session.get(f"{BASE_URL}/pages.json", params={"title": "Saldos"})
    if resp2.status_code == 200:
        pages = resp2.json().get("pages", [])
        for p in pages:
            print(f"  Page: {p['title']} (handle: {p['handle']}, id: {p['id']})")
