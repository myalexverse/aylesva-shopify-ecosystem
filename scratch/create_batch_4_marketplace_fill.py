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
        time.sleep(1.2)
        
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
                    
        # Si se especificaron colecciones manuales / personalizadas, añadir collects
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
# 1. MINI ASPIRADORA INALÁMBRICA PORTÁTIL 2 EN 1 (AUTO Y HOGAR)
# ─────────────────────────────────────────────────────────────
vacuum_product = {
    "title": "Mini Aspiradora Inalámbrica Portátil 2 en 1 Ciclónica de Alta Potencia para Auto y Hogar",
    "vendor": "Aylesva Auto & Home",
    "product_type": "Aspiradoras y Limpieza",
    "tags": "Aspiradoras y robots de limpieza, Accesorios de interior (tapetes, fundas, etc.), Hogar, Vehículos, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Limpieza Profunda e Instantánea en tu Auto y Espacios del Hogar</h3>
    <p>La <strong>Mini Aspiradora Inalámbrica Ciclónica 2 en 1</strong> ofrece la combinación perfecta de potencia compacta y máxima libertad sin cables. Equipada con un motor digital de alta velocidad capaz de generar una fuerte succión ciclónica, aspira polvo, migajas, pelo de mascotas y arena de las rendijas más difíciles del automóvil, teclados, sofás y muebles del hogar.</p>
    <h4>Características Clave y Especificaciones:</h4>
    <ul>
      <li><strong>Diseño Ultraligero y Portátil:</strong> Pesa menos de 400 gramos, permitiendo maniobrarla cómodamente con una sola mano y guardarla en la guantera o cajón.</li>
      <li><strong>Boquilla Multifuncional 2 en 1:</strong> Incluye boquilla para hendiduras estrechas y cepillo suave integrado para tapicerías, rejillas de ventilación y electrónicos.</li>
      <li><strong>Filtro HEPA Lavable y Reutilizable:</strong> Retiene partículas finas y alérgenos. Se enjuaga con agua corriente sin necesidad de comprar repuestos costosos.</li>
      <li><strong>Batería de Litio Recargable por USB-C:</strong> Carga rápida compatible con cargadores de auto, baterías externas o adaptadores de pared.</li>
      <li><strong>Depósito Transparente de Desarmado Rápido:</strong> Vacía la suciedad con un simple giro sin ensuciarte las manos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://belroshop.com/cdn/shop/files/vacuum_1200x1200.png?v=1745652303", "alt": "Mini Aspiradora Portátil Inalámbrica en Acción"},
        {"src": "https://belroshop.com/cdn/shop/files/download-2025-04-26T151034.671.jpg?v=1745652309", "alt": "Blanco Nórdico Minimalista"},
        {"src": "https://belroshop.com/cdn/shop/files/download-2025-04-26T151034.878.jpg?v=1745652309", "alt": "Verde Menta Nórdico"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Nórdico", "price": "540.00", "compare_at_price": "920.00", "sku": "VAC-MINI-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Verde Menta", "price": "540.00", "compare_at_price": "920.00", "sku": "VAC-MINI-GRN", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 2. MAGNETIC PHONE CAMERA GRIP BLUETOOTH & LED MAGSAFE
# ─────────────────────────────────────────────────────────────
camera_grip = {
    "title": "Magnetic Phone Camera Grip con Disparador Inalámbrico Bluetooth y Luz LED MagSafe",
    "vendor": "Aylesva Tech",
    "product_type": "Accesorios para Celular",
    "tags": "Accesorios para celular (fundas, cargadores, audífonos), Gadgets y accesorios tecnológicos, Electrónicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Transforma tu Smartphone en una Cámara Profesional Ergonómica</h3>
    <p>El <strong>Magnetic Phone Camera Grip</strong> redefine la experiencia fotográfica móvil. Diseñado con una empuñadura ergonómica antideslizante inspirada en las cámaras réflex DSLR, brinda estabilidad milimétrica para capturar fotos con una sola mano, selfies perfectas y transmisiones en vivo sin temblores.</p>
    <h4>Detalles y Funcionalidades:</h4>
    <ul>
      <li><strong>Fijación Magnética Ultra Fuerte:</strong> Alineación instantánea MagSafe compatible con iPhone 12 en adelante y smartphones Android (incluye anillo magnético adhesivo para cualquier teléfono).</li>
      <li><strong>Disparador Bluetooth Desmontable:</strong> Botón obturador inalámbrico recargable que se desmonta para tomar fotos y grabar a distancia hasta 10 metros.</li>
      <li><strong>Luz de Relleno LED Integrada y Desmontable:</strong> 3 temperaturas de color (cálida, neutra y fría) con brillo graduable para iluminar tus tomas en baja iluminación.</li>
      <li><strong>Rosca Universal 1/4\" para Trípode:</strong> Móntalo en trípodes, monopiés o soportes de escritorio para streaming continuo y videollamadas.</li>
    </ul>
    """,
    "images": [
        {"src": "https://oddlyepic.com/cdn/shop/files/Magnetic-Phone-Camera-Grip-and-Light.png?v=1762024886", "alt": "Magnetic Phone Camera Grip con Luz LED MagSafe"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Magnetic_Phone_Camera_Grip_-_Content_Creator_Essentials.avif?v=1762026650", "alt": "Grip Ergonómico Básico (Negro)"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Magnetic_Phone_Camera_Grip_-_Oddly_Epic.avif?v=1762026650", "alt": "Grip + Luz de Relleno LED"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Magnetic-Phone-Camera-Grip_-Tripid-and-Mag-Light.png?v=1762026650", "alt": "Kit Completo (Grip + Luz LED + Trípode)"}
    ],
    "options": [{"name": "Configuración"}],
    "variants": [
        {"option1": "Grip Ergonómico Básico (Negro)", "price": "490.00", "compare_at_price": "850.00", "sku": "GRP-MAG-BASIC", "inventory_management": None, "requires_shipping": True},
        {"option1": "Grip + Luz de Relleno LED", "price": "590.00", "compare_at_price": "990.00", "sku": "GRP-MAG-LIGHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Kit Completo (Grip + Luz LED + Trípode)", "price": "690.00", "compare_at_price": "1190.00", "sku": "GRP-MAG-TRIPOD", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3. LED PIXEL DISPLAY RELOJ AMBIENTAL INTELIGENTE 16X16
# ─────────────────────────────────────────────────────────────
pixel_display = {
    "title": "LED Pixel Display Reloj Ambiental Inteligente 16x16 con Panel RGB Programable y App Control",
    "vendor": "Aylesva Tech",
    "product_type": "Gadgets y Decoración",
    "tags": "Accesorios para celular (fundas, cargadores, audífonos), Gadgets y accesorios tecnológicos, Electrónicos, Hogar, Decoración del Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Arte Retro, Animaciones Personalizadas y Notificaciones en Tiempo Real</h3>
    <p>El <strong>LED Pixel Display Inteligente</strong> es la pieza definitiva para escritorios gamer, oficinas creativas y mesas de noche. Su matriz de 256 LEDs RGB brillantes (16x16) permite proyectar Pixel Art interactivo, animaciones en bucle, hora sincronizada, clima, temporizador pomodoro y visualizador de música con sensor acústico.</p>
    <h4>Funciones Destacadas:</h4>
    <ul>
      <li><strong>Control Total desde tu Celular:</strong> Conexión Bluetooth con app gratuita (iOS y Android) con galería de miles de diseños creados por la comunidad o creador propio.</li>
      <li><strong>Visualizador de Espectro de Audio:</strong> Micrófono de alta sensibilidad integrado que baila y reacciona al ritmo de la música o tu voz.</li>
      <li><strong>Reloj de Mesa y Herramienta de Productividad:</strong> Muestra reloj digital personalizable, cuenta regresiva, cronómetro y notificaciones de redes sociales.</li>
      <li><strong>Alimentación Continua USB:</strong> Conexión estable mediante cable tipo C para funcionamiento permanente en tu estación de trabajo.</li>
    </ul>
    """,
    "images": [
        {"src": "https://oddlyepic.com/cdn/shop/files/LED-Pixel-Display-3.jpg?v=1755641531", "alt": "LED Pixel Display Inteligente Encendido"},
        {"src": "https://oddlyepic.com/cdn/shop/files/LED-Pixel-Display-Controls.jpg?v=1756114648", "alt": "Panel Trasero y Controles Intuitivos"},
        {"src": "https://oddlyepic.com/cdn/shop/files/LED-Pixel-Display-1.jpg?v=1756114648", "alt": "Pixel Art en Escritorio de Trabajo"},
        {"src": "https://oddlyepic.com/cdn/shop/files/LED-Pixel-Display-2.jpg?v=1756114648", "alt": "Animaciones RGB Decorativas"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Mate (Display RGB 16x16)", "price": "890.00", "compare_at_price": "1450.00", "sku": "PIX-DISP-RGB-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4. DESCORCHADOR ELÉCTRICO RECARGABLE DE VINO
# ─────────────────────────────────────────────────────────────
wine_opener = {
    "title": "Descorchador Eléctrico Recargable de Botellas de Vino con Cortador de Sello, Vertedor y Tapón al Vacío",
    "vendor": "Aylesva Living",
    "product_type": "Hogar y Cocina",
    "tags": "Hogar, Decoración del Hogar, Cocina, Mujer, Damas, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Abre tus Vinos en Menos de 6 Segundos sin Ningún Esfuerzo</h3>
    <p>El <strong>Set de Descorchador Eléctrico Recargable</strong> es el accesorio de sofisticación imprescindible para amantes del buen vino, cenas con invitados y celebraciones especiales. Olvídate de los corchos rotos o la fuerza manual: con solo presionar un botón, el mecanismo espiral de precisión extrae y expulsa el corcho suavemente de forma automática.</p>
    <h4>Set Integral 4 en 1 Incluye:</h4>
    <ul>
      <li><strong>Descorchador Automático de Alta Eficiencia:</strong> Abre hasta 40 botellas con una sola carga rápida. Cuenta con ventana transparente y luz LED indicadora.</li>
      <li><strong>Cortador de Sellos de Aluminio:</strong> Retira las cápsulas protectoras del cuello de la botella de forma limpia y segura con un solo giro.</li>
      <li><strong>Aireador y Vertedor Antigoteo:</strong> Oxigena el vino al servirlo para despertar sus notas aromáticas evitando derrames en el mantel.</li>
      <li><strong>Tapón Preservador al Vacío:</strong> Extrae el oxígeno sobrante de la botella abierta para mantener el sabor y frescura del vino hasta por 7 días.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/image_20_36426099-eff4-4d6b-a9a9-9d5c8754dfa9.jpg?v=1739905262", "alt": "Set de Descorchador Eléctrico Recargable con Accesorios"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/image_21_001c70ae-4ae8-4b27-b157-d90a9acca688.jpg?v=1739905525", "alt": "Descorche Automático en 6 Segundos"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/image_23_36cbddd9-8006-4fd4-bcdd-ce0abe6c9969.jpg?v=1739905618", "alt": "Vertedor Aireador y Tapón al Vacío"},
        {"src": "https://cdn.shopify.com/s/files/1/0178/9896/3044/files/image_24_e1953fd5-0b20-4f0f-ad6b-cd747c8cd49a.jpg?v=1739905703", "alt": "Empaque y Presentación de Regalo Elegante"}
    ],
    "options": [{"name": "Acabado"}],
    "variants": [
        {"option1": "Negro Satinado Premium", "price": "590.00", "compare_at_price": "990.00", "sku": "WNE-OPEN-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5. RELOJ DESPERTADOR INTELIGENTE SUNRISE WAKE-UP LIGHT
# ─────────────────────────────────────────────────────────────
sunrise_light = {
    "title": "Reloj Despertador Inteligente Sunrise Wake-Up Light con Simulación de Amanecer, 10 Modos de Luz RGB y Sonidos Naturales",
    "vendor": "Aylesva Living",
    "product_type": "Hogar y Bienestar",
    "tags": "Hogar, Decoración del Hogar, Mujer, Damas, Cuidado Personal, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Despierta Renovado con la Luz Natural del Sol y Duerme con Calma Profunda</h3>
    <p>Inspirado en los ritmos circadianos naturales del cuerpo humano, el <strong>Reloj Despertador Sunrise Wake-Up Light</strong> transforma tus mañanas y noches. En lugar de ruidos estridentes que elevan el cortisol, incrementa gradualmente una cálida luz ámbar de 0% a 100% emulando un amanecer real, estimulando al cuerpo a despertar de manera fresca, lúcida y de buen humor.</p>
    <h4>Beneficios Clínicos y Tecnológicos:</h4>
    <ul>
      <li><strong>Simulación de Amanecer y Atardecer:</strong> Temporizador graduable de 10 a 60 minutos para conciliar el sueño con penumbra relajante y despertar de forma natural.</li>
      <li><strong>10 Efectos de Iluminación Ambiental RGB:</strong> Desde luz de lectura cálida hasta gradientes multicolor para crear la atmósfera perfecta en tu recámara.</li>
      <li><strong>Sonidos de la Naturaleza y Alarma Dual:</strong> Configura 2 horarios independientes de alarma con cantos de pájaros, olas de mar o arroyo suave.</li>
      <li><strong>Función Snooze Inteligente:</strong> 9 minutos adicionales de descanso con un simple toque suave táctil.</li>
      <li><strong>Puerto de Carga USB Integrado:</strong> Carga tu smartphone cómodamente junto a tu cama durante la noche.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/b61ac2a9-1bb5-4b97-a31d-cfafda936678.jpg?v=1779656206", "alt": "Reloj Despertador Sunrise Wake-Up Light con Efecto Amanecer"},
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/f4c351e6-be19-403d-87d3-42f98044de63.jpg?v=1779656206", "alt": "Iluminación Suave en Mesa de Noche"},
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/1c1f1a80-366c-458f-a861-5c32916fee19.jpg?v=1779656206", "alt": "Efectos Cromáticos Ambientales RGB"},
        {"src": "https://cdn.shopify.com/s/files/1/0818/9699/7182/files/e9ca8338-58b5-42d8-8385-45c062b685cc.jpg?v=1779656206", "alt": "Display Digital Intuitivo y Ajuste Táctil"}
    ],
    "options": [{"name": "Modelo"}],
    "variants": [
        {"option1": "Blanco Puro Sunrise RGB", "price": "890.00", "compare_at_price": "1490.00", "sku": "WAKE-SUN-RGB", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("🚀 Iniciando creación de Lote 4: Solución a Colecciones Vacías del Marketplace...")
    
    # 1. Mini Aspiradora: v0->img1 (Blanco Nórdico), v1->img2 (Verde Menta)
    pid_vac = create_product_with_variant_images(vacuum_product, {0: 1, 1: 2})
    time.sleep(1.0)
    
    # 2. Camera Grip: v0->img1 (Básico), v1->img2 (Con Luz LED), v2->img3 (Kit Completo Trípode)
    pid_grip = create_product_with_variant_images(camera_grip, {0: 1, 1: 2, 2: 3})
    time.sleep(1.0)
    
    # 3. LED Pixel Display: v0->img0 (Display RGB 16x16)
    pid_pix = create_product_with_variant_images(pixel_display, {0: 0})
    time.sleep(1.0)
    
    # 4. Descorchador Eléctrico: v0->img0 (Negro Satinado) + Añadido a damas-spot (485516541975)
    pid_wine = create_product_with_variant_images(wine_opener, {0: 0}, custom_collection_ids=[485516541975])
    time.sleep(1.0)
    
    # 5. Sunrise Wake-Up Light: v0->img0 (Blanco Puro Sunrise RGB) + Añadido a damas-spot (485516541975)
    pid_sun = create_product_with_variant_images(sunrise_light, {0: 0}, custom_collection_ids=[485516541975])
    time.sleep(1.0)
    
    # 6. Actualizar tags de los productos de audio y carga de Lote 3 para enriquecer la colección de celulares
    print("\n🔄 Optimizando tags de productos complementarios de lote 3...")
    update_product_tags(8947043467287, "Accesorios para celular (fundas, cargadores, audífonos)") # Audífonos ST99
    update_product_tags(8947043270679, "Accesorios para celular (fundas, cargadores, audífonos)") # Cargador 3 en 1 MagSafe
    
    print("\n🎉 ¡Lote 4 desplegado y colecciones vacías activadas exitosamente!")
