"""
Extract the globalestates rendered content from aylesva.COM
by fetching the public page and parsing the section's HTML
to identify all image URLs, text content, and structure.
"""
import requests
import re
import json
import urllib3
urllib3.disable_warnings()

url = "https://www.aylesva.com/pages/globalestates"
print(f"Fetching {url}...")
r = requests.get(url, verify=False, timeout=30, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
})
html = r.text

# Save full HTML
with open("globalestates_com_full.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"Full HTML saved ({len(html)} bytes)")

# Extract the aylesva-luxury-landing section
# Look for the section wrapper
section_match = re.search(r'<div id="ayl-[^"]*">(.*?)</div>\s*<script>', html, re.DOTALL)
if not section_match:
    # Try broader pattern
    section_match = re.search(r'class="aylesva-luxury-landing">(.*?)</section>\s*(?:</div>)?\s*<script>', html, re.DOTALL)

# Extract ALL image URLs from the page
cdn_images = set()
for match in re.finditer(r'(//www\.aylesva\.com/cdn/shop/files/[^"\'?\s]+)', html):
    cdn_images.add(match.group(1))

# Also look for shop_images 
for match in re.finditer(r'(//www\.aylesva\.com/cdn/shop/files/[^"\'?\s]+|https://cdn\.shopify\.com/s/files/[^"\'?\s]+)', html):
    cdn_images.add(match.group(1))

# Look for all img src in the body content
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
if body_match:
    body = body_match.group(1)
    all_imgs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', body)
    for img in all_imgs:
        if 'aylesva.com/cdn' in img or 'cdn.shopify.com' in img:
            cdn_images.add(img)

print(f"\n=== Found {len(cdn_images)} CDN images ===")
for img in sorted(cdn_images):
    print(f"  {img}")

# Extract text content sections
# Hero
hero_match = re.search(r'class="ayl-hero">(.*?)</header>', html, re.DOTALL)
if hero_match:
    hero = hero_match.group(1)
    eyebrow = re.search(r'class="ayl-eyebrow">(.*?)</span>', hero)
    title = re.search(r'class="ayl-serif ayl-hero__title">(.*?)</h1>', hero)
    subtitle = re.search(r'class="ayl-hero__sub">(.*?)</p>', hero)
    print("\n=== HERO ===")
    if eyebrow: print(f"  Eyebrow: {eyebrow.group(1).strip()}")
    if title: print(f"  Title: {title.group(1).strip()}")
    if subtitle: print(f"  Subtitle: {subtitle.group(1).strip()}")

# Map section
map_match = re.search(r'class="ayl-map-section">(.*?)</section>', html, re.DOTALL)
if map_match:
    map_html = map_match.group(1)
    map_eyebrow = re.search(r'class="ayl-eyebrow">(.*?)</span>', map_html)
    map_title = re.search(r'class="ayl-serif">(.*?)</h2>', map_html)
    print("\n=== MAP ===")
    if map_eyebrow: print(f"  Eyebrow: {map_eyebrow.group(1).strip()}")
    if map_title: print(f"  Title: {map_title.group(1).strip()}")
    
    # Pins
    pins = re.findall(r'class="ayl-pin[^"]*"[^>]*style="left:\s*([\d.]+)%;\s*top:\s*([\d.]+)%', map_html)
    pin_names = re.findall(r'class="ayl-pin__tip">\s*<strong>(.*?)</strong>\s*<span>(.*?)</span>', map_html, re.DOTALL)
    for i, (x, y) in enumerate(pins):
        name = pin_names[i][0].strip() if i < len(pin_names) else "?"
        status = pin_names[i][1].strip() if i < len(pin_names) else "?"
        print(f"  Pin: {name} ({status}) at ({x}%, {y}%)")

# Projects
proj_sections = re.findall(r'class="ayl-proj ayl-proj--(.*?)"[^>]*>(.*?)</section>', html, re.DOTALL)
print(f"\n=== {len(proj_sections)} PROJECTS ===")
for bg, proj_html in proj_sections:
    proj_title = re.search(r'class="ayl-serif ayl-proj__title">(.*?)</h2>', proj_html)
    proj_eyebrow = re.search(r'class="ayl-eyebrow">(.*?)</span>', proj_html)
    proj_loc = re.search(r'class="ayl-loc">.*?</svg>\s*(.*?)\s*</div>', proj_html, re.DOTALL)
    
    print(f"\n  --- Project (bg: {bg}) ---")
    if proj_eyebrow: print(f"  Eyebrow: {proj_eyebrow.group(1).strip()}")
    if proj_title: print(f"  Title: {proj_title.group(1).strip()}")
    if proj_loc: print(f"  Location: {proj_loc.group(1).strip()}")
    
    # Images in this project
    proj_imgs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', proj_html)
    for img in proj_imgs:
        if 'aylesva' in img or 'cdn.shopify' in img:
            print(f"  Image: {img[:120]}")
    
    # Video
    proj_videos = re.findall(r'<video[^>]*src=["\']([^"\']+)["\']', proj_html)
    for v in proj_videos:
        print(f"  Video: {v[:120]}")

# Stats
stats = re.findall(r'class="ayl-stats__num">(.*?)</div>\s*<div class="ayl-stats__label">(.*?)</div>', html, re.DOTALL)
print("\n=== STATS ===")
for num, label in stats:
    print(f"  {num.strip()} — {label.strip()}")

# Testimonials
testis = re.findall(r'class="ayl-testi__quote">(.*?)</p>\s*<div class="ayl-testi__author">\s*<strong>(.*?)</strong>\s*<span>(.*?)</span>', html, re.DOTALL)
print(f"\n=== {len(testis)} TESTIMONIALS ===")
for quote, author, title in testis:
    print(f"  {author.strip()} ({title.strip()}): {quote.strip()[:80]}...")

print("\nDone!")
