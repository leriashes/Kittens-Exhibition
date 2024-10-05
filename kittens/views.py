from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

class KittenRatingView(generics.GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, kitten_id):
        user = request.user
        kitten = Kitten.objects.get(id=kitten_id)
        value = request.data.get('value')

        if value is None:
            return Response({'detail': 'The "value" parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            value = int(value)
        except ValueError:
            return Response({'detail': 'The value must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        if value < 1 or value > 5:
            return Response({'detail': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            kitten=kitten, user=user, 
            defaults={
                'value': value
            }
        )

        if created:
            return Response({'detail': 'Rating added'}, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Rating updated'}, status=status.HTTP_200_OK)