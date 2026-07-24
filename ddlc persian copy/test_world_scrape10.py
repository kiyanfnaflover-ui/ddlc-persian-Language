import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'identity',
}

# Try to find API endpoints from the homepage
r = requests.get("https://rule34.world/?tags=raiden_shogun", headers=headers, timeout=15)
html = r.text

# Search for API URL patterns in scripts
api_urls = re.findall(r'https?://[^"\'<>\s]*/api/[^"\'<>\s]*', html)
print("API URLs found in HTML:")
for u in api_urls:
    print(f"  {u}")

# Also search for /api/v2 or similar
api_v2 = re.findall(r'/api/v\d[^"\'<>\s]*', html)
print(f"\nAPI v2+ paths: {len(api_v2)}")
for p in api_v2[:20]:
    print(f"  {p}")

# Try calling the actual API endpoints that the Angular app uses
api_endpoints = [
    "https://rule34.world/api/v2/post/list?tags=raiden_shogun&limit=20",
    "https://rule34.world/api/v2/post?tags=raiden_shogun",
    "https://rule34.world/api/v2/posts?tags=raiden_shogun",
    "https://rule34.world/api/v2/search?q=raiden_shogun",
    "https://rule34.world/api/v2/tag?name=raiden_shogun",
]

api_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'identity',
    'Referer': 'https://rule34.world/',
}

for url in api_endpoints:
    try:
        r2 = requests.get(url, headers=api_headers, timeout=15)
        content_type = r2.headers.get('Content-Type', '')
        print(f"\n{url}")
        print(f"  Status: {r2.status_code}, Content-Type: {content_type}")
        if r2.status_code == 200 and 'json' in content_type:
            data = r2.json() if len(r2.text) < 100000 else r2.text[:500]
            if isinstance(data, dict):
                print(f"  Keys: {list(data.keys())[:10]}")
                # Find image URLs
                data_str = json.dumps(data)
                img_urls = re.findall(r'https?://[^"\'<>\s,}]+\.(?:jpg|png|webp|mp4)[^"\'<>\s,}]*', data_str)
                print(f"  Image URLs: {len(img_urls)}")
                for u in img_urls[:10]:
                    print(f"    {u}")
            elif isinstance(data, list):
                print(f"  Array length: {len(data)}")
                if data:
                    if isinstance(data[0], dict):
                        print(f"  Item keys: {list(data[0].keys())[:15]}")
            else:
                print(f"  Response (first 500): {r2.text[:500]}")
        elif r2.status_code == 200:
            print(f"  Response (first 500): {r2.text[:500]}")
    except Exception as e:
        print(f"  Error: {e}")