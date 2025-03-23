from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length = 20)
    item_desc = models.CharField(max_length = 50)
    item_price = models.IntegerField()
    item_pic = models.CharField(max_length = 200, default = "https://picsum.photos/id/125/200/300")

    def __str__(self):
        return self.item_name
    
