import os
import sys
import base64
from shopify_base import BASE_URL, get_shopify_session, THEME_ID

def push_asset(local_path):
    session = get_shopify_session()
    theme_dir = os.path.join(os.getcwd(), 'theme')
    
    if not local_path.startswith(theme_dir):
        # Convert relative to absolute
        abs_path = os.path.abspath(local_path)
        if not abs_path.startswith(theme_dir):
            print("❌ File must be inside the 'theme' directory.")
            return
        local_path = abs_path
        
    # Get the asset key (e.g., templates/index.json)
    key = os.path.relpath(local_path, theme_dir)
    # Ensure forward slashes for Shopify
    key = key.replace('\\', '/')
    
    print(f"Pushing {key} to Shopify...")
    
    payload = {
        "asset": {
            "key": key
        }
    }
    
    # Read file content
    try:
        # Try reading as text first
        with open(local_path, 'r', encoding='utf-8') as f:
            payload['asset']['value'] = f.read()
    except UnicodeDecodeError:
        # It's a binary file
        with open(local_path, 'rb') as f:
            payload['asset']['attachment'] = base64.b64encode(f.read()).decode('utf-8')
            
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    response = session.put(url, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"✅ Successfully updated {key}")
    else:
        print(f"❌ Failed to update {key}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python push_theme.py <path_to_file>")
        sys.exit(1)
    
    push_asset(sys.argv[1])
