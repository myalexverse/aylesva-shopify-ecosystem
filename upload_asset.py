#!/usr/bin/env python3
"""Upload an image file to the Shopify theme assets."""
import sys, os, base64
sys.path.insert(0, os.path.dirname(__file__))
from shopify_base import get_shopify_session, THEME_ID, BASE_URL

session = get_shopify_session()
def upload_asset(local_path, asset_key):
    with open(local_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    
    resp = session.put(
        f"{BASE_URL}/themes/{THEME_ID}/assets.json",
        json={"asset": {"key": asset_key, "attachment": data}}
    )
    if resp.status_code in (200, 201):
        url = resp.json().get("asset", {}).get("public_url", "")
        print(f"✅ Uploaded: {asset_key}")
        print(f"   URL: {url}")
        return url
    else:
        print(f"❌ Error {resp.status_code}: {resp.text[:300]}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_asset.py <local_path> <filename>")
        sys.exit(1)
    local = sys.argv[1]
    name = sys.argv[2]
    upload_asset(local, f"assets/{name}")
