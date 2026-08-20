"""
Script to check collections via the public storefront.
Uses the /collections/{handle}/products.json storefront endpoint.
"""
import json
import time
import requests
import urllib3

urllib3.disable_warnings()

SHOP_URL = "https://aylesvamx.myshopify.com"

# Full list of collection handles from the theme code analysis
ALL_HANDLES = [
    # Custom collections (from API)
    "camaras-1", "celulares", "damas-spot", "dji", "tenis", "yeti",
    
    # Root parent categories
    "mujer", "hombre", "nino", "nina", "bebe", "artesanal", "hogar", "alimentos", "electronicos", "vehiculos",
    
    # Level 2 - Mujer
    "ropa-mujer", "calzado-mujer", "ropa-interior-y-lenceria", "joyeria-y-accesorios", "bolsas-y-carteras",
    "accesorios-de-moda", "belleza-y-cuidado-personal", "maternidad",
    
    # Level 2 - Hombre  
    "ropa-hombre", "calzado-hombre", "ropa-interior-hombre", "accesorios-hombre", "joyeria", "cuidado-personal",
    
    # Level 2 - Niño
    "ropa-nino", "calzado-nino", "ropa-interior-nino", "accesorios-nino",
    
    # Level 2 - Niña
    "ropa-nina", "calzado-nina", "ropa-interior-nina", "accesorios-nina",
    
    # Level 2 - Bebé
    "ropa-bebe", "calzado-bebe", "ropa-interior-y-panaleria", "accesorios-bebe", "higiene-y-cuidado",
    
    # Level 2 - Artesanal
    "textiles-y-tejidos", "ceramica-y-barro", "madera", "joyeria-artesanal", "cuero-y-piel",
    "papel-y-carton", "vidrio-y-cristal", "metal", "piedra", "arte-decorativo-y-pinturas",
    "velas-y-aromaterapia-artesanal", "juguetes-y-muncos-tradicionales", "instrumentos-musicales-artesanales",
    
    # Level 2 - Hogar
    "muebles", "decoracion-del-hogar", "iluminacion", "cocina-y-comedor", "bano",
    "recamara", "recamara-y-ropa-de-cama", "jardin", "jardin-y-exterior",
    "organizacion-y-almacenamiento", "arte-y-coleccionables",
    
    # Level 2 - Alimentos
    "alimentos-artesanales", "bebidas-artesanales", "productos-organicos", "productos-organicos-y-naturales",
    "reposteria", "reposteria-y-panaderia", "regalos-gourmet", "canastas-y-regalos-gourmet",
    
    # Level 2 - Electrónicos
    "telefonos", "telefonos-y-comunicacion", "computadoras", "computadoras-y-laptops",
    "audio-y-video", "audio-y-sonido", "television-y-video", "fotografia-y-video",
    "videojuegos", "electrodomesticos", "gadgets", "wearables-y-gadgets",
    "redes-e-internet", "energia-y-carga", "seguridad-electronica",
    
    # Level 2 - Vehículos
    "automoviles", "motocicletas", "vehiculos-trabajo", "vehiculos-de-carga-y-trabajo",
    "refacciones", "accesorios-y-refacciones", "vehiculos-recreativos", "transporte-publico-y-comercial",
    
    # Special/Utility
    "all", "frontpage", "on-sale", "ofertas", "saldos", "mayoreo", "2x1",
    
    # Level 3 - Mujer > Ropa
    "blusas-y-camisas", "vestidos-mujer", "faldas-mujer", "pantalones-y-jeans-mujer",
    "shorts-y-bermudas-mujer", "abrigos-y-chaquetas-mujer", "sudaderas-y-hoodies-mujer",
    "trajes-y-blazers-mujer", "ropa-deportiva-mujer", "pijamas-y-ropa-de-dormir-mujer", "overoles-y-monos-mujer",
    
    # Level 3 - Mujer > Calzado
    "tacones-y-stilettos", "sandalias-mujer", "flats-y-bailarinas", "botas-y-botines-mujer",
    "tenis-y-sneakers-mujer", "zapatos-de-trabajo", "pantuflas-y-chanclas", "plataformas",
    
    # Level 3 - Mujer > Lencería
    "brasieres-y-bras", "panties-y-calzones", "bodies", "fajas-y-moldeadores",
    "medias-y-calcetas", "pijamas-y-lenceria",
    
    # Level 3 - Mujer > Joyería
    "collares", "aretes-y-pendientes", "pulseras-y-brazaletes", "anillos-mujer", "relojes-mujer",
    
    # Level 3 - Mujer > Bolsas
    "bolsas-de-mano", "mochilas-mujer", "clutches-y-sobre", "bolsas-de-playa",
    "carteras-y-billeteras-mujer", "tote-bags",
    
    # Level 3 - Mujer > Accesorios
    "cinturones-mujer", "bufandas-y-chales", "gorros-y-sombreros-mujer",
    "lentes-de-sol-mujer", "diademas-y-accesorios-para-el-cabello-mujer",
    
    # Level 3 - Mujer > Belleza
    "maquillaje", "skincare-cuidado-de-la-piel", "perfumes-y-fragancias",
    "cuidado-del-cabello-mujer", "cuidado-de-unas",
    
    # Level 3 - Mujer > Maternidad
    "ropa-de-embarazo", "ropa-de-lactancia", "fajas-postparto",
    
    # Level 3 - Hombre > Ropa
    "camisas-formales-y-casuales", "camisetas-y-polos-hombre", "pantalones-y-jeans-hombre",
    "shorts-y-bermudas-hombre", "trajes-y-blazers-hombre", "abrigos-y-chaquetas-hombre",
    "sudaderas-y-hoodies-hombre", "ropa-deportiva-hombre", "pijamas-y-ropa-de-dormir-hombre",
    
    # Level 3 - Hombre > Calzado
    "zapatos-formales", "botas-y-botines-hombre", "botas-exoticas", "tenis-y-sneakers-hombre",
    "sandalias-y-chanclas", "mocasines-y-loafers", "pantuflas-hombre",
    
    # Level 3 - Hombre > Ropa Interior
    "calzoncillos-y-boxers", "camisetas-interiores-hombre", "medias-y-calcetines-hombre", "pijamas-hombre",
    
    # Level 3 - Hombre > Accesorios
    "cinturones-hombre", "corbatas-y-panuelos", "relojes-hombre", "lentes-de-sol-hombre",
    "gorras-y-sombreros-hombre", "maletines-y-mochilas",
    
    # Level 3 - Hombre > Joyería
    "anillos-hombre", "pulseras", "cadenas-y-collares", "aretes",
    
    # Level 3 - Hombre > Cuidado Personal
    "perfumes-y-colonias", "cuidado-de-la-barba", "skincare-masculino", "cuidado-del-cabello-hombre",
    
    # Additional from header
    "camisas-vaqueras-y-de-broche", "chalecos-blazers-y-chamarras",
]

def log(msg):
    print(msg, flush=True)

def check_collection(handle):
    """Check if a collection exists and has products via storefront"""
    url = f"{SHOP_URL}/collections/{handle}/products.json?limit=1"
    try:
        r = requests.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            data = r.json()
            products = data.get('products', [])
            return {'exists': True, 'has_products': len(products) > 0}
        elif r.status_code == 404:
            return {'exists': False, 'has_products': False}
        else:
            return {'exists': None, 'has_products': None}
    except Exception as e:
        return {'exists': None, 'has_products': None, 'error': str(e)}

def main():
    log("=" * 90)
    log("ANÁLISIS DE COLECCIONES VÍA STOREFRONT - AYLESVA")
    log("=" * 90)
    
    results = []
    total = len(ALL_HANDLES)
    
    for i, handle in enumerate(ALL_HANDLES):
        result = check_collection(handle)
        result['handle'] = handle
        results.append(result)
        
        if result['exists'] is None:
            status = "⚠️  ERROR"
        elif not result['exists']:
            status = "🔴 NO EXISTE"
        elif result['has_products']:
            status = "✅ CON PRODS"
        else:
            status = "❌ VACÍA"
        
        log(f"  {i+1}/{total} {status} {handle}")
        time.sleep(0.3)  # Throttle to avoid rate limits
    
    # Categorize
    log("\n" + "=" * 90)
    log("RESUMEN")
    log("=" * 90)
    
    not_exist = [r for r in results if r.get('exists') == False]
    empty = [r for r in results if r.get('exists') == True and r.get('has_products') == False]
    with_products = [r for r in results if r.get('exists') == True and r.get('has_products') == True]
    errors = [r for r in results if r.get('exists') is None]
    
    log(f"\n✅ Colecciones con productos: {len(with_products)}")
    log(f"❌ Colecciones vacías (existen pero sin productos): {len(empty)}")
    log(f"🔴 Colecciones que no existen en Shopify: {len(not_exist)}")
    log(f"⚠️  Errores de conexión: {len(errors)}")
    
    if with_products:
        log("\n--- CON PRODUCTOS ---")
        for r in with_products:
            log(f"  ✅ {r['handle']}")
    
    if empty:
        log("\n--- VACÍAS (existen pero 0 productos) ---")
        for r in empty:
            log(f"  ❌ {r['handle']}")
    
    if not_exist:
        log("\n--- NO EXISTEN EN SHOPIFY ---")
        for r in not_exist:
            log(f"  🔴 {r['handle']}")
    
    with open("collections_storefront_analysis.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"\n💾 Datos guardados en collections_storefront_analysis.json")

if __name__ == "__main__":
    main()
