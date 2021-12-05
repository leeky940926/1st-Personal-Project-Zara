from django.db   import models

from core.models import TimeStampModel

class Role(TimeStampModel) :
    role = models.CharField(max_length=20)
    
    class Meta :
        db_table = 'roles'
        
class User(TimeStampModel) :
    role     = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    email    = models.EmailField(unique=True, max_length=40)
    password = models.CharField(max_length=500)
    
    class Meta :
        db_table = 'users'