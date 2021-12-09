from products.models    import (
    Menu,
    Category,
    Size,
    Thumbnail,
    Product,
    ProductImage,
    Color,
    DetailProduct
)

from django.db.models import Q

class Filter :
    def __init__(self, offset, limit, category_id, item_id, color_id, size_id, price) :
            self.offset      = offset
            self.limit       = limit
            self.category_id = category_id
            self.item_id     = item_id
            self.color_id    = color_id
            self.size_id     = size_id
            self.price       = price
        
    def filter_products(offset, limit, category_id, item_id, color_id, size_id, price) :
        filter_product = Q(category_id=category_id)
        
        if item_id :
            filter_product.add(Q(item_id__in=item_id), Q.AND)
            
        print('item_id : ', item_id, filter_product)
        
        # if color_id :
        #     filter_product.add(Q(color_id__in=color_id), Q.AND)
        
        # print('color_id :', color_id, filter_product)
        
        # if size_id :
        #     filter_product.add(Q(size_id__in=size_id), Q.AND)
        
        # print('size_id :', size_id, filter_product)
        
        # if price :
        #     filter_product.add(Q(price=price))
        
        # print('price :', price, filter_product)
        
        products = Product.objects.select_related('item').prefetch_related('detailproduct').filter(filter_product)[offset:offset+limit]
        
        return products