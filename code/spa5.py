import requests


def get_spa5(page_count=10):

    headers = {
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://spa4.scrape.center/',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': 'UM_distinctid=17c3fb7f30c45-0fa515fb751b75-4343363-144000-17c3fb7f30d354',
        'Connection': 'keep-alive'
    }
    for page in range(page_count):
        url = f"https://spa5.scrape.center/api/book/?limit=18&offset={page * 10}"
        response = requests.request("GET", url, headers=headers).json()
        data_list = response.get('results')
        for result in data_list:
            yield {
            "id": result.get('id'),
            "title": result.get('name'),
            "authors": result.get('authors', []),
            "cover": result.get('cover'),
            "score": result.get('score'),
            "url": result.get('url'),
            "source": result.get('source'),
            "domain": result.get('domain'),
            "website": result.get('website'),
            "thumb": result.get('thumb'),
            "published_at": result.get('published_at'),
            "updated_at": result.get('updated_at')
        }


if __name__ == "__main__":
    for i in get_spa5():
        print(i)