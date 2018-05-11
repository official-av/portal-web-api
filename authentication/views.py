from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer,AccountGetSerializer,QuestionSerializer,InviteSerializer,DirectSerializer,DeptSerializer,Question
from .models import Account,PortalQuestion,PortalRecommendation,Department
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json,nexmo,random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings


class AuthRegister(APIView): #Register  API
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

class Update(APIView):  #ChangePassword



    def post(self,request,format=None):
        data=request.data
        a=User.objects.get(username=data['username'])

        if(data['password']==data['confirm_password']):

            a.password=make_password(data['password'])
            a.save()
            return Response({'sucess':'Yes'}, status=status.HTTP_201_CREATED)

        return Response({'sucess':'No'}, status=status.HTTP_400_BAD_REQUEST)

class Profile(APIView): #ViewProfile
    serializer_class = AccountGetSerializer


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

class OtpRegister(APIView):  #OTP

    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        length=5
        data=request.data

        mobile_number=data['phonenum']
        client = nexmo.Client(key='66505af0', secret='cltyPLV3jQJQYYwX')
        b=random.sample(range(10**(length-1), 10**length), 1)[0]
        client.send_message({'from': '919473805008', 'to': mobile_number, 'text': b})

        return Response({'text':b}, status=status.HTTP_201_CREATED)

class CreateQuestion(APIView):  #CreateQuestion
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)


    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class checkPassword(APIView):           #Verify username and Password


    def post(self,request,format=None):
        data=request.data
        account = authenticate(username=data['username'],password=data['password'])
        if(account!=None):
            return Response({'response':'match'},status=status.HTTP_201_CREATED)
        else:
            return Response({'response':'error'},status=status.HTTP_400_BAD_REQUEST)

class checkUsername(APIView):                       #Check Username

    permission_classes = (AllowAny,)
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

class Invitation(APIView):                           #Invite Other Ministeries For Collaboration

    serializer_class = InviteSerializer


    print(InviteSerializer())
    def post(self, request, format=None):
        value=request.data
        for i in range(0,len(value['student'])):
            serializer = self.serializer_class(data=value['student'][i])
            print(serializer)
            print(serializer.is_valid)
            if serializer.is_valid():
                a=PortalQuestion.objects.get(pk=value['student'][i]['ques_id'])
                print(a)
                a.is_collaborative=True
                a.save()
                serializer.save()
        return Response({'yes':'0'}, status=status.HTTP_201_CREATED)

class DirectAnswer(APIView):            #Retrieve All Answer With Question
    serializer_class = DirectSerializer


    def get(self,request,dept_id,format=None):
        account=PortalQuestion.objects.filter(asked_to=dept_id)
        a=[ ]


        for i in account:
            recommend=PortalRecommendation.objects.filter(ques_id=i.id)
            serializer=self.serializer_class(recommend,many=True)
            y={'content':i.content,
            'asked_on':i.asked_on,
            'asked_to':dept_id,
            'deadline':i.deadline,
            'answered_on':i.answered_on,
            'answer':i.answer,
            'is_collaborative':i.is_collaborative,
            'ques_id':i.id,

             'collaborations':serializer.data}
            a.append(y)

        return Response(a)

class InvitedAnswer(APIView):            #Retrieve Invited Answer With Question
    serializer_class = DirectSerializer

    def get(self,request,dept_id,format=None):



            recommend=PortalRecommendation.objects.filter(invited_dept=dept_id)
            a=[]

            for i in recommend:
                account=PortalQuestion.objects.get(id=i.ques_id.id)
                print(account)
                y={'content':account.content,
                'asked_on':account.asked_on,
                'asked_to':account.asked_to.id,
                'deadline':account.deadline,
                'rec_answer':i.rec_answer,
                'answered_on':i.answered_on,
                'recasked_on':i.asked_on,
                'ques_id':i.ques_id.id,
                'answer':account.answer,
                }
                a.append(y)
                print(y)

            return Response(a)



class DepartmentList(APIView):           #Retrievelist

    serializer_class= DeptSerializer
    permission_classes=(AllowAny,)

    def get(self,request,format=None):

        list_name=Department.objects.all()
        serializer=self.serializer_class(list_name,many=True)

        return Response(serializer.data)


class DirectReply(APIView):  #Direct Reply
    serializer_class= Question

    def post(self,request,format=None):

        data=request.data
        print(data)
        answ=PortalQuestion.objects.get(pk=data['ques_id'])
        answ.answer= data['answer']
        answ.answered_on= data['answered_on']
        answ.save()
        serializer=self.serializer_class(answ)
        return Response(serializer.data)

class InviteReply(APIView): #Invited Reply

    serializer_class=DirectSerializer

    def post(self,request,format=None):

        data=request.data
        answ=PortalRecommendation.objects.get(ques_id=data['ques_id'],invited_dept=data['invited_dept'])
        answ.rec_answer= data['rec_answer']
        answ.answered_on= data['answered_on']
        answ.save()
        serializer=self.serializer_class(answ)
        return Response(serializer.data)


class EmailNotify(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,format=None):
        try:
            data = request.data
            msg_plain = "Email Working"
            from_email = settings.EMAIL_HOST_USER
            to_email = User.objects.get(username=data['username']).email
            send_mail(
                'NOTIFICATION EMAIL',
                msg_plain,
                from_email,
                [to_email],
                fail_silently=False
            )
            return Response({'Status':'SENT'})

        except:
            return Response({'Status':'FALSE'})
