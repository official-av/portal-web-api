from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer,AccountGetSerializer,QuestionSerializer
from .models import Account,PortalQuestion
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
import json,nexmo,random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AuthRegister(APIView):
    """
    Register a new user.
    """
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)


    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Update(APIView):



    def post(self,request,format=None):
        data=request.data
        a=User.objects.get(username=data['username'])

        if(data['password']==data['confirm_password']):

            a.password=make_password(data['password'])
            a.save()
            return Response({'sucess':'Yes'}, status=status.HTTP_201_CREATED)
        return Response({'sucess':'No'}, status=status.HTTP_400_BAD_REQUEST)

class Profile(APIView):
    serializer_class = AccountGetSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, username):
        try:

            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("Error")

    def get(self,request,username,format=None):


        account = self.get_object(username)
        acc=Account.objects.get(user_id=account)
        serializer=self.serializer_class(acc)
        return Response(serializer.data)

class OtpRegister(APIView):

    def post(self,request,format=None):
        length=5
        data=request.data

        mobile_number=data['phonenum']
        client = nexmo.Client(key='66505af0', secret='cltyPLV3jQJQYYwX')
        b=random.sample(range(10**(length-1), 10**length), 1)[0]
        client.send_message({'from': '919473805008', 'to': mobile_number, 'text': b})

        return Response({'text':b}, status=status.HTTP_201_CREATED)

class CreateQuestion(APIView):
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)


    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        data=request.data
        if serializer.is_valid():
            serializer.save()
            a=PortalQuestion.objects.get(text=data['text'],asked_by_id=data['asked_by_id'])
            c=Account.objects.get(pk=data['asked_by_id'])
            b=AuthViewer.objects.create(question_id=a,department_id=c.dept)
            b.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class checkPassword(APIView):


    def post(self,request,format=None):
        data=request.data
        account = authenticate(username=data['username'],password=data['password'])
        if(account!=None):
            return Response({'response':'match'},status=status.HTTP_201_CREATED)
        else:
            return Response({'response':'error'},status=status.HTTP_400_BAD_REQUEST)

class checkUsername(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def post(self,request,format=None):
        account=self.get_object(request.data['username'])
        if(account!=None):
            return Response({'user':'exists'},status=status.HTTP_201_CREATED)
        else:
            return Response({'user':'does not exists'},status=status.HTTP_400_BAD_REQUEST)
