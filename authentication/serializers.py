from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Member
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': "A user with that username already exists."})
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords don't match"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})

        account = User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)

        account.is_active = False

        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)