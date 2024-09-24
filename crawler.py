import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from collections import Counter
import re
def crawl(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headers = soup.find_all(['h1', 'h2', 'h3'])
        data = []
        titles=[]
        for header in headers:
            title = header.text.strip()
            link = header.find('a')
            href = link['href'] if link and 'href' in link.attrs else None
            data.append({'Tiêu đề': title, 'Liên kết': href})
            titles.append(title)
        df = pd.DataFrame(data)
        df.to_excel('crawl.xlsx', index=False)
        print("Dữ liệu đã được lưu vào file crawl.xlsx.")
        #keyword xuat hien nhieu nhat
        words = re.findall(r'\b\w+\b', ' '.join(titles).lower())
        word_counts = Counter(words)
        most_common_word, most_common_count = word_counts.most_common(1)[0]
        print(f'Từ khóa phổ biến nhất là "{most_common_word}" với {most_common_count} lần xuất hiện.')
        #mo file excel chua data
        os.startfile('crawl.xlsx')
    else:
        print(f'Lỗi: Không thể truy cập trang {url}')
url_to_crawl = 'https://vnexpress.net/'
crawl(url_to_crawl)
