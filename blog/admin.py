from django.contrib import admin
from .models import CuisineType, Recipe
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'author', 'created_on')
    search_fields = ['title', 'cuisines_type', 'status']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions', )

# Register your models here.
admin.site.register(CuisineType)
