from django.urls import path

from shoppingList.views import shoppingList

app_name = 'shop'
urlpatterns = [
    path('shoppinglist/', shoppingList, name="shopping-list")
]
