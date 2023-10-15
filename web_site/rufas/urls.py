
from django.urls import path

from rufas.views import UserCreateView


urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup-user'),
]