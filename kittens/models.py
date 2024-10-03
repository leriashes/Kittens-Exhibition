from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kitten(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Rating(models.Model):
    value = models.PositiveIntegerField()

    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value