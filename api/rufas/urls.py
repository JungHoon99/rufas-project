from django.urls import path
from rufas.views import UserCreateView, UserLoginView, ServiceViewSet


urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup-user'),
    path('login/', UserLoginView.as_view(), name='login-user'),
    path('service/',ServiceViewSet.as_view({'get':'list','post':'create'}), name='service'),
]