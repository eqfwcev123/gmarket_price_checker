from django.db import models


# Create your models here.
from member.models import User


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_original_price = models.CharField(max_length=100, blank=True)
    item_discount_price = models.CharField(max_length=100, blank=True)
    item_discount_rate = models.CharField(max_length=100, blank=True)
    item_image = models.ImageField(blank=True)

    def __str__(self):
        return self.item_name, self.item_original_price, self.item_discount_price
