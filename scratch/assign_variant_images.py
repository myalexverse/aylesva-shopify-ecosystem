import urllib.request, json, time

env_vars = {}
with open('.env') as fh:
    for line in fh:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip()

shop = env_vars.get('SHOP_NAME', 'aylesvamx.myshopify.com')
token = env_vars.get('ACCESS_TOKEN', '')

pid = 8944277454871 # Curren CUR-230

# 1. Obtener imágenes actuales y eliminarlas para ordenarlas perfectamente
get_req = urllib.request.Request(
    f"https://{shop}/admin/api/2024-01/products/{pid}.json",
    headers={"X-Shopify-Access-Token": token}
)
with urllib.request.urlopen(get_req) as resp:
    curr = json.loads(resp.read().decode('utf-8'))['product']
    for img in curr.get('images', []):
        del_req = urllib.request.Request(
            f"https://{shop}/admin/api/2024-01/products/{pid}/images/{img['id']}.json",
            headers={"X-Shopify-Access-Token": token},
            method="DELETE"
        )
        try:
            urllib.request.urlopen(del_req)
        except Exception:
            pass
        time.sleep(0.3)

# 2. Subir las 4 imágenes ordenadas por variante + 2 de detalle
ordered_images = [
    # Pos 1: Negro
    {
        "src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S7524da209be34c739400423807bf5a92f.webp?v=1736092103",
        "alt": "Negro Táctico Stealth"
    },
    # Pos 2: Azul
    {
        "src": "https://cdn.shopify.com/s/files/1/0304/3821/files/currenwatches230.jpg?v=1736091983",
        "alt": "Azul Cobalto Deportivo"
    },
    # Pos 3: Naranja
    {
        "src": "https://cdn.shopify.com/s/files/1/0304/3821/files/currenwatches-230.png?v=1736092245",
        "alt": "Naranja Racing Adventure"
    },
    # Pos 4: Rojo
    {
        "src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S42271fafe51f4f1a87e955e595255e13U.webp?v=1736092039",
        "alt": "Rojo Escudería Sport"
    },
    # Pos 5: Detalle Estuche
    {
        "src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S55a5ed18be9c4cef8e8241396555bb0aH.webp?v=1736092000",
        "alt": "Curren CUR-230 Estuche y Garantía"
    }
]

put_req = urllib.request.Request(
    f"https://{shop}/admin/api/2024-01/products/{pid}.json",
    data=json.dumps({"product": {"images": ordered_images}}).encode('utf-8'),
    headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
    method="PUT"
)
with urllib.request.urlopen(put_req) as resp:
    p_upd = json.loads(resp.read().decode('utf-8'))['product']
    print(f"✅ {len(p_upd['images'])} imágenes cargadas y ordenadas.")

time.sleep(1)

# 3. Mapear cada variante con su imagen correspondiente
get_req2 = urllib.request.Request(
    f"https://{shop}/admin/api/2024-01/products/{pid}.json",
    headers={"X-Shopify-Access-Token": token}
)
with urllib.request.urlopen(get_req2) as resp:
    fresh = json.loads(resp.read().decode('utf-8'))['product']
    images = fresh['images']
    variants = fresh['variants']

    # img 0 -> Negro, img 1 -> Azul, img 2 -> Naranja, img 3 -> Rojo
    mapping = {
        "Negro Táctico Stealth": images[0]['id'],
        "Azul Cobalto Deportivo": images[1]['id'],
        "Naranja Racing Adventure": images[2]['id'],
        "Rojo Escudería Sport": images[3]['id']
    }

    for v in variants:
        title = v['title']
        img_id = mapping.get(title)
        if img_id:
            v_payload = {"variant": {"id": v['id'], "image_id": img_id}}
            v_req = urllib.request.Request(
                f"https://{shop}/admin/api/2024-01/variants/{v['id']}.json",
                data=json.dumps(v_payload).encode('utf-8'),
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                method="PUT"
            )
            with urllib.request.urlopen(v_req) as v_resp:
                v_res = json.loads(v_resp.read().decode('utf-8'))['variant']
                print(f"🎯 Variante '{title}' vinculada con imagen ID: {v_res['image_id']}")
            time.sleep(0.4)

print("\n🎉 Todas las variantes quedaron vinculadas con su imagen oficial en Shopify!")
