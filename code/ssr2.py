"""
爬取目标网址：https://ssr1.scrape.center/
1. 利用 requests 爬取这个站点每一页的电影列表，顺着列表再爬取每个电影的详情页
2. 用正则表达式提取每部电影的名称、封面、类别、上映时间、评分、剧情简介等内容
3. 把以上爬取的内容保存为 JSON 文本文件
4. 使用多进程实现爬取的加速
5. 单进程版本
"""

import requests
import logging
import re
from urllib.parse import urljoin
import json
from os.path import exists
from os import makedirs

RESULT_DIR = 'results'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')

BASE_URL = 'https://ssr2.scrape.center'
TOTAL_PAGE = 10
logging.captureWarnings(True)

def save_data(data):
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def scrape_page(url):
    """
    获取列表页的 html
    """
    logging.info('scraping %s ...', url)

    try:
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            return response.text

        logging.error('get invalid status code %s while scraping %',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """
    构造分页
    """
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


def parse_index(html):
    """
    获取并拼接列表页的 url
    """
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []

    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    """
    获取详情页的 html
    """
    return scrape_page(url)


def parse_detail(html):
    """
    详情页提取关键信息
    """
    # 电影封面
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    # 电影名称
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    # 电影类别
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    # 上映时间
    published_pattern = re.compile('(\d{4}-\d{2}-\d{2}\s上映)')
    # 剧情简介
    drama_pattern = re.compile('<div.*?drama.*?<p.*?>(.*?)</p>', re.S)
    # 评分
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_pattern, html).group(1) if re.search(published_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None

    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_html = scrape_index(page)
        detail_urls = parse_index(index_html)
        # logging.info('detail urls %s', list(detail_urls))

        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            data = parse_detail(detail_html)
            logging.info('get detail data %s', data)
            logging.info('saving data to json file')
            save_data(data)
            logging.info('data saved successfully')


if __name__ == '__main__':
    main()