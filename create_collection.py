"""
Crear colección 'Zapatos de Trabajo' en Shopify
"""
import requests
import urllib3
from dotenv import load_dotenv
import os, json

urllib3.disable_warnings()
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", os.getenv("SHOPIFY_ACCESS_TOKEN", ""))
SHOP_NAME = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
API_VERSION = os.getenv("API_VERSION", "2025-01")
BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

collection_data = {
    "smart_collection": {
        "title": "Zapatos de Trabajo",
        "rules": [
            {
                "column": "tag",
                "relation": "equals",
                "condition": "zapatos-de-trabajo"
            },
            {
                "column": "tag",
                "relation": "equals", 
                "condition": "Zapatos de Trabajo"
            }
        ],
        "disjunctive": True,
        "published": True,
        "sort_order": "best-selling"
    }
}

print("Creando colección 'Zapatos de Trabajo'...")
r = requests.post(
    f"{BASE_URL}/smart_collections.json",
    headers=HEADERS,
    json=collection_data,
    verify=False,
    timeout=30
)

if r.status_code in [200, 201]:
    data = r.json()['smart_collection']
    print(f"✅ Colección creada:")
    print(f"   ID: {data['id']}")
    print(f"   Handle: {data['handle']}")
    print(f"   Título: {data['title']}")
else:
    print(f"❌ Error {r.status_code}: {r.text[:500]}")
