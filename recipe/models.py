from django.db import models
from ingredient.models import Ingredient
from django.contrib.auth.models import User

#the recipe model, that includes the name, publication date, the recipe text and the difficulty of the recipe
class Recipe(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    recipe_text = models.TextField(max_length=None)
    difficulty = models.PositiveIntegerField(default= 0)
    pub_date = models.DateTimeField() 

    #to_str
    def __str__(self):
        return self.name

# Model that describes the ingredients in a recipe. Connects an ingredient with a recipe combined with the quantity
class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe  = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)


# Model to store user ratings of recipes
class RatingRecipe(models.Model): 
    CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]

    class Meta:
        # a user can only rate a recipe once
        unique_together = ['user', 'recipe']

    rating = models.IntegerField(choices=CHOICES, default=1)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
