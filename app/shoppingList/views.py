from django.shortcuts import render, redirect

from shoppingList.crawler import data_crawler
from shoppingList.models import Item


def shoppingList(request):
    if request.method == 'POST':
        item = Item.objects.all()
        if item:
            Item.objects.all().delete()
        data_crawler(request, user=request.user, keyword=request.POST['keyword'])

        return redirect('shop:shopping-list')
    else:
        items = Item.objects.all()
    if request.user.is_authenticated:
        context = {
            'items': items
        }
        return render(request, 'shop/shoppingList.html', context)
    else:
        return redirect('members:login')
