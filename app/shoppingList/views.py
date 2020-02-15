import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def shoppingList(request):
    return render(request, 'shop/shoppingList.html')


def data_crawler(request, keyword):
    word = keyword
    url = f'http://browse.gmarket.co.kr/search?keyword={word}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    product_title_list = [title.text for title in soup.find_all(class_='text__item')]
    product_discount_list = [discount_rate.text for discount_rate in
                             soup.select('div.box__discount > span.text__value')]
    product_selling_price_list = [selling_price.text for selling_price in
                                  soup.select('div.box__price-seller > strong.text__value')]
    product_original_price_list = [original_price.text for original_price in
                                   soup.select('div.box__price-original > span.text__value')]
    full_list = [(h, i, j, k) for h, i, j, k in
                 zip(product_title_list, product_discount_list, product_selling_price_list,
                     product_original_price_list)]
    return HttpResponse(full_list)
