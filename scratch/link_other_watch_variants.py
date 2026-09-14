import urllib.request, json, time

env_vars = {}
with open('.env') as fh:
    for line in fh:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip()

shop = env_vars.get('SHOP_NAME', 'aylesvamx.myshopify.com')
token = env_vars.get('ACCESS_TOKEN', '')

def link_product(pid, mapping_by_index):
    get_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products/{pid}.json",
        headers={"X-Shopify-Access-Token": token}
    )
    with urllib.request.urlopen(get_req) as resp:
        fresh = json.loads(resp.read().decode('utf-8'))['product']
        images = fresh.get('images', [])
        variants = fresh.get('variants', [])
        
        for v_idx, img_idx in mapping_by_index.items():
            if v_idx < len(variants) and img_idx < len(images):
                v = variants[v_idx]
                img = images[img_idx]
                payload = {"variant": {"id": v['id'], "image_id": img['id']}}
                v_req = urllib.request.Request(
                    f"https://{shop}/admin/api/2024-01/variants/{v['id']}.json",
                    data=json.dumps(payload).encode('utf-8'),
                    headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                    method="PUT"
                )
                with urllib.request.urlopen(v_req) as v_resp:
                    res = json.loads(v_resp.read().decode('utf-8'))['variant']
                    print(f"[{pid}] Variante '{res['title']}' -> Imagen ID: {res['image_id']}")
                time.sleep(0.4)

# CUR-212 (Chronograph)
link_product(8944277422103, {0: 0, 1: 3})

# CUR-219 (Smartwatch)
link_product(8944277356567, {0: 0, 1: 1})

print("✅ Todos los relojes tienen sus variantes vinculadas a sus imágenes.")
