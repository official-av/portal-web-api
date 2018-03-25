from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'email', 'password', 'confirm_password','phonenum')



    def create(self, validated_data):

        print('create')
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        print('update')
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username',
                                               instance.username)
        instance.first_name = validated_data.get('first_name',
                                                instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                               instance.last_name)

        instance.phonenum = validated_data.get('phonenum',
                                               instance.phonenum)

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and password == confirm_password:
            instance.set_password(password)

        instance.save()
        return instance

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
            'id', 'username', 'first_name', 'last_name',
            'email', 'password','phonenum')
