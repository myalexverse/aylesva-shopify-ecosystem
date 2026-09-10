import urllib.request, json, time

env_vars = {}
with open('.env') as fh:
    for line in fh:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip()

shop = env_vars.get('SHOP_NAME', 'aylesvamx.myshopify.com')
token = env_vars.get('ACCESS_TOKEN', '')

def update_product_fully(pid, new_data):
    print(f"\n==========================================")
    print(f"🔄 Actualizando Producto [{pid}] con datos 100% reales de e-commerce...")

    # 1. Obtener imágenes actuales y eliminarlas para evitar mezclas
    get_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products/{pid}.json",
        headers={"X-Shopify-Access-Token": token}
    )
    with urllib.request.urlopen(get_req) as resp:
        curr = json.loads(resp.read().decode('utf-8'))['product']
        old_images = curr.get('images', [])
        print(f"  - Eliminando {len(old_images)} imágenes anteriores para asegurar consistencia total...")
        for img in old_images:
            del_req = urllib.request.Request(
                f"https://{shop}/admin/api/2024-01/products/{pid}/images/{img['id']}.json",
                headers={"X-Shopify-Access-Token": token},
                method="DELETE"
            )
            try:
                with urllib.request.urlopen(del_req) as d_resp:
                    pass
            except Exception as de:
                print(f"    * Error borrando imagen {img['id']}: {de}")
            time.sleep(0.3)

    # 2. Actualizar datos base del producto y nuevas imágenes
    payload = {"product": new_data}
    put_req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products/{pid}.json",
        data=json.dumps(payload).encode('utf-8'),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(put_req) as resp:
        updated = json.loads(resp.read().decode('utf-8'))['product']
        print(f"✅ Producto [{pid}] actualizado:")
        print(f"   Título: {updated['title']}")
        print(f"   Imágenes asignadas: {len(updated['images'])}")
        print(f"   Variantes: {len(updated['variants'])}")
        for i, img in enumerate(updated['images']):
            print(f"   Foto {i+1}: {img['src'][:80]}...")

# --- 1. PRODUCTO 8944277454871: RELOJ ESQUELETO CURREN CUR-230 REAL ---
skeleton_data = {
    "title": "Reloj Deportivo Esqueleto Curren CUR-230 Sumergible con Caja Cuadrada y Correa de Silicón",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Novedades, Reloj Esqueleto",
    "body_html": """
    <h3>Diseño Vanguardista con Dial Esqueleto en Capas</h3>
    <p>El <strong>Curren CUR-230</strong> revoluciona la estética deportiva incorporando un dial esqueleto tridimensional que rinde homenaje a la alta relojería contemporánea en una robusta caja de aleación con geometría cuadrada de 44mm.</p>
    <h4>Especificaciones del Producto Real:</h4>
    <ul>
      <li><strong>Diseño Esqueleto Multifunción:</strong> Esfera calada en múltiples niveles con visualización de engranajes y manecillas con lumen nocturno de alta intensidad.</li>
      <li><strong>Correa de Silicón de Alta Densidad:</strong> Suave al tacto, hipoalergénica, transpirable y resistente al sudor, agua y polvo con hebilla de acero inoxidable.</li>
      <li><strong>Resistencia al Agua 3 ATM / 30 Metros:</strong> Protección contra salpicaduras, lluvia, lavado de manos y actividades cotidianas.</li>
      <li><strong>Cristal Hardlex Mineral:</strong> Máxima claridad óptica y alta resistencia contra rayaduras y golpes fortuitos.</li>
      <li><strong>Diámetro de Caja:</strong> 44 mm | <strong>Grosor:</strong> 13 mm | <strong>Largo de Banda:</strong> 24 cm.</li>
    </ul>
    <p><em>Producto 100% original con empaque de protección y garantía de funcionamiento directo.</em></p>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/currenwatches230.jpg?v=1736091983"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S55a5ed18be9c4cef8e8241396555bb0aH.webp?v=1736092000"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S9faee5e6a9644e40af2b1188e54807bak.webp?v=1736092012"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/Sba62d680739e4339b1560d689b74f799W.webp?v=1736092026"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/S42271fafe51f4f1a87e955e595255e13U.webp?v=1736092039"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/files/Sd2760021252a495ebf5cff24da5cfa321.webp?v=1736092052"}
    ],
    "variants": [
        {
            "option1": "Negro Táctico Stealth",
            "price": "890.00",
            "compare_at_price": "1450.00",
            "sku": "CUR-230-BLK",
            "inventory_management": None,
            "requires_shipping": True
        },
        {
            "option1": "Azul Cobalto Deportivo",
            "price": "890.00",
            "compare_at_price": "1450.00",
            "sku": "CUR-230-BLU",
            "inventory_management": None,
            "requires_shipping": True
        },
        {
            "option1": "Naranja Racing Adventure",
            "price": "890.00",
            "compare_at_price": "1450.00",
            "sku": "CUR-230-ORG",
            "inventory_management": None,
            "requires_shipping": True
        },
        {
            "option1": "Rojo Escudería Sport",
            "price": "890.00",
            "compare_at_price": "1450.00",
            "sku": "CUR-230-RED",
            "inventory_management": None,
            "requires_shipping": True
        }
    ]
}

# --- 2. PRODUCTO 8944277422103: RELOJ CRONÓGRAFO CURREN CUR-212 ACERO REAL ---
chrono_data = {
    "title": "Reloj Cronógrafo Curren CUR-212 en Acero Inoxidable con Subdiales y Fechador",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Ofertas, Cronografo",
    "body_html": """
    <h3>Acero Quirúrgico Macizo con Funcionalidad Cronográfica Total</h3>
    <p>El <strong>Curren CUR-212</strong> es un reloj cronógrafo de presencia imponente construido íntegramente en acero inoxidable de grado quirúrgico. Sus 3 subdiales funcionales permiten medir segundos, minutos y milisegundos con exactitud militar.</p>
    <h4>Características Destacadas:</h4>
    <ul>
      <li><strong>Construcción Full Steel:</strong> Caja y extensible de eslabones sólidos de acero inoxidable con pulido satinado y broche desplegable de doble pulsador.</li>
      <li><strong>Cronógrafo Real:</strong> Agujas de cronometraje activas accionadas mediante pulsadores laterales ergonómicos.</li>
      <li><strong>Ventana Fechadora:</strong> Indicador de día del mes ubicado estratégicamente a las 4 en punto.</li>
      <li><strong>Bisel Graduado & Manecillas Luminiscentes:</strong> Marcadores horarios en relieve con recubrimiento reflectivo para visión en oscuridad.</li>
      <li><strong>Diámetro de Caja:</strong> 45 mm | <strong>Grosor:</strong> 14 mm | <strong>Ancho de Correa:</strong> 24 mm.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/currenwatches.jpg?v=1618492487"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-Watches-Men-Fashion-Military-Sports-Quartz-Wristwatches-for-Male-Stainless-Steel-Clock-with-Chronograph-and.jpg?v=1618492499"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-Watches-Men-Fashion-Military-Sports-Quartz-Wristwatches-for-Male-Stainless-Steel-Clock-with-Chronograph-and_61cbe2d0-c4b6-49f1-8fa9-d71d699298e4.jpg?v=1618492511"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v--789251404__-1045807092.jpg?v=1618492524"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/v--1492066935__1009807713.jpg?v=1618492536"}
    ],
    "variants": [
        {
            "option1": "Azul Zafiro / Acero Plateado",
            "price": "790.00",
            "compare_at_price": "1290.00",
            "sku": "CUR-212-BLU",
            "inventory_management": None,
            "requires_shipping": True
        },
        {
            "option1": "Negro / Bisel Oro Rosa",
            "price": "790.00",
            "compare_at_price": "1290.00",
            "sku": "CUR-212-BKG",
            "inventory_management": None,
            "requires_shipping": True
        }
    ]
}

# --- 3. PRODUCTO 8944277356567: SMARTWATCH CURREN CUR-219 REAL ---
smartwatch_data = {
    "title": "Smartwatch Curren CUR-219 Deportivo IP68 con Llamadas Bluetooth y Monitoreo Cardíaco",
    "vendor": "Curren",
    "product_type": "Relojes",
    "tags": "Relojes Hombre, Relojes inteligentes (smartwatches), Accesorios Hombre, Dropshipping, Novedades",
    "body_html": """
    <h3>Tecnología Conectada con la Calidad de Relojería Curren</h3>
    <p>El <strong>Smartwatch Curren CUR-219</strong> integra una pantalla táctil HD de alta resolución con conectividad Bluetooth dual para gestionar llamadas telefónicas y alertas de mensajería al instante sin sacar el smartphone del bolsillo.</p>
    <h4>Funciones Inteligentes Completas:</h4>
    <ul>
      <li><strong>Llamadas Bluetooth Directas:</strong> Marcador telefónico, agenda de contactos y altavoz HD con micrófono anti-ruido ambiental.</li>
      <li><strong>Salud y Biometría 24 Horas:</strong> Sensor óptico de ritmo cardíaco dinámico, presión arterial y saturación de oxígeno (SpO2).</li>
      <li><strong>Certificación IP68 a Prueba de Agua:</strong> Resistente a inmersión, sudor extremo, natación superficial y lluvia torrencial.</li>
      <li><strong>Seguimiento Deportivo Multidisciplinario:</strong> Conteo de pasos, calorías quemadas, distancia recorrida y múltiples modos de entrenamiento.</li>
      <li><strong>Compatibilidad Multiplataforma:</strong> Compatible con smartphones Android y Apple iOS mediante app oficial dedicada.</li>
    </ul>
    """,
    "images": [
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/Currensmartwatch218.jpg?v=1655203460"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-2022-Men-Smart-Watch-Heart-Rate-Blood-Pressure-IP68-Waterproof-Sports-Fitness-Watch-Bluetooth-Call.jpg?v=1655203490"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-2022-Men-Smart-Watch-Heart-Rate-Blood-Pressure-IP68-Waterproof-Sports-Fitness-Watch-Bluetooth-Call_b6a2b4be-b206-4dd1-b680-710cbe530e28.jpg?v=1655203502"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-2022-Men-Smart-Watch-Heart-Rate-Blood-Pressure-IP68-Waterproof-Sports-Fitness-Watch-Bluetooth-Call_705b2e3c-ea79-4651-9bc1-c2837eb7dd36.jpg?v=1655203513"},
        {"src": "https://cdn.shopify.com/s/files/1/0304/3821/products/CURREN-2022-Men-Smart-Watch-Heart-Rate-Blood-Pressure-IP68-Waterproof-Sports-Fitness-Watch-Bluetooth-Call_ccd8310e-fbc6-4b01-ae6b-7f2c20a66582.jpg?v=1655203525"}
    ],
    "variants": [
        {
            "option1": "Negro Táctico Mate",
            "price": "1090.00",
            "compare_at_price": "1690.00",
            "sku": "CUR-219-BLK",
            "inventory_management": None,
            "requires_shipping": True
        },
        {
            "option1": "Azul Naval Deportivo",
            "price": "1090.00",
            "compare_at_price": "1690.00",
            "sku": "CUR-219-BLU",
            "inventory_management": None,
            "requires_shipping": True
        }
    ]
}

# Ejecutar las actualizaciones
update_product_fully(8944277454871, skeleton_data)
update_product_fully(8944277422103, chrono_data)
update_product_fully(8944277356567, smartwatch_data)

print("\n🎉 Todos los productos fueron sincronizados con fotos y datos 100% reales de e-commerce!")
