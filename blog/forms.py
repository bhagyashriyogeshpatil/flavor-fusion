# Standard library imports
from django import forms
# Third-party imports
from django_summernote.widgets import SummernoteWidget
# Local application imports
from .models import Recipe, Comment

class NewFlavorsForm(forms.ModelForm):
    """
    NewFlavors Form to create/add new recipes
    """
    class Meta:
        """
        Specifies the model and fields used in the form, 
        along with custom widgets and labels.
        """
        model = Recipe
        fields = ['title', 'description', 'featured_image', 'ingredients', 'instructions', 'cuisine_type', 'status', 'prep_time', 'cooking_time', 'servings', ]

        # ref: https://github.com/summernote/django-summernote
        widgets = {
            'ingredients': SummernoteWidget(),
            'instructions': SummernoteWidget(),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a Description of your recipe here'}),
            'prep_time': forms.NumberInput(attrs={'placeholder': 'Specify the Preparation time in minutes'}),
            'cooking_time': forms.NumberInput(attrs={'placeholder': 'Specify the Cooking time in minutes'}),
            'servings': forms.NumberInput(attrs={'placeholder': 'Quantity of servings'}),
            'cuisine_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'featured_image': ' Image',
            'ingredients': 'Recipe Ingredients',
            'instructions': 'Recipe Instructions',
            'cuisines_type': 'Cuisine Type',
            'status': 'Status (Save as a Draft / Publish Now)',
            'prep_time': 'Preparation Time (Time in minutes)',
            'cooking_time': 'Cooking Time (Time in minutes)',
            'servings': 'Servings',
        }

class CommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Comment
        fields = ('text',)