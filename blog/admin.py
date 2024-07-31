from django.contrib import admin
from .models import CuisineType, Recipe

# Register your models here.
admin.site.register(CuisineType)
admin.site.register(Recipe)