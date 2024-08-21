# Standard Library Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.db.models import Q
# Third-Party Imports
from django.views.generic import (
    TemplateView, CreateView, ListView, DeleteView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Local Application Imports
from .models import Recipe, Comment
from .forms import NewFlavorsForm, CommentForm

# Create your views here.


class Index(TemplateView):
    """
    Displays the index page of the blog.
    """
    template_name = "blog/index.html"


class RecipesList(ListView):
    """
    Displays a paginated list of recipes with optional search filtering.

    **Context**
    ``recipes_list``
        List of recipes, filtered by search query if provided.
    ``no_results``
        Indicates if no recipes were found for the search query
        (only if a query is used).
    ``search_query``
        The search query used, included if no results are found.

    **Template:**
    :template:`blog/recipes.html`
    """
    template_name = "blog/recipes.html"
    model = Recipe
    context_object_name = "recipes_list"
    paginate_by = 6

    def get_queryset(self):
        """
        Returns a list of recipes, filtered by a search query if provided.

         If a search query is given, it filters recipes by title,
        description, cuisine type, and author, and orders them by
        creation date. If no query is provided, it returns all recipes.

        **Returns**
        QuerySet: A queryset of Recipe objects.
        """
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
        """
        Adds extra context for the template, including search results info.

        **Context**
        Adds `no_results` if no recipes matched the search query and
        `search_query` with the query used.

        **Returns**
        dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        if query and not context['recipes_list']:
            context['no_results'] = True
            context['search_query'] = query
        return context


class NewFlavors(LoginRequiredMixin, CreateView):
    """
    Allows logged-in users to add a new recipe.

    **Context**
    ``form``
        The form for creating a new recipe.

    **Template:**
    :template:`blog/new_flavors.html`

    **Success URL:**
    Redirects to ``/recipes/`` upon successful submission.
    """
    template_name = "blog/new_flavors.html"
    model = Recipe
    form_class = NewFlavorsForm
    success_url = "/recipes/"

    def form_valid(self, form):
        """
        Sets the current user as the author and shows a success message.
        """
        form.instance.author = self.request.user
        msg = "Your recipe has been posted successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(NewFlavors, self).form_valid(form)


def recipe_detail(request, slug):
    """
    Function-based view to render recipe in detail.
    Shows details of a recipe and handles comment submissions.

    **Context**
    ``recipe``
        The recipe being displayed.
    ``comments``
        Comments for the recipe.
    ``comment_form``
        Form to submit a new comment.

    **Template:**
    :template:`blog/recipe_detail.html`

    **Error Template:**
    :template:`403.html`
    (if the recipe is a draft and the user is not authorized)
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    comments = recipe.comments.all()

    # Check if the recipe is a draft (status = 0)
    if recipe.status == 0:
        # Allow access only to the author or an admin
        if request.user != recipe.author and not request.user.is_staff:
            context = {
                # Pass this context variable to the 403 template
                'draft_recipe': True,
                'recipe_title': recipe.title
            }
            return render(request, '403.html', context)

    # Handle the POST request for comments
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
                messages.success(
                    request,
                    "Your comment has been submitted and is awaiting approval."
                    )
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
    """
    Deletes a recipe that belongs to the logged-in user.

    **Template:**
    :template:blog/confirm_delete.html

    **Success URL:**
    Redirects to the recipes list page after deletion.
    """
    model = Recipe
    success_url = reverse_lazy('recipes')

    def test_func(self):
        """
        Checks if the user is the recipe's author.
        """
        return self.request.user == self.get_object().author

    def form_valid(self, request, *args, **kwargs):
        """
        Shows a success message and deletes the recipe.
        """
        msg = "Your recipe has been deleted successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().delete(request, *args, **kwargs)


class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows a logged-in user to edit their own recipe.

    **Context**
    ``form``
        The form used to edit the recipe.

    **Template:**
    :template:`blog/edit_recipe.html`

    **Success URL:**
    Redirects to the recipes list page after updating.
    """
    model = Recipe
    form_class = NewFlavorsForm
    template_name = "blog/edit_recipe.html"
    success_url = reverse_lazy('recipes')

    def test_func(self):
        """
        Checks if the user is the recipe's author.
        """
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        """
        Updates the recipe with the current user and shows a success message.
        """
        form.instance.author = self.request.user
        msg = "Your recipe has been updated successfully."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


def like_recipe(request, slug):
    """
    Allows users to like or unlike a recipe.

    **Template:**
    Redirects to the recipe detail page after the action is performed.

    **Details:**
    - Authenticated users can like or unlike a recipe via POST request.
    - `action` parameter determines whether to add or remove the like.
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
    Displays the recipe detail page with a form to edit a comment.

    **Context**

    ``recipe``
        The recipe being viewed.

    ``editing_comment``
        The comment being edited.

    ``comment_form``
        Form for editing the comment.

    ``comments``
        List of all comments for the recipe.

    **Template:**
    :template:`blog/recipe_detail.html`
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

    **Template:**
    Redirects to the recipe detail page after the comment is updated.

    **Details:**
    - Only the comment author can update the comment.
    - On successful update, the comment is set to pending approval.
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
            messages.error(
                request,
                "There was an error updating your comment.")
    return redirect('recipe_detail', slug=slug)


def comment_delete_view(request, slug, comment_id):
    """
    View to handle the comment deletion.

    **Template:**
    Redirects to the recipe detail page after the comment is updated.

    **Details:**
    - Only the comment author can delete the comment.
    - The comment is deleted on POST request.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect('recipe_detail', slug=slug)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    return redirect('recipe_detail', slug=slug)

# To test the 500 Internal Server Error page
def trigger_500_error(request):
    raise Exception("This is a simulated 500 error.")
