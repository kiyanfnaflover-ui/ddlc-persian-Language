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

# Try multiple tag variations
test_urls = [
    "https://rule34.world/index.php?page=post&s=list&tags=girlfriend",
    "https://rule34.world/index.php?page=post&s=list&tags=fnf",
    "https://rule34.world/index.php?page=post&s=list&tags=genshin_impact",
    "https://rule34.world/index.php?page=post&s=list&tags=frieren",
    "https://rule34.world/",
    "https://rule34.world/index.php?page=post&s=list&tags=raiden_shogun",
]

for url in test_urls:
    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        print(f"\nURL: {url}")
        print(f"Status: {r.status_code}, Final URL: {r.url}, Length: {len(r.text)}")
        
        html = r.text
        if len(html) > 100:
            # Check for image patterns
            img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
            world_urls = re.findall(r'https?://rule34\.world/[^"\'<> ]+', html) 
            post_paths = re.findall(r'/posts/\d+/\d+/[^"\'<> ]+', html)
            
            print(f"  <img> tags: {len(img_srcs)}")
            print(f"  rule34.world URLs: {len(world_urls)}")
            print(f"  /posts/ paths: {len(post_paths)}")
            
            if img_srcs:
                for s in img_srcs[:5]:
                    print(f"    img: {s}")
            if world_urls:
                for u in world_urls[:5]:
                    print(f"    url: {u}")
            if post_paths:
                for p in post_paths[:5]:
                    print(f"    post: {p}")
    except Exception as e:
        print(f"Error for {url}: {e}")