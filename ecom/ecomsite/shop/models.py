from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=300)

class Order(models.Model):
    items = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    zip = models.CharField(max_length=100)