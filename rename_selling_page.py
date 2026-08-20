"""
Actualizar la página recién creada a handle 'lanza-tu-propia-marca' y título 'Lanza tu propia marca'
"""
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()
page_id = 151301816343

print(f"🔄 Actualizando página {page_id}...")
update_resp = session.put(
    f"{BASE_URL}/pages/{page_id}.json",
    json={
        "page": {
            "id": page_id,
            "title": "Lanza tu propia marca",
            "handle": "lanza-tu-propia-marca",
            "template_suffix": "lanza-tu-propia-marca"
        }
    }
)

if update_resp.status_code == 200:
    updated = update_resp.json()["page"]
    print(f"✅ Página actualizada con éxito:")
    print(f"   Título: {updated['title']}")
    print(f"   Handle: {updated['handle']}")
    print(f"   Template Suffix: {updated.get('template_suffix')}")
    print(f"   URL: https://aylesva.mx/pages/{updated['handle']}")
else:
    print(f"❌ Error al actualizar: {update_resp.status_code} - {update_resp.text}")
