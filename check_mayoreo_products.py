import json
from shopify_base import get_shopify_session, BASE_URL

def check_products(collection_id):
    session = get_shopify_session()
    # Fetch first 10 products in the collection
    url = f"{BASE_URL}/collections/{collection_id}/products.json?limit=10"
    r = session.get(url)
    if r.status_code == 200:
        products = r.json().get('products', [])
        print(f"\n--- COLLECTION {collection_id} (Count: {len(products)}) ---")
        for p in products:
            print(f"ID: {p['id']}, Title: {p['title']}, Vendor: {p['vendor']}, Tags: {p.get('tags', '')}")
    else:
        print(f"Error fetching for {collection_id}: {r.status_code} - {r.text}")

def main():
    check_products(486239961111)
    check_products(486240059415)
    check_products(486240157719)

if __name__ == "__main__":
    main()
