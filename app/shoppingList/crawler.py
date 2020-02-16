import re

import requests
from bs4 import BeautifulSoup

from shoppingList.models import Item


def data_crawler(request, keyword, user):
    word = keyword
    url = f'http://browse.gmarket.co.kr/search?keyword={word}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    product_title_list = [title.text for title in soup.find_all(class_='text__item')]
    discount_rate = [''.join(re.compile('["률"](\d+%)').findall(a.text)) for a in soup.select(
        'div.box__component > div.box__item-container > div.box__information > div.box__information-major')]
    original_price = [''.join(re.compile('(상품금액 \d+,\d+)').findall(a.text)) for a in soup.select(
        'div.box__component > div.box__item-container > div.box__information > div.box__information-major')]
    discount_price = [''.join(re.compile('(할인적용금액 \d+,\d+)').findall(a.text)) for a in soup.select(
        'div.box__component > div.box__item-container > div.box__information > div.box__information-major')]
    full_list = [(h, i, j, k) for h, i, j, k in zip(product_title_list, discount_rate, original_price, discount_price)]

    for items in full_list:
        Item.objects.create(
            user=request.user,
            item_name=items[0],
            item_discount_rate=items[1],
            item_original_price=items[2],
            item_discount_price=items[3],
        )
