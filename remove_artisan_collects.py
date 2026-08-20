import time
import requests
from shopify_base import get_shopify_session, BASE_URL

COLLECTIONS = [486239961111, 486240059415, 486240157719]

def get_collect_id(session, collection_id, product_id):
    """Retrieve the Collect ID for a given product and collection combination"""
    url = f"{BASE_URL}/collects.json?collection_id={collection_id}&product_id={product_id}"
    r = session.get(url)
    if r.status_code == 200:
        collects = r.json().get('collects', [])
        if collects:
            return collects[0]['id']
    return None

def remove_from_collection(session, collect_id):
    """Delete the collect connection (remove product from collection)"""
    url = f"{BASE_URL}/collects/{collect_id}.json"
    r = session.delete(url)
    return r.status_code in [200, 204]

def run_cleanup():
    session = get_shopify_session()
    
    for collection_id in COLLECTIONS:
        print(f"\n==========================================")
        print(f"STARTING CLEANUP FOR COLLECTION: {collection_id}")
        print(f"==========================================")
        
        # 1. Fetch all products in this collection
        url = f"{BASE_URL}/collections/{collection_id}/products.json?limit=250"
        all_products = []
        page = 1
        
        while url:
            r = session.get(url)
            if r.status_code != 200:
                print(f"Error fetching products on page {page}: {r.status_code}")
                break
            data = r.json()
            products = data.get('products', [])
            if not products:
                break
            all_products.extend(products)
            
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
            
        print(f"Found {len(all_products)} total products in collection.")
        
        # 2. Filter products to find artisan candidates
        removed_count = 0
        failed_count = 0
        
        for i, p in enumerate(all_products):
            title = p.get('title', '')
            title_lower = title.lower()
            p_type_lower = p.get('product_type', '').lower()
            tags = [t.lower() for t in p.get('tags', '').split(', ')]
            
            # Identify if it is artisan
            is_artisan = False
            reasons = []
            
            if "artesanal" in p_type_lower or "artesania" in p_type_lower or "hecho a mano" in p_type_lower:
                is_artisan = True
                reasons.append("Type")
                
            for kw in ["artesanal", "artesania", "hecho a mano", "artesano", "comunidad", "técnica"]:
                if any(kw in t for t in tags) or kw in title_lower:
                    is_artisan = True
                    reasons.append(f"Keyword '{kw}' in Title/Tag")
                    
            if is_artisan:
                # Remove this product from the collection
                print(f"[{i+1}/{len(all_products)}] MATCH: '{title}' (ID: {p['id']}, Reasons: {list(set(reasons))})")
                collect_id = get_collect_id(session, collection_id, p['id'])
                if collect_id:
                    success = remove_from_collection(session, collect_id)
                    if success:
                        print(f"  -> SUCCESS: Removed from collection. (Collect ID: {collect_id})")
                        removed_count += 1
                    else:
                        print(f"  -> FAILED to remove from collection.")
                        failed_count += 1
                else:
                    print(f"  -> WARNING: Collect ID not found.")
                    failed_count += 1
                
                time.sleep(0.5)  # Rate limiting
                
        print(f"\nCollection {collection_id} finished. Removed: {removed_count}, Failed: {failed_count}")
        time.sleep(1.0)

if __name__ == "__main__":
    run_cleanup()
