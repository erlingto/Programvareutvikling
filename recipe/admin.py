from django.contrib import admin
from recipe.models import Recipe, RecipeIngredient, RatingRecipe
from ingredient.models import Ingredient


class IngredientInline(admin.TabularInline):
    model=RecipeIngredient
    extra=2
#Admin page to manually add recipes
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ID', {'fields':['id']}),
        ('Navn', {'fields': ['name']}),
        ('Oppskriftstekst', {'fields': ['recipe_text']}),
        ('Publication Date', {'fields': ['pub_date']}),
        ('Vanskelighetsgrad' ,{'fields': ['difficulty']})
    ]
    #Defines the ingredients needed to make the recipe
    inlines = [IngredientInline]

class RatingRecipeAdmin(admin.ModelAdmin): 
    #Admin page to manually add user ratings to a recipe
    fieldsets = [ 
        ('User', {'fields': ['user']}),
        ('Recipe', {'fields': ['recipe']}),
        ('Rating', {'fields' : ['rating']}),
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RatingRecipe, RatingRecipeAdmin)
