import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

# Test different search URL patterns
test_urls = [
    "https://rule34.world/?tags=girlfriend_fnf",
    "https://rule34.world/?tags=raiden_shogun",
    "https://rule34.world/?tags=genshin_impact",
    "https://rule34.world/post?tags=girlfriend_fnf",
    "https://rule34.world/post/list?tags=girlfriend",
    "https://rule34.world/search?q=girlfriend",
    "https://rule34.world/posts?tags=girlfriend",
    "https://rule34.world/index.php?page=post&s=list&tags=girlfriend",
]

for url in test_urls:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        html = r.text
        img_count = len(re.findall(r'<img[^>]+src="/posts/', html))
        print(f"URL: {url}")
        print(f"  Status: {r.status_code}, Final: {r.url}, Length: {len(html)}, Images: {img_count}")
        if img_count > 0:
            # Extract a few full-res URLs
            post_paths = re.findall(r'<img[^>]+src="(/posts/\d+/\d+/\d+\.pic256\.jpg)"', html)
            if post_paths:
                # Convert to full resolution (replace pic256 with full)
                full_urls = [f"https://rule34.world{p.replace('.pic256.jpg', '.jpg')}" for p in post_paths[:5]]
                print(f"  Sample full-res URLs: {full_urls}")
                # Also extract .pic256 thumbnails as fallback
                thumb_urls = [f"https://rule34.world{p}" for p in post_paths[:5]]
                print(f"  Sample thumbnail URLs: {thumb_urls}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
    print()