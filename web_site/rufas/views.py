from django.shortcuts import render
from rest_framework.viewsets import generics
# Create your views here.

class UserCreateView(generics.CreateAPIView):
    