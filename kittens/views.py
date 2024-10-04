from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.
class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class KittenListView(generics.ListAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        breed_id = self.request.query_params.get('breed')

        if breed_id:
            queryset = queryset.filter(breed=breed_id)

        return queryset