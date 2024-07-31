from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

# Define STATUS_CHOICES
STATUS_CHOICES = (
    (0, "Draft"),
    (1, "Published"),
)

# Create your models here.
# Define the CuisineType model
class CuisineType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Define the Recipe model
class Recipe(models.Model):
    title = models.CharField(unique=True, max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_owner')
    description = models.CharField(max_length=500, null=False, blank=False)
    featured_image = CloudinaryField('image', default='placeholder')
    ingredients = models.TextField(blank=False, default="List ingredients here")
    instructions = models.TextField(blank=False, default="Describe the cooking instructions here")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    prep_time = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(300)], default=15)
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(600)], default=15)
    servings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"




