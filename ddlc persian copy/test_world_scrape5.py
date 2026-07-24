import requests
import re
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

r = requests.get('https://rule34.world/', headers=headers, timeout=15)
html = r.text

results = []
results.append(f"Status: {r.status_code}, HTML length: {len(html)}")

# Write first 3000 chars to see structure
results.append("\n=== FIRST 3000 CHARS ===")
results.append(html[:3000])

# Find all script tags with content
script_pattern = re.compile(r'<script[^>]*>(.*?)</script>', re.DOTALL)
scripts = script_pattern.findall(html)
results.append(f"\n=== Found {len(scripts)} script tags ===")
for i, s in enumerate(scripts):
    results.append(f"\nScript {i} ({len(s)} chars): {s[:300]}")

# img tags
img_pattern = re.compile(r'<img[^>]*>', re.IGNORECASE)
imgs = img_pattern.findall(html)
results.append(f"\n=== Found {len(imgs)} img tags ===")
for i in imgs[:20]:
    results.append(f"  {i[:300]}")

# Check for any URL patterns
file_urls = re.findall(r'https?://[^"\'<>\s]*\.(?:jpg|jpeg|png|webp|mp4|gif|webm)[^"\'<>\s]*', html)
results.append(f"\n=== Found {len(file_urls)} image/video URLs ===")
for f in file_urls[:30]:
    results.append(f"  {f}")

# Post references
post_refs = re.findall(r'/[^"\'<>\s]*post[^"\'<>\s]*', html)
results.append(f"\n=== Post references: {len(post_refs)} ===")
for p in post_refs[:30]:
    results.append(f"  {p}")

# Links
links = re.findall(r'href="([^"]+)"', html)
results.append(f"\n=== All href links: {len(links)} ===")
for l in links[:40]:
    results.append(f"  {l}")

# JSON patterns
json_blobs = re.findall(r'window\.__[A-Z_]+__\s*=\s*({.*?});', html, re.DOTALL)
results.append(f"\n=== Window __STATE__ blobs: {len(json_blobs)} ===")
for j in json_blobs[:5]:
    results.append(f"  {j[:500]}")

# Check for <body> content
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
if body_match:
    body = body_match.group(1)
    results.append(f"\n=== BODY content ({len(body)} chars) ===")
    results.append(body[:2000])

with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\analysis_results.txt", "w", encoding="utf-8") as f:
    for line in results:
        f.write(str(line) + "\n")

print("Analysis complete - saved to analysis_results.txt")