import urllib.request, json, time

env_vars = {}
with open('.env') as fh:
    for line in fh:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip()

shop = env_vars.get('SHOP_NAME', 'aylesvamx.myshopify.com')
token = env_vars.get('ACCESS_TOKEN', '')

products_data = [
    # 1. SMARTWATCH TÁCTICO MILITAR
    {
        "title": "Smartwatch Táctico Militar Sumergible IP68 con Llamadas Bluetooth y Monitoreo Salud",
        "vendor": "Aylesva Direct",
        "product_type": "Relojes",
        "tags": "Relojes Hombre, Relojes inteligentes (smartwatches), Accesorios Hombre, Dropshipping, Novedades",
        "body_html": """
        <h3>Rendimiento Extremo, Resistencia de Grado Militar</h3>
        <p>Diseñado para soportar las condiciones más exigentes. El <strong>Smartwatch Táctico Militar</strong> combina una carcasa de aleación de zinc de alta resistencia con cristal mineral reforzado antiarañazos y certificación IP68 impermeable (sumergible hasta 50 metros).</p>
        <h4>Características Principales:</h4>
        <ul>
          <li><strong>Llamadas Bluetooth HD:</strong> Responde y realiza llamadas directamente desde tu muñeca gracias a su micrófono y altavoz integrados con reducción de ruido.</li>
          <li><strong>Monitoreo de Salud 24/7:</strong> Medición continua de frecuencia cardíaca, oxigenación en sangre (SpO2), presión arterial y monitor avanzado de sueño.</li>
          <li><strong>+100 Modos Deportivos:</strong> Running, ciclismo, senderismo, natación, entrenamiento funcional y más con registro GPS conectado.</li>
          <li><strong>Batería de Ultra Larga Duración:</strong> Hasta 10-14 días de uso continuo y 30 días en modo espera con una sola carga rápida magnética.</li>
          <li><strong>Compatibilidad Universal:</strong> Compatible con iOS (iPhone) y Android mediante sincronización fluida.</li>
        </ul>
        <p><em>Envío exprés disponible a todo México con garantía directa de 12 meses.</em></p>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1508057198894-247b23fe5ade?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=1200&q=85"}
        ],
        "options": [{"name": "Color"}],
        "variants": [
            {
                "option1": "Negro Carbón Táctico",
                "price": "1199.00",
                "compare_at_price": "1899.00",
                "sku": "AYL-WAT-001-BLK",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Verde Militar Ranger",
                "price": "1199.00",
                "compare_at_price": "1899.00",
                "sku": "AYL-WAT-001-GRN",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Coyote Arena Táctico",
                "price": "1199.00",
                "compare_at_price": "1899.00",
                "sku": "AYL-WAT-001-SND",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 2. RELOJ CRONÓGRAFO DE ACERO INOXIDABLE
    {
        "title": "Reloj Cronógrafo de Cuarzo Curren Elegance en Acero Inoxidable y Cristal Mineral",
        "vendor": "Aylesva Direct",
        "product_type": "Relojes",
        "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Ofertas",
        "body_html": """
        <h3>Elegancia Ejecutiva con Precisión Japonesa</h3>
        <p>El <strong>Reloj Cronógrafo Curren Elegance</strong> es la pieza definitiva para el caballero contemporáneo. Forjado en acero inoxidable 316L con acabado cepillado de alto brillo y dial tridimensional con tres subesferas funcionales.</p>
        <h4>Especificaciones de Alta Gama:</h4>
        <ul>
          <li><strong>Mecanismo:</strong> Movimiento de cuarzo de alta precisión con función de cronómetro y fechador automático.</li>
          <li><strong>Materiales:</strong> Caja y extensible de acero inoxidable quirúrgico hipoalergénico con cierre de seguridad mariposa.</li>
          <li><strong>Cristal Hardlex:</strong> Resistente a impactos, rayaduras y desgaste diario.</li>
          <li><strong>Resistencia al Agua:</strong> 3 ATM (resistente a lluvia, salpicaduras y lavado de manos).</li>
          <li><strong>Manecillas Luminiscentes:</strong> Lectura perfecta en entornos de poca luz.</li>
        </ul>
        <p><em>Incluye estuche de presentación de lujo y herramienta de ajuste de eslabones.</em></p>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=1200&q=85"}
        ],
        "options": [{"name": "Combinación"}],
        "variants": [
            {
                "option1": "Negro / Oro Rosa",
                "price": "780.00",
                "compare_at_price": "1250.00",
                "sku": "AYL-WAT-002-BROG",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Azul Zafiro / Plata",
                "price": "780.00",
                "compare_at_price": "1250.00",
                "sku": "AYL-WAT-002-BLSL",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Total Black Mate",
                "price": "780.00",
                "compare_at_price": "1250.00",
                "sku": "AYL-WAT-002-FULLBLK",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 3. RELOJ AUTOMÁTICO MECÁNICO ESQUELETO
    {
        "title": "Reloj Automático Mecánico Esqueleto Steampunk en Acero Inoxidable y Piel Genuina",
        "vendor": "Aylesva Direct",
        "product_type": "Relojes",
        "tags": "Relojes Hombre, Accesorios Hombre, Dropshipping, Premium",
        "body_html": """
        <h3>El Arte de la Relojería Mecánica al Descubierto</h3>
        <p>Una verdadera obra de arte en tu muñeca. El <strong>Reloj Automático Esqueleto</strong> prescinde de baterías, funcionando mediante un mecanismo mecánico que se recarga con el propio movimiento natural de tu muñeca o cuerda manual.</p>
        <h4>Detalles de Alta Relojería:</h4>
        <ul>
          <li><strong>Dial Esqueleto Transparente:</strong> Permite apreciar los engranajes, rubíes y el volante espiral en constante movimiento rítmico.</li>
          <li><strong>Correa de Cuero Auténtico:</strong> Piel vacuno de primera selección con costuras reforzadas y textura grabada.</li>
          <li><strong>Caja de Aleación Reforzada:</strong> Diámetro de 42mm, grosor de 13mm, peso equilibrado y sensación prémium.</li>
          <li><strong>Tapa Trasera de Exposición:</strong> Cristal posterior con vista panorámica del rotor de carga bidireccional.</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1542496658-e33a6d0d50f6?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=1200&q=85"}
        ],
        "options": [{"name": "Estilo"}],
        "variants": [
            {
                "option1": "Correa Café / Caja Oro Antiguo",
                "price": "1450.00",
                "compare_at_price": "2200.00",
                "sku": "AYL-WAT-003-BRWGLD",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Correa Negra / Caja Acero Plateado",
                "price": "1450.00",
                "compare_at_price": "2200.00",
                "sku": "AYL-WAT-003-BLKSLV",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 4. MOCHILA TÁCTICA MILITAR 45L (CROSSCOUNTRY)
    {
        "title": "Mochila Táctica Militar 45L Impermeable con Sistema MOLLE para Expedición y Outdoor",
        "vendor": "Crosscountry",
        "product_type": "Outdoor",
        "tags": "Crosscountry, Accesorios Hombre, Mochilas, Outdoor, Dropshipping, Novedades",
        "body_html": """
        <h3>Capacidad Táctica, Resistencia Inquebrantable</h3>
        <p>Inspirada en el equipamiento de fuerzas especiales, la <strong>Mochila Táctica CrossCountry 45L</strong> está confeccionada en tela Oxford 900D de densidad militar con recubrimiento interno de PVC 100% impermeable.</p>
        <h4>Diseño para Misiones Extremas:</h4>
        <ul>
          <li><strong>Capacidad Expansible de 45 Litros:</strong> 5 compartimentos independientes con cremalleras bidireccionales de uso rudo y apertura de 180° estilo maleta.</li>
          <li><strong>Sistema Modular MOLLE:</strong> Puntos de anclaje frontales y laterales para colgar accesorios, botiquín, cantimplora o linterna.</li>
          <li><strong>Ergonomía y Transpirabilidad:</strong> Panel trasero acolchado con malla transpirable 3D, tirantes ajustables y correa pectoral y lumbar para distribución perfecta del peso.</li>
          <li><strong>Compartimento para Laptop:</strong> Aloja laptops de hasta 17 pulgadas con protección acolchada antichoques.</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1546938576-6e6a64f317cc?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1200&q=85"}
        ],
        "options": [{"name": "Color"}],
        "variants": [
            {
                "option1": "Negro Táctico Operativo",
                "price": "980.00",
                "compare_at_price": "1490.00",
                "sku": "CC-BAG-045-BLK",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Verde Ranger Militar",
                "price": "980.00",
                "compare_at_price": "1490.00",
                "sku": "CC-BAG-045-GRN",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Coyote Tan Desierto",
                "price": "980.00",
                "compare_at_price": "1490.00",
                "sku": "CC-BAG-045-COY",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 5. LINTERNA TÁCTICA LED 10,000 LM (CROSSCOUNTRY)
    {
        "title": "Linterna Táctica Militar LED Recargable USB 10,000 Lúmenes Zoom Alta Potencia",
        "vendor": "Crosscountry",
        "product_type": "Outdoor",
        "tags": "Crosscountry, Accesorios Hombre, Outdoor, Dropshipping",
        "body_html": """
        <h3>Ilumina la Noche con Potencia Láser Táctica</h3>
        <p>La linterna táctica más potente de su categoría. Equipada con el chip LED XHP70 de última generación, es capaz de emitir hasta <strong>10,000 lúmenes</strong> reales alcanzando una distancia de haz de más de 500 metros.</p>
        <h4>Características Técnicas:</h4>
        <ul>
          <li><strong>5 Modos de Iluminación:</strong> Alto, Medio, Bajo, Estroboscópico de emergencia y señal SOS.</li>
          <li><strong>Zoom Telescópico Ajustable:</strong> Pasa de un haz de reflector amplio para iluminar un campamento a un haz concentrado de largo alcance.</li>
          <li><strong>Cuerpo de Aluminio Aeroespacial:</strong> Acabado anodizado militar resistente a impactos de caídas de hasta 2 metros y resistencia al agua IPX6.</li>
          <li><strong>Recargable USB-C y Power Bank:</strong> Batería recargable 26650 de alta capacidad con salida USB para cargar tu teléfono celular en emergencias.</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1517404215738-15263e9f9178?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?w=1200&q=85"}
        ],
        "options": [{"name": "Kit"}],
        "variants": [
            {
                "option1": "Kit Estándar (Linterna + Batería 26650 + Cable USB-C)",
                "price": "540.00",
                "compare_at_price": "890.00",
                "sku": "CC-LNT-010-STD",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Kit Pro (Linterna + 2 Baterías + Estuche Rígido + Funda)",
                "price": "690.00",
                "compare_at_price": "1150.00",
                "sku": "CC-LNT-010-PRO",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 6. TRÍPODE PROFESIONAL DE FIBRA DE CARBONO (DJI / TECH)
    {
        "title": "Trípode Profesional de Fibra de Carbono 165cm con Rótula Panorámica 360° para Cámara y Celular",
        "vendor": "DJI",
        "product_type": "Fotografía",
        "tags": "dji, electronicos, Accesorios para cámara (lentes, tripies, memorias), Dropshipping, Novedades",
        "body_html": """
        <h3>Estabilidad Profesional, Peso Pluma Ultraligero</h3>
        <p>Construido con 8 capas de fibra de carbono de alto módulo, este trípode ofrece la máxima rigidez y absorción de vibraciones con un peso de tan solo 1.25 kg, convirtiéndolo en el compañero ideal para creadores de contenido, fotógrafos de viaje y usuarios de DJI Osmo Pocket / Action.</p>
        <h4>Rendimiento Cinematográfico:</h4>
        <ul>
          <li><strong>Rótula de Bola CNC de 36mm:</strong> Movimiento fluido de 360° con escala micrométrica para tomas panorámicas perfectas y perilla de bloqueo dual.</li>
          <li><strong>Altura Ajustable de 45cm a 165cm:</strong> Patas de 4 secciones con bloqueo rápido de rosca ergonómica.</li>
          <li><strong>Modo Monopié 2 en 1:</strong> Una de las patas se desenrosca fácilmente para transformarse en un monopié o bastón de senderismo.</li>
          <li><strong>Zapata Rápida Arca-Swiss:</strong> Compatible con cámaras DSLR, sin espejo, monturas DJI y soporte universal para smartphones (incluido).</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=1200&q=85"}
        ],
        "options": [{"name": "Material"}],
        "variants": [
            {
                "option1": "Fibra de Carbono Pro (Ultraligero 1.25kg)",
                "price": "1399.00",
                "compare_at_price": "2190.00",
                "sku": "DJI-ACC-TRP-CARB",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Aleación de Aluminio Aeroespacial (1.5kg)",
                "price": "980.00",
                "compare_at_price": "1550.00",
                "sku": "DJI-ACC-TRP-ALU",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 7. KIT MINI PANEL LUZ LED RGB (DJI / TECH)
    {
        "title": "Mini Panel de Luz LED RGB Portátil 2500K-9000K para Fotografía, Vlogging y Cámaras",
        "vendor": "DJI",
        "product_type": "Fotografía",
        "tags": "dji, electronicos, Accesorios para cámara (lentes, tripies, memorias), Dropshipping",
        "body_html": """
        <h3>Iluminación Cinematográfica de Bolsillo</h3>
        <p>El accesorio indispensable para transformar la calidad visual de tus videos y fotos. Con 60 perlas LED de alto índice de reproducción cromática (CRI 95+), el <strong>Mini Panel RGB</strong> cabe en la palma de tu mano y se monta al instante en cualquier cámara, celular o estabilizador DJI.</p>
        <h4>Control Total de Color:</h4>
        <ul>
          <li><strong>Gama RGB 360°:</strong> Acceso a millones de colores con saturación ajustable de 0 a 100%.</li>
          <li><strong>Temperatura Bicolor Regulable:</strong> De luz cálida 2500K a luz fría blanca 9000K con dimmer de precisión.</li>
          <li><strong>20 Efectos Especiales de Escena:</strong> Simulación de luz de policía, ambulancia, relámpago, fuegos artificiales, vela, estroboscópico y TV.</li>
          <li><strong>Batería de Litio de 2000mAh:</strong> Hasta 2 horas continuas a máxima potencia, recargable mediante USB Tipo C.</li>
          <li><strong>Montaje Magnético y Zapata Fría:</strong> Imán trasero para fijar a superficies metálicas y 3 monturas de zapata fría para apilar múltiples paneles.</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1588702547919-26089e690ecc?w=1200&q=85"},
            {"src": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=1200&q=85"}
        ],
        "options": [{"name": "Paquete"}],
        "variants": [
            {
                "option1": "Panel Individual + Difusor Silicona + Adaptador Zapata",
                "price": "620.00",
                "compare_at_price": "950.00",
                "sku": "DJI-ACC-RGB-SGL",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Kit Creador (Panel + Mini Trípode Extensible + Pinza Celular)",
                "price": "790.00",
                "compare_at_price": "1250.00",
                "sku": "DJI-ACC-RGB-KIT",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    },

    # 8. CINTURÓN DE PIEL GENUINA VAQUERO CON HEBILLA GRABADA
    {
        "title": "Cinturón de Piel Genuina de Res Grabado Estilo Vaquero Occidental 38mm",
        "vendor": "Centenario",
        "product_type": "Accesorios Hombre",
        "tags": "Accesorios de cuero, Accesorios Hombre, Botas y botines Hombre, Dropshipping, Novedades",
        "body_html": """
        <h3>Piel Auténtica, Tradición Artesanal del Bajío</h3>
        <p>Confeccionado por maestros talabarteros con piel de flor entera de vacuno seleccionada de 4mm de grosor, garantizando máxima durabilidad sin deformarse con el uso.</p>
        <h4>Detalles Artesanales:</h4>
        <ul>
          <li><strong>Piel 100% Genuina:</strong> Cuero curtido vegetal de alta resistencia con textura y olor a piel auténtica.</li>
          <li><strong>Hebilla Metálica Grabada Removible:</strong> Acabado plata envejecida con grabados florales western y sistema de broches para cambiar de hebilla fácilmente.</li>
          <li><strong>Ancho Universal 38mm:</strong> Compatible con presillas estándar de jeans, pantalones de vestir y pantalones vaqueros.</li>
          <li><strong>Bordes Bruñidos a Mano:</strong> Acabado pulido en cantos que previene el deshilachado.</li>
        </ul>
        """,
        "images": [
            {"src": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=1200&q=85"}
        ],
        "options": [{"name": "Talla y Color"}],
        "variants": [
            {
                "option1": "Café Tabaco - Talla 32-34",
                "price": "520.00",
                "compare_at_price": "790.00",
                "sku": "CEN-BLT-TAB-34",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Café Tabaco - Talla 36-38",
                "price": "520.00",
                "compare_at_price": "790.00",
                "sku": "CEN-BLT-TAB-38",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Negro Clásico - Talla 32-34",
                "price": "520.00",
                "compare_at_price": "790.00",
                "sku": "CEN-BLT-BLK-34",
                "inventory_management": None,
                "requires_shipping": True
            },
            {
                "option1": "Negro Clásico - Talla 36-38",
                "price": "520.00",
                "compare_at_price": "790.00",
                "sku": "CEN-BLT-BLK-38",
                "inventory_management": None,
                "requires_shipping": True
            }
        ]
    }
]

created_products = []

for p_data in products_data:
    payload = {"product": p_data}
    req = urllib.request.Request(
        f"https://{shop}/admin/api/2024-01/products.json",
        data=json.dumps(payload).encode("utf-8"),
        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))["product"]
            pid = res["id"]
            title = res["title"]
            print(f"✅ Producto Creado Exitosamente: [{pid}] {title}")
            created_products.append(res)
            
            # Si es de DJI, conectarlo explícitamente a la colección dji (ID: 485787435031)
            if p_data["vendor"] == "DJI":
                try:
                    c_payload = {"collect": {"collection_id": 485787435031, "product_id": pid}}
                    c_req = urllib.request.Request(
                        f"https://{shop}/admin/api/2024-01/collects.json",
                        data=json.dumps(c_payload).encode("utf-8"),
                        headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(c_req) as c_resp:
                        print(f"   ↳ Vinculado a colección DJI (ID: 485787435031)")
                except Exception as ce:
                    print(f"   ↳ Aviso collect DJI: {ce}")

        time.sleep(0.6) # respetar rate limits
    except urllib.error.HTTPError as he:
        print(f"❌ Error creando {p_data['title'][:30]}: {he.code} {he.read().decode('utf-8')}")

print(f"\n🎉 Total productos creados: {len(created_products)}")
