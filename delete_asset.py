import sys
from shopify_base import BASE_URL, get_shopify_session, THEME_ID

def delete_asset(key):
    session = get_shopify_session()
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]={key}"
    print(f"Deleting {key} from Shopify theme {THEME_ID}...")
    response = session.delete(url)
    if response.status_code in [200, 204]:
        print(f"✅ Successfully deleted {key}")
    else:
        print(f"❌ Failed to delete {key}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_asset.py <asset_key>")
        sys.exit(1)
    delete_asset(sys.argv[1])
