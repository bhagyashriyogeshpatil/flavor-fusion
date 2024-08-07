from django.urls import path
from .views import Index, NewFlavors, RecipesList, recipe_detail, DeleteRecipe, EditRecipe, like_recipe

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new_flavors/', NewFlavors.as_view(), name='new_flavors'),
    path('recipes/', RecipesList.as_view(), name='recipes'),
    path('recipe_detail/<slug:slug>/', recipe_detail, name='recipe_detail'),
    path('delete_recipe/<slug:slug>/', DeleteRecipe.as_view(), name='delete_recipe'),
    path('edit_recipe/<slug:slug>/', EditRecipe.as_view(), name='edit_recipe'),
    path('like/<slug:slug>/', like_recipe, name='recipe_like'),
    # To test the 403 Forbidden error page
    # path('forbidden/', my_view, name='forbidden'),
]