import time
from shopify_base import get_shopify_session, BASE_URL

def find_candidates(collection_id):
    session = get_shopify_session()
    url = f"{BASE_URL}/collections/{collection_id}/products.json?limit=250"
    page = 1
    candidates = []
    
    while url:
        r = session.get(url)
        if r.status_code != 200:
            print(f"Error: {r.status_code}")
            break
        data = r.json()
        products = data.get('products', [])
        if not products:
            break
            
        for p in products:
            title = p.get('title', '').lower()
            vendor = p.get('vendor', '')
            p_type = p.get('product_type', '').lower()
            tags = [t.lower() for t in p.get('tags', '').split(', ')]
            
            is_artisan = False
            reasons = []
            
            # Check vendor
            if vendor != "Diana Zapateria Inc":
                is_artisan = True
                reasons.append(f"Vendor is {vendor}")
                
            # Check type
            if "artesanal" in p_type or "artesania" in p_type or "hecho a mano" in p_type:
                is_artisan = True
                reasons.append(f"Type is {p.get('product_type')}")
                
            # Check tags
            for keyword in ["artesanal", "artesania", "hecho a mano", "artesano", "comunidad", "técnica"]:
                if any(keyword in t for t in tags):
                    is_artisan = True
                    reasons.append(f"Tag contains {keyword}")
            
            if is_artisan:
                candidates.append({
                    'id': p['id'],
                    'title': p['title'],
                    'vendor': vendor,
                    'type': p.get('product_type'),
                    'tags': p.get('tags'),
                    'reasons': reasons
                })
                
        # Pagination
        link_header = r.headers.get('Link', '')
        if 'rel="next"' in link_header:
            parts = link_header.split(',')
            for part in parts:
                if 'rel="next"' in part:
                    url = part.split('<')[1].split('>')[0]
                    page += 1
                    break
        else:
            url = None
        time.sleep(0.5)
        
    print(f"\nCandidates in Collection {collection_id}: {len(candidates)}")
    for c in candidates:
        print(f"  - ID: {c['id']}, Title: {c['title']}, Vendor: {c['vendor']}, Type: {c['type']}, Reasons: {c['reasons']}")
    return candidates

def main():
    find_candidates(486239961111)
    find_candidates(486240059415)
    find_candidates(486240157719)

if __name__ == "__main__":
    main()
