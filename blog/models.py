# Standard Library Imports
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
# Third-Party Imports
from cloudinary.models import CloudinaryField

# Define STATUS_CHOICES
STATUS_CHOICES = (
    (0, "Draft"),
    (1, "Published"),
)

# Create your models here.


class CuisineType(models.Model):
    """
    Represents a type of cuisine.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Represents a cooking recipe created by a user.
    This model stores key details about a recipe, such as its title,
    description, ingredients, and instructions.
    It is linked to the following models:
    - :model:`auth.User`: The user who created the recipe
    and users who like the recipe.
    - :model:`CuisineType`: The type of cuisine the recipe belongs to.
    """
    title = models.CharField(unique=True, max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe_owner')
    description = models.CharField(max_length=500, null=False, blank=False)
    featured_image = CloudinaryField('image', default='placeholder')
    ingredients = models.TextField(blank=False,
                                   default="List ingredients here")
    instructions = models.TextField(
        blank=False,
        default="Describe the cooking instructions here")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    prep_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)],
        default=15)
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)],
        default=15)
    servings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)])
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,
                                   related_name='liked_recipes', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate
        a slug from the title. The slug is generated using the
        slugify function, which converts the title into a URL-friendly
        format. The method then calls the parent's save method
        to save the object to the database.
        """
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def get_likes_count(self):
        return self.likes.count()


class Comment(models.Model):
    """
    Stores a single comment entry related to :model:`auth.User`
    and :model:`Recipe`.
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name='comments',
        on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment by {self.author} on {self.recipe}"

    def approve(self):
        self.approved = True
        self.save()
