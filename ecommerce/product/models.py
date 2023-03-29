from django.db import models
from ecommerce.core.models import TimeStampAbstractModel
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError

class Category(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image',null=True,blank=True)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
class Size(TimeStampAbstractModel):
    title = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.title

class Color(TimeStampAbstractModel):
    color = ColorField(format="hexa")
    def __str__(self):
        return self.color


class Product(TimeStampAbstractModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_image',null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
 

    
    def __str__(self):
        return self.name
    

class Stock(TimeStampAbstractModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f'{self.product.name}  {self.quantity}  {self.color.color}   {self.size.title}'
    
    class Meta:
        unique_together = ('product','color','size')
        
 