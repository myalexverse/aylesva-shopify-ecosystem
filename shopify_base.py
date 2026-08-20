import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings()

# Load credentials from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", os.getenv("SHOPIFY_ACCESS_TOKEN", ""))
SHOP_NAME = os.getenv("SHOP_NAME", "aylesvamx.myshopify.com")
API_VERSION = os.getenv("API_VERSION", "2025-01")
THEME_ID = os.getenv("THEME_ID", "172455165975")

BASE_URL = f"https://{SHOP_NAME}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_shopify_session():
    """Returns a requests session configured with Shopify headers"""
    session = requests.Session()
    session.headers.update(HEADERS)
    return session
