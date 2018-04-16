from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account,Department,PortalQuestion,PortalRecommendation
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
              'first_name', 'last_name',
            'email', 'dept','phonenum','mobile_flag','email_flag')



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model=PortalQuestion
        fields=('content','asked_on','deadline','asked_to','answer','answered_on')

        def create(self,validated):
            a=PortalQuestion.objects.create(
                content = validated_data['content'],asked_on = validated_data['asked_on'],deadline =validated_data['deadline'],
           asked_to = validated_data['asked_to'])

            a.save()
            return a

class InviteSerializer(serializers.ModelSerializer):

    class Meta:
        model=PortalRecommendation
        fields='__all__'

        def create(self,validated):
            a=PortalRecommendation.objects.create(ques_id=validated_data['ques_id'],invited_dept=validated_data['invited_dept'])
            a.save()
            return a



class DirectSerializer(serializers.ModelSerializer):

    class Meta:
        model=PortalRecommendation
        fields='__all__'


class DeptSerializer(serializers.ModelSerializer):

    class Meta:
        model=Department
        fields=('id','name')

class Question(serializers.ModelSerializer):

    class Meta:
        model=PortalQuestion
        fields='__all__'
