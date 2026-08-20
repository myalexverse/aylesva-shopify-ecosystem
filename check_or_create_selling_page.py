"""
Buscar o crear la página 'start-selling' en aylesva.mx
"""
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()

print("🔍 Buscando página con handle 'start-selling'...")
resp = session.get(f"{BASE_URL}/pages.json", params={"handle": "start-selling"})
pages = resp.json().get("pages", [])

if pages:
    page = pages[0]
    print(f"✅ Encontrada página en aylesva.mx:")
    print(f"   ID: {page['id']}")
    print(f"   Handle: {page['handle']}")
    print(f"   Title: {page['title']}")
    print(f"   Template Suffix: {page.get('template_suffix')}")
else:
    print("❌ No se encontró la página 'start-selling'. Procediendo a crearla...")
    # Crear la página con el suffix 'start-selling'
    create_resp = session.post(
        f"{BASE_URL}/pages.json",
        json={
            "page": {
                "title": "Lanza tu marca",
                "handle": "start-selling",
                "template_suffix": "start-selling"
            }
        }
    )
    if create_resp.status_code == 201:
        new_page = create_resp.json()["page"]
        print(f"✅ Página creada con éxito:")
        print(f"   ID: {new_page['id']}")
        print(f"   Handle: {new_page['handle']}")
        print(f"   Template Suffix: {new_page.get('template_suffix')}")
    else:
        print(f"❌ Error al crear la página: {create_resp.status_code} - {create_resp.text}")
