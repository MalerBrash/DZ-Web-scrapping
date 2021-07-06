from bs4 import BeautifulSoup
import requests
import re
# from pprint import pprint
from datetime import date


def response(link):
    res = requests.Session().get(link)
    if res.status_code != 200:
        raise ValueError('No response')
    soup = BeautifulSoup(res.text, 'html.parser')
    res.close()
    articles = soup.findAll('article')
    return articles


def start_parser(link):
    articles = response(link)
    links = set()
    for article in articles:
        tags_a = article.findAll('a', class_='hub-link')
        hub_link = {i.text.lower() for i in tags_a}
        for i in KEYWORDS:
            r = re.compile(f".*{i.lower()}")
            new_list = list(filter(r.match, hub_link))
            if new_list:
                href = article.find('a', class_="post__title_link").attrs.get('href')
                title = article.find('a', class_="post__title_link").text
                output = f'{date.today()} - {title} - {href}'
                links.add(output)
    if not links:
        print('Совпадений не найдено!')

    return links


KEYWORDS = ('Python', 'linux', 'алгоритмы', 'solid')
url = 'http://habr.com/ru/all'


if __name__ == '__main__':
    for result in start_parser(url):
        print(result)
