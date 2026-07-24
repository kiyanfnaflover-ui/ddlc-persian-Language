import requests
import re
import json

api_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'identity',
    'Referer': 'https://rule34.world/',
}

# Try the search/root API that was found in ng-state
api_urls = [
    "https://rule34.world/api/v2/post/search/root?tags=raiden_shogun&limit=20",
    "https://rule34.world/api/v2/post/search/root?tags=girlfriend_fnf&limit=20",
    "https://rule34.world/api/v2/post/search/root",
    "https://rule34.world/api/v2/post/search/root?tags=",
]

for url in api_urls:
    try:
        r = requests.get(url, headers=api_headers, timeout=30)
        content_type = r.headers.get('Content-Type', '')
        print(f"URL: {url}")
        print(f"  Status: {r.status_code}, Content-Type: {content_type}, Length: {len(r.text)}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())}")
                    data_str = json.dumps(data)
                    img_urls = re.findall(r'https?://[^"\'<>\s,}]+\.(?:jpg|png|webp|mp4|gif)[^"\'<>\s,}]*', data_str)
                    print(f"  Image URLs found: {len(img_urls)}")
                    for u in img_urls[:10]:
                        print(f"    {u}")
                    # Also look for file_url in the response
                    if 'posts' in data:
                        posts = data['posts']
                        print(f"  Posts count: {len(posts)}")
                        if posts:
                            if isinstance(posts[0], dict):
                                print(f"  First post keys: {list(posts[0].keys())[:20]}")
                                for key in ['file_url', 'fileUrl', 'url', 'source', 'sample', 'preview', 'thumbnail']:
                                    if key in posts[0]:
                                        print(f"  Post has '{key}': {posts[0][key]}")
                elif isinstance(data, list):
                    print(f"  Array length: {len(data)}")
                    if data and isinstance(data[0], dict):
                        print(f"  First item keys: {list(data[0].keys())[:15]}")
                else:
                    print(f"  Type: {type(data)}, first 500: {str(data)[:500]}")
            except Exception as e:
                print(f"  JSON parse error (first 300): {r.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")
    print()