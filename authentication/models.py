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

class PortalQuestion(models.Model):


    text = models.CharField(max_length=500, null=False)
    timestamp = models.DateTimeField("Date Question is Published")
    deadline = models.DateTimeField("Date to be Answered Within")
    asked_by_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_recommended = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class PortalRecommendation(models.Model):

    ques_id = models.ForeignKey(PortalQuestion, on_delete=models.CASCADE)
    by_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    recommendation_answer = models.CharField(max_length=500, null=False)

    def __str__(self):
        return  str(self.recommendation_id)
