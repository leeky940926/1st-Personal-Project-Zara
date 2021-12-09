from django.db   import models

from core.models import TimeStampModel

class Menu(TimeStampModel) :
    name = models.CharField(max_length=20)
    
    class Meta :
        db_table = 'menus'

class Category(TimeStampModel) :
    menu               = models.ForeignKey(Menu, on_delete=models.CASCADE)
    parent_category    = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    name               = models.CharField(max_length=40)
    
    class Meta :
        db_table = 'categories'
        
class Item(TimeStampModel) :
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name     = models.CharField(max_length=30)
    
    class Meta :
        db_table = 'items'
        
class Product(TimeStampModel) :
    item  = models.ForeignKey(Item, on_delete=models.CASCADE)
    name  = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    
    class Meta :
        db_table = 'products'

class Thumbnail(TimeStampModel) :
    url     = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    
    class Meta :
        db_table = 'thumbnails'

class ProductImage(TimeStampModel) :
    url     = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta :
        db_table = 'product_images'
        
class Size(TimeStampModel) :
    size = models.CharField(max_length=20)
    
    class Meta :
        db_table = 'sizes'

class Color(TimeStampModel) :
    color = models.CharField(max_length=20)
    
    class Meta :
        db_table = 'colors'
        
class DetailProduct(TimeStampModel) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)
    
    class Meta :
        db_table = 'detail_products'