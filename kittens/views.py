from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *

# Create your views here.
class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class KittenListCreateView(generics.ListCreateAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        breed_id = self.request.query_params.get('breed')

        if breed_id:
            queryset = queryset.filter(breed=breed_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class KittenRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You can't edit this kitten")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You can't delete this kitten")
        instance.delete()
