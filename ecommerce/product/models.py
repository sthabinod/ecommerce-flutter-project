from django.db import models
from ecommerce.core.models import TimeStampAbstractModel


class Category(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image',null=True,blank=True)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name



class Product(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_image',null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    
    