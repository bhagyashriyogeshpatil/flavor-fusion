from django.contrib import admin
from .models import CuisineType, Recipe, Ingredient, Instruction

# Register your models here.
admin.site.register(CuisineType)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)