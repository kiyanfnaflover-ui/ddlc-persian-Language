import requests
import re

# Test scraping rule34.world for "girlfriend_fnf"
url = "https://rule34.world/index.php?page=post&s=list&tags=girlfriend_fnf"

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
    'Connection': 'keep-alive',
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    
    html = response.text
    
    # Method 1: Find all <img> tags with src
    img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    print(f"\n--- Found {len(img_srcs)} raw <img> src attributes ---")
    for s in img_srcs[:20]:
        print(f"  {s}")
    
    # Method 2: Angular SSR JSON state - look for JSON objects with file_url
    json_matches = re.findall(r'\{[^}]*"file_url"[^}]*\}', html)
    print(f"\n--- Found {len(json_matches)} JSON objects with file_url ---")
    for j in json_matches[:5]:
        print(f"  {j[:200]}")
    
    # Method 3: Look for __NEXT_DATA__ or ng-state or similar state blobs
    script_matches = re.findall(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"\n--- __NEXT_DATA__ scripts: {len(script_matches)} ---")
    
    script_ng = re.findall(r'<script[^>]*id="ng-state"[^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"--- ng-state scripts: {len(script_ng)} ---")
    
    # Method 4: Look for any URLs containing rule34.world
    world_urls = re.findall(r'https?://rule34\.world/[^"\'<> ]+', html)
    print(f"\n--- Found {len(world_urls)} rule34.world URLs ---")
    for u in world_urls[:20]:
        print(f"  {u}")
    
    # Method 5: Look for /posts/ relative paths
    post_paths = re.findall(r'/posts/\d+/\d+/[^"\'<> ]+', html)
    print(f"\n--- Found {len(post_paths)} /posts/ paths ---")
    for p in post_paths[:20]:
        print(f"  {p}")
    
    # Method 6: Look for thumbnails
    thumbs = re.findall(r'thumb[^"\'<> ]*', html)
    print(f"\n--- Found {len(thumbs)} thumb references ---")
    for t in thumbs[:20]:
        print(f"  {t}")
    
    # Save HTML for analysis
    with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\rule34_world_html.txt", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nFull HTML saved to rule34_world_html.txt")
    
    # Also try the post page directly (first post detail page)
    detail_url = "https://rule34.world/index.php?page=post&s=view&id=1"
    response2 = requests.get(detail_url, headers=headers, timeout=30)
    if response2.status_code == 200:
        html2 = response2.text
        # Look for file_url pattern in detail page
        detail_json = re.findall(r'file_url["\s:=]+["\']([^"\']+)["\']', html2)
        print(f"\n--- Detail page file_urls ---")
        for u in detail_json[:5]:
            print(f"  {u}")

except Exception as e:
    print(f"Error: {e}")