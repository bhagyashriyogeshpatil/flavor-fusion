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
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
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
    
    # Returns all ingredients associated with the recipe
    def ingredients_list(self):
        return self.ingredients.all()

    #  Returns all instructions associated with the recipe
    def instructions_list(self):
        return self.instructions.all()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} {self.name}"

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.step_number}. {self.description}"



