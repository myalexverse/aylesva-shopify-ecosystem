import requests
from shopify_base import get_shopify_session, BASE_URL

def main():
    session = get_shopify_session()
    r = session.get(f"{BASE_URL}/products/count.json")
    if r.status_code == 200:
        print(f"Total products in store: {r.json().get('count')}")
    else:
        print(f"Error: {r.status_code} - {r.text}")

if __name__ == "__main__":
    main()
