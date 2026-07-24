import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
}

# Get the homepage to see the full HTML structure
r = requests.get("https://rule34.world/", headers=headers, timeout=15)
html = r.text

# Save full HTML for inspection
with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\homepage.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Homepage length: {len(html)}")

# Find all script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nTotal script tags: {len(scripts)}")

# Find any script with src
script_srcs = re.findall(r'<script[^>]*src="([^"]+)"', html)
print(f"Script srcs: {len(script_srcs)}")
for s in script_srcs[:20]:
    print(f"  {s}")

# Find API-like patterns in HTML
api_patterns = re.findall(r'https?://[^"\'<> ]*api[^"\'<> ]*', html)
print(f"\nAPI-like URLs: {len(api_patterns)}")
for a in api_patterns[:10]:
    print(f"  {a}")

# Find any JSON/state patterns
state_patterns = re.findall(r'"baseUrl":"([^"]+)"', html)
print(f"\nbaseUrl patterns: {state_patterns}")

# Check meta tags  
metas = re.findall(r'<meta[^>]+>', html)
for m in metas[:10]:
    print(f"  Meta: {m[:200]}")

# Check if Angular is used
if 'angular' in html.lower():
    print("\nAngular detected!")
ng_version = re.findall(r'ng-version="([^"]+)"', html)
print(f"ng-version: {ng_version}")

# Check for main.js or similar
main_js = re.findall(r'(main\.[a-z0-9]+\.js|polyfills\.[a-z0-9]+\.js)', html)
print(f"Main JS files: {main_js}")

# Try the tag-based page with different naming
alt_urls = [
    "https://rule34.world/posts/",
    "https://rule34.world/api/",
    "https://rule34.world/api/v1/",
    "https://rule34.world/post/list/",
    "https://rule34.world/post/list/1/",
]

for url in alt_urls:
    try:
        r2 = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"\n{url} -> Status: {r2.status_code}, Length: {len(r2.text)}")
    except Exception as e:
        print(f"\n{url} -> Error: {e}")