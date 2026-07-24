import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding': 'identity',
}

# Test if the full-res images actually load
test_urls = [
    "https://rule34.world/posts/1365/1365842/1365842.jpg",
    "https://rule34.world/posts/1365/1365842/1365842.pic256.jpg",
    "https://rule34.world/posts/1365/1365842/1365842.pic256avif.avif",
]

for url in test_urls:
    r = requests.head(url, headers=headers, timeout=10)
    print(f"URL: {url}")
    print(f"  Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}, Content-Length: {r.headers.get('Content-Length')}")
    print()

# Also check if we can get the post detail page to extract full-res file_url
detail_url = "https://rule34.world/post/1365842"
r = requests.get(detail_url, headers=headers, timeout=15)
html = r.text
print(f"Detail page: /post/1365842")
print(f"  Status: {r.status_code}, Length: {len(html)}")

# Check for src="/posts/ in detail page
import re
post_paths = re.findall(r'src="(/posts/\d+/\d+/\d+\.(?:pic256|pic256avif)\.(?:jpg|avif))"', html)
print(f"  Post images found: {len(post_paths)}")
for p in post_paths[:10]:
    print(f"    {p}")

# Look for any full file URLs or JSON data blobs in detail page
full_urls = re.findall(r'(https?://[^"\'<>\s]*rule34\.world[^"\'<>\s]*\.(?:jpg|png|webp|mp4))', html)
print(f"\n  Full URLs: {len(full_urls)}")
for u in full_urls[:10]:
    print(f"    {u}")

# Also check the thumbnail page
thumb_count = len(re.findall(r'\.pic256\.jpg', html))
print(f"\n  .pic256.jpg references: {thumb_count}")
full_jpg_count = len(re.findall(r'/(\d+)\.jpg[^"\'<>]', html))
print(f"  Full .jpg references: {full_jpg_count}")