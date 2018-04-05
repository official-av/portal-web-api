from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account,Department,PortalQuestion
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            'username', 'email', 'password', 'confirm_password', 'phonenum', 'first_name', 'last_name','dept')

    def create(self, validated_data):
        a = Account.objects.create(
                                  email=validated_data['email'],
                                  phonenum=validated_data['phonenum'],
                                  user=User.objects.create(username=validated_data['username'],
                                                           password=make_password(validated_data['password'])),
                                  last_name=validated_data['last_name'],
                                  first_name=validated_data['first_name'],
                                  dept=validated_data['dept'])

        a.save()
        return a

    def validate(self, data):
        '''
        Ensure the passwords are the same
        '''
        if data['password']:
            print ("Here")
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError(
                    "The passwords have to be the same"
                )
        return data
class AccountGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
             'username', 'first_name', 'last_name',
            'email', 'dept','phonenum','mobile_flag','email_flag')

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model=PortalQuestion
        fields=('text','timestamp','deadline','asked_by_id')

        def create(self,validated):
            a=PortalQuestion.objects.create(
                text = validated_data['text'],timestamp = validated_data['timestamp'],deadline =validated_data['deadline'],
           asked_by_id = validated_data['asked_by_id'])
            a.save()

            return a
