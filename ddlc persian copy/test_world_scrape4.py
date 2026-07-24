import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

# Test with "Accept-Encoding": "identity" to bypass Cloudflare br/gzip issues
r = requests.get('https://rule34.world/', headers=headers, timeout=15)
html = r.text  # raw content since Accept-Encoding: identity
print(f"Status: {r.status_code}, HTML length: {len(html)}")

# Save the raw HTML
with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\homepage_raw.txt", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved homepage_raw.txt")

# Check the first 500 chars (printable)
printable = ''.join(c if c.isprintable() or c in '\n\r\t' else '.' for c in html[:2000])
print(printable[:2000])

# Find script tags with content
script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL)
scripts = script_pattern.findall(html)
print(f"\n=== Found {len(scripts)} script tags ===")

# Check for any image tags
img_pattern = re.compile(r'<img[^>]*>', re.IGNORECASE)
imgs = img_pattern.findall(html)
print(f"=== Found {len(imgs)} img tags ===")

# Check for base64 patterns
b64_pattern = re.compile(r'data:image/[^;]+;base64,[^"\'<>]+')
b64s = b64_pattern.findall(html)
print(f"=== Found {len(b64s)} base64 images ===")

# Look for any JSON data blobs
json_state = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', html, re.DOTALL)
print(f"=== __INITIAL_STATE__: {len(json_state)} ===")

# Look for Angular transfer state
ng_transfer = re.findall(r'<script[^>]+id="ng-state"[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"=== ng-state: {len(ng_transfer)} ===")

# Check for <app-root> or similar Angular root
app_root = re.findall(r'<[a-z]+-root[^>]*>', html)
print(f"=== App root elements: {app_root} ===")

# Look for any file extension patterns (.jpg, .png, .webp, .mp4)
file_urls = re.findall(r'https?://[^"\'<>\s]+\.(?:jpg|jpeg|png|webp|mp4|gif|webm)[^"\'<>\s]*', html)
print(f"=== Found {len(file_urls)} file URLs ===")
for f in file_urls[:15]:
    print(f"  {f}")

# Look for any URL with /posts/ or post ID patterns
post_refs = re.findall(r'/[^"\'<>\s]*post[^"\'<>\s]*', html)
print(f"\n=== Post references: {len(post_refs)} ===")
for p in post_refs[:20]:
    print(f"  {p}")

# Try to find Angular root div
ng_root = re.findall(r'<div[^>]*id="(?:root|app|main)"[^>]*>', html)
print(f"\n=== Root divs: {ng_root} ===")

# Check for ANY href or link
links = re.findall(r'href="([^"]+)"', html)
print(f"\n=== Links: {len(links)} ===")
for l in links[:20]:
    print(f"  {l}")