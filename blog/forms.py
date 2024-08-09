from django import forms
from .models import Recipe, Comment
from django_summernote.widgets import SummernoteWidget

class NewFlavorsForm(forms.ModelForm):
    """
    NewFlavors Form to create/add new recipes
    """
    class Meta:
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
    class Meta:
        model = Comment
        fields = ('text',)