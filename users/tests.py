import json
import bcrypt
import jwt

from django.test import (
    TransactionTestCase,
    Client
)

from users.models import Role, User

class TestSignUpUserView(TransactionTestCase) :
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
            "password" : "1234"
        }
        
        response = client.post('/users/signup/general', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATE_USER'})
    
    def test_fail_sign_up_user_raise_key_error(self) :
        client = Client()
        
        user_info = {
            
        }
        
        response = client.post('/users/signup/general', json.dumps(user_info), content_type='application/json') 
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_fail_sign_up_user_raise_integrity_error(self) :
        client = Client()
        
        user_info = {
            "id"       : 2,
            "email"    : "user@test.com",
            "password" : "1234"
        }
        
        response = client.post('/users/signup/general', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'INTEGRITY_ERROR'})

class TestSignUpAdminView(TransactionTestCase) :
    def setUp(self) :
        admin_role = Role.objects.create(id=1, role='admin')
        User.objects.create(id=1, email='admin@test.com', password=bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), role=admin_role)
        
    def tearDown(self) :
        Role.objects.all().delete()
        User.objects.all().delete()
    
    def test_success_sign_up_admin(self) :
        client = Client()
        
        user_info = {
            "id"       : 2,
            "email"    : "test@test.com",
            "password" : "1234"
        }
        
        response = client.post('/users/signup/admin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{'message' : 'CREATE_ADMIN'})
    
    def test_failure_sign_up_admin_raise_key_error(self) :
        client = Client()
        
        user_info = {
            
        }
        
        response = client.post('/users/signup/admin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
    
    def test_failure_sign_up_admin_raise_integrity_error(self) :
        client = Client()
        
        user_info = {
            "id"       : 2,
            "email"    : "admin@test.com",
            "password" : "1234"
        }
        
        response = client.post('/users/signup/admin', json.dumps(user_info), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INTEGRITY_ERROR'})