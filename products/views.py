import json
   
from enum               import Enum
from django.http        import JsonResponse
from django.views       import View
from django.db          import (
    transaction,
    IntegrityError
)
from django.db.models   import F

from users.utils        import login_required
from products.models    import (
    Color,
    ProductImage,
    Size,
    Thumbnail,
    Product,
    DetailProduct
)
from products.filters    import ProductList

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
            
            product_list = [
                {
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
            
            return JsonResponse({'product_list' : product_list}, status=200)
        
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    @login_required
    def post(self, request) :
        try :
            with transaction.atomic() :
                if request.user.role_id != RoleID.ADMIN.value :
                    return JsonResponse({'message' : 'PERMISSION_DENIED'}, status=403)
            
                data = json.loads(request.body)
                
                item_id = data['item_id']
                name    = data['name']
                price   = data['price']
                url     = data['url']
            
                product = Product.objects.create(
                    item_id  = item_id,
                    name     = name,
                    price    = price
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
        
class DetailProductView(View) :
    def get(self, request, product_id) :
        try :
            product         = Product.objects.prefetch_related('productimage_set').get(id=product_id)
            detail_products = DetailProduct.objects.select_related('size', 'color', 'product').filter(product=product)
            
            data_set = [{
                'id'     : product_id,
                'name'   : product.name,
                'price'  : product.price,
                'detail' : [{
                    'color_id'   : detail['color'],
                    'color_name' : Color.objects.get(id=detail['color']).color,
                    'size' : [{
                        'size_id'   : size['size'],
                        'size_name' : Size.objects.get(id=size['size']).size
                    }for size in detail_products.filter(color_id=detail['color']).values('size')]
                }for detail in detail_products.values('color').distinct()],
                'images' : [{
                    'id'  : image.id,
                    'url' : image.url
                }for image in product.productimage_set.all()]
            }]
            
            return JsonResponse({'data_set' : data_set}, status=200)
        
        except TypeError :
            return JsonResponse({'message' : 'TYPE_ERROR'}, status=400)
        
        except Product.DoesNotExist :
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)
    
    def post(self, request, product_id) :
        try :
            with transaction.atomic() :
                data = json.loads(request.body)
                
                thumbnail_url = data.get('thumbnail', None)
                name          = data.get('name')
                sales         = data.get('sales')
                product       = Product.objects.select_related('thumbnail').get(id=product_id)
                
                if thumbnail_url :
                    thumbnail = product.thumbnail_set.get()
                    thumbnail.url = thumbnail_url
                    thumbnail.save()
                
                if sales :
                    product.price = F('price') * (100-int(sales)) / 100
                    product.save()
                                 
                if name :
                    product.name = name
                    product.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
            
        except Product.DoesNotExist :
            return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)