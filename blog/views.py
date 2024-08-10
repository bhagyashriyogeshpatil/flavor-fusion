from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, CreateView, ListView, DeleteView, UpdateView)
from .models import Recipe, Comment
from .forms import NewFlavorsForm
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(cuisine_type__name__icontains=query) |
                Q(author__username__icontains=query),
                status=1
            ).order_by('-created_on')
        else:
            queryset = Recipe.objects.all()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        if query and not context['recipes_list']:
            context['no_results'] = True
            context['search_query'] = query
        return context

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
    comments = recipe.comments.all() 

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
                messages.success(request, "Your comment has been submitted and is awaiting approval.")
                return redirect('recipe_detail', slug=recipe.slug)
        else:
            messages.error(request, "You need to be logged in to comment.")
            return redirect('login')
    else:
        comment_form = CommentForm()

    return render(
        request, 
        "blog/recipe_detail.html", 
        {"recipe": recipe, "comments": comments, "comment_form": comment_form})

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

class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Edit/update a recipe """
    model = Recipe
    form_class = NewFlavorsForm
    template_name = "blog/edit_recipe.html"
    success_url = reverse_lazy('recipes')

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        form.instance.author = self.request.user
        msg = "Your recipe has been updated successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)

def like_recipe(request, slug):
    """
    View to like or unlike a recipe.
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    user = request.user

    if user.is_authenticated:
        if request.method == "POST":
            action = request.POST.get('action')
            if action == 'like':
                recipe.likes.add(user)
            elif action == 'unlike':
                recipe.likes.remove(user)
    
    return redirect('recipe_detail', slug=slug)


def comment_edit_view(request, slug, comment_id):
    """
    View to display the recipe detail page with the comment editing form.
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        messages.error(request, "You can only edit your own comments.")
        return redirect('recipe_detail', slug=slug)

    comment_form = CommentForm(instance=comment)
    
    return render(request, 'blog/recipe_detail.html', {
        'recipe': recipe,
        'editing_comment': comment,
        'comment_form': comment_form,
        'comments': recipe.comments.all(),
    })

def comment_update_view(request, slug, comment_id):
    """
    View to handle the comment update.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        messages.error(request, "You can only update your own comments.")
        return redirect('recipe_detail', slug=slug)

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.approved = False  # Re-approve the comment after edit
            comment.save()
            messages.success(request, "Comment updated and awaiting approval.")
        else:
            messages.error(request, "There was an error updating your comment.")
    
    return redirect('recipe_detail', slug=slug)

# To test the 403 Forbidden error page
# def my_view(request):
#     raise PermissionDenied