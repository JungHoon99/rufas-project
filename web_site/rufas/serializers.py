from rest_framework import serializers
from rufas.models import User

class UserSeriailzer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['userid', 'pw1', 'pw2', 'name', 'address', 'gender', 'phone']

class UserLoginSeriailzer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['userid', 'pw']