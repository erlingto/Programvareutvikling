# Create your models here.
from django.db import models
from django.urls import reverse
from ingredient.models import Ingredient
from django.contrib.auth.models import User

#The fridge has a user instance and a name. 
#We made this model as we had intentions to let the user have multiple fridges,
#but at the moment this model is redundant and we could just connect the ingredients directly to a user instead of fridge in the FridgeIngredient model 
class Fridge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fridge")
    name = models.CharField(max_length=20, default="fridge")

    def __str__(self):
        return self.name+" property of "+self.user.username

#The ingredients in the fridge, connects the type of ingredient to a quantity and a users fridge.
class FridgeIngredient(models.Model):
    
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default = 0)
    def get_quantity(self):
        return self.quantity
    def get_ingredient(self):
        return self.ingredient

    
