from django.db import models
from ecommerce.core.models import TimeStampAbstractModel


class Category(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name

class Inventory(TimeStampAbstractModel):
    quantity = models.IntegerField()
    
    def __str__(self) -> str:
        return self.quantity

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    inventory = models.OneToOneField(Inventory,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
    