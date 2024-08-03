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
    context_object_name = "recipes"


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
