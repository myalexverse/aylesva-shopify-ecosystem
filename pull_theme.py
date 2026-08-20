import os
import sys
import time
import base64
from shopify_base import BASE_URL, get_shopify_session, THEME_ID

def pull_theme():
    session = get_shopify_session()
    
    # Get list of all assets
    print(f"Fetching list of theme assets from theme ID {THEME_ID}...")
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch assets list: {response.text}")
        return
        
    assets = response.json().get('assets', [])
    print(f"Found {len(assets)} assets. Downloading...")
    
    theme_dir = os.path.join(os.getcwd(), 'theme')
    
    for i, asset in enumerate(assets, 1):
        key = asset['key']
        print(f"[{i}/{len(assets)}] Downloading {key}...")
        
        # Determine local path
        local_path = os.path.join(theme_dir, key)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Fetch the actual asset content
        asset_url = f"{url}?asset[key]={key}"
        
        max_retries = 5
        for attempt in range(max_retries):
            res = session.get(asset_url)
            if res.status_code == 429:
                time.sleep(2)
                continue
            break
            
        if res.status_code != 200:
            print(f"  ❌ Failed to download {key}: {res.status_code}")
            continue
            
        asset_data = res.json().get('asset', {})
        
        if 'value' in asset_data:
            # Text file
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(asset_data['value'])
        elif 'attachment' in asset_data:
            # Binary file
            with open(local_path, 'wb') as f:
                f.write(base64.b64decode(asset_data['attachment']))
        else:
            print(f"  ⚠️ Warning: {key} has no content to save.")
            
    print("✅ Theme pull complete! All files saved to the 'theme' directory.")

if __name__ == "__main__":
    pull_theme()
