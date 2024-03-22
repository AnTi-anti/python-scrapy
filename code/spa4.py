import requests


def get_spa4(page_count=10):

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
        url = f"https://spa4.scrape.center/api/news/?limit=10&offset={page * 10}"
        response = requests.request("GET", url, headers=headers).json()
        data_list = response.get('results')
        for info in data_list:
            yield {
                "id": info.get('id'),
                "title": info.get('title'),
                "code": info.get('code'),
                "url": info.get('url'),
                "source": info.get('source'),
                "domain": info.get('domain'),
                "website": info.get('website'),
                "thumb": info.get('thumb'),
                "published_at": info.get('published_at'),
                "updated_at": info.get('updated_at')
            }


if __name__ == "__main__":
    for i in get_spa4():
        print(i)