from rest_framework import serializers
from .models import *

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class KittenListSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Kitten
        exclude = ['description']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

class KittenDetailSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Kitten
        fields = ['id', 'name', 'age', 'breed', 'color', 'description', 'owner', 'user_rating']

    def get_user_rating(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            rating = Rating.objects.filter(kitten=obj, user=user).first()
            if rating:
                return rating.value
        return None
        
    