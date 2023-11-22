from django.urls import path
from recomands.views import RecommendationView, CreateUserItemWithRatingView,track

urlpatterns = [
    path('recommendation/<str:username>/', RecommendationView.as_view(), name='recommendation'),
    path('create-user-item/', CreateUserItemWithRatingView.as_view(), name='create_user_item'),
    path('track/', track.as_view(), name='tracker')
]