from django.shortcuts import render
from rest_framework.viewsets import generics

from rufas.serializers import UserSeriailzer
# Create your views here.

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSeriailzer
    