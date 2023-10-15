from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from rufas.models import User

class UserSeriailzer(serializers.ModelSerializer):
    pw1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password] # 비밀번호 유효성 검사
    )
    pw2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인

    class Meta:
        model = User
        fields = ('userid', 'pw1', 'pw2', 'name', 'address', 'gender', 'phone')

    def validate(self, data):
        if data['pw1'] != data['pw2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        if('position' not in data):
            raise serializers.ValidationError({"position":"직책을 입력해주세요"})
        return data

    def create(self, validated_data):
        # create 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성함.
        user = User.objects.create(
            userid=validated_data['userid'],
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
            gender=validated_data['gender'],
            phone=validated_data['phone'] 
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'pw']