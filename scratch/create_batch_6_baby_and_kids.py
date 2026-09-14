import urllib.request, json, time, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

env_vars = {}
with open('/Users/alexdoven/Desktop/PROYECTOS VARAL/aylesva_respaldo_desarrollo/.env') as fh:
    for line in fh:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip()

shop = env_vars.get('SHOP_NAME', 'aylesvamx.myshopify.com')
token = env_vars.get('ACCESS_TOKEN', '')

def req_with_retry(req, max_retries=4, delay=2.0):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"   ⚠️ Reintento {attempt+1}/{max_retries} tras error: {e}")
            time.sleep(delay * (attempt + 1))

def create_product_with_variant_images(product_data, variant_image_index_map, custom_collection_ids=None):
    payload = {"product": product_data}
    req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products.json",
        data=json.dumps(payload).encode('utf-8'),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="POST"
    )
    created = req_with_retry(req)['product']
    pid = created['id']
    print(f"\n✅ Creado: [{pid}] {created['title']}")
    
    # Esperar a que Shopify procese las imágenes en CDN
    time.sleep(1.8)
    
    # Obtener el producto actualizado con sus IDs de imágenes
    get_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products/{pid}.json",
        headers={"X-Shopify-Access-Token": token}
    )
    product_fresh = req_with_retry(get_req)['product']
    images = product_fresh.get('images', [])
    variants = product_fresh.get('variants', [])
    print(f"   📸 {len(images)} imágenes registradas, {len(variants)} variantes")
    
    for v_idx, img_idx in variant_image_index_map.items():
        if v_idx < len(variants) and img_idx < len(images):
            v = variants[v_idx]
            img = images[img_idx]
            v_payload = {"variant": {"id": v['id'], "image_id": img['id']}}
            v_req = urllib.request.Request(
                f"https://{shop}/admin/api/2024-01/variants/{v['id']}.json",
                data=json.dumps(v_payload).encode('utf-8'),
                headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                method="PUT"
            )
            v_res = req_with_retry(v_req)['variant']
            print(f"   🎯 Variante '{v_res['title']}' vinculada a foto {img_idx+1} (ID: {v_res['image_id']})")
            time.sleep(0.5)
            
    if custom_collection_ids:
        for cid in custom_collection_ids:
            try:
                c_payload = {"collect": {"collection_id": cid, "product_id": pid}}
                c_req = urllib.request.Request(
                    f"https://{shop}/admin/api/2024-01/collects.json",
                    data=json.dumps(c_payload).encode('utf-8'),
                    headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                    method="POST"
                )
                req_with_retry(c_req)
                print(f"   📂 Agregado a colección manual ID {cid}")
            except Exception as e:
                print(f"   ⚠️ Error agregando a colección {cid}: {e}")
            time.sleep(0.4)
                
    return pid

# ─────────────────────────────────────────────────────────────
# 2. MÁQUINA PORTÁTIL DE RUIDO BLANCO Y LUZ NOCTURNA BEBÉ
# ─────────────────────────────────────────────────────────────
white_noise_baby = {
    "title": "Máquina Portátil de Ruido Blanco y Sonidos Relajantes para Bebé con Luz Nocturna LED y Batería Recargable",
    "vendor": "Aylesva Baby",
    "product_type": "Sueño y Relajación Infantil",
    "tags": "Bebé, Accesorios, Cuidado Personal, Electrónicos, Gadgets y accesorios tecnológicos, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>El Secreto para Noches de Sueño Ininterrumpido y Calma Profunda</h3>
    <p>La <strong>Máquina de Ruido Blanco Portátil para Bebé</strong> reproduce con fidelidad acústica 20 sonidos relajantes no repetitivos clínicamente probados para calmar el llanto y facilitar la transición al sueño profundo: shushing suave, latidos cardíacos maternos, olas del mar, lluvia apacible y canciones de cuna clásicas.</p>
    <h4>Ventajas para Padres y Bebés:</h4>
    <ul>
      <li><strong>Luz Nocturna de Tono Cálido Graduable:</strong> Permite amamantar y cambiar pañales en la oscuridad sin alterar el ciclo de melatonina del bebé.</li>
      <li><strong>Temporizador de Autoapagado Inteligente (30, 60 y 90 Minutos):</strong> Se apaga cuando el bebé duerme plácidamente o puede dejarse en reproducción continua toda la noche.</li>
      <li><strong>Clip Portátil para Carriolas y Cunas:</strong> Cuélgalo con facilidad en la carriola durante paseos matutinos, en el autoasiento o en el barandal de la cuna.</li>
      <li><strong>Batería de Alta Capacidad USB-C:</strong> Más de 15 horas continuas de música y ruido blanco por carga.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/Babelio_White_NOise_Sound_Machine_DB30_20.webp?v=1774433959", "alt": "Blanco Calma - Máquina de Ruido Blanco Infantil"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/Babelio_White_NOise_Sound_Machine_DB30_17.webp?v=1774508616", "alt": "Negro Noche - Máquina de Ruido Blanco Infantil"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/Babelio_White_NOise_Sound_Machine_DB30_4.webp?v=1774508616", "alt": "Luz LED Nocturna y Controles Superiores"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Calma", "price": "580.00", "compare_at_price": "990.00", "sku": "SND-BABY-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro Noche", "price": "580.00", "compare_at_price": "990.00", "sku": "SND-BABY-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3. TAPETE Y GIMNASIO SENSORIAL ACOLCHADO CONVERTIBLE (5 JUGUETES)
# ─────────────────────────────────────────────────────────────
play_mat_baby = {
    "title": "Tapete y Gimnasio Sensorial Acolchado Convertible para Bebé con 5 Juguetes Didácticos de Estimulación Temprana",
    "vendor": "Aylesva Baby",
    "product_type": "Estimulación Temprana y Juguetes",
    "tags": "Bebé, Accesorios, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Espacio Seguro y Confortable para Tummy Time, Giros y Primeros Gateos</h3>
    <p>Recomendado por especialistas en desarrollo infantil, el <strong>Tapete y Gimnasio Sensorial Convertible</strong> ofrece dos modos de uso evolutivo: como gimnasio acolchado de 90x90 cm con arcos de juego para los primeros meses de alcance y coordinación visual, y expandible a 130x130 cm como tapete amplio de gateo y juego activo.</p>
    <h4>Beneficios de Estimulación Sensorial:</h4>
    <ul>
      <li><strong>5 Juguetes Didácticos Colgantes Incluidos:</strong> Espejo de autodescubrimiento irrompible, librito de texturas crujientes, mordedera suave de silicón grado alimenticio, peluche musical sonajero y figura de agarre psicomotriz.</li>
      <li><strong>Espuma Viscoelástica de Alta Densidad (2.5 cm):</strong> Amortigua caídas y aísla eficazmente del frío del piso, cuidando rodillas y articulaciones del bebé.</li>
      <li><strong>Base Antiderrapante Segura:</strong> Textura de micro-puntos de silicón que evita deslizamientos accidentales sobre pisos de duela, loseta o laminado.</li>
      <li><strong>Funda Removible y Lavable en Lavadora:</strong> Tela aterciopelada suave hipoalergénica con cierre perimetral para lavado rápido ante derrames.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/11_a189eb15-3c37-49d0-b824-639507cfc6bd.webp?v=1788512309", "alt": "Tapete Gimnasio Sensorial para Bebé con Arcos y Juguetes"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/2_85a807a3-bdc8-479c-8831-97e98c8e2cc8.webp?v=1788512339", "alt": "Estimulación de Gateo y Tummy Time"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/6_4b3997d5-0e57-4a04-ad73-b5438ec869a9.webp?v=1788512327", "alt": "Detalle de los 5 Juguetes Didácticos"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/3_7669f045-56fc-4ea0-be2d-e6596e8b266a.webp?v=1788512325", "alt": "Modo Tapete Amplio Extendido 130x130cm"}
    ],
    "options": [{"name": "Edición"}],
    "variants": [
        {"option1": "Verde Menta Nórdico + 5 Juguetes", "price": "890.00", "compare_at_price": "1490.00", "sku": "MAT-BABY-GN", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4. MOCHILA PAÑALERA MULTIFUNCIONAL TÉRMICA E IMPERMEABLE USB
# ─────────────────────────────────────────────────────────────
diaper_backpack = {
    "title": "Mochila Pañalera Multifuncional Térmica e Impermeable para Bebé con Puerto de Carga USB y Bolsillos Térmicos",
    "vendor": "Aylesva Baby",
    "product_type": "Bolsos y Accesorios Maternidad",
    "tags": "Bebé, Accesorios, Mujer, Damas, Dropshipping, Novedades",
    "body_html": """
    <h3>Organización Inteligente y Estilo Moderno para Salir de Casa con tu Bebé</h3>
    <p>La <strong>Mochila Pañalera Multifuncional Grid Wizard</strong> redefine el equipaje para papás y mamás. Confeccionada en tela Oxford militar impermeable y resistente a rasgaduras, cuenta con más de 14 compartimentos dedicados para llevar pañales, mudas de ropa, toallitas húmedas, juguetes y biberones a temperatura perfecta.</p>
    <h4>Distribución y Características:</h4>
    <ul>
      <li><strong>Compartimento Frontal con 3 Bolsillos Térmicos:</strong> Aislamiento de aluminio multicapa que mantiene la temperatura de biberones de leche caliente o fresca por más de 5 horas.</li>
      <li><strong>Bolsillo Lateral de Acceso Rápido para Toallitas:</strong> Ranura dispensadora lateral que permite extraer toallas desinfectantes con una sola mano sin abrir la mochila.</li>
      <li><strong>Puerto de Carga USB Externo:</strong> Conecta tu power bank en el interior y recarga tu celular cómodamente mientras paseas con la carriola.</li>
      <li><strong>Bolsillo de Seguridad Antirrobo Trasero:</strong> Espacio oculto pegado a la espalda para resguardar llaves, cartera y documentos importantes.</li>
      <li><strong>Ganchos Universales para Carriola Incluidos:</strong> Correas acolchadas transpirables y clips metálicos para colgarla del manillar de cualquier carriola.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/1_d4dde9c0-0066-4f2c-9b60-5bba85530235.webp?v=1788419718", "alt": "Gris Oxford - Mochila Pañalera Multifuncional"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/2_d9865697-c3b2-4da0-bb2a-d114538d209f.webp?v=1788419718", "alt": "Negro Carbón - Mochila Pañalera Multifuncional"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/3_ff721cb4-785f-4a6b-ba5d-948658983863.webp?v=1788419718", "alt": "Compartimentos Térmicos de Biberones y Toallitas"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/4_DIY.webp?v=1788486756", "alt": "Organización Interna de Gran Capacidad"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Gris Oxford", "price": "790.00", "compare_at_price": "1350.00", "sku": "BAG-DIAP-GRY", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro Carbón", "price": "790.00", "compare_at_price": "1350.00", "sku": "BAG-DIAP-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5. SET DE 16 BROCHES Y MOÑOS FLORALES PARA CABELLO NIÑA Y BEBÉ
# ─────────────────────────────────────────────────────────────
hair_clips_set = {
    "title": "Set de 16 Broches y Moños Florales Dulces para Cabello de Niña y Bebé con Forro Antideslizante Suave",
    "vendor": "Aylesva Kids",
    "product_type": "Accesorios para el Cabello",
    "tags": "Diademas y accesorios para el cabello Bebé, Diademas y accesorios para el cabello Niña, Bebé, Niña, Accesorios, Dropshipping, Novedades",
    "body_html": """
    <h3>El Toque Dulce y Encantador para Peinados Infantiles sin Tirones ni Molestias</h3>
    <p>El <strong>Set de 16 Moños y Broches Florales para Niña</strong> incluye una variada colección de diseños pastel, moños de listón acanalado y motivos botánicos primaverales. Diseñados pensando en la delicada cabellera de bebés y niñas pequeñas, cada clip metálico está completamente forrado en cinta de grosgrain suave para asegurar sujeción firme sin jalar ni lastimar el cuero cabelludo.</p>
    <h4>Características Destacadas:</h4>
    <ul>
      <li><strong>Clips 100% Forrados y Seguros:</strong> Sin bordes filosos metálicos expuestos. Máxima seguridad para bebés desde los 6 meses hasta niñas de 8 años.</li>
      <li><strong>Gran Variedad en un Solo Set (16 Piezas):</strong> Diseños de flores bordadas, lazos clásicos y figuras tiernas en tonos pastel para combinar con cualquier vestido o ropa casual.</li>
      <li><strong>Sujeción Firme en Cabello Fino:</strong> No se resbalan ni se caen durante el juego o actividades escolares.</li>
      <li><strong>Presentación en Caja de Regalo:</strong> Empaque decorativo ideal para regalos de cumpleaños, bautizos, baby showers o celebraciones.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/S6c9eae8b12b4493a8318a1c4a3fcaf0bx.webp?v=1787627666", "alt": "Colección Rosa Pastel - Set 16 Broches"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/S22c8477b40114d508482141302c9b44cv.webp?v=1787627667", "alt": "Colección Amarillo & Menta - Set 16 Broches"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/Sce991472af9a4b79a74cc723f92bb24cJ.webp?v=1787627666", "alt": "Colección Lavanda Dulce - Set 16 Broches"},
        {"src": "https://cdn.shopify.com/s/files/1/0515/6110/3530/files/S75d8fbe9f1e94af19f3a8dd7e96bcdd3C.webp?v=1787627666", "alt": "Detalle Forro Protector Suave"}
    ],
    "options": [{"name": "Colección"}],
    "variants": [
        {"option1": "Colección Rosa Pastel (16 Pzas)", "price": "340.00", "compare_at_price": "590.00", "sku": "CLP-GRL-PNK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Colección Amarillo & Menta (16 Pzas)", "price": "340.00", "compare_at_price": "590.00", "sku": "CLP-GRL-YEL", "inventory_management": None, "requires_shipping": True},
        {"option1": "Colección Lavanda Dulce (16 Pzas)", "price": "340.00", "compare_at_price": "590.00", "sku": "CLP-GRL-LAV", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("🚀 Reanudando Lote 6: Bebé, Niños y Maternidad con reintento automático...")
    
    # 2. Máquina Ruido Blanco: v0->img0 (Blanco), v1->img1 (Negro)
    pid_snd = create_product_with_variant_images(white_noise_baby, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 3. Tapete y Gimnasio Sensorial: v0->img0
    pid_mat = create_product_with_variant_images(play_mat_baby, {0: 0})
    time.sleep(1.2)
    
    # 4. Mochila Pañalera: v0->img0 (Gris), v1->img1 (Negro) + Añadido a damas-spot (485516541975)
    pid_bag = create_product_with_variant_images(diaper_backpack, {0: 0, 1: 1}, custom_collection_ids=[485516541975])
    time.sleep(1.2)
    
    # 5. Set Broches y Moños: v0->img0 (Rosa), v1->img1 (Amarillo), v2->img2 (Lavanda)
    pid_clp = create_product_with_variant_images(hair_clips_set, {0: 0, 1: 1, 2: 2})
    
    print("\n🎉 ¡Lote 6 completado exitosamente con todos los productos de Bebé y Niños!")
