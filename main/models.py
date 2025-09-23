from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# buat definisiin datatypenya
class ShopAtSinItem(models.Model):
    name = models.CharField(max_length=255)  
    price = models.IntegerField()  
    description = models.TextField()  
    thumbnail = models.URLField()  
    category = models.CharField(max_length=100)  
    is_featured = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(default=0)  
    brand = models.CharField(max_length=100, blank=True, null=True)  
    rating = models.FloatField(default=0.0)  
    date_added = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.category}"
    