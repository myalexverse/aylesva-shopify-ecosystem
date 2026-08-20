import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()
load_dotenv()

# We can specify custom values or fallback to environment variables
SHOP_NAME = "aylesva-mayoreo.myshopify.com"
# The user can set MAYOREO_ACCESS_TOKEN in .env or we can use ACCESS_TOKEN if it is updated
ACCESS_TOKEN = os.getenv("MAYOREO_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")
API_VERSION = "2025-01"

BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"

# Beautiful HTML contents for the pages
FAQ_BODY = """
<div class="ayl-faq-container" style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; color: #333;">
  <h2 style="text-align: center; color: #4A0E17; margin-bottom: 30px; font-weight: 800;">Preguntas Frecuentes (FAQ)</h2>
  
  <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
    <h3 style="color: #4A0E17; font-size: 18px; margin-bottom: 8px;">¿Cuál es el mínimo de compra para mayoreo?</h3>
    <p style="color: #666; line-height: 1.6; font-size: 15px;">El mínimo de compra para acceder a precios de distribuidor es de 36 piezas, o adquiriendo cualquiera de nuestros paquetes preconfigurados (Starter, Emprendedor o Tienda Pro).</p>
  </div>
  
  <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
    <h3 style="color: #4A0E17; font-size: 18px; margin-bottom: 8px;">¿Cómo me registro como distribuidor?</h3>
    <p style="color: #666; line-height: 1.6; font-size: 15px;">Puedes crear una cuenta de distribuidor ingresando a la sección "Registrarse" en el menú superior o en el footer. Una vez registrado, nuestro equipo validará tu cuenta para darte acceso a las tarifas de mayoreo.</p>
  </div>

  <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
    <h3 style="color: #4A0E17; font-size: 18px; margin-bottom: 8px;">¿Cuánto tiempo tarda en llegar mi pedido?</h3>
    <p style="color: #666; line-height: 1.6; font-size: 15px;">El procesamiento de pedidos de mayoreo toma de 2 a 4 días hábiles. El envío terrestre por paquetería express tarda de 3 a 5 días hábiles adicionales a todo México.</p>
  </div>

  <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
    <h3 style="color: #4A0E17; font-size: 18px; margin-bottom: 8px;">¿Qué métodos de pago aceptan?</h3>
    <p style="color: #666; line-height: 1.6; font-size: 15px;">Aceptamos pagos seguros mediante tarjetas de crédito/débito, transferencias electrónicas SPEI, y pagos en efectivo en tiendas de conveniencia mediante procesadores autorizados en nuestra pasarela de pagos.</p>
  </div>
</div>
"""

ABOUT_BODY = """
<div class="ayl-about-container" style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; color: #333; line-height: 1.8;">
  <h2 style="text-align: center; color: #4A0E17; margin-bottom: 30px; font-weight: 800;">Nuestra Historia</h2>
  <p style="font-size: 16px; margin-bottom: 15px; text-align: justify;">
    <strong>Aylesva</strong> nació con la pasión de llevar la esencia, elegancia y calidad de la moda country y vaquera a cada rincón de México. Creemos que vestir con estilo vaquero es una declaración de libertad, orgullo y tradición.
  </p>
  <p style="font-size: 16px; margin-bottom: 15px; text-align: justify;">
    Como distribuidores autorizados de las marcas más reconocidas y fabricantes de calzado vaquero de alta calidad, nos especializamos en ofrecer una selección exclusiva de botas exóticas, sombreros finos, chalecos premium y camisas vaqueras diseñadas tanto para el trabajo diario como para eventos especiales.
  </p>
  <p style="font-size: 16px; margin-bottom: 15px; text-align: justify;">
    Nuestra plataforma de <strong>Mayoreo</strong> está diseñada para apoyar a emprendedores y tiendas establecidas a hacer crecer sus negocios, ofreciéndoles inventario garantizado, atención al cliente de primer nivel y precios sumamente competitivos.
  </p>
</div>
"""

TRACKING_BODY = """
<div class="ayl-track-container" style="max-width: 600px; margin: 0 auto; padding: 40px 20px; font-family: sans-serif; color: #333; text-align: center;">
  <h2 style="color: #4A0E17; margin-bottom: 15px; font-weight: 800;">Rastrea tu Pedido</h2>
  <p style="color: #666; margin-bottom: 30px; font-size: 15px;">Ingresa el número de guía de tu paquetería para consultar el estado actual de tu envío de mayoreo.</p>
  
  <div style="background: #fdfdfd; border: 1px solid #e0e0e0; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
    <input type="text" id="tracking_number" placeholder="Número de rastreo (Ej. 12345678)" style="width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; box-sizing: border-box;" />
    <button onclick="trackOrder()" style="width: 100%; padding: 12px; background: #4A0E17; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s;">Consultar Envío</button>
  </div>
  
  <script>
    function trackOrder() {
      var num = document.getElementById('tracking_number').value.trim();
      if (!num) {
        alert('Por favor, ingresa un número de rastreo.');
        return;
      }
      // Redirect to a universal tracking service or dynamic search
      window.open('https://www.17track.net/txtr?nums=' + num, '_blank');
    }
  </script>
</div>
"""

WISHLIST_BODY = """
<div class="ayl-wishlist-container" style="max-width: 800px; margin: 0 auto; padding: 40px 20px; font-family: sans-serif; text-align: center; color: #333;">
  <h2 style="color: #4A0E17; margin-bottom: 20px; font-weight: 800;">Mis Favoritos</h2>
  <p style="color: #666; font-size: 16px;">Aquí podrás ver los productos de mayoreo que has guardado en tu lista de deseos.</p>
  
  <!-- App block placeholder / custom script target -->
  <div id="wishlist-hero-app-container" style="margin-top: 40px; min-height: 200px; display: flex; align-items: center; justify-content: center; border: 2px dashed #ddd; border-radius: 8px; background: #fafafa;">
    <p style="color: #999;">Tu lista de favoritos está vacía. Navega por nuestro catálogo de mayoreo y haz clic en el icono de corazón en tus productos preferidos.</p>
  </div>
</div>
"""

PAGES_TO_CREATE = [
    {
        "title": "Preguntas Frecuentes",
        "handle": "preguntas-frecuentes",
        "body_html": FAQ_BODY
    },
    {
        "title": "Nuestra Historia",
        "handle": "acerca-de-nosotros",
        "body_html": ABOUT_BODY
    },
    {
        "title": "Rastrea tu pedido",
        "handle": "rastreo",
        "body_html": TRACKING_BODY
    },
    {
        "title": "Wishlist",
        "handle": "wishlist",
        "body_html": WISHLIST_BODY
    }
]

def create_pages():
    if not ACCESS_TOKEN:
        print("❌ Error: No API Access Token found. Please set MAYOREO_ACCESS_TOKEN or ACCESS_TOKEN in your environment or .env file.")
        print("You can also run this script by editing the token directly inside the code.")
        return

    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    session = requests.Session()
    session.headers.update(headers)

    print(f"Connecting to {SHOP_NAME}...")

    for page in PAGES_TO_CREATE:
        handle = page["handle"]
        title = page["title"]
        
        # Check if page already exists
        check_url = f"{BASE_URL}/pages.json?handle={handle}"
        try:
            r = session.get(check_url, verify=False, timeout=30)
            if r.status_code == 200:
                existing = r.json().get("pages", [])
                if existing:
                    print(f"ℹ️ Page '{title}' ({handle}) already exists (ID: {existing[0]['id']}). Skipping creation.")
                    continue
            else:
                print(f"⚠️ Warning checking '{handle}': {r.status_code} - {r.text}")
        except Exception as e:
            print(f"❌ Error connecting to check page: {e}")
            continue

        print(f"Creating page '{title}'...")
        payload = {
            "page": page
        }
        
        r = session.post(f"{BASE_URL}/pages.json", json=payload, verify=False, timeout=30)
        if r.status_code in [200, 201]:
            data = r.json()["page"]
            print(f"✅ Successfully created page! ID: {data['id']}, URL: /pages/{data['handle']}")
        else:
            print(f"❌ Failed to create page '{title}': {r.status_code} - {r.text}")

if __name__ == "__main__":
    create_pages()
