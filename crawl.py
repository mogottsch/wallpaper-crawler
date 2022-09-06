import sys
from darknet import image_contains_people
from pexels import get_random_wallpaper_url, get_wallpaper_urls, download_wallpaper


MAX_RETRIES = 10


if len(sys.argv) != 2:
    print("Usage: python crawl.py <filepath>")
    exit(1)

filepath = sys.argv[1]

wallpaper_urls = get_wallpaper_urls()
print(f"Found {len(wallpaper_urls)} wallpapers")

tmp_filepath = "/tmp/wallpaper.jpg"
for i in range(MAX_RETRIES):
    wallpaper_url = get_random_wallpaper_url(wallpaper_urls)
    print(f"Downloading {wallpaper_url}")
    wallpaper_raw = download_wallpaper(wallpaper_url)

    with open(tmp_filepath, "wb") as f:
        f.write(wallpaper_raw)

    if not image_contains_people(tmp_filepath):
        break
    print(f"Image contains people, retrying ({i + 1}/{MAX_RETRIES})")


# save the image and make readable for everyone
with open(filepath, "wb") as f:
    f.write(wallpaper_raw)
