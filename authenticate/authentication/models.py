from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class AccountManager(BaseUserManager):
    def create_user(self,username,password=None,**kwargs):

        if not username:
            raise ValueError('Users must have a valid username')


        account=self.model(

        username=username,
        first_name=kwargs.get('first_name',"Ritika"),
        last_name=kwargs.get('last_name',"Mittal"),
        email=kwargs.get('email',"ritikamittal1701@gmail.com"),
        phonenum=kwargs.get('phonenum',"9871402961"),
        )
        account.is_staff = False
        account.is_superuser=False
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self,username,password=None,**kwargs):
        
        account=self.create_user(username,password,**kwargs)
        account.is_superuser=True
        account.is_admin=True
        account.is_staff = True
        account.save()

        return account


class Account(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(unique=True,max_length=50)
    first_name=models.CharField(max_length=100,default='Ritika')
    last_name=models.CharField(max_length=100,default='Mittal')
    email=models.EmailField(default='ritika1701@gmail.com')
    phonenum=models.CharField(max_length=10,default='9871402961')
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)


    objects=AccountManager()

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]
