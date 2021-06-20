import requests
from bs4 import BeautifulSoup
import re


def get_url_text(url):
    response = requests.get(url)
    return response.text


def get_articles(url_text):
    soup = BeautifulSoup(url_text, features='html.parser')
    articles = soup.find_all('article')

    return articles


def filter_articles(articles):
    keywords = ['дизайн', 'фото', 'web', 'python']
    filtered_articles = []

    for article in articles:
        try:
            text = article.find('div', class_='post__text_v1').text
        except AttributeError:
            text = article.find('div', class_='post__text_v2').text

        for keyword in keywords:
            if re.search(keyword, text, flags=re.IGNORECASE):
                filtered_articles.append([
                    article.find('span', class_='post__time').text,
                    article.find('a', class_='post__title_link').text,
                    article.find('a', class_='post__title_link').get('href')
                ])

    return filtered_articles


def main():
    url_text = get_url_text('https://habr.com/ru/all/')
    articles = get_articles(url_text)
    filtered_articles = filter_articles(articles)

    print(*filtered_articles, sep='\n')


main()
