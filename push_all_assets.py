import os
import time
from push_theme import push_asset

def push_all():
    theme_dir = os.path.join(os.getcwd(), 'theme')
    if not os.path.exists(theme_dir):
        print(f"❌ Directory {theme_dir} does not exist.")
        return

    print(f"🚀 Starting full theme upload from {theme_dir}...")
    
    # Track success/failure
    success_count = 0
    fail_count = 0
    
    for root, dirs, files in os.walk(theme_dir):
        for file in files:
            if file.startswith('.') or file == 'config.yml':
                continue
                
            local_path = os.path.join(root, file)
            try:
                # We reuse the logic from push_theme.py
                # Note: push_asset prints its own status
                push_asset(local_path)
                success_count += 1
            except Exception as e:
                print(f"❌ Fatal error pushing {file}: {e}")
                fail_count += 1
            
            # Small sleep to be polite to Shopify API (though push_asset is synchronous)
            time.sleep(0.1)

    print(f"\n--- Upload Complete ---")
    print(f"✅ Successfully updated: {success_count}")
    if fail_count > 0:
        print(f"❌ Failed: {fail_count}")
    else:
        print(f"✨ All assets uploaded successfully.")

if __name__ == "__main__":
    push_all()
