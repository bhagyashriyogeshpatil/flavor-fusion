# Standard library imports
from django.contrib import admin
# Third-party imports
from django_summernote.admin import SummernoteModelAdmin
# Local application imports
from .models import CuisineType, Recipe, Comment

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    Admin settings for the Recipe model.
    Displays fields in the admin list, allows searching and filtering,
    and uses a rich-text editor for ingredients and instructions.
    """   
    list_display = ('title', 'slug', 'status', 'author', 'created_on')
    search_fields = ['title', 'cuisines_type', 'status']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions', )

# Register your models here.
admin.site.register(CuisineType)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin settings for the Comment model.
    Displays comment details, allows searching and filtering,
    and provides actions to approve or disapprove comments.
    """
    list_display = ('recipe', 'author', 'text', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('author', 'text')
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        """Approve selected comments."""
        queryset.update(approved=True)
        self.message_user(request, "Selected comments have been approved.")

    def disapprove_comments(self, request, queryset):
        """Disapprove selected comments."""
        queryset.update(approved=False)
        self.message_user(request, "Selected comments have been disapproved.")
