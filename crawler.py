import urllib.request
from bs4 import BeautifulSoup
from random import randint
import sys
import subprocess
import json
import os
from darknet import check_image_has_no_people

if len(sys.argv) != 2:
    print("Usage: python3 crawl.py <filepath>")
    exit(1)

filepath = sys.argv[1]


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}
base_url = "https://www.pexels.com"


def get_wallpaper_urls():
    req = urllib.request.Request(
        f"{base_url}/search/nature/?orientation=landscape&size=large",
        headers=headers,
    )
    with urllib.request.urlopen(req) as url:
        wallpaper_overview_html_raw = url.read().decode()

    soup = BeautifulSoup(wallpaper_overview_html_raw, "html.parser")

    # find article tags with class 'photo-item'
    wallpaper_tags = soup.find_all("article", class_="photo-item")

    # get the first url in each tag
    wallpaper_urls = [tag.find("a")["href"] for tag in wallpaper_tags]
    return wallpaper_urls


def get_random_wallpaper_url(wallpaper_urls):
    wallpaper_url = base_url + wallpaper_urls[randint(0, len(wallpaper_urls) - 1)]
    return wallpaper_url


def download_wallpaper(url):
    req = urllib.request.Request(
        wallpaper_url,
        headers=headers,
    )
    with urllib.request.urlopen(req) as url:
        wallpaper_html_raw = url.read().decode()

    soup = BeautifulSoup(wallpaper_html_raw, "html.parser")

    # find a tag with class 'js-download-a-tag'
    download_button = soup.find("a", class_="js-download-a-tag")
    download_url = base_url + download_button["href"]

    # download the image
    req = urllib.request.Request(
        download_url,
        headers=headers,
    )
    with urllib.request.urlopen(req) as url:
        wallpaper_raw = url.read()

    return wallpaper_raw


wallpaper_urls = get_wallpaper_urls()

project_path = "/home/moritz/dev/privat/wallpaper-crawler"

MAX_RETRIES = 10
tmp_filepath = "/tmp/wallpaper.jpg"
for i in range(MAX_RETRIES):
    wallpaper_url = get_random_wallpaper_url(wallpaper_urls)
    wallpaper_raw = download_wallpaper(wallpaper_url)

    with open(tmp_filepath, "wb") as f:
        f.write(wallpaper_raw)

    if check_image_has_no_people(tmp_filepath):
        break


# save the image and make readable for everyone
with open(filepath, "wb") as f:
    f.write(wallpaper_raw)
