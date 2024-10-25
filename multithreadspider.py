import os
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def create_img_folder(folder_name):
    """创建保存图片的文件夹"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(img_url, folder_name):
    """下载图片并保存到指定文件夹"""
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            file_name = os.path.join(folder_name, img_url.split('/')[-1])
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name}")
        else:
            print(f"Failed to retrieve image from {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def fetch_news_page(news_url):
    """抓取新闻页面的文本和图片链接"""
    try:
        response = requests.get(news_url)
        response.encoding = response.apparent_encoding  # 设置编码
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            #text_content = soup.get_text(separator="\n", strip=True)
            article_title = soup.find('span', class_='Article_Title')
            text_title = article_title.get_text().strip() if article_title else ''
            article_content = soup.find('div', class_='Article_Content')
            text_content = text_title + '\n' + article_content.get_text().strip() if article_content else ''
            if article_content.find_all('img', attrs={'data-layer': 'photo'}):
                img_tags = article_content.find_all('img', attrs={'data-layer': 'photo'}) if article_content else []
                img_srcs = [img['src'] for img in img_tags if 'src' in img.attrs]
                img_urls = []
                for src in img_srcs:
                    if re.search(r'(/_upload/[^"]+)', src):
                        if not src.startswith('http'):
                            img_urls.append(f'https://ien.shou.edu.cn{src}')
                        else:
                            img_urls.append(src)
            else:
                img_urls = re.findall(r'(/_upload/article/images/[^\s"\'<>]+)', response.text)
                img_urls = [f'https://ien.shou.edu.cn{img_url}' for img_url in img_urls]
            return text_content, img_urls
        else:
            print(f"Failed to retrieve news page: {news_url}")
            return "", []
    except Exception as e:
        print(f"Error fetching {news_url}: {e}")
        return "", []

def main():
    start_time = time.time()  # 开始计时
    base_url = "https://ien.shou.edu.cn"
    response = requests.get(base_url + "/2202/list.htm")
    soup = BeautifulSoup(response.text, 'html.parser')
    total_pages = int(soup.find('em', class_='all_pages').text)
    total_pages = 10
    print(f"Total pages: {total_pages}")
    all_texts = []
    
    create_img_folder('img')

    # 创建一个线程池
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = []
        
        # 抓取所有新闻页面
        for i in range(1, total_pages + 1):
            try:
                response = requests.get(base_url + f"/2202/list{i}.htm")
                if response.status_code == 200:
                    list_soup = BeautifulSoup(response.text, 'html.parser')
                    news_links = [a['href'] for a in list_soup.find_all('a', href=True) if 'page.htm' in a['href']]
                    
                    for news_link in news_links:
                        full_url = news_link if news_link.startswith('http') else base_url + news_link
                        futures.append(executor.submit(fetch_news_page, full_url))
                else:
                    print(f"Failed to retrieve news list page: {base_url + f'/2202/list{i}.htm'}")
            except Exception as e:
                print(f"Error fetching news list: {e}")

        # 处理每个新闻页面的结果
        for future in as_completed(futures):
            text, img_urls = future.result()
            all_texts.append(text)

            # 下载图片
            with ThreadPoolExecutor(max_workers=32) as img_executor:
                img_futures = [img_executor.submit(download_image, img_url, 'img') for img_url in img_urls]
                for img_future in as_completed(img_futures):
                    img_future.result()

    # 将所有文本写入文件
    with open('ien.txt', 'w', encoding='utf-8') as text_file:
        text_file.write("\n\n".join(all_texts))
    
    # 统计图片数量
    img_count = len(os.listdir('img'))
    print(f"Downloaded {img_count} images to the 'img' folder.")
    
    end_time = time.time()  # 结束计时
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
