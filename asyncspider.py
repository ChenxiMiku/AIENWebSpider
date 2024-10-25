import os
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

async def create_img_folder(folder_name):
    """Create a folder to save images."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

async def download_image(session, img_url, folder_name):
    """Download an image and save it to the specified folder."""
    try:
        async with session.get(img_url) as response:
            if response.status == 200:
                file_name = os.path.join(folder_name, img_url.split('/')[-1])
                with open(file_name, 'wb') as file:
                    file.write(await response.read())
                print(f"Downloaded {file_name}")
            else:
                print(f"Failed to retrieve image from {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

async def fetch_news_page(session, news_url):
    """Fetch the news page text and image links."""
    try:
        async with session.get(news_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                article_title = soup.find('span', class_='Article_Title')
                text_title = article_title.get_text().strip() if article_title else ''
                article_content = soup.find('div', class_='Article_Content')
                text_content = text_title + '\n' + article_content.get_text().strip() if article_content else ''
                
                img_urls = []
                if article_content.find_all('img', attrs={'data-layer': 'photo'}):
                    img_tags = article_content.find_all('img', attrs={'data-layer': 'photo'}) if article_content else []
                    img_srcs = [img['src'] for img in img_tags if 'src' in img.attrs]
                    for src in img_srcs:
                        if re.search(r'(/_upload/[^"]+)', src):
                            img_urls.append(f'https://ien.shou.edu.cn{src}' if not src.startswith('http') else src)
                else:
                    img_urls = re.findall(r'(/_upload/article/images/[^\s"\'<>]+)', html)
                    img_urls = [f'https://ien.shou.edu.cn{img_url}' for img_url in img_urls]
                
                return text_content, img_urls
            else:
                print(f"Failed to retrieve news page: {news_url}")
                return "", []
    except Exception as e:
        print(f"Error fetching {news_url}: {e}")
        return "", []

async def main():
    start_time = time.time()  # Start timing
    base_url = "https://ien.shou.edu.cn"
    
    async with aiohttp.ClientSession() as session:
        # Create image folder
        await create_img_folder('img')

        # Fetch the main news page to get total pages
        response = await session.get(base_url + "/2202/list.htm")
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        total_pages = int(soup.find('em', class_='all_pages').text)
        print(f"Total pages: {total_pages}")
        
        all_texts = []

        # Collect futures for news pages
        news_futures = []
        for i in range(1, total_pages + 1):
            try:
                response = await session.get(base_url + f"/2202/list{i}.htm")
                if response.status == 200:
                    list_html = await response.text()
                    list_soup = BeautifulSoup(list_html, 'html.parser')
                    news_links = [a['href'] for a in list_soup.find_all('a', href=True) if 'page.htm' in a['href']]
                    
                    for news_link in news_links:
                        full_url = news_link if news_link.startswith('http') else base_url + news_link
                        news_futures.append(fetch_news_page(session, full_url))
                else:
                    print(f"Failed to retrieve news list page: {base_url + f'/2202/list{i}.htm'}")
            except Exception as e:
                print(f"Error fetching news list: {e}")

        # Fetch news pages concurrently
        news_results = await asyncio.gather(*news_futures)

        # Download images concurrently
        img_futures = []
        for text, img_urls in news_results:
            all_texts.append(text)
            img_futures.extend([download_image(session, img_url, 'img') for img_url in img_urls])

        # Wait for all image downloads to complete
        await asyncio.gather(*img_futures)

    # Write all text to file
    with open('ien.txt', 'w', encoding='utf-8') as text_file:
        text_file.write("\n\n".join(all_texts))
    
    # Count images downloaded
    img_count = len(os.listdir('img'))
    print(f"Downloaded {img_count} images to the 'img' folder.")
    
    end_time = time.time()  # End timing
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
