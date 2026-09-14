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

def create_product_with_variant_images(product_data, variant_image_index_map):
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
        
        # Esperar a que Shopify procese las imágenes
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
        return pid

# ─────────────────────────────────────────────────────────────
# 1. DIFUSOR Y HUMIDIFICADOR ULTRASÓNICO EFECTO LLAMA DE FUEGO
# ─────────────────────────────────────────────────────────────
flame_diffuser = {
    "title": "Difusor y Humidificador Ultrasónico de Aromas con Efecto Llama de Fuego LED y Apagado Automático",
    "vendor": "Aylesva Living",
    "product_type": "Hogar y Decoración",
    "tags": "Hogar, Decoración del Hogar, Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Atmósfera de Calidez y Relajación con Efecto de Fuego Real</h3>
    <p>El <strong>Difusor de Aromas con Efecto Llama de Fuego</strong> transforma cualquier habitación u oficina en un santuario de paz. Combina tecnología ultrasónica silenciosa de niebla fría con luces LED de alta precisión que simulan el hipnótico resplandor de una chimenea encendida, 100% libre de quemaduras o peligro.</p>
    <h4>Características Destacadas:</h4>
    <ul>
      <li><strong>Efecto de Llama Realista:</strong> Iluminación LED sincronizada con vaporización en frío que emula el vaivén del fuego natural sin calor ni humo.</li>
      <li><strong>Aromaterapia Eficiente:</strong> Compatible con aceites esenciales naturales para purificar el ambiente y reducir el estrés diario.</li>
      <li><strong>Operación Ultrasónica Silenciosa:</strong> Nivel sonoro menor a 30 dB, ideal para descansar, estudiar o meditar sin interrupciones.</li>
      <li><strong>Sistema de Seguridad Inteligente:</strong> Apagado automático preventivo de chip inteligente cuando el nivel de agua en el tanque es bajo.</li>
      <li><strong>Alimentación Universal USB-C:</strong> Conéctalo fácilmente a adaptadores de pared, laptop o batería portátil.</li>
    </ul>
    """,
    "images": [
        {"src": "https://elevatohome.com/cdn/shop/files/1_LE_auto_x2_1_79966382-1da0-4ebe-a26a-484a5a7bf887.jpg?v=1722329701", "alt": "Difusor Efecto Llama de Fuego LED Encendido"},
        {"src": "https://elevatohome.com/cdn/shop/files/11_O1CN01Vx3ZD11DX5yCoebYI__2212410720225-0-cib.png?v=1722329029", "alt": "Negro Obsidiana"},
        {"src": "https://elevatohome.com/cdn/shop/files/10_O1CN01DMiSs21DX5yB2p9xk__2212410720225-0-cib.png?v=1722329043", "alt": "Blanco Minimalista"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Obsidiana", "price": "690.00", "compare_at_price": "1150.00", "sku": "DIF-FLAME-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Blanco Minimalista", "price": "690.00", "compare_at_price": "1150.00", "sku": "DIF-FLAME-WHT", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 2. HUMIDIFICADOR Y DIFUSOR EFECTO MEDUSA FLOTANTE
# ─────────────────────────────────────────────────────────────
jellyfish_diffuser = {
    "title": "Humidificador y Difusor Ultrasónico Efecto Medusa Flotante con Anillos de Vapor y Luz Ambiental LED",
    "vendor": "Aylesva Living",
    "product_type": "Hogar y Decoración",
    "tags": "Hogar, Decoración del Hogar, Electrónicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Experiencia Visual Única: Anillos de Niebla en Forma de Medusa</h3>
    <p>El <strong>Difusor Efecto Medusa Flotante</strong> introduce un concepto fascinante de relajación y decoración de interiores. Gracias a su cámara de vórtice oscilante, expulsa rítmicos anillos circulares de vapor frío que flotan suavemente por el aire emulando el nado etéreo de las medusas marinas.</p>
    <h4>Beneficios y Especificaciones:</h4>
    <ul>
      <li><strong>Doble Modo de Humidificación:</strong> Modo pulso medusa decorativo o modo de niebla continua para máxima hidratación del ambiente.</li>
      <li><strong>Iluminación Ambiental Graduable:</strong> Tonos cálidos y suaves que crean un entorno envolvente para salas de estar y recámaras.</li>
      <li><strong>Depósito de Fácil Relleno:</strong> Carga superior sin derrames y diseño ergonómico de fácil limpieza.</li>
      <li><strong>Material Seguro Libre de BPA:</strong> Construcción de polímero ABS de alta resistencia y grado alimenticio.</li>
    </ul>
    """,
    "images": [
        {"src": "https://elevatohome.com/cdn/shop/files/61CRrFLsXjL._AC_SX679__LE_auto_x2_8524fc37-a193-4b8e-852b-da655fac6c1d.jpg?v=1725299681", "alt": "Humidificador Efecto Medusa Iluminado"},
        {"src": "https://elevatohome.com/cdn/shop/files/6_e149b556-4c47-4fea-8c96-847c8fa814c7_trans.png?v=1725440988", "alt": "Blanco Nórdico"},
        {"src": "https://elevatohome.com/cdn/shop/files/7_3e1f7ed2-c71c-47e8-8929-4a75af290e7b_trans.png?v=1725440989", "alt": "Negro Mate"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Blanco Nórdico", "price": "780.00", "compare_at_price": "1280.00", "sku": "DIF-JELLY-WHT", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro Mate", "price": "780.00", "compare_at_price": "1280.00", "sku": "DIF-JELLY-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 3. BASE DE CARGA RÁPIDA INALÁMBRICA 3 EN 1 PLEGABLE MAGSAFE
# ─────────────────────────────────────────────────────────────
charger_3in1 = {
    "title": "Estación de Carga Rápida Inalámbrica 3 en 1 Plegable MagSafe para Smartphone, Smartwatch y Audífonos",
    "vendor": "Aylesva Tech",
    "product_type": "Electrónicos y Accesorios",
    "tags": "Electrónicos, Gadgets y accesorios tecnológicos, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Orden Total en tu Escritorio y Buró: Carga 3 Dispositivos a la Vez</h3>
    <p>La <strong>Estación de Carga Magnética 3 en 1</strong> elimina por completo el desorden de cables enredados. Su estructura inteligente articulada permite plegarla en segundos para llevarla en tu bolsillo o mochila, o desplegarla como base de pie ergonómica de ángulo ajustable.</p>
    <h4>Tecnología y Compatibilidad:</h4>
    <ul>
      <li><strong>Carga Simultánea 3 en 1:</strong> Módulo magnético para celular (compatible con MagSafe y carga Qi hasta 15W), base desplegable para Smartwatch y almohadilla trasera para audífonos inalámbricos.</li>
      <li><strong>Plegado Ultracompacto 180°:</strong> Se compacta al tamaño de una cartera delgada, convirtiéndose en el accesorio de viaje imprescindible.</li>
      <li><strong>Alineación Magnética Fuerte:</strong> Imanes de neodimio N52 integrados que aseguran sujeción firme horizontal y vertical para videollamadas o streaming.</li>
      <li><strong>Protección Multipunto:</strong> Control térmico inteligente con protección contra sobretensión, cortocircuitos y detección de objetos extraños metálicos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://oddlyepic.com/cdn/shop/files/3-in-1-magnetic-wireless-charger.webp?v=1753260536", "alt": "Base de Carga 3 en 1 MagSafe Plegable"},
        {"src": "https://oddlyepic.com/cdn/shop/files/foldable-wireless-charging-station.webp?v=1753260545", "alt": "Negro Carbón / Naranja"},
        {"src": "https://oddlyepic.com/cdn/shop/files/compact-travel-wireless-charger.webp?v=1753260560", "alt": "Blanco Polar / Naranja"},
        {"src": "https://oddlyepic.com/cdn/shop/files/multi-device-charging-dock-usb-c.webp?v=1753260571", "alt": "Carga Simultánea de Múltiples Dispositivos"},
        {"src": "https://oddlyepic.com/cdn/shop/files/wireless-charger-black-orange-trim.webp?v=1753260580", "alt": "Detalle Acabado Premium"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Carbón / Naranja", "price": "650.00", "compare_at_price": "1090.00", "sku": "CHG-3IN1-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Blanco Polar / Naranja", "price": "650.00", "compare_at_price": "1090.00", "sku": "CHG-3IN1-WHT", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 4. BOCINA BLUETOOTH CON SONIDOS NATURALES Y LUZ LED
# ─────────────────────────────────────────────────────────────
speaker_natural = {
    "title": "Bocina Bluetooth Portátil Táctil Sonido 360° con Sonidos Naturales Relajantes y Luz Ambiental LED",
    "vendor": "Aylesva Tech",
    "product_type": "Audio y Bocinas",
    "tags": "Electrónicos, Gadgets y accesorios tecnológicos, Hogar, Dropshipping, Novedades",
    "body_html": """
    <h3>Audio Acústico Inmersivo y Máquina de Sonidos Naturales para Descanso</h3>
    <p>Diseñada tanto para amantes de la buena música como para quienes buscan relajarse y dormir profundamente, la <strong>Bocina Bluetooth Natural Sound</strong> integra conectividad inalámbrica 5.2 de alta fidelidad y un generador integrado de sonidos de la naturaleza (lluvia suave, olas de mar, canto de aves y bosque).</p>
    <h4>Características Clave:</h4>
    <ul>
      <li><strong>Sonido Envolvente 360°:</strong> Driver acústico de rango completo con diafragma pasivo para graves profundos y voces cristalinas.</li>
      <li><strong>Modo Ruido Blanco y Naturaleza:</strong> Sonidos precargados que reducen el estrés, ideales para trabajar con enfoque, meditar o conciliar el sueño.</li>
      <li><strong>Control Táctil Intuitivo:</strong> Botones táctiles retroiluminados superiores para cambio de pista, volumen, modos y luz ambiental tenue.</li>
      <li><strong>Batería de Larga Duración:</strong> Hasta 8 horas continuas de reproducción con una sola carga rápida mediante USB-C.</li>
    </ul>
    """,
    "images": [
        {"src": "https://oddlyepic.com/cdn/shop/files/Natural_Sound_Bluetooth_Speaker_Controls.jpg?v=1776850273", "alt": "Panel Táctil Superior y Luz LED"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Natural-Sound-Bluetooth-Speaker-Green.jpg?v=1776850770", "alt": "Verde Océano Nórdico"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Natural_Sound_Speaker_Off_White.png?v=1776850922", "alt": "Blanco Cálido Arena"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Natural_Sound_Speaker_White_de3ae1e4-6704-489c-9cbe-5a72aeca06b9.webp?v=1776851031", "alt": "Blanco Puro Minimalista"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Natural_Sound_Bluetooth_Speaker_White.jpg?v=1776850272", "alt": "Perspectiva Frontal"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Verde Océano Nórdico", "price": "720.00", "compare_at_price": "1190.00", "sku": "SPK-NAT-GRN", "inventory_management": None, "requires_shipping": True},
        {"option1": "Blanco Cálido Arena", "price": "720.00", "compare_at_price": "1190.00", "sku": "SPK-NAT-SND", "inventory_management": None, "requires_shipping": True},
        {"option1": "Blanco Puro Minimalista", "price": "720.00", "compare_at_price": "1190.00", "sku": "SPK-NAT-WHT", "inventory_management": None, "requires_shipping": True}
    ]
}

# ─────────────────────────────────────────────────────────────
# 5. AUDÍFONOS INALÁMBRICOS ST99 DEGRADADO CROMÁTICO
# ─────────────────────────────────────────────────────────────
headphones_st99 = {
    "title": "Audífonos Inalámbricos Bluetooth 5.2 ST99 con Cancelación Pasiva y Degradado Cromático Pastel",
    "vendor": "Aylesva Tech",
    "product_type": "Audio y Audífonos",
    "tags": "Electrónicos, Gadgets y accesorios tecnológicos, Dropshipping, Novedades",
    "body_html": """
    <h3>Estilo Visual Vanguardista con Audio Inalámbrico de Baja Latencia</h3>
    <p>Los audífonos <strong>ST99 Gradient</strong> destacan a primera vista gracias a su exclusivo acabado en tono degradado mate suave al tacto. Con drivers de 40mm ajustados para un equilibrio sonoro superior entre graves contundentes y agudos nítidos, ofrecen una experiencia envolvente para música, clases y gaming.</p>
    <h4>Especificaciones Técnicas:</h4>
    <ul>
      <li><strong>Bluetooth 5.2 de Baja Latencia:</strong> Conexión estable sin desfase en audio para videos, películas y videojuegos móviles.</li>
      <li><strong>Almohadillas de Espuma Viscoelástica Memory Foam:</strong> Aislamiento pasivo de ruido exterior y comodidad ergonómica durante largas horas.</li>
      <li><strong>Micrófono HD Integrado:</strong> Llamadas manos libres con claridad vocal optimizada y reducción de eco.</li>
      <li><strong>Diseño Plegable y Ajustable:</strong> Diadema retráctil con bisagras reforzadas para fácil transporte en mochilas o bolsos.</li>
    </ul>
    """,
    "images": [
        {"src": "https://oddlyepic.com/cdn/shop/files/7qTZAbL4zJoaauQn.webp?v=1756059086", "alt": "Azul Glaciar Degradado"},
        {"src": "https://oddlyepic.com/cdn/shop/files/Pl4jHHMmnFSltlgF.webp?v=1756059504", "alt": "Rosa Aurora Degradado"},
        {"src": "https://oddlyepic.com/cdn/shop/files/zeGYzfnShnQyHIyC.webp?v=1756059504", "alt": "Púrpura Lavanda Degradado"},
        {"src": "https://oddlyepic.com/cdn/shop/files/z4Vm6AMoF4XehXvC.webp?v=1756059504", "alt": "Verde Menta Pastel"},
        {"src": "https://oddlyepic.com/cdn/shop/files/1v1I1FocxnLccQ4C.webp?v=1756059504", "alt": "Negro Ónix Espacial"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Azul Glaciar Degradado", "price": "590.00", "compare_at_price": "990.00", "sku": "HP-ST99-BLU", "inventory_management": None, "requires_shipping": True},
        {"option1": "Rosa Aurora Degradado", "price": "590.00", "compare_at_price": "990.00", "sku": "HP-ST99-PNK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Púrpura Lavanda Degradado", "price": "590.00", "compare_at_price": "990.00", "sku": "HP-ST99-PUR", "inventory_management": None, "requires_shipping": True},
        {"option1": "Verde Menta Pastel", "price": "590.00", "compare_at_price": "990.00", "sku": "HP-ST99-GRN", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro Ónix Espacial", "price": "590.00", "compare_at_price": "990.00", "sku": "HP-ST99-BLK", "inventory_management": None, "requires_shipping": True}
    ]
}

if __name__ == '__main__':
    print("🚀 Iniciando creación de lote 3: Electrónicos y Hogar con fotos vinculadas...")
    
    # 1. Difusor Llama: v0->img1 (Negro), v1->img2 (Blanco)
    create_product_with_variant_images(flame_diffuser, {0: 1, 1: 2})
    time.sleep(1.0)
    
    # 2. Difusor Medusa: v0->img1 (Blanco), v1->img2 (Negro)
    create_product_with_variant_images(jellyfish_diffuser, {0: 1, 1: 2})
    time.sleep(1.0)
    
    # 3. Base de Carga 3 en 1: v0->img1 (Negro), v1->img2 (Blanco)
    create_product_with_variant_images(charger_3in1, {0: 1, 1: 2})
    time.sleep(1.0)
    
    # 4. Bocina Sonidos Naturales: v0->img1 (Verde), v1->img2 (Blanco Cálido), v2->img3 (Blanco Puro)
    create_product_with_variant_images(speaker_natural, {0: 1, 1: 2, 2: 3})
    time.sleep(1.0)
    
    # 5. Audífonos ST99: v0->img0 (Azul), v1->img1 (Rosa), v2->img2 (Púrpura), v3->img3 (Verde), v4->img4 (Negro)
    create_product_with_variant_images(headphones_st99, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4})
    
    print("\n🎉 ¡Lote 3 de Electrónicos y Hogar completado exitosamente!")
