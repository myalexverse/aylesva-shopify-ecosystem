import json
import requests
from shopify_base import get_shopify_session, BASE_URL

def main():
    session = get_shopify_session()
    
    print("--- CUSTOM COLLECTIONS ---")
    r = session.get(f"{BASE_URL}/custom_collections.json")
    if r.status_code == 200:
        for c in r.json().get('custom_collections', []):
            print(f"ID: {c['id']}, Title: {c['title']}, Handle: {c['handle']}")
    else:
        print(f"Error fetching custom collections: {r.status_code} - {r.text}")

    print("\n--- SMART COLLECTIONS ---")
    r = session.get(f"{BASE_URL}/smart_collections.json")
    if r.status_code == 200:
        for c in r.json().get('smart_collections', []):
            print(f"ID: {c['id']}, Title: {c['title']}, Handle: {c['handle']}")
    else:
        print(f"Error fetching smart collections: {r.status_code} - {r.text}")

if __name__ == "__main__":
    main()
