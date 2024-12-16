import os
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

def download_images_with_requests(image_urls, folder):
    os.makedirs(folder, exist_ok=True)
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder, f"image_{i+1}.jpg"), 'wb') as file:
                file.write(response.content)
    print(f"Images downloaded using requests in folder: {folder}")

async def download_image(session, url, folder, index):
    async with session.get(url) as response:
        if response.status == 200:
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, f"image_{index+1}.jpg"), 'wb') as file:
                file.write(await response.read())

async def download_images_with_aiohttp(image_urls, folder):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url, folder, i) for i, url in enumerate(image_urls)]
        await asyncio.gather(*tasks)
    print(f"Images downloaded using aiohttp in folder: {folder}")

def main():
    image_urls = [
        "https://35photo.pro/photos_main/2303/11515946.jpg",  # Replace with actual image URLs
        "https://35photo.pro/photos_main/2303/11515254.jpg",
        "https://35photo.pro/photos_main/2303/11515169.jpg",
        "https://35photo.pro/photos_main/2302/11514761.jpg",
        "https://35photo.pro/photos_series/2742/2742776.jpg",
    ] * 2

    download_images_with_requests(image_urls, "images_requests")
    asyncio.run(download_images_with_aiohttp(image_urls, "images_aiohttp"))


if __name__ == "__main__":
    main()
