from django.db import models
from django.contrib.auth.models import PermissionsMixin,User



class Department(models.Model):
    department_name=models.CharField(unique=True,max_length=100)

    def __str__(self):
        return self.department_name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,default='Ritika')
    last_name=models.CharField(max_length=100,default='Mittal')
    email=models.EmailField(unique=True)
    phonenum=models.CharField(unique=True,max_length=10)
    dept=models.ForeignKey(Department, on_delete=models.CASCADE)
    mobile_flag=models.BooleanField(default=False)
    email_flag=models.BooleanField(default=False)
    status_flag=models.BooleanField(default=False)


    def __str__(self):
        return self.email
