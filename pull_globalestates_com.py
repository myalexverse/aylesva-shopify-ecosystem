"""
Pull the globalestates page template from aylesva.COM
(pad7vv-sx.myshopify.com / shop_id 74907353285 / theme 156693823685)

This script requires the Shopify Admin API access token for aylesva.com.
"""
import os
import json
import requests
import urllib3
urllib3.disable_warnings()

# aylesva.COM credentials 
# The storefront token is: c6ca01044fb4dbb4b9e932b007f2f939
# The myshopify domain is: pad7vv-sx.myshopify.com
# The active theme ID is: 156693823685
SHOP_NAME = "pad7vv-sx.myshopify.com"
THEME_ID = "156693823685"
API_VERSION = "2025-01"

# Try to get the access token from env
ACCESS_TOKEN = os.getenv("AYLESVA_COM_ACCESS_TOKEN", "")

if not ACCESS_TOKEN:
    print("❌ No access token for aylesva.COM found.")
    print("   Please set AYLESVA_COM_ACCESS_TOKEN in your environment or .env file.")
    print("")
    print("   To get the token, go to aylesva.com Shopify Admin > Settings > Apps and sales channels > Develop apps")
    print("   Or check if you have the token in any other config file.")
    print("")
    print("   Alternatively, you can get the template directly from the Shopify admin:")
    print(f"   1. Go to https://pad7vv-sx.myshopify.com/admin/themes/{THEME_ID}/editor")
    print("   2. Navigate to templates/page.globalestates.json")
    print("   3. Copy the content")
    exit(1)

BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Pull the template file
print(f"Pulling template from aylesva.COM (theme {THEME_ID})...")
url = f"{BASE_URL}/themes/{THEME_ID}/assets.json?asset[key]=templates/page.globalestates.json"
r = requests.get(url, headers=HEADERS, verify=False, timeout=30)

if r.status_code == 200:
    data = r.json()
    value = data["asset"]["value"]
    template = json.loads(value)
    
    # Save prettified
    output_path = os.path.join(os.path.dirname(__file__), "globalestates_com_template.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Template saved to: {output_path}")
    print(json.dumps(template, indent=2, ensure_ascii=False)[:3000])
else:
    print(f"❌ Failed: {r.status_code}")
    print(r.text[:500])
