from django.urls import path
from .views import Index, NewFlavors, RecipesList, recipe_detail, DeleteRecipe

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new_flavors/', NewFlavors.as_view(), name='new_flavors'),
    path('recipes/', RecipesList.as_view(), name='recipes'),
    path('recipe_detail/<slug:slug>/', recipe_detail, name='recipe_detail'),
    path('delete_recipe/<slug:slug>/', DeleteRecipe.as_view(), name='delete_recipe'),
    # To test the 403 Forbidden error page
    # path('forbidden/', my_view, name='forbidden'),
]