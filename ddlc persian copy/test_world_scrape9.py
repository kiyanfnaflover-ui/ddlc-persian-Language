import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

r = requests.get("https://rule34.world/?tags=girlfriend_fnf", headers=headers, timeout=15)
html = r.text

# Extract ng-state
ng_state_match = re.search(r'<script[^>]+id="ng-state"[^>]*>(.*?)</script>', html, re.DOTALL)
if ng_state_match:
    ng_state_raw = ng_state_match.group(1)
    print(f"ng-state length: {len(ng_state_raw)}")
    
    # Save the raw ng-state
    with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\ng_state.txt", "w", encoding="utf-8") as f:
        f.write(ng_state_raw)
    
    # The ng-state might be HTML-escaped JSON, try to unescape
    ng_state_unescaped = ng_state_raw.replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&#92;', '\\\\').replace('&#47;', '/')
    
    # Save unescaped
    with open("C:\\Users\\Lion\\Desktop\\ddlc persian copy\\ng_state_unescaped.txt", "w", encoding="utf-8") as f:
        f.write(ng_state_unescaped)
    
    print(f"\nFirst 2000 chars of raw ng-state:")
    print(ng_state_raw[:2000])
    
    # Search for file_url or image URLs in the state
    file_urls = re.findall(r'file_url["\s]*:["\s]*([^,"}\]]+)', ng_state_unescaped)
    print(f"\nfile_url patterns found: {len(file_urls)}")
    for f in file_urls[:20]:
        print(f"  {f}")
    
    # Search for any URLs with file extensions
    url_patterns = re.findall(r'https?://[^"\'<>\s,}]+\.(?:jpg|png|webp|mp4|gif)[^"\'<>\s,}]*', ng_state_unescaped)
    print(f"\nURL patterns found: {len(url_patterns)}")
    for u in url_patterns[:20]:
        print(f"  {u}")
    
    # Search for "url" or "src" patterns
    src_patterns = re.findall(r'"(?:url|src|source|preview|sample|full)["\s]*:["\s]*"([^"]+)"', ng_state_unescaped)
    print(f"\nURL/src patterns found: {len(src_patterns)}")
    for s in src_patterns[:20]:
        print(f"  {s}")
    
    # Try to find "posts" or "images" arrays
    post_data = re.findall(r'"posts"["\s]*:[["\s]*({[^}]+})', ng_state_unescaped)
    print(f"\nPosts data: {len(post_data)}")
    for p in post_data[:5]:
        print(f"  {p[:300]}")
    
    # Search for "id" followed by numeric near "file" or "url"
    id_file = re.findall(r'"id"\s*:\s*(\d+)[^}]*"file"', ng_state_unescaped)
    print(f"\nID + file patterns: {len(id_file)}")
    
    # Generic search for all property names that might contain image URLs
    img_keys = re.findall(r'"(\w+)":\s*"([^"]*\.(?:jpg|png|webp|mp4|gif)[^"]*)"', ng_state_unescaped)
    print(f"\nImage key-value pairs: {len(img_keys)}")
    for k, v in img_keys[:30]:
        print(f"  {k}: {v}")