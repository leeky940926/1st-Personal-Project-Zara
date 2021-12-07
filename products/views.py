import json
import requests
   
from enum               import Enum
from bs4                import BeautifulSoup
from django.http        import JsonResponse
from django.views       import View

from users.models       import (
    User,
    Role
)
from users.utils        import login_required
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

class RoleID(Enum) :
    ADMIN = 1
    USER  = 2

class MenuView(View) :
    @login_required
    def post(self, request) :
        try :
            data = json.loads(request.body)
            
            user = request.user
            
            login_user = User.objects.select_related('role').get(id = user.id)
        
            if login_user.role_id != RoleID.ADMIN.value :
                return JsonResponse({'message' : 'PERMISSION_DENIED'}, status=403)
            
            Menu.objects.create(name = data['name'])
            
            return JsonResponse({'message' : 'SUECCESS'}, status=201)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist :
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status=400)
        
        except Role.DoesNotExist :
            return JsonResponse({'message' : 'ROLE_DOES_NOT_EXIST'}, status=400)
    
    def get(self, request) :
        
        req = requests.get('https://www.zara.com/kr/')
       
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        
        menus = soup.select('#sidebar > div > nav > div > ul')

        menu_list = [menu.text for menu in menus]

        return JsonResponse({'menu_list' : menu_list}, status=200)