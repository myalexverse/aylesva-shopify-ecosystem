"""
Actualizar la página 'Aylesva Recursos' para invalidar la caché del CDN de Shopify.
"""
from shopify_base import BASE_URL, get_shopify_session

session = get_shopify_session()
page_id = 150855811095

print(f"🔄 Solicitando datos de la página {page_id}...")
r = session.get(f"{BASE_URL}/pages/{page_id}.json")
if r.status_code == 200:
    page_data = r.json()["page"]
    # Agregar un espacio sutil al body_html para forzar cambio y actualización de caché
    current_body = page_data.get("body_html") or ""
    new_body = current_body + " "
    
    print("🔄 Guardando página con cambio sutil para invalidar caché...")
    resp = session.put(
        f"{BASE_URL}/pages/{page_id}.json",
        json={"page": {"id": page_id, "body_html": new_body}}
    )
    if resp.status_code == 200:
        print("✅ Página guardada. Caché invalidado en los servidores CDN de Shopify.")
    else:
        print(f"❌ Error al guardar: {resp.status_code} - {resp.text}")
else:
    print(f"❌ Error al obtener página: {r.status_code} - {r.text}")
