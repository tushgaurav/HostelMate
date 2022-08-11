from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_capacity = models.IntegerField()

    def __str__(self):
        return str(self.name)

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    room_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    occupants = models.ManyToManyField(User, related_name='occupant', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body[0:50])
