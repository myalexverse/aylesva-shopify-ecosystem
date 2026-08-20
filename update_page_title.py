"""
Actualizar el título de la página a 'Aylesva Recursos'
"""
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()
page_id = 150855811095

print(f"🔄 Actualizando título de la página {page_id} a 'Aylesva Recursos'...")
resp = session.put(
    f"{BASE_URL}/pages/{page_id}.json",
    json={"page": {"id": page_id, "title": "Aylesva Recursos"}}
)

if resp.status_code == 200:
    print(f"✅ Título actualizado: {resp.json()['page']['title']}")
else:
    print(f"❌ Error: {resp.status_code} - {resp.text}")
