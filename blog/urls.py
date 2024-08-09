from django.urls import path
from .views import Index, NewFlavors, RecipesList, recipe_detail, DeleteRecipe, EditRecipe, like_recipe, comment_edit

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new_flavors/', NewFlavors.as_view(), name='new_flavors'),
    path('recipes/', RecipesList.as_view(), name='recipes'),
    path('recipe_detail/<slug:slug>/', recipe_detail, name='recipe_detail'),
    path('delete_recipe/<slug:slug>/', DeleteRecipe.as_view(), name='delete_recipe'),
    path('edit_recipe/<slug:slug>/', EditRecipe.as_view(), name='edit_recipe'),
    path('like/<slug:slug>/', like_recipe, name='recipe_like'),
    path('<slug:slug>/comment/<int:comment_id>/edit/', comment_edit, name='comment_edit'),
    # To test the 403 Forbidden error page
    # path('forbidden/', my_view, name='forbidden'),
]