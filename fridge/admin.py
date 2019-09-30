from django.contrib import admin
from fridge.models import Fridge, FridgeIngredient
from ingredient.models import Ingredient
from django.contrib.auth.models import User
#sets up the django admin page for editing the models
class IngredientInline(admin.TabularInline):
    model=FridgeIngredient
    extra=1
    
class FridgeAdmin(admin.ModelAdmin):
    #creates FridgeIngredient objects connected to the chosen fridge in admin
    inlines = [IngredientInline]

# Register your models here.
admin.site.register(Fridge, FridgeAdmin)