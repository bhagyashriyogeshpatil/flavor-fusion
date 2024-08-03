from django.urls import path
from .views import Index, NewFlavors, RecipesList, recipe_detail

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new_flavors/', NewFlavors.as_view(), name='new_flavors'),
    path('recipes/', RecipesList.as_view(), name='recipes'),
    path('recipe_detail/<slug:slug>/', recipe_detail, name='recipe_detail'),
]