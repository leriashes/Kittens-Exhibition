from django.urls import include, path
from .views import *

urlpatterns = [
    path('breeds/', BreedListView.as_view(), name='breed-list')
]