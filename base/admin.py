import imp
from django.contrib import admin

# Register your models here.
from .models import Room, Comments, Type

admin.site.register(Room)
admin.site.register(Comments)
admin.site.register(Type)