import json
import bcrypt
import jwt

from django.db    import IntegrityError
from django.http  import JsonResponse
from django.views import View

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
            role_id  = data['role_id']
            
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            role = Role.objects.get(id=role_id)
              
            User.objects.create(
                email    = email,
                password = password,
                role     = role
            )
            
            return JsonResponse({'message' : 'CREATE_USER'}, status=201)
 
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except IntegrityError :
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=400)
        
        except Role.DoesNotExist :
            return JsonResponse({'message' : 'ROLE_DOES_NOT_EXIST'}, status=400)