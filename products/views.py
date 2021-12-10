import json
   
from enum               import Enum
from django.http        import JsonResponse
from django.views       import View
from django.db          import (
    transaction,
    IntegrityError
)

from users.utils        import login_required
from products.models    import (
    Item,
    Menu,
    Category,
    Size,
    Thumbnail,
    Product,
    ProductImage,
    Color,
    DetailProduct
)
from products.filters    import (
    ProductList,
    OneProduct
)

class RoleID(Enum) :
    ADMIN = 1
    USER  = 2
    
class ProductView(View) :
    def get(self, request) :
        try :
            offset      = int(request.GET.get('offset', 0))
            limit       = int(request.GET.get('limit', 15))
            category_id = int(request.GET['category_id'])
            item_id     = request.GET.getlist('item_id', None)
            color_id    = request.GET.getlist('color_id', None)
            size_id     = request.GET.getlist('size_id', None)
            min_price   = int(request.GET.get('min_price', 20000))
            max_price   = int(request.GET.get('max_price', 200000))
            
            if limit > 20 :
                return JsonResponse({'message' : 'TOO_MUCH_LIST'}, status=400)
            
            products = ProductList.filter_products(offset, limit, category_id, item_id, color_id, size_id, min_price, max_price)
            
            product_list = [{
                    'id'        : product.id,
                    'name'      : product.name,
                    'price'     : product.price,
                    'item_id'   : product.item.id,
                    'item_name' : product.item.name,
                    'thumbnail' : [
                        {
                            'id'  : thumbnail.id,
                            'url' : thumbnail.url
                        } for thumbnail in product.thumbnail_set.all()],
                    'detail_set' : [
                        {
                            'color_id'   : detail.color_id,
                            'color_name' : detail.color.color,
                            'size_id'    : detail.size_id,
                            'size_name'  : detail.size.size
                        }
                    for detail in product.detailproduct_set.all()]
                } for product in products
            ]
            
            return JsonResponse({'message' : product_list}, status=200)
        
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=500)
    
    @login_required
    def post(self, request) :
        try :
            with transaction.atomic() :
                if request.user.role_id != RoleID.ADMIN.value :
                    return JsonResponse({'message' : 'PERMISSION_DENIED'}, status=403)
            
                data = json.loads(request.body)
                
                category_id = data['category_id']
                name        = data['name']
                price       = data['price']
                url         = data['url']
            
                product = Product.objects.create(
                    category_id = category_id,
                    name        = name,
                    price       = price
                )
                
                Thumbnail.objects.create(
                    product = product,
                    url     = url
                )
                
                return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except IntegrityError :
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=400)