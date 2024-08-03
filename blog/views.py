from django.shortcuts import render, get_object_or_404
from django.views.generic import (TemplateView, CreateView, ListView)
from .models import Recipe
from .forms import NewFlavorsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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