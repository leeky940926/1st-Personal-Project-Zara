from django.db.models import Q

from products.models  import (
    Product,
    DetailProduct
)

class ProductList :
    def __init__(self, offset, limit, category_id, item_id, color_id, size_id, min_price, max_price) :
            self.offset      = offset
            self.limit       = limit
            self.category_id = category_id
            self.item_id     = item_id
            self.color_id    = color_id
            self.size_id     = size_id
            self.min_price   = min_price
            self.max_price   = max_price
        
    def filter_products(offset, limit, category_id, item_id, color_id, size_id, min_price, max_price) :
        product_filter = Q(item__category_id=category_id)
            
        if item_id :
            product_filter.add(Q(item__id__in = item_id), Q.AND)
        
        if color_id :
            product_filter.add(Q(detailproduct__color_id__in = color_id), Q.AND)
        
        if size_id : 
            product_filter.add(Q(detailproduct__size_id__in = size_id), Q.AND)
        
        if min_price and max_price :
            product_filter.add(Q(price__gte=min_price)&Q(price__lte=max_price), Q.AND)
            
        products = Product.objects.select_related('item').prefetch_related('detailproduct_set', 'thumbnail_set').\
            filter(product_filter).order_by('-created_at')[offset:offset+limit]
            
        return products