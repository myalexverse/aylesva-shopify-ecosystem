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

# 1. Crear o asegurar Smart Collection 'petshop'
def ensure_pet_collection():
    chk_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/smart_collections.json?handle=petshop",
        headers={"X-Shopify-Access-Token": token}
    )
    res = req_with_retry(chk_req).get('smart_collections', [])
    if res:
        cid = res[0]['id']
        print(f"✅ Colección Petshop ya existe: [{cid}] {res[0]['title']}")
        return cid
    
    # Crear Smart Collection
    payload = {
        "smart_collection": {
            "title": "Mascotas y Pet Shop",
            "handle": "petshop",
            "body_html": "<p>Todo para consentir, alimentar y cuidar a tu mejor amigo. Comederos inteligentes, fuentes de agua, transportadoras ergonómicas y accesorios de alta calidad con entrega rápida a todo México.</p>",
            "rules": [
                {
                    "column": "tag",
                    "relation": "equals",
                    "condition": "Mascotas"
                }
            ]
        }
    }
    create_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/smart_collections.json",
        data=json.dumps(payload).encode('utf-8'),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="POST"
    )
    created = req_with_retry(create_req)['smart_collection']
    cid = created['id']
    print(f"🎉 Smart Collection creada: [{cid}] {created['title']} (/{created['handle']})")
    return cid

# 2. Función para crear producto con fotos y variantes 1:1
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
    
    # Esperar a que Shopify procese las imágenes en CDN
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
# PRODUCTO 1: COMEDERO AUTOMÁTICO INTELIGENTE 4L CON APP Y VOZ
# ─────────────────────────────────────────────────────────────
feeder_product = {
    "title": "Comedero Automático Inteligente para Mascotas 4L con Conexión Wi-Fi, Control por App y Grabación de Voz",
    "vendor": "Aylesva Pets",
    "product_type": "Comederos Inteligentes",
    "tags": "Mascotas, Hogar, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Alimentación Precisa y Saludable para tu Mascota, Incluso Cuando No Estás en Casa</h3>
    <p>El <strong>Comedero Automático Inteligente para Mascotas Aylesva Pets 4L</strong> te permite programar y monitorear las comidas de tu perro o gato directamente desde tu smartphone. Olvídate de preocuparte si te retrasas en el trabajo o sales de viaje: programa hasta 10 porciones al día con gramos exactos para prevenir obesidad y reflujo gástrico.</p>
    <h4>Ventajas y Especificaciones Técnicas:</h4>
    <ul>
      <li><strong>Control Remoto por Aplicación Móvil (iOS / Android):</strong> Configura horarios regulares de alimentación y activa dispensado manual extra desde cualquier lugar con un solo toque.</li>
      <li><strong>Grabadora de Voz Personalizada (10 Segundos):</strong> Graba un mensaje cariñoso que se reproducirá automáticamente cada vez que se sirva la comida, haciendo que tu mascota se sienta acompañada.</li>
      <li><strong>Sistema Anti-Atascos Patentado:</strong> Rotor de silicona flexible de 360° compatible con croquetas y alimento seco de 2 a 12 mm sin riesgo de bloqueos.</li>
      <li><strong>Doble Fuente de Alimentación con Respaldo de Batería:</strong> Funciona conectado a la corriente eléctrica vía cable USB e integra compartimento de baterías de emergencia para garantizar la comida aun durante cortes de luz.</li>
      <li><strong>Plato de Acero Inoxidable Grado Alimenticio Desmontable:</strong> Previene el acné felino y la acumulación de bacterias; apto para lavavajillas.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/fresh-element-solo-mobile-connection.png?v=1762930206", "alt": "Blanco Nórdico - Comedero Automático Inteligente"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/petkit-yumshare-dual-hopper-2-cat-feeder-ai-camera-2-year-warranty.png?v=1773383821", "alt": "Gris Grafito - Comedero Automático Inteligente"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/fresh-element-solo-fresh-bite.jpg?v=1762930245", "alt": "Dispensado Fresco y Plato Higiénico"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/pet-feeder-feeding-log-overview.jpg?v=1773383821", "alt": "Monitoreo en Tiempo Real desde Smartphone"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Nórdico (4 Litros)", "price": "1090.00", "compare_at_price": "1890.00", "sku": "PET-FEED-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Gris Grafito (4 Litros)", "price": "1090.00", "compare_at_price": "1890.00", "sku": "PET-FEED-GRY", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# PRODUCTO 2: FUENTE DE AGUA INALÁMBRICA SILENCIOSA 3.2L
# ─────────────────────────────────────────────────────────────
fountain_product = {
    "title": "Fuente de Agua Inalámbrica para Mascotas 3.2L con Bomba Ultra Silenciosa y Sistema de Filtración Cuádruple",
    "vendor": "Aylesva Pets",
    "product_type": "Fuentes e Hidratación",
    "tags": "Mascotas, Hogar, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Agua Viva, Oxigenada y Siempre Fresca para Proteger los Riñones de tu Mascota</h3>
    <p>Los gatos y perros por instinto prefieren beber agua en movimiento. La <strong>Fuente de Agua Inteligente Aylesva Pets 3.2L</strong> recrea una corriente cristalina de manantial que los estimula a hidratarse constantemente, ayudando a prevenir cálculos urinarios e infecciones renales crónicas.</p>
    <h4>Características Destacadas:</h4>
    <ul>
      <li><strong>Bomba de Inducción Magnética Ultra Silenciosa (&lt;20 dB):</strong> Apenas perceptible en dormitorios durante la noche. Funcionamiento suave sin vibraciones molestas.</li>
      <li><strong>Sistema de Filtración Cuádruple Profunda:</strong> Malla micrométrica para pelos y residuos, carbón activado de cáscara de coco que elimina olores y cloro, e resina de intercambio iónico que suaviza metales pesados del agua corriente.</li>
      <li><strong>Capacidad Familiar de 3.2 Litros:</strong> Abastece de agua limpia y potable a un gato o perro mediano por hasta 10 días sin necesidad de rellenar a diario.</li>
      <li><strong>Sensor LED Inteligente de Nivel de Agua:</strong> Luz azul suave nocturna indicadora de nivel que cambia a rojo y apaga la bomba automáticamente si el nivel es bajo para evitar daños.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/eversweet-max-cordless-pet-water-fountain-app-control.png?v=1766732707", "alt": "Fuente de Agua Inteligente para Mascotas 3.2L"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/eversweet-max-cordless-pet-water-fountain-cat-drinking.jpg?v=1766732789", "alt": "Mascota Bebiendo Agua Fresca Oxigenada"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/eversweet-max-cordless-battery-operated-wireless-design.jpg?v=1766732898", "alt": "Diseño Ergonómico Inalámbrico y Bomba Silenciosa"}
    ],
    "options": [{"name": "Edición"}],
    "variants": [
        {"option1": "Blanco Polar 3.2L + Kit de 3 Filtros", "price": "790.00", "compare_at_price": "1390.00", "sku": "PET-FOUNT-3L", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# PRODUCTO 3: MOCHILA TRANSPORTADORA PANORÁMICA CON VENTILACIÓN
# ─────────────────────────────────────────────────────────────
carrier_product = {
    "title": "Mochila Transportadora Ergonómica Panorámica para Mascotas con Malla de Ventilación y Bolsillos Térmicos",
    "vendor": "Aylesva Pets",
    "product_type": "Transportadoras y Viaje",
    "tags": "Mascotas, Accesorios, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Paseos Cómodos, Seguros y con Visión Panorámica para tu Mejor Amigo</h3>
    <p>La <strong>Mochila Transportadora Panorámica Aylesva Breezy</strong> está concebida para brindar máxima comodidad tanto a tu mascota como a ti en visitas al veterinario, viajes por carretera, paseos en bicicleta o caminatas urbanas. Aprobada para aerolíneas como equipaje de cabina bajo el asiento.</p>
    <h4>Puntos Clave de Seguridad y Confort:</h4>
    <ul>
      <li><strong>Ventana Panorámica Tintada Antirreflejos:</strong> Permite que tu gato o perro pequeño explore el paisaje exterior sin encandilarse con los rayos directos del sol.</li>
      <li><strong>Sistema Multicanal de Ventilación y Malla Transpirable:</strong> Orificios estratégicos perimetrales y malla reforzada de alta densidad que garantizan flujo continuo de aire fresco.</li>
      <li><strong>Correas Ergonómicas Acolchadas y Soporte Lumbar:</strong> Distribuyen el peso equitativamente sobre hombros y espalda, reduciendo la fatiga en caminatas largas.</li>
      <li><strong>Mosquetón Interior de Seguridad:</strong> Engancha el arnés de tu mascota para evitar cualquier intento de escape al abrir la cremallera.</li>
      <li><strong>Capacidad:</strong> Ideal para gatos de hasta 8 kg y cachorros o perros miniatura de hasta 6.5 kg.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/products/breezy-2-cat-carrier-cream-white-product-display.png?v=1766743121", "alt": "Blanco Crema - Mochila Transportadora Panorámica"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/products/breezy-2-cat-carrier-gradient-pink-blue-product-display.png?v=1766744586", "alt": "Rosa & Azul Pastel - Mochila Transportadora Panorámica"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/products/breezy-2-cat-carrier-cream-white-wearing.jpg?v=1766743143", "alt": "Paseo Cómodo con Soporte Ergonómico"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/products/breezy-2-cat-carrier-multiple-ventilation-holes.jpg?v=1766743166", "alt": "Malla y Ventilación Activa Respirable"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Crema", "price": "890.00", "compare_at_price": "1490.00", "sku": "PET-BAG-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Rosa & Azul Pastel", "price": "890.00", "compare_at_price": "1490.00", "sku": "PET-BAG-PNK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# PRODUCTO 4: ARENERO AUTOMÁTICO AUTOLIMPIABLE INTELIGENTE
# ─────────────────────────────────────────────────────────────
litterbox_product = {
    "title": "Arenero Automático Inteligente Autolimpiable para Gatos con Sensor de Presencia y Control Anti-Olor",
    "vendor": "Aylesva Pets",
    "product_type": "Higiene y Areneros",
    "tags": "Mascotas, Hogar, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Adiós a la Pala: Limpieza 100% Manos Libres y Cero Olores en tu Hogar</h3>
    <p>El <strong>Arenero Automático Inteligente Aylesva Purobot</strong> separa de manera completamente autónoma los desechos de arena limpia después de que tu gato hace sus necesidades, depositándolos en un compartimento sellado hermético que neutraliza los malos olores al instante.</p>
    <h4>Seguridad y Tecnología de Punta:</h4>
    <ul>
      <li><strong>Protección de Seguridad con Sensores Infrarrojos Cuádruples:</strong> El mecanismo se detiene instantáneamente si el gato se acerca o intenta ingresar durante el ciclo de limpieza.</li>
      <li><strong>Módulo Generador de Iones Desodorizantes:</strong> Elimina hasta el 99.8% de las moléculas causantes del olor y desinfecta el ambiente de manera continua sin fragancias químicas agresivas.</li>
      <li><strong>Diseño Abierto de Fácil Acceso:</strong> Excelente para gatitos desde 1.5 kg hasta gatos grandes de 9 kg sin la sensación de encierro de los areneros cerrados tradicionales.</li>
      <li><strong>Bolsa Sellada de Gran Capacidad:</strong> Un solo gato puede usarlo hasta por 14 días sin necesidad de vaciar el depósito de residuos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/purobot-crystal-duo-automatic-cat-litter-box-with-ai-camera-2-year-warranty.png?v=1773392845", "alt": "Blanco Perla - Arenero Automático Inteligente"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/PETKIT_Gray_Purobot_Crystal_Duo_product_pic.png?v=1773827190", "alt": "Gris Espacial - Arenero Automático Inteligente"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/purobot-crystal-duo-automatic-cat-litter-box-with-a-cat.jpg?v=1773392845", "alt": "Comodidad y Amplitud para Gatos"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/purobot-crystal-duo-open-top-safe-design.jpg?v=1773392845", "alt": "Diseño Seguro Antiatrapamiento"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Perla", "price": "2490.00", "compare_at_price": "3990.00", "sku": "PET-LIT-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Gris Espacial", "price": "2490.00", "compare_at_price": "3990.00", "sku": "PET-LIT-GRY", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# PRODUCTO 5: CEPILLO A VAPOR MASAJEADOR AUTOLIMPIABLE 3 EN 1
# ─────────────────────────────────────────────────────────────
brush_product = {
    "title": "Cepillo Removedor de Pelo al Vapor y Masajeador 3 en 1 para Perros y Gatos con Carga USB",
    "vendor": "Aylesva Pets",
    "product_type": "Aseo y Cuidado Mascota",
    "tags": "Mascotas, Accesorios, Cuidado Personal, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Despídete del Pelo Suelto y Dale a tu Mascota una Sesión de Spa Relajante</h3>
    <p>El <strong>Cepillo a Vapor 3 en 1 para Mascotas</strong> es la solución definitiva para mantener tu ropa y muebles libres de pelo mientras consientes a tu mascota. Su tecnología de micro-nebulización tibia afloja el pelo muerto, disuelve la suciedad acumulada y elimina la estática sin empapar el pelaje.</p>
    <h4>Beneficios Exclusivos:</h4>
    <ul>
      <li><strong>Cerdas Suaves de Silicona con Puntas Redondeadas:</strong> No lastiman la piel sensible; desenredan suavemente y proporcionan un agradable masaje que activa la circulación sanguínea.</li>
      <li><strong>Niebla Fina Antiestática:</strong> Evita que los pelos vuelen por el aire durante el cepillado; quedan atrapados prolijamente en el cepillo.</li>
      <li><strong>Compatible con Esencias y Suavizantes de Pelaje:</strong> Agrega agua tibia y unas gotas de aceite desenredante para dejar el pelaje brillante, suave y perfumado.</li>
      <li><strong>Batería Recargable USB de Larga Duración:</strong> Hasta 2 semanas de cepillados diarios con una sola carga de 30 minutos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/front-entry-hood-with-purobot-crystal-duo.png?v=1765251561", "alt": "Verde Menta - Cepillo Masajeador a Vapor"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/front-entry-hood-odor-control.jpg?v=1765251724", "alt": "Amarillo Canario - Cepillo Masajeador a Vapor"},
        {"src": "https://cdn.shopify.com/s/files/1/0569/0526/9388/files/cat-litter-pad-max-3-2x-anti-sticking-performance-upgrade.jpg?v=1784533437", "alt": "Detalle Cerdas de Silicona y Botón de Vapor"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Verde Menta Spa", "price": "360.00", "compare_at_price": "620.00", "sku": "PET-BRSH-GRN", "inventory_management": None, "requires_shipping": True},
        {"option1": "Amarillo Canario", "price": "360.00", "compare_at_price": "620.00", "sku": "PET-BRSH-YEL", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("🐾 Iniciando despliegue de Lote 7: Mascotas / Pet Shop...")
    
    # Asegurar colección
    cid = ensure_pet_collection()
    time.sleep(1.0)
    
    # 1. Comedero inteligente: v0->img0 (Blanco), v1->img1 (Gris)
    pid_feeder = create_product_with_variant_images(feeder_product, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 2. Fuente de agua: v0->img0
    pid_fountain = create_product_with_variant_images(fountain_product, {0: 0})
    time.sleep(1.2)
    
    # 3. Transportadora: v0->img0 (Blanco), v1->img1 (Rosa)
    pid_carrier = create_product_with_variant_images(carrier_product, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 4. Arenero automático: v0->img0 (Blanco), v1->img1 (Gris)
    pid_litter = create_product_with_variant_images(litterbox_product, {0: 0, 1: 1})
    time.sleep(1.2)
    
    # 5. Cepillo a vapor: v0->img0 (Verde), v1->img1 (Amarillo)
    pid_brush = create_product_with_variant_images(brush_product, {0: 0, 1: 1})
    
    print("\n🎉 ¡Lote 7 de Mascotas / Pet Shop desplegado exitosamente!")
