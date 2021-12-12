import jwt
import bcrypt
import json

from django.test     import (
    Client,
    TestCase,
    TransactionTestCase,
    client
)
from django.conf     import settings
from products.models import (
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
from users.models   import (
    Role, 
    User
)

class TestProductView(TransactionTestCase) :
    
    TransactionTestCase.maxDiff = None
    
    def setUp(self) :
        global headers1, headers2
        
        menu      = Menu.objects.create(id=1, name='여성')
        category  = Category.objects.create(id=1, menu=menu, parent_category=None)
        item      = Item.objects.create(id=1, category=category, name='item1')
        product1  = Product.objects.create(id=1, item=item, name='신상품옷', price=1111111)
        product2  = Product.objects.create(id=2, item=item, name='최신상품', price=2222222)
        thumb1    = Thumbnail.objects.create(id=1, url="test1", product=product1)
        thumb2    = Thumbnail.objects.create(id=2, url="test2", product=product2)
        
        size_1    = Size.objects.create(id=1, size="s")
        color_1   = Color.objects.create(id=1, color='RED')
        detail1   = DetailProduct.objects.create(id=1, size=size_1, color=color_1, product=product1)
        detail2   = DetailProduct.objects.create(id=2, size=size_1, color=color_1, product=product2)
        
        role1     = Role.objects.create(id=1, role='admin')
        role2     = Role.objects.create(id=2, role='user')
        
        admin     = User.objects.create(id=1, email='test1', password='1234', role=role1)
        user      = User.objects.create(id=2, email='test2', password='1234', role=role2)
        
        access_token1 = jwt.encode({'id' : admin.id}, settings.SECRET_KEY, settings.ALGORITHMS)
        access_token2 = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHMS)
        
        headers1 = {'HTTP_Authorization' : access_token1}
        headers2 = {'HTTP_Authorization' : access_token2}
    
    def tearDown(self) :
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Item.objects.all().delete()
        Product.objects.all().delete()
        Thumbnail.objects.all().delete()
        Role.objects.all().delete()
        User.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        DetailProduct.objects.all().delete()
    
    def test_success_post_product(self) :
        client = Client()
        
        product = {
            'item_id' : 1,
            'name'    : 'hihi',
            'price'   : 22222,
            'url'     : 'url'
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers1)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS'
        })
    
    def test_failure_post_product_raise_forbidden(self) :
        client = Client()
        
        product = {
            'item_id' : 1,
            'name'    : 'hihi',
            'price'   : 22222,
            'url'     : 'url'
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers2)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'message': 'PERMISSION_DENIED'
        })
    
    def test_failure_post_product_raise_key_error(self) :
        client = Client()
        
        product = {
            
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers1)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message': 'KEY_ERROR'
        })
    
    def test_failure_post_product_raise_category_does_not_exist(self) :
        client = Client()
        
        product = {
            'item_id'     : 100,
            'name'        : 'hihi',
            'price'       : 22222,
            'url'         : 'url'
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers1)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message': 'INTEGRITY_ERROR'
        })
        
    def test_success_get_product_list(self) :
        client = Client()
        
        product_list = [
            {
                'id'        : 1,
                'name'      : "신상품옷",
                'price'     : 1111111,
                'item_id'   : 1,
                'item_name' : "item1",
                'thumbnail' : [
                    {
                        'id'  : 1,
                        'url' : "test1",
                    }],
                'detail_set' : [
                    {
                        'color_id'   : 1,
                        'color_name' : "RED",
                        'size_id'    : 1,
                        'size_name'  : "s"
                    }
                ]
            }
        ]
        
        response = client.get('/products?category_id=1')
        
        self.assertEqual(response.status_code, 200)
    
    def test_failure_get_list_raise_key_error(self) :
        client = Client()
        
        response = client.get('/products')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message' : 'KEY_ERROR' 
        })

class TestDetailProductView(TestCase) :
    def setUp(self) :
        menu      = Menu.objects.create(id=1, name='여성')
        category  = Category.objects.create(id=1, menu=menu, parent_category=None)
        item      = Item.objects.create(id=1, category=category, name='item1')
        product   = Product.objects.create(id=1, item=item, name='신상품옷', price=1111111)
        size_1    = Size.objects.create(id=1, size="s")
        color_1   = Color.objects.create(id=1, color='RED')
        color_2   = Color.objects.create(id=2, color='BLUE')
        
        details   = [
            DetailProduct(id=1, size=size_1, color=color_1, product=product),
            DetailProduct(id=2, size=size_1, color=color_2, product=product)
        ]
        
        DetailProduct.objects.bulk_create(details)
        
        product_image = [
            ProductImage(id=1, product=product, url="url1"),
            ProductImage(id=2, product=product, url="url2"),
            ProductImage(id=3, product=product, url="url3")
        ]
        
        ProductImage.objects.bulk_create(product_image)
    
    def tearDown(self) :
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Item.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        DetailProduct.objects.all().delete()
        ProductImage.objects.all().delete()
    
    def test_success_get_detail(self) :
        client = Client()
        
        data_set = [{
            'id'     : 1,
            'name'   : '신상품옷',
            'price'  : 1111111,
            'detail' : [{
                'color_id'   : 1,
                'color_name' : 'RED',
                'size' : [{
                    'size_id'   : 1,
                    'size_name' : 's'
                }],
            },
            {
                'color_id'   : 2,
                'color_name' : 'BLUE',
                'size' : [{
                    'size_id'  : 1,
                    'size_name' : 's'
                }]    
            }],
            'images' : [{
                'id'  : 1,
                'url' : 'url1'
            },
            {
                'id'  : 2,
                'url' : 'url2'
            },
            {
                'id'  : 3,
                'url' : 'url3'
            }]
        }]
            
        
        response = client.get('/products/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'data_set' : data_set
        })