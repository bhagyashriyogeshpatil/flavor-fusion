from django.urls import path
from .views import (Index, NewFlavors, RecipesList,
                    recipe_detail, DeleteRecipe, EditRecipe,
                    like_recipe, comment_edit_view,
                    comment_update_view, comment_delete_view)

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new_flavors/', NewFlavors.as_view(), name='new_flavors'),
    path('recipes/', RecipesList.as_view(), name='recipes'),
    path('recipe_detail/<slug:slug>/', recipe_detail, name='recipe_detail'),
    path('delete_recipe/<slug:slug>/',
         DeleteRecipe.as_view(), name='delete_recipe'),
    path('edit_recipe/<slug:slug>/', EditRecipe.as_view(), name='edit_recipe'),
    path('like/<slug:slug>/', like_recipe, name='recipe_like'),
    path('recipe_detail/<slug:slug>/comment/<int:comment_id>/edit/',
         comment_edit_view, name='comment_edit'),
    path('recipe_detail/<slug:slug>/comment/<int:comment_id>/update/',
         comment_update_view, name='comment_update'),
    path('recipe_detail/<slug:slug>/comment/<int:comment_id>/delete/',
         comment_delete_view, name='comment_delete'),
    # To test the 500 Internal Server Error page
    # path('test-500/', trigger_500_error, name='test_500'),
]
