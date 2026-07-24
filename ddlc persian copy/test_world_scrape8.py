import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

# Get the detail page and look for JSON data
r = requests.get("https://rule34.world/post/1365842", headers=headers, timeout=15)
html = r.text

# Save for analysis
with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\detail_page.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Detail page length: {len(html)}")

# Find ALL script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nTotal scripts: {len(scripts)}")

# Check each script for JSON-like content
for i, s in enumerate(scripts):
    if s.startswith('{') or s.startswith('[{"'):
        print(f"\nScript {i} starts with JSON ({len(s)} chars): {s[:500]}")
    elif 'file_url' in s or 'fileUrl' in s or 'thumbnail' in s or 'source' in s.lower():
        print(f"\nScript {i} has media-related content ({len(s)} chars): {s[:500]}")
    elif i < 3:
        print(f"\nScript {i} ({len(s)} chars): {s[:300]}")

# Look for Angular state transfer format
# Angular Universal SSR stores state in script with type="application/json" and id="serverApp-state"
state_scripts = re.findall(r'<script[^>]+id="(?:serverApp-state|ng-state|__NEXT_DATA__|app-state)"[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nState scripts found: {len(state_scripts)}")

# Look for any JSON-like patterns in the full HTML
json_blobs = re.findall(r'"file_url":\s*"([^"]+)"', html)
print(f"\nJSON file_url patterns: {len(json_blobs)}")
for u in json_blobs[:20]:
    print(f"  {u}")

json_blobs2 = re.findall(r'"fileUrl":\s*"([^"]+)"', html)
print(f"\nJSON fileUrl patterns: {len(json_blobs2)}")
for u in json_blobs2[:20]:
    print(f"  {u}")

# Look for ng-state or similar Angular SSR state markers
ng_state = re.findall(r'id="(?:ng-state|server-state|app-state|__NEXT_DATA__)"', html)
print(f"\nAngular state ID matches: {ng_state}")

# Check the homepage script content more carefully
r2 = requests.get("https://rule34.world/?tags=girlfriend_fnf", headers=headers, timeout=15)
html2 = r2.text
print(f"\n\nHomepage with tags length: {len(html2)}")

scripts2 = re.findall(r'<script[^>]*>(.*?)</script>', html2, re.DOTALL)
print(f"Homepage scripts: {len(scripts2)}")

for i, s in enumerate(scripts2):
    if len(s) > 1000 and not s.strip().startswith('try'):
        print(f"\nLarge script {i} ({len(s)} chars): {s[:800]}")
        break

# Extract ALL JSON-like objects from the page
all_json = re.findall(r'\{[^{}]*"file_url"[^{}]*\}', html2)
print(f"\nJSON objects with file_url: {len(all_json)}")
for j in all_json[:5]:
    print(f"  {j[:500]}")