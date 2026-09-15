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
            with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"   ⚠️ Reintento {attempt+1}/{max_retries} tras error: {e}")
            time.sleep(delay * (attempt + 1))

def create_product_with_variant_images(product_data, variant_image_index_map):
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
    
    # Esperar procesamiento de imágenes en CDN
    time.sleep(2.0)
    
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
            
    return pid

# ─────────────────────────────────────────────────────────────
# 1. CAFÉ DE ESPECIALIDAD CHIAPAS DE ALTURA 100% ARÁBICA (1 KG)
# ─────────────────────────────────────────────────────────────
coffee_chiapas = {
    "title": "Café de Especialidad Chiapas de Altura 100% Arábica Gourmet Tueste Medio (1 Kg)",
    "vendor": "Aylesva Gourmet",
    "product_type": "Café Gourmet",
    "tags": "Alimentos, Alimentos Artesanales, Café de especialidad, Bebidas Artesanales, Gourmet, Novedades, Dropshipping",
    "body_html": """
    <h3>Aroma Envolvente, Acidez Brillante y Notas Achocolatadas del Sur de México</h3>
    <p>Cultivado bajo sombra a más de 1,350 metros sobre el nivel del mar en las montañas de Chiapas, el <strong>Café de Especialidad Chiapas Gourmet Aylesva</strong> representa lo mejor de la tradición cafetalera mexicana. Cosechado a mano y procesado mediante lavado artesanal, ofrece un perfil de taza redondo con cuerpo cremoso y elegantes notas de avellana tostada, caramelo y chocolate de mesa.</p>
    <h4>Ficha Técnica del Origen:</h4>
    <ul>
      <li><strong>Región de Origen:</strong> Sierra Madre de Chiapas, México.</li>
      <li><strong>Variedad:</strong> 100% Arábica (Bourbon, Typica y Caturra).</li>
      <li><strong>Tipo de Tueste:</strong> Medio Equilibrado (conserva aceites esenciales y dulzor natural sin amargor excesivo).</li>
      <li><strong>Presentaciones Disponibles:</strong> En Grano Entero (para amantes de la molienda fresca) y Molido Medio (ideal para cafetera de goteo, prensa francesa o moka italiana).</li>
      <li><strong>Empaque con Válvula Desgasificadora Unidireccional:</strong> Preserva la frescura y aroma por meses sin oxidarse.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/paquete-5-bolsas-de-1-kg-cafe-de-chiapas-exclusivo-cdmxtresso-5766431.jpg?v=1787238028", "alt": "Café de Especialidad Chiapas de Altura 1 Kg en Grano"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/paquete-5-bolsas-de-1-kg-cafe-de-chiapas-exclusivo-cdmxtresso-5714582.jpg?v=1787238028", "alt": "Café de Especialidad Chiapas Molido Medio"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/paquete-5-bolsas-cafe-de-veracruz-region-altas-montanas-1kg-12-kg-exclusivo-cdmxtresso-4363735.jpg?v=1787237529", "alt": "Tueste Artesanal Fresco de Altura"}
    ],
    "options": [{"name": "Molienda"}],
    "variants": [
        {"option1": "Grano Entero (1 Kg)", "price": "420.00", "compare_at_price": "680.00", "sku": "CAF-CHIAP-GRN", "inventory_management": None, "requires_shipping": True},
        {"option1": "Molido Medio (1 Kg)", "price": "420.00", "compare_at_price": "680.00", "sku": "CAF-CHIAP-MOL", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 2. CAFÉ CON CHOCOLATE ARTESANAL DE MESA GRANULADO (250G / 500G)
# ─────────────────────────────────────────────────────────────
coffee_chocolate = {
    "title": "Café Gourmet Veracruzano con Chocolate Artesanal para Mesa Granulado con Canela",
    "vendor": "Aylesva Gourmet",
    "product_type": "Café y Chocolate",
    "tags": "Alimentos, Alimentos Artesanales, Café de especialidad, Chocolates y dulces, Bebidas Artesanales, Gourmet, Novedades, Dropshipping",
    "body_html": """
    <h3>La Mezcla Tradicional Más Reconfortante: Café de Estricta Altura y Cacao Puro</h3>
    <p>El <strong>Café con Chocolate de Mesa Granulado Aylesva</strong> combina granos selectos de Veracruz tostados a la perfección con cacao mexicano de molienda rústica, azúcar mascabado moreno y un toque aromático de canela en vara. Una bebida cálida, nostálgica y llena de energía natural que rinde homenaje a las recetas de las abuelas mexicanas.</p>
    <h4>Modo de Preparación Sugerido:</h4>
    <ul>
      <li><strong>En Leche o Bebida Vegetal Caliente:</strong> Añade 2 a 3 cucharadas por taza para obtener un café moca espumoso y aterciopelado sin necesidad de endulzantes adicionales.</li>
      <li><strong>En Cafetera Tradicional o de Olla:</strong> Prepara tu café habitual agregando una cucharada de la mezcla para infusionar notas de cacao y canela.</li>
      <li><strong>Ingredientes 100% Naturales:</strong> Café tostado y molido, pasta de cacao puro, azúcar de caña no refinada y canela natural. Sin conservadores ni colorantes artificiales.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/cafe-veracruz-con-chocolate-para-mesa-granulado-250-gtresso-5812537.jpg?v=1787238008", "alt": "Café Veracruz con Chocolate de Mesa Granulado 250g"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/cafe-veracruz-con-chocolate-para-mesa-granulado-250-gtresso-1411214.jpg?v=1787238008", "alt": "Presentación Dúo 500g Café con Chocolate"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/paquete-3-bolsa-cacao-en-polvo-natural-400g-exclusivo-cdmxtresso-7358667.jpg?v=1787237529", "alt": "Cacao Puro Natural y Canela"}
    ],
    "options": [{"name": "Presentación"}],
    "variants": [
        {"option1": "Bolsa Hermética 250g", "price": "260.00", "compare_at_price": "420.00", "sku": "CAF-CHOC-250G", "inventory_management": None, "requires_shipping": True},
        {"option1": "Pack Dúo Ahorro 500g (2x250g)", "price": "460.00", "compare_at_price": "790.00", "sku": "CAF-CHOC-500G", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3. GRANOS DE CAFÉ TOSTADO CUBIERTOS CON CHOCOLATE AMARGO ARTESANAL
# ─────────────────────────────────────────────────────────────
coffee_beans_chocolate = {
    "title": "Granos de Café Tostado Cubiertos con Chocolate Amargo Artesanal 70% Cacao",
    "vendor": "Aylesva Gourmet",
    "product_type": "Chocolates Gourmet",
    "tags": "Alimentos, Alimentos Artesanales, Chocolates y dulces, Gourmet, Novedades, Dropshipping",
    "body_html": """
    <h3>La Fusión Perfecta de Crunch Crujiente y Suavidad Chocolatosa Gourmet</h3>
    <p>Cada bocado de los <strong>Granos de Café Cubiertos con Chocolate Amargo Aylesva</strong> ofrece una experiencia sensorial inigualable: granos de café arábica perfectamente tostados con textura crujiente recubiertos por una generosa capa de fino chocolate amargo 70% cacao mexicano.</p>
    <h4>El Snack Gourmet Ideal:</h4>
    <ul>
      <li><strong>Shot de Energía y Antioxidantes:</strong> La dosis perfecta de cafeína natural y teobromina del cacao para tus jornadas de trabajo o estudio.</li>
      <li><strong>Chocolate 70% Cacao Puro:</strong> Elaborado con manteca de cacao natural sin grasas hidrogenadas ni exceso de azúcar.</li>
      <li><strong>Frasco de Vidrio Reutilizable con Cierre Hermético:</strong> Conserva el crujiente perfecto y es ideal como obsequio elegante o detalle gourmet.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/granos-de-cafe-cubiertos-con-chocolate-150gtresso-6149645.jpg?v=1787238015", "alt": "Frasco Granos de Café con Chocolate Amargo 150g"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/granos-de-cafe-cubiertos-con-chocolate-150gtresso-8584178.jpg?v=1787238015", "alt": "Pack Dúo Granos de Café con Chocolate 300g"}
    ],
    "options": [{"name": "Presentación"}],
    "variants": [
        {"option1": "Frasco Gourmet 150g", "price": "240.00", "compare_at_price": "390.00", "sku": "CHOC-BEANS-150G", "inventory_management": None, "requires_shipping": True},
        {"option1": "Pack Dúo 300g (2 Frascos)", "price": "420.00", "compare_at_price": "690.00", "sku": "CHOC-BEANS-300G", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4. CANASTA & CAJA DE REGALO GOURMET "SABORES DE MÉXICO"
# ─────────────────────────────────────────────────────────────
gift_basket = {
    "title": "Caja Canasta de Regalo Gourmet Tradicional Mexicano con 2 Tisanas Frutales y 2 Cafés de Altura",
    "vendor": "Aylesva Gourmet",
    "product_type": "Canastas de Regalo",
    "tags": "Alimentos, Alimentos Artesanales, Canastas y Regalos Gourmet, Canastas de regalo, Café de especialidad, Bebidas Artesanales, Gourmet, Novedades, Dropshipping",
    "body_html": """
    <h3>Un Pedacito de México en una Caja de Regalo Elegante y Lista para Enviar</h3>
    <p>La <strong>Caja Canasta de Regalo Gourmet Sabores de México</strong> es el obsequio perfecto para celebrar cumpleaños, agradecimientos empresariales, aniversarios o consentir a familiares dentro y fuera de México. Incluye una curaduría exclusiva de tés, tisanas deshidratadas y café de alta gama artesanal.</p>
    <h4>Contenido de la Caja de Regalo:</h4>
    <ul>
      <li><strong>2 Frascos de Tisanas Frutales Artesanales (160g c/u):</strong> Mezcla Perfect Mix (manzana, fresa, arándano, hibisco) y Moras Silvestres (zarzamora, frambuesa, grosella).</li>
      <li><strong>2 Bolsas de Café de Especialidad de Altura (250g c/u):</strong> Granos cosechados en Chiapas y Veracruz de tueste medio.</li>
      <li><strong>Empaque Rústico Premium:</strong> Caja rígida de cartón kraft con viruta protectora de madera, lazo decorativo y tarjeta dedicatoria personalizada.</li>
      <li><strong>Envíos Nacionales e Internacionales:</strong> Lista para entregarse en domicilio en 2 a 5 días hábiles a cualquier estado de la República Mexicana o enviarse a Estados Unidos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/combinacion-especial-regalo-2-tisanas-2-cafestresso-6559227.jpg?v=1787238089", "alt": "Caja Canasta de Regalo Gourmet Edición Grano Entero"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/combinacion-especial-regalo-2-tisanas-2-cafestresso-1213344.jpg?v=1787238089", "alt": "Caja Canasta de Regalo Gourmet Edición Molido Artesanal"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/paquete-dulces-momentostresso-7117495.jpg?v=1787238072", "alt": "Presentación de Regalo con Moño Artesanal"}
    ],
    "options": [{"name": "Variedad de Café"}],
    "variants": [
        {"option1": "Edición Grano Entero", "price": "980.00", "compare_at_price": "1590.00", "sku": "GIFT-BOX-GRN", "inventory_management": None, "requires_shipping": True},
        {"option1": "Edición Molido Artesanal", "price": "980.00", "compare_at_price": "1590.00", "sku": "GIFT-BOX-MOL", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5. SET DE TISANAS FRUTALES ARTESANALES CON INFUSOR DE ACERO
# ─────────────────────────────────────────────────────────────
tisana_set = {
    "title": "Set de Degustación de Tisanas Frutales Artesanales Mexicanas con Infusor de Acero Inoxidable",
    "vendor": "Aylesva Gourmet",
    "product_type": "Tés y Tisanas",
    "tags": "Alimentos, Alimentos Artesanales, Canastas y Regalos Gourmet, Canastas de regalo, Bebidas Artesanales, Gourmet, Novedades, Dropshipping",
    "body_html": """
    <h3>Infusiones 100% Naturales de Fruta Mexicana Deshidratada Sin Cafeína</h3>
    <p>El <strong>Set de Tisanas Frutales Mexicanas Aylesva</strong> ofrece una selección de frutas deshidratadas de temporada, bayas silvestres y flores aromáticas. Se disfrutan tanto calientes en noches frescas como en frappé o té helado refrescante en días soleados.</p>
    <h4>Contenido del Set:</h4>
    <ul>
      <li><strong>2 Frascos Herméticos de Cristal (160g c/u):</strong> Variedades Moras Silvestres y Ponche Frutal Dulce o Perfect Mix.</li>
      <li><strong>Infusor de Acero Inoxidable Grado Alimenticio Incluido:</strong> Malla fina de acero que evita que los trozos de fruta pasen a la taza; fácil de limpiar bajo el grifo.</li>
      <li><strong>100% Libre de Cafeína y Azúcares Añadidos:</strong> Bebida saludable y relajante apta para toda la familia a cualquier hora del día.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/dulce-regalo-2-frascos-de-tisanas-infusortresso-9981073.jpg?v=1787238076", "alt": "Set Moras Silvestres + Ponche Frutal con Infusor"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/dulce-regalo-2-frascos-de-tisanas-infusortresso-8349833.jpg?v=1787238076", "alt": "Set Perfect Mix + Moras Silvestres con Infusor"},
        {"src": "https://cdn.shopify.com/s/files/1/0088/6715/1934/files/coleccion-mini-tisanas-best-sellerstresso-1813778.jpg?v=1787238071", "alt": "Variedad de Frutas Deshidratadas e Infusor"}
    ],
    "options": [{"name": "Selección de Frutas"}],
    "variants": [
        {"option1": "Moras Silvestres + Ponche Frutal (con Infusor)", "price": "540.00", "compare_at_price": "890.00", "sku": "TIS-SET-MRA-PCH", "inventory_management": None, "requires_shipping": True},
        {"option1": "Perfect Mix + Moras Silvestres (con Infusor)", "price": "540.00", "compare_at_price": "890.00", "sku": "TIS-SET-PFX-MRA", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("☕ Iniciando despliegue de Lote 8: Alimentos Tradicionales & Gourmet Mexicanos...")
    
    # 1. Café Chiapas: v0->img0 (Grano), v1->img1 (Molido)
    pid_coffee = create_product_with_variant_images(coffee_chiapas, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 2. Café con Chocolate: v0->img0 (250g), v1->img1 (500g)
    pid_choc = create_product_with_variant_images(coffee_chocolate, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 3. Granos de Café con Chocolate: v0->img0 (150g), v1->img1 (300g)
    pid_beans = create_product_with_variant_images(coffee_beans_chocolate, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 4. Caja Canasta Regalo: v0->img0 (Grano), v1->img1 (Molido)
    pid_basket = create_product_with_variant_images(gift_basket, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 5. Set Tisanas Frutales con Infusor: v0->img0 (Moras+Ponche), v1->img1 (Perfect Mix+Moras)
    pid_tisana = create_product_with_variant_images(tisana_set, {0: 0, 1: 1})
    
    print("\n🎉 ¡Lote 8 de Alimentos Tradicionales & Gourmet Mexicanos desplegado con éxito!")
