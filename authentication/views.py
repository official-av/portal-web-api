from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer,AccountGetSerializer
from .models import Account
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

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
            print('error')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Update(APIView):

    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise Http404

    def put(self,request,username,format=None):
        account = self.get_object(username)
        serializer = self.serializer_class(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Profile(APIView):
    serializer_class = AccountGetSerializer
    permission_classes = (IsAuthenticated)

    def get_object(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise Http404

    def get(self,request,username,format=None):
        account = self.get_object(username)
        serializer=self.serializer_class(account)
        return Response(serializer.data)
