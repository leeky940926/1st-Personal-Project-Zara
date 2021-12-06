import json
import bcrypt
import jwt

from django.db    import IntegrityError
from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import (
    Role,
    User
)

class SignUpView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            role_id  = int(data['role_id'])
            
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            role = Role.objects.get(id=role_id)
              
            User.objects.create(
                email    = email,
                password = password,
                role     = role
            )
            
            return JsonResponse({'message' : 'CREATE_SUCCESS'}, status=201)
 
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except IntegrityError :
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=400)
        
        except Role.DoesNotExist :
            return JsonResponse({'message' : 'ROLE_DOES_NOT_EXIST'}, status=400)

class SignInView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            
            user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) :
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=401)
            
            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHMS)
            
            return JsonResponse({'access_token' : access_token}, status=201)
        
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist :
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status=400)