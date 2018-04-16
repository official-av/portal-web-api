from django.db import models
from django.contrib.auth.models import PermissionsMixin,User



class Department(models.Model):
    name=models.CharField(unique=True,max_length=100)

    def __str__(self):
        return str(self.id)


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
        return str(self.id)

class PortalQuestion(models.Model):


    content = models.CharField(max_length=500, null=False)
    asked_on = models.DateTimeField("Date Question is Published")
    deadline = models.DateTimeField("Date to be Answered Within")
    asked_to = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_collaborative = models.BooleanField(default=False)
    answer=models.CharField(max_length=500,null=True)
    answered_on=models.DateTimeField("Answered On",null=True)

    def __str__(self):
        return str(self.id)


class PortalRecommendation(models.Model):

    ques_id = models.ForeignKey(PortalQuestion, on_delete=models.CASCADE)
    invited_dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    rec_answer = models.CharField(max_length=500, null=True)
    asked_on = models.DateTimeField("Question Asked On")
    answered_on = models.DateTimeField("Question Answered On",null=True)


    def __str__(self):
        return  str(self.id)
