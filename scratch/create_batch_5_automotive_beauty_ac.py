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

def create_product_with_variant_images(product_data, variant_image_index_map, custom_collection_ids=None):
    payload = {"product": product_data}
    req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products.json",
        data=json.dumps(payload).encode('utf-8'),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, context=ctx) as resp:
        created = json.loads(resp.read().decode('utf-8'))['product']
        pid = created['id']
        print(f"\n✅ Creado: [{pid}] {created['title']}")
        
        # Esperar a que Shopify procese las imágenes en CDN
        time.sleep(1.3)
        
        # Obtener el producto actualizado con sus IDs de imágenes
        get_req = urllib.request.Request(
            f"https://{shop}/admin/api/2024-01/products/{pid}.json",
            headers={"X-Shopify-Access-Token": token}
        )
        with urllib.request.urlopen(get_req, context=ctx) as get_resp:
            product_fresh = json.loads(get_resp.read().decode('utf-8'))['product']
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
                    with urllib.request.urlopen(v_req, context=ctx) as v_resp:
                        v_res = json.loads(v_resp.read().decode('utf-8'))['variant']
                        print(f"   🎯 Variante '{v_res['title']}' vinculada a foto {img_idx+1} (ID: {v_res['image_id']})")
                    time.sleep(0.4)
                    
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
                    with urllib.request.urlopen(c_req, context=ctx) as c_resp:
                        print(f"   📂 Agregado a colección manual ID {cid}")
                except Exception as e:
                    print(f"   ⚠️ Error agregando a colección {cid}: {e}")
                time.sleep(0.3)
                    
        return pid

def update_product_tags(pid, additional_tag):
    try:
        get_req = urllib.request.Request(
            f"https://{shop}/admin/api/2024-01/products/{pid}.json",
            headers={"X-Shopify-Access-Token": token}
        )
        with urllib.request.urlopen(get_req, context=ctx) as get_resp:
            p = json.loads(get_resp.read().decode('utf-8'))['product']
            current_tags = [t.strip() for t in p.get('tags', '').split(',') if t.strip()]
            if additional_tag not in current_tags:
                current_tags.append(additional_tag)
                new_tags = ', '.join(current_tags)
                put_payload = {"product": {"id": pid, "tags": new_tags}}
                put_req = urllib.request.Request(
                    f"https://{shop}/admin/api/2024-01/products/{pid}.json",
                    data=json.dumps(put_payload).encode('utf-8'),
                    headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                    method="PUT"
                )
                with urllib.request.urlopen(put_req, context=ctx) as put_resp:
                    print(f"🏷️ Producto [{pid}] {p['title'][:35]}... actualizado con tag: '{additional_tag}'")
            else:
                print(f"ℹ️ Producto [{pid}] ya contaba con el tag '{additional_tag}'")
    except Exception as e:
        print(f"⚠️ Error actualizando tags para [{pid}]: {e}")

# ─────────────────────────────────────────────────────────────
# 1. ARRANCADOR DE BATERÍA Y COMPRESOR 2 EN 1 (2000A / 160 PSI)
# ─────────────────────────────────────────────────────────────
jump_compressor = {
    "title": "Arrancador de Batería y Compresor de Aire Digital Portátil 2 en 1 (2000A / 160 PSI) con Power Bank y Linterna LED SOS",
    "vendor": "Aylesva Auto",
    "product_type": "Herramientas Automotrices",
    "tags": "Herramientas automotrices, Vehículos, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Seguridad Total en Carretera: Arranca Motores Muertos e Infla Llantas en Minutos</h3>
    <p>El <strong>Arrancador de Batería y Compresor de Aire Digital 2 en 1</strong> es el equipo de emergencia automotriz definitivo. Diseñado para brindar independencia absoluta frente a imprevistos viales, combina una potencia de arranque de 2000A pico capaz de encender motores de gasolina de hasta 4.0L y diesel de 3.0L con batería totalmente descargada, junto con un compresor digital de 160 PSI de parada automática.</p>
    <h4>Características Principales:</h4>
    <ul>
      <li><strong>Arrancador 2000A Pico con Función Force Start:</strong> Pinzas inteligentes a prueba de chispas y polaridad invertida. Enciende tu auto en segundos sin necesidad de pedir corriente a otro vehículo.</li>
      <li><strong>Compresor Digital de Alta Velocidad (160 PSI):</strong> Motor de 22,000 RPM que infla un neumático de 28 a 35 PSI en solo 60 segundos con sensor digital y corte automático de presión.</li>
      <li><strong>Batería de Litio 8000mAh Power Bank:</strong> Carga smartphones, tablets y accesorios mediante puerto USB de carga rápida.</li>
      <li><strong>Linterna LED de Emergencia Multifunción:</strong> Luz continua potente, estroboscópica y señal SOS para averías nocturnas en carretera.</li>
      <li><strong>Set Completo Incluido:</strong> Pinzas inteligentes, manguera de aire, 3 boquillas adaptadoras (bicicleta, balones, inflables), cable de carga y estuche protector.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0609/9225/8262/files/1_edabeb07-3eec-48f4-a54e-746caab4105f.jpg?v=1789121897", "alt": "Negro Titanio - Arrancador y Compresor 2 en 1"},
        {"src": "https://cdn.shopify.com/s/files/1/0609/9225/8262/files/1_5e0decd7-371f-42d8-a1f1-3e65d206bb27.jpg?v=1789121959", "alt": "Naranja Rescate - Arrancador y Compresor 2 en 1"},
        {"src": "https://cdn.shopify.com/s/files/1/0609/9225/8262/files/2_ce1013ab-01e6-448c-87d9-ae64cf0eca06.jpg?v=1789121901", "alt": "Pantalla Digital LCD y Conexión Rápida"},
        {"src": "https://cdn.shopify.com/s/files/1/0609/9225/8262/files/3_c0687832-eb09-4283-9cef-611954e188fb.jpg?v=1789121907", "alt": "Pinzas Inteligentes Anti Chispas y Manguera"},
        {"src": "https://cdn.shopify.com/s/files/1/0609/9225/8262/files/4_64bc2bfe-29b4-4d2f-84e1-0b695f3ffe3a.jpg?v=1789121911", "alt": "Inflado de Neumáticos en Carretera"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Titanio", "price": "1690.00", "compare_at_price": "2850.00", "sku": "JMP-X5-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Naranja Rescate", "price": "1690.00", "compare_at_price": "2850.00", "sku": "JMP-X5-ORN", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 2. ENFRIADOR Y AIRE ACONDICIONADO PORTÁTIL OSCILANTE 90°
# ─────────────────────────────────────────────────────────────
air_conditioner = {
    "title": "Aire Acondicionado y Enfriador Portátil de Torre Sin Ventana con Control Remoto y Oscilación 90°",
    "vendor": "Aylesva Living",
    "product_type": "Climatización y Ventilación",
    "tags": "Aires acondicionados y ventiladores, Hogar, Electrodomésticos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Frescura Inmediata y Silenciosa sin Instalaciones Complejas de Ventana</h3>
    <p>El <strong>Enfriador y Aire Acondicionado Portátil de Torre</strong> brinda un flujo continuo de aire fresco y purificado para recámaras, salas y departamentos sin necesidad de perforar paredes ni instalar pesados ductos exteriores. Su potente turbina aerodinámica impulsa aire a velocidades de hasta 25 pies por segundo con oscilación gran angular de 90°.</p>
    <h4>Beneficios Clave:</h4>
    <ul>
      <li><strong>4 Modos de Confort Inteligente:</strong> Modo Normal, Brisa Natural, Modo Nocturno ultrasilencioso para dormir fresco y Modo Automático de ahorro energético.</li>
      <li><strong>Oscilación Panorámica de 90 Grados:</strong> Distribuye el aire de forma homogénea eliminando bolsas de calor en toda la habitación.</li>
      <li><strong>Temporizador Programable de 12 Horas:</strong> Apagado automático nocturno para ahorrar electricidad mientras descansas placenteramente.</li>
      <li><strong>Control Remoto de Largo Alcance:</strong> Modifica velocidad, modos y temporizador cómodamente desde tu cama o sillón.</li>
      <li><strong>Estructura Slim de Fácil Limpieza:</strong> Ocupa solo 30x30 cm de espacio en el suelo y cuenta con filtro desmontable y lavable.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/Gemini_Generated_Image_mjo2pzmjo2pzmjo2.jpg?v=1772909746", "alt": "Aire Acondicionado Portátil de Torre en Recámara"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/Gemini_Generated_Image_8bimuk8bimuk8bim.jpg?v=1772909746", "alt": "Diseño Slim Vertical Minimalista"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/Gemini_Generated_Image_qvofriqvofriqvof.jpg?v=1772909746", "alt": "Panel Táctil Superior y Control Remoto"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/imageye___-_imgi_1_51daVRx2bxL._AC_SL1324.jpg?v=1772909746", "alt": "Flujo de Aire Oscilante 90 Grados"}
    ],
    "options": [{"name": "Modelo"}],
    "variants": [
        {"option1": "Blanco Polar Slim 35\"", "price": "1490.00", "compare_at_price": "2490.00", "sku": "AC-TWR-35WHT", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3. SECADOR Y MOLDEADOR DE CABELLO IÓNICO SLOPEHILL (110K RPM)
# ─────────────────────────────────────────────────────────────
hair_dryer = {
    "title": "Secador y Moldeador de Cabello Profesional Iónico Slopehill de Alta Velocidad (110,000 RPM) con Boquillas Magnéticas",
    "vendor": "Aylesva Beauty",
    "product_type": "Cuidado del Cabello",
    "tags": "Cuidado del cabello Mujer, Damas, Mujer, Cuidado Personal, Electrónicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Secado Ultrarrápido en Menos de 4 Minutos Protegiendo el Brillo Natural</h3>
    <p>El <strong>Secador de Cabello Profesional Iónico Slopehill</strong> incorpora un motor digital brushless de 110,000 RPM que genera un flujo de aire supersónico de 26 m/s, reduciendo el tiempo de secado a la mitad sin maltratar las fibras capilares por exceso de calor.</p>
    <h4>Tecnología y Accesorios de Salón:</h4>
    <ul>
      <li><strong>Emisión de 200 Millones de Iones Negativos:</strong> Neutraliza el frizz al instante, sella la cutícula y potencia el brillo sedoso natural de tu cabello.</li>
      <li><strong>Control Térmico Inteligente con Sensor de Calor Constante:</strong> Monitorea la temperatura 50 veces por segundo para evitar quemaduras o resequedad.</li>
      <li><strong>Boquillas Magnéticas Giratorias 360°:</strong> Incluye boquilla concentradora de alisado y difusor para definir rizos naturales con cambio magnético instantáneo.</li>
      <li><strong>Ultraligero y Ergonómico (Solo 300g):</strong> Diseñado para estilizar sin fatiga en brazos o muñecas, ideal para uso diario o viajes.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0705/6716/6121/files/03_766702d2-e24e-48b0-97a2-72aef0b05000.jpg?v=1784539972", "alt": "Secador Profesional Iónico Slopehill"},
        {"src": "https://cdn.shopify.com/s/files/1/0705/6716/6121/files/05_deb5c762-3d28-4b88-b7fb-63a897ab822a.jpg?v=1784539972", "alt": "Gris Espacial Metálico"},
        {"src": "https://cdn.shopify.com/s/files/1/0705/6716/6121/files/07_032604a9-4221-4f40-a02b-43a0523a56c8.jpg?v=1784539972", "alt": "Café Moca Elegance"},
        {"src": "https://cdn.shopify.com/s/files/1/0705/6716/6121/files/06_e93b751d-cfc6-4a7f-a48b-33368b048c61.jpg?v=1784539971", "alt": "Boquillas Magnéticas Intercambiables"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Gris Espacial Metálico", "price": "1290.00", "compare_at_price": "2190.00", "sku": "DRY-SLP-GRY", "inventory_management": None, "requires_shipping": True},
        {"option1": "Café Moca Elegance", "price": "1290.00", "compare_at_price": "2190.00", "sku": "DRY-SLP-MOCHA", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4. PROYECTOR PLANETARIO HD GALAXY 360° CON 12 CONSTELACIONES
# ─────────────────────────────────────────────────────────────
planetarium_projector = {
    "title": "Proyector Planetario HD Galaxy 360° con 12 Discos Ópticos de Constelaciones y Temporizador Nocturno",
    "vendor": "Aylesva Living",
    "product_type": "Decoración y Gadgets",
    "tags": "Decoración del Hogar, Hogar, Electrónicos, Gadgets y accesorios tecnológicos, Damas, Dropshipping, Novedades",
    "body_html": """
    <h3>Tu Propio Planetario Astronómico de Alta Definición en el Techo de tu Habitación</h3>
    <p>El <strong>Proyector Planetario HD Galaxy</strong> lleva la majestuosidad del cosmos a tu hogar. A diferencia de las luces de discoteca convencionales, utiliza un sistema de lentes ópticos de ultra alta definición con 12 discos intercambiables reales del telescopio espacial (Sistema Solar, Vía Láctea, Galaxia de Andrómeda, Nebulosas y Cielo Profundo).</p>
    <h4>Características Destacadas:</h4>
    <ul>
      <li><strong>Óptica de Precisión HD 4K:</strong> Enfoque manual giratorio milimétrico que proyecta estrellas nítidas a distancias de 2 hasta 5 metros en techos y paredes.</li>
      <li><strong>12 Discos de Film Fotográfico Astronómico:</strong> Explora diferentes paisajes estelares cada noche según tu estado de ánimo.</li>
      <li><strong>Rotación Lenta Silenciosa 360°:</strong> Emula el giro natural de la bóveda celeste creando un ambiente hipnótico de paz.</li>
      <li><strong>Temporizador de Apagado Nocturno (1h / 2h):</strong> Diseñado especialmente para conciliar el sueño bajo las estrellas sin preocuparse por dejarlo encendido.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/Star-Projector-Galaxy-Projector-wtih-Timer-4K-13-HD-Film-Discsfor-Bedroom-Night-Light-Projector-for-Kids-Adults-Bedroom-Christmas-Decor_52a0f15e-f97c-4adc-bde3-c677126105f4.f351912e48.avif?v=1772622281", "alt": "Proyector Planetario Óptico HD Galaxy"},
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/79c72713-1076-4953-a04a-6e127d78173c.01319ea277cd8b2fa39b76d4eb6d400b.webp?v=1772622281", "alt": "Proyección Galáctica en Techo de Habitación"},
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/4862dde1-84be-41b8-94fe-4afa7f3af218.7e7bb742e68d1b86d3caa10815ece46f.webp?v=1772622281", "alt": "Set de 12 Discos Ópticos Reales"}
    ],
    "options": [{"name": "Edición"}],
    "variants": [
        {"option1": "Edición Planetario HD + 12 Discos", "price": "890.00", "compare_at_price": "1490.00", "sku": "PLN-STAR-12D", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5. ANTENA DIGITAL HDTV 4K INTERIORES CON AMPLIFICADOR SMART
# ─────────────────────────────────────────────────────────────
hdtv_antenna = {
    "title": "Antena Digital HDTV 4K para Interiores de Ultra Largo Alcance con Amplificador de Señal Inteligente",
    "vendor": "Aylesva Tech",
    "product_type": "Electrónicos y Audio",
    "tags": "Electrónicos, Gadgets y accesorios tecnológicos, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Canales Locales en Alta Definición 1080P y 4K Totalmente Gratis</h3>
    <p>La <strong>Antena Digital HDTV 4K de Largo Alcance</strong> te permite sintonizar tus canales de televisión abierta locales (noticieros, deportes, telenovelas y entretenimiento) con la máxima fidelidad de audio y video sin pagar contratos mensuales ni suscripciones de cable.</p>
    <h4>Ventajas y Especificaciones:</h4>
    <ul>
      <li><strong>Chip Amplificador de Señal de Nueva Generación:</strong> Filtra interferencias de telefonía móvil 4G/5G y estabiliza la recepción de señal VHF y UHF.</li>
      <li><strong>Diseño Extra Delgado y Discreto:</strong> Se adhiere fácilmente detrás de la pantalla, en la pared o junto a una ventana mediante adhesivo de alta fijación.</li>
      <li><strong>Cable Coaxial Reforzado de 5 Metros:</strong> Máxima libertad para ubicar la antena en la zona con mejor recepción de la casa.</li>
      <li><strong>Instalación Plug & Play en 2 Minutos:</strong> Conecta directamente a la entrada coaxial de tu TV, realiza una búsqueda automática de canales y listo.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/500MilesUpgradedTVAntennaDigitalHDAntenaIndoorHDTV1080P4KLongRange0.webp?v=1739392041", "alt": "Antena Digital HDTV 4K Ultrafina"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/500MilesUpgradedTVAntennaDigitalHDAntenaIndoorHDTV1080P4KLongRange4.webp?v=1739392040", "alt": "Montaje Fácil en Pared o Ventana"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/500MilesUpgradedTVAntennaDigitalHDAntenaIndoorHDTV1080P4KLongRange14_8563c41d-af35-4a4f-87a4-d243f6d8fdc8.webp?v=1739392041", "alt": "Conexión Plug and Play con Amplificador"}
    ],
    "options": [{"name": "Modelo"}],
    "variants": [
        {"option1": "Negro Ultrafino 4K / 5 Metros", "price": "490.00", "compare_at_price": "890.00", "sku": "ANT-HDTV-4K", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("🚀 Iniciando creación de Lote 5: Activando Herramientas Automotrices, Climatización y Belleza...")
    
    # 1. Arrancador + Compresor 2 en 1: v0->img0 (Negro), v1->img1 (Naranja)
    pid_jmp = create_product_with_variant_images(jump_compressor, {0: 0, 1: 1})
    time.sleep(1.0)
    
    # 2. Aire Acondicionado Portátil: v0->img0 (Blanco Polar)
    pid_ac = create_product_with_variant_images(air_conditioner, {0: 0})
    time.sleep(1.0)
    
    # 3. Secador Slopehill: v0->img1 (Gris), v1->img2 (Café Moca) + Añadido a damas-spot (485516541975)
    pid_dry = create_product_with_variant_images(hair_dryer, {0: 1, 1: 2}, custom_collection_ids=[485516541975])
    time.sleep(1.0)
    
    # 4. Proyector Planetario HD: v0->img0 + Añadido a damas-spot (485516541975)
    pid_star = create_product_with_variant_images(planetarium_projector, {0: 0}, custom_collection_ids=[485516541975])
    time.sleep(1.0)
    
    # 5. Antena HDTV 4K: v0->img0
    pid_ant = create_product_with_variant_images(hdtv_antenna, {0: 0})
    time.sleep(1.0)
    
    # 6. Activar la colección de Limpieza Automotriz vinculando el tag a la Mini Aspiradora
    print("\n🔄 Optimizando tags para activar colección 'Artículos de limpieza automotriz'...")
    update_product_tags(8947077349399, "Artículos de limpieza automotriz")
    
    print("\n🎉 ¡Lote 5 desplegado y colecciones vacías activadas exitosamente!")
