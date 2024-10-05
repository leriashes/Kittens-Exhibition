from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('breeds/', BreedListView.as_view(), name='breed-list'),

    path('kittens/', KittenListCreateView.as_view(), name='kitten-list-create'),
    path('kittens/<int:pk>/', KittenRetrieveUpdateDestroyView.as_view(), name='kitten-detail'),

    path('kittens/<int:kitten_id>/rate/', KittenRatingView.as_view(), name='kitten-rating'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]