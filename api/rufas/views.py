from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.response import Response

from rufas.models import main_service

from rufas.serializers import UserSeriailzer, UserLoginSeriailzer, ServiceSerializer
# Create your views here.

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSeriailzer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSeriailzer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        res = Response(
            {
                "userid": serializer.validated_data['email'].id,
                "message": "로그인 성공",
                "token": {
                    "access": serializer.validated_data['access'],
                    "refresh": serializer.validated_data['refresh'],
                }
            },
            status=status.HTTP_201_CREATED,
        )

        # jwt 토큰을 쿠키에 저장
        res.set_cookie("refresh", serializer.validated_data['refresh'], httponly=True)

        return res
    
class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = main_service.objects.all()