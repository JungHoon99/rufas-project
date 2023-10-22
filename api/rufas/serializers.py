from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from secrets import token_urlsafe

from rufas.models import User, main_service

class UserSeriailzer(serializers.ModelSerializer):
    pw1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password] # 비밀번호 유효성 검사
    )
    pw2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인

    class Meta:
        model = User
        fields = ('email', 'pw1', 'pw2', 'username', 'gender', 'phone', 'date_of_birth')

    def validate(self, data):
        if data['pw1'] != data['pw2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        # create 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성함.
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            gender=validated_data['gender'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth']
        )
        user.set_password(validated_data['pw1'])
        user.save()
        return user

class UserLoginSeriailzer(TokenObtainPairSerializer):
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user:
            data = super().validate(attrs)
            data['email'] = user
            return data
        else:
            raise serializers.ValidationError("아이디 혹은 비밀번호가 일치하지 않습니다.")
        

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_service
        fields = ['owner', 'name', 'domain', 'category', 'enabled']

    def create(self, validated_data):
        service = main_service(
            owner=validated_data['owner'],
            name=validated_data['name'],
            domain=validated_data['domain'],
            category=validated_data['category'],
            enabled=validated_data['enabled'],
            secret_key=token_urlsafe(16)
        )
        return super().create(validated_data)
