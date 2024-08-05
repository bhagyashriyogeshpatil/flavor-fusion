from django.shortcuts import render, get_object_or_404
from django.views.generic import (TemplateView, CreateView, ListView, DeleteView)
from .models import Recipe
from .forms import NewFlavorsForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy

# To test the 403 Forbidden error page
# from django.core.exceptions import PermissionDenied

# Create your views here.

class Index(TemplateView):
    template_name = "blog/index.html"


class RecipesList(ListView):
    """View all recipes"""
    template_name = "blog/recipes.html"
    model = Recipe
    context_object_name = "recipes_list"
    paginate_by = 6


class NewFlavors(LoginRequiredMixin, CreateView):
    """Add New Flavors view"""
    template_name = "blog/new_flavors.html"
    model = Recipe
    form_class = NewFlavorsForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        msg = "Your recipe has been posted successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(NewFlavors, self).form_valid(form)


def recipe_detail(request, slug):
    """
    Function-based view to render recipe in detail.
    """
    queryset = Recipe.objects.filter(status=1)
    recipe = get_object_or_404(queryset, slug=slug)

    return render(
        request, 
        "blog/recipe_detail.html", 
        {"recipe": recipe})

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a recipe"""
    model = Recipe
    success_url = reverse_lazy('recipes')

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, request, *args, **kwargs):
        msg = "Your recipe has been deleted successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().delete(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     # Add a debug statement before the delete
    #     print("Attempting to delete recipe...") 
    #     response = super().delete(request, *args, **kwargs)
    #     # Add a debug statement after the delete
    #     print("Recipe deleted.")
    #     # Add the success message
    #     msg = "Your recipe has been deleted successfully."
    #     messages.success(self.request, msg)
    #     # Debugging statements
    #     for message in messages.get_messages(request):
    #         print(f"Message: {message}")
    #     return response

# To test the 403 Forbidden error page
# def my_view(request):
#     raise PermissionDenied