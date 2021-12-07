import jwt
import bcrypt
import json

from django.test     import (
    Client,
    TestCase,
    TransactionTestCase
)
from django.conf     import settings
from products.models import (
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
    def setUp(self) :
        menu      = Menu.objects.create(id=1, name='여성')
        category  = Category.objects.create(id=1, menu=menu, parent_category=None)
        product   = Product.objects.create(id=1, category=category, name='신상품옷', price=1111111)
        thumbnail = Thumbnail.objects.create(id=1, url="test", product=product)
        
        role1     = Role.objects.create(id=1, role='admin')
        role2     = Role.objects.create(id=2, role='user')
        
        admin     = User.objects.create(id=1, email='test1', password='1234', role=role1)
        user      = User.objects.create(id=2, email='test2', password='1234', role=role2)
        
        access_token1 = jwt.encode({'id' : admin.id}, settings.SECRET_KEY, settings.ALGORITHMS)
        access_token2 = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHMS)
        
        global headers1, headers2
        headers1 = {'HTTP_Authorization' : access_token1}
        headers2 = {'HTTP_Authorization' : access_token2}
    
    def tearDown(self) :
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Thumbnail.objects.all().delete()
        Role.objects.all().delete()
        User.objects.all().delete()
    
    def test_success_post_product(self) :
        client = Client()
        
        product = {
            'category_id' : 1,
            'name'        : 'hihi',
            'price'       : 22222,
            'url'         : 'url'
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers1)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS'
        })
    
    def test_failure_post_product_raise_forbidden(self) :
        client = Client()
        
        product = {
            'category_id' : 1,
            'name'        : 'hihi',
            'price'       : 22222,
            'url'         : 'url'
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
            'category_id' : 100,
            'name'        : 'hihi',
            'price'       : 22222,
            'url'         : 'url'
        }
        
        response = client.post('/products', json.dumps(product), content_type='application/json', **headers1)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message': 'INTEGRITY_ERROR'
        })