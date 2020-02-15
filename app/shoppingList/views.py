from django.shortcuts import render

# Create your views here.
def shoppingList(request):
    return render(request, 'shop/shoppingList.html')