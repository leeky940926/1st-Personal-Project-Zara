import json
import bcrypt
import jwt

from django.test  import (
    TransactionTestCase,
    TestCase,
    Client
)
from django.conf  import settings

from users.models import Role, User

class TestSignUpView(TransactionTestCase) :
    def setUp(self) :
        general_role = Role.objects.create(id=2, role='user')
        User.objects.create(id=1, email='user@test.com', password=bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), role=general_role)
    
    def tearDown(self) :
        Role.objects.all().delete()
        User.objects.all().delete()
    
    def test_success_sign_up_user(self) :
        client = Client()
        
        user_info = {
            "id"       : 2,
            "email"    : "newuser@test.com",
            "password" : "1234",
            "role_id"  : 2
        }
        
        response = client.post('/users/signup', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATE_SUCCESS'})
    
    def test_fail_sign_up_user_raise_key_error(self) :
        client = Client()
        
        user_info = {
            
        }
        
        response = client.post('/users/signup', json.dumps(user_info), content_type='application/json') 
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_fail_sign_up_user_raise_integrity_error(self) :
        client = Client()
        
        user_info = {
            "id"       : 2,
            "email"    : "user@test.com",
            "password" : "1234",
            "role_id"  : 2
        }
        
        response = client.post('/users/signup', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'INTEGRITY_ERROR'})

class TestSignInView(TestCase) :
    def setUp(self) :
        general_role = Role.objects.create(id=2, role='user')
        user1        = User.objects.create(id=1, email='user@test.com', password=bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), role=general_role)
        
        global access_token
        access_token = jwt.encode({'id':user1.id}, settings.SECRET_KEY, settings.ALGORITHMS)
        
    def tearDown(self) :
        Role.objects.all().delete()
        User.objects.all().delete()
    
    def test_success_sign_in(self) :
        client = Client()
        
        user_info = {
            "email"    : "user@test.com",
            "password" : "1234"
        }
        
        response = client.post('/users/signin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'access_token' : access_token})
    
    def test_failure_sign_in_raise_key_error(self) :
        client = Client()
        
        user_info = {
            "email"    : "user@test.com"
        }
        
        response = client.post('/users/signin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_failure_sign_in_raise_user_does_not_exist(self) :
        client = Client()
        
        user_info = {
            "email"    : "user1234@test.com",
            "password" : "1234"
        }
        
        response = client.post('/users/signin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'USER_DOES_NOT_EXIST'})
    
    def test_failure_sign_in_raise_invalid_password(self) :
        client = Client()
        
        user_info = {
            "email"    : "user@test.com",
            "password" : "12345"
        }
        
        response = client.post('/users/signin', json.dumps(user_info), content_type='appilcation/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})