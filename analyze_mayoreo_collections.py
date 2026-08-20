import json
import time
from shopify_base import get_shopify_session, BASE_URL

def analyze_collection(collection_id):
    session = get_shopify_session()
    vendors = {}
    types = {}
    total_products = 0
    
    url = f"{BASE_URL}/collections/{collection_id}/products.json?limit=250"
    page = 1
    
    while url:
        r = session.get(url)
        if r.status_code != 200:
            print(f"Error fetching page {page} for collection {collection_id}: {r.status_code}")
            break
            
        data = r.json()
        products = data.get('products', [])
        if not products:
            break
            
        total_products += len(products)
        for p in products:
            vendor = p.get('vendor', 'Unknown')
            p_type = p.get('product_type', 'Unknown')
            vendors[vendor] = vendors.get(vendor, 0) + 1
            types[p_type] = types.get(p_type, 0) + 1
            
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
        
    print(f"\n==========================================")
    print(f"COLLECTION ID: {collection_id}")
    print(f"Total Products Checked: {total_products}")
    print("Vendors:")
    for v, count in sorted(vendors.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {v}: {count}")
    print("Product Types:")
    for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {t}: {count}")
    print(f"==========================================")

def main():
    analyze_collection(486239961111)
    analyze_collection(486240059415)
    analyze_collection(486240157719)

if __name__ == "__main__":
    main()
