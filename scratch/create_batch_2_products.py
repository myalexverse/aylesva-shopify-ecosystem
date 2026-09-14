import urllib.request, json, time

env_vars = {}
with open('.env') as fh:
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
    with urllib.request.urlopen(req) as resp:
        created = json.loads(resp.read().decode('utf-8'))['product']
        pid = created['id']
        print(f"\n✅ Creado: [{pid}] {created['title']}")
        
        # Vincular cada variante con su imagen respectiva
        images = created.get('images', [])
        variants = created.get('variants', [])
        
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
                with urllib.request.urlopen(v_req) as v_resp:
                    v_res = json.loads(v_resp.read().decode('utf-8'))['variant']
                    print(f"   🎯 Variante '{v_res['title']}' vinculada a foto {img_idx+1} (ID: {v_res['image_id']})")
                time.sleep(0.3)
        return pid

# ─────────────────────────────────────────────────────────────
# 1. CURREN CUR-208: RELOJ CRONÓGRAFO MILITAR ACERO
# ─────────────────────────────────────────────────────────────
cur208_data = {
    "title": "Reloj Deportivo Cronógrafo Curren CUR-208 en Acero Inoxidable con Fechador y Bisel Táctico",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Novedades, Cronografo",
    "body_html": """
    <h3>Robustez Militar con Cronómetro de Alta Precisión</h3>
    <p>El <strong>Curren CUR-208</strong> impone presencia gracias a su contundente caja de 48mm en acero inoxidable cepillado con bisel graduado y esfera de tres subesferas funcionales accionadas por pulsadores ergonómicos de uso rudo.</p>
    <h4>Características Principales:</h4>
    <ul>
      <li><strong>Mecanismo de Cuarzo Cronógrafo:</strong> Medición en tiempo real de minutos, segundos y fracciones de segundo con ventana de fecha rápida.</li>
      <li><strong>Caja y Extensible en Acero Quirúrgico:</strong> Eslabones macizos de alta durabilidad con cierre desplegable de doble seguridad.</li>
      <li><strong>Resistencia al Agua 3 ATM:</strong> A prueba de lluvia, salpicaduras accidentales y lavado de manos cotidiano.</li>
      <li><strong>Diámetro de Esfera:</strong> 48 mm | <strong>Grosor de Caja:</strong> 15 mm | <strong>Ancho de Banda:</strong> 24 mm.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-93818879__-350693342.jpg?v=1597148754", "alt": "Negro Total Táctico"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/currenwtches877.jpg?v=1597148754", "alt": "Azul Marino y Oro Rosa"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v--482040320__608084695.jpg?v=1597148754", "alt": "Negro con Bisel Dorado"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-1280924735__1206250495.jpg?v=1597148754", "alt": "Acero Plateado y Negro"}
    ],
    "options": [{"name": "Estilo"}],
    "variants": [
        {"option1": "Negro Total Táctico", "price": "820.00", "compare_at_price": "1350.00", "sku": "CUR-208-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Azul Marino / Oro Rosa", "price": "820.00", "compare_at_price": "1350.00", "sku": "CUR-208-BLRO", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro / Bisel Dorado", "price": "820.00", "compare_at_price": "1350.00", "sku": "CUR-208-BKGL", "inventory_management": None, "requires_shipping": True},
        {"option1": "Acero Plateado / Negro", "price": "820.00", "compare_at_price": "1350.00", "sku": "CUR-208-SLBK", "inventory_management": None, "requires_shipping": True}
    ]
}
create_product_with_variant_images(cur208_data, {0: 0, 1: 1, 2: 2, 3: 3})

# ─────────────────────────────────────────────────────────────
# 2. CURREN CUR-211: RELOJ DIGITAL DUAL-TIME MILITAR
# ─────────────────────────────────────────────────────────────
cur211_data = {
    "title": "Reloj Digital Militar Dual-Time Curren CUR-211 con Pantalla LED, Cronómetro y Alarma",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Novedades, Reloj Digital",
    "body_html": """
    <h3>Tecnología Híbrida: Agujas Analógicas + Pantalla Digital LED</h3>
    <p>El <strong>Curren CUR-211</strong> fusiona la elegancia de las manecillas analógicas tradicionales con un módulo digital multifunción de pantalla LED retroiluminada de alta visibilidad para expediciones y uso táctico.</p>
    <h4>Funciones Integradas:</h4>
    <ul>
      <li><strong>Hora Dual (Dual-Time):</strong> Configura dos zonas horarias simultáneas de manera independiente.</li>
      <li><strong>Luz de Fondo LED:</strong> Iluminación nocturna clara para lectura precisa en oscuridad total.</li>
      <li><strong>Funciones Deportivas:</strong> Cronómetro de precisión 1/100s, alarma programable diaria y señal horaria.</li>
      <li><strong>Caja Robusta de 48mm:</strong> Construida en aleación reforzada con cristal mineral resistente a impactos y correa de acero inoxidable con seguro.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-93818879__1151524243.jpg?v=1615725854", "alt": "Negro Mate Militar"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-3027034__-926733059.jpg?v=1615725854", "alt": "Azul Real Deportivo"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-3178592__-1462608936.jpg?v=1615725854", "alt": "Dorado Ejecutivo Gold"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/curenwatches89.jpg?v=1615725854", "alt": "Acero Plateado Silver"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Mate Militar", "price": "790.00", "compare_at_price": "1290.00", "sku": "CUR-211-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Azul Real Deportivo", "price": "790.00", "compare_at_price": "1290.00", "sku": "CUR-211-BLU", "inventory_management": None, "requires_shipping": True},
        {"option1": "Dorado Imperial Gold", "price": "890.00", "compare_at_price": "1450.00", "sku": "CUR-211-GLD", "inventory_management": None, "requires_shipping": True},
        {"option1": "Acero Plateado Silver", "price": "790.00", "compare_at_price": "1290.00", "sku": "CUR-211-SLV", "inventory_management": None, "requires_shipping": True}
    ]
}
create_product_with_variant_images(cur211_data, {0: 0, 1: 1, 2: 2, 3: 3})

# ─────────────────────────────────────────────────────────────
# 3. CURREN CUR-213: RELOJ CRONÓGRAFO AVIADOR EN PIEL
# ─────────────────────────────────────────────────────────────
cur213_data = {
    "title": "Reloj Cronógrafo Aviador Curren CUR-213 con Correa de Piel Genuina Cosida y Fechador",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Novedades, Cuero",
    "body_html": """
    <h3>Estilo Clásico de Aviación con Piel Genuina Cosida</h3>
    <p>Inspirado en los instrumentos de vuelo de los pilotos de aviación, el <strong>Curren CUR-213</strong> destaca por su esfera de números contrastados de gran formato, subdiales cronográficos y una correa de piel auténtica de tacto cálido y costuras reforzadas en hilo blanco.</p>
    <h4>Detalles Exclusivos:</h4>
    <ul>
      <li><strong>Correa de Piel Cosida a Mano:</strong> Confeccionada en piel suave de alta resistencia con textura vintage y hebilla clásica de acero grabado.</li>
      <li><strong>Cronógrafo Real:</strong> 3 diales activos que registran minutos, segundos y décimas de segundo con botones de accionamiento rápido.</li>
      <li><strong>Fechador Automático:</strong> Ventana numérica angular situada a las 4 horas para rápida lectura.</li>
      <li><strong>Diámetro de Caja:</strong> 47 mm | <strong>Grosor:</strong> 14 mm | <strong>Material:</strong> Aleación de zinc ionizada anti-desgaste.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/currenwatches890.jpg?v=1632222549", "alt": "Café Tabaco y Bisel Negro"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-3027034__758874222.jpg?v=1632222586", "alt": "Azul Profundo Deportivo"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v-1330756848__1166128658.jpg?v=1632222597", "alt": "Negro con Bisel Rojo Rally"}
    ],
    "options": [{"name": "Combinación"}],
    "variants": [
        {"option1": "Café Tabaco / Bisel Negro", "price": "760.00", "compare_at_price": "1190.00", "sku": "CUR-213-BRW", "inventory_management": None, "requires_shipping": True},
        {"option1": "Azul Profundo Deportivo", "price": "760.00", "compare_at_price": "1190.00", "sku": "CUR-213-BLU", "inventory_management": None, "requires_shipping": True},
        {"option1": "Negro / Detalles Rojo Rally", "price": "760.00", "compare_at_price": "1190.00", "sku": "CUR-213-RED", "inventory_management": None, "requires_shipping": True}
    ]
}
create_product_with_variant_images(cur213_data, {0: 0, 1: 1, 2: 2})

# ─────────────────────────────────────────────────────────────
# 4. CUADRA: CARTERA BIFOLD EN PIEL GENUINA DE BOVINO AZTECA
# ─────────────────────────────────────────────────────────────
cartera_data = {
    "title": "Cartera Bifold para Caballero en Piel Genuina de Bovino Azteca con Bloqueo RFID",
    "vendor": "Cuadra",
    "product_type": "Accesorios Hombre",
    "tags": "Accesorios Hombre, Accesorios de cuero, Botas y botines Hombre, Dropshipping, Novedades, Cuadra",
    "body_html": """
    <h3>Artesanía Mexicana de Clase Mundial en Piel de Res de Grano Entero</h3>
    <p>La <strong>Cartera Bifold Cuadra</strong> está elaborada por maestros talabarteros en piel genuina de vacuno tipo Azteca, caracterizada por un tacto sedoso y una pátina natural que embellece con el paso del tiempo.</p>
    <h4>Organización y Seguridad:</h4>
    <ul>
      <li><strong>Protección RFID Integrada:</strong> Forro interno con blindaje electromagnético que previene la clonación inalámbrica de tarjetas de crédito y débito.</li>
      <li><strong>Capacidad Funcional:</strong> 8 ranuras para tarjetas bancarias e identificaciones, 2 compartimentos ocultos y doble división para billetes de distintas denominaciones.</li>
      <li><strong>Perfil Delgado (Slim Bifold):</strong> Diseñada para llevar cómodamente en el bolsillo delantero o trasero del pantalón sin abultar.</li>
      <li><strong>Emblema Metálico Cuadra:</strong> Aplique grabado en microfusión sobre el frontal con acabado envejecido.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/BC059RS_NEGRO-res-azteca-MO-00.jpg?v=1784328716", "alt": "Cartera Piel Azteca Frontal"},
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/BC059RS_NEGRO-res-azteca-MO-IA.jpg?v=1784328716", "alt": "Cartera Piel Abierta Ranuras"},
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/BC059RS_NEGRO-res-azteca-MO-01.jpg?v=1784328716", "alt": "Cartera Piel Vista Trasera"},
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/BC059RS_NEGRO-res-azteca-MO-detalle.jpg?v=1784328716", "alt": "Detalle Textura Cuero Azteca"}
    ],
    "options": [{"name": "Talla"}],
    "variants": [
        {"option1": "Estándar Bifold Slim", "price": "750.00", "compare_at_price": "1150.00", "sku": "CUA-WAL-AZT-STD", "inventory_management": None, "requires_shipping": True}
    ]
}
create_product_with_variant_images(cartera_data, {0: 0})

# ─────────────────────────────────────────────────────────────
# 5. CUADRA: CINTURÓN VAQUERO FULL EXOTIC EN PIEL DE PITÓN
# ─────────────────────────────────────────────────────────────
piton_data = {
    "title": "Cinturón Vaquero Full Exotic en Piel Genuina de Pitón para Caballero 40mm",
    "vendor": "Cuadra",
    "product_type": "Accesorios Hombre",
    "tags": "Accesorios Hombre, Accesorios de cuero, Botas y botines Hombre, Dropshipping, Novedades, Exoticos",
    "body_html": """
    <h3>Exclusividad Absoluta: Piel Genuina de Pitón Seleccionada a Mano</h3>
    <p>Elaborado bajo los más rigurosos estándares de la marroquinería de lujo, el <strong>Cinturón Full Exotic de Pitón</strong> destaca por la textura inconfundible de sus escamas naturales protegidas con acabado nubuck mate de tacto aterciopelado.</p>
    <h4>Atributos de Lujo:</h4>
    <ul>
      <li><strong>Piel de Pitón 100% Auténtica:</strong> Certificación de procedencia sustentable con forro interior de vacuno suave que aporta soporte estructural duradero.</li>
      <li><strong>Hebilla Metálica Forrada en Piel:</strong> Diseño de pasador western con doble broche a presión para fácil desmontaje o intercambio de hebilla.</li>
      <li><strong>Ancho Vaquero de 40mm:</strong> Proporción exacta para acompañar botas vaqueras, calzado western o vestimenta de gala campirana.</li>
      <li><strong>Fabricación Artesanal en León, Guanajuato:</strong> Acabado al canto pulido con costuras al tono de alta resistencia.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/CV519PH_NEGRO-piton-back-nubuck-MO-0.jpg?v=1782142661", "alt": "Negro Pitón Nubuck Mate"},
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/CV519PH_CAFE-piton-back-iran-MO-00.jpg?v=1782142814", "alt": "Café Tabaco Pitón Irán"},
        {"src": "https://cdn.shopify.com/s/files/1/0607/2179/1174/files/CV519PH_NEGRO-piton-back-nubuck-MO-puntas.jpg?v=1782142661", "alt": "Detalle Puntas y Hebilla Pitón"}
    ],
    "options": [{"name": "Color"}],
    "variants": [
        {"option1": "Negro Pitón Nubuck", "price": "1650.00", "compare_at_price": "2490.00", "sku": "CUA-BLT-PIT-BLK", "inventory_management": None, "requires_shipping": True},
        {"option1": "Café Tabaco Pitón", "price": "1650.00", "compare_at_price": "2490.00", "sku": "CUA-BLT-PIT-BRW", "inventory_management": None, "requires_shipping": True}
    ]
}
create_product_with_variant_images(piton_data, {0: 0, 1: 1})

print("\n🎉 Todos los 5 nuevos productos fueron creados y sus variantes vinculadas con imágenes!")
