import chardet as chardet
import requests
from isbntools.app import *
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re


def google_book_info(title):
    isbn = isbn_from_words(title)
    url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn
    response = requests.get(url)
    if response.status_code == 200:
        lst = []
        for item in response.json()['items']:
            t = item['volumeInfo']
            res_dict = {'title': t['title'],
                        'author': t['authors'][0],
                        'year': t['publishedDate'][:4],
                        'description': t['description'],
                        'price': None}
            lst.append(res_dict)
        return lst
    else:
        return None


def steimatzki_book_info(title):
    try:
        urls = steimatzki_urls(title)
        lst = []
        for url in urls:
            req = Request(url, headers={'User-Agent': 'Chrome'})
            webpage = urlopen(req).read()
            encoding = chardet.detect(webpage)
            webpage = webpage.decode(encoding['encoding'])
            t = BeautifulSoup(webpage.split('<div class="page-content" dir="rtl">')[1], features="lxml") \
                .prettify().splitlines()
            i = 0 if t[5].count('<') < 1 else -1
            res_dict = {'title': t[i + 13].strip(),
                        'author': t[i + 21].strip(),
                        'year': None,
                        'description': t[i + 5].strip(),
                        'price': webpage.split('<span class="price">')[1][:5].strip()}
            if i == -1:
                res_dict['description'] = None
            try:
                float(res_dict['price'])
            except ValueError:
                pattern = "\d{1,3}\.\d{2,2}"
                res_dict['price'] = re.findall(pattern, webpage.split('<span class="price">')[1])[0].strip()
            lst.append(res_dict)
        return lst
    except Exception as e:
        return None


def steimatzki_urls(title):
    try:
        link = "https://www.steimatzky.co.il/catalogsearch/result/?q=" + title.strip().replace(' ', '+')
        req = Request(link, headers={'User-Agent': 'Chrome'})
        webpage = urlopen(req).read()
        encoding = chardet.detect(webpage)
        webpage = webpage.decode(encoding['encoding'])
        webpage = BeautifulSoup(webpage.split('<div class="load_next_wrapper scroll">')[0]
                                .split('<ul class="products list items product-items ">')[-1], features="lxml")
        pattern = "https://www.steimatzky.co.il/\d{9,9}"
        return set(re.findall(pattern, str(webpage)))
    except Exception as e:
        return None

