"""
Buscar la página 'prestamos-fink' en aylesva.mx y renombrarla a 'aylesva-recursos'
"""
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()

print("🔍 Buscando página con handle 'prestamos-fink'...")
resp = session.get(f"{BASE_URL}/pages.json", params={"handle": "prestamos-fink"})
pages = resp.json().get("pages", [])

if not pages:
    print("❌ No se encontró la página con handle 'prestamos-fink'. Intentando buscar 'aylesva-recursos'...")
    resp_recursos = session.get(f"{BASE_URL}/pages.json", params={"handle": "aylesva-recursos"})
    pages_recursos = resp_recursos.json().get("pages", [])
    if pages_recursos:
        page = pages_recursos[0]
        print(f"✅ Encontrada página de recursos existente: ID={page['id']}, handle={page['handle']}")
    else:
        print("❌ No se encontró ninguna de las páginas. Procediendo a crear 'aylesva-recursos'...")
        create_resp = session.post(
            f"{BASE_URL}/pages.json",
            json={
                "page": {
                    "title": "Ahí les va Recursos",
                    "handle": "aylesva-recursos",
                    "template_suffix": "aylesva-recursos"
                }
            }
        )
        if create_resp.status_code == 201:
            new_page = create_resp.json()["page"]
            print(f"✅ Página creada con éxito: ID={new_page['id']}, handle={new_page['handle']}")
        else:
            print(f"❌ Error al crear: {create_resp.status_code} - {create_resp.text}")
else:
    page = pages[0]
    page_id = page["id"]
    print(f"✅ Encontrada página: ID={page_id}. Renombrando a 'aylesva-recursos'...")
    update_resp = session.put(
        f"{BASE_URL}/pages/{page_id}.json",
        json={
            "page": {
                "id": page_id,
                "title": "Ahí les va Recursos",
                "handle": "aylesva-recursos",
                "template_suffix": "aylesva-recursos"
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
