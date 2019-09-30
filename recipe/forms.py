from django import forms
from recipe.models import Recipe, RecipeIngredient
import datetime
from django.forms.formsets import BaseFormSet
from ingredient.models import Ingredient
from dal import autocomplete
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
from django.forms.formsets import BaseFormSet
from dal import autocomplete
from django.shortcuts import render
from django.contrib.auth.models import User
from recipe.models import RatingRecipe, Recipe
from django.utils.timezone import now

class RatingRecipeForm(forms.Form):
    #form for rating recipes 
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    rating = forms.ChoiceField()
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(), widget=forms.HiddenInput())
    #overriding initial to set the values of recipe to the recipe that is viewed and the user to the user viewing
    def __init__(self, user, pk=None, *args, **kwargs):
        super(RatingRecipeForm, self).__init__(*args, **kwargs)
        self.initial['user'] = user
        self.initial['recipe'] = Recipe.objects.get(id=pk)
        #Defines the choice values of rating
        CHOICES = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5)
        ]
        #checks if the user already has rated this recipe and sets the initial value of the rating field to the users previous rating. The initial value Is 1 otherwise
        self.fields['rating'] = forms.ChoiceField(label='Rating', widget=forms.Select, choices=CHOICES)
        try:
            r = RatingRecipe.objects.get(user = user, recipe = Recipe.objects.get(id=pk))
            self.initial['rating']= r.rating
        except RatingRecipe.DoesNotExist:
            pass

    def save(self):
            data = self.cleaned_data
            rating = RatingRecipe(user=data['user'], recipe=data['recipe'], rating=data['rating'])
            return rating.save()

#The work we did on the recipe form that would allow chefs to submit their own recipes

class RecipeForm(forms.Form):

    name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                #'placeholder':'give a title for the recipe',
                'autocomplete':'off',
                'class':'add-recipe-box'
            }
        )
    )
    # kan styles som vi ønsker
    recipe_text = forms.CharField(
        widget = forms.Textarea(
            attrs={
                #'placeholder':'give a detailed description of how to make the recipe',
                'autocomplete':'off', 
                'class':'add-recipe-longbox'
            }
        )
    )

    pub_date = forms.DateTimeField()
    
    difficulty = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                #'placeholder':'set the difficulty of the recipe (1-5)',
                'autocomplete':'off'
            }
        )
    )
    ingredient_1 = forms.ModelChoiceField(queryset = Ingredient.objects.all(), widget=autocomplete.ModelSelect2(
        url='fridge:ingredientautocomplete',attrs={'class' : 'ingredient'}))
    quantity_1 = forms.DecimalField()
    """
    ingredient_3 = forms.ModelChoiceField(queryset = Ingredient.objects.all(), widget=autocomplete.ModelSelect2(
        url='fridge:ingredientautocomplete',attrs={'class' : 'ingredient'}))
    quantity_3 = forms.DecimalField()
    ingredient_4 = forms.ModelChoiceField(queryset = Ingredient.objects.all(), widget=autocomplete.ModelSelect2(
        url='fridge:ingredientautocom
        plete',attrs={'class' : 'ingredient'}))
    quantity_4 = forms.DecimalField()
    """

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.initial['pub_date'] = timezone.now     

    def save(self):
        data = self.cleaned_data
        recipe = Recipe(
            id = Recipe.objects.latest('id').id + 1,
            name = data['name'], recipe_text = data['recipe_text'],
            pub_date = data['pub_date'], difficulty = data['difficulty'])
        recipe.save()
        recipeIngredient_1 = RecipeIngredient(recipe = recipe, ingredient = data['ingredient_1'],
        quantity = data['quantity_1']
        )
        
        #recipeIngredient_3 = RecipeIngredient(recipe = recipe, ingredient = data['ingredient_3'],
        #quantity = data['quantity_3']
        #)
        
        recipeIngredient_1.save()
        #recipeIngredient_3.save()
    
    def clean(self):
        ingredients = set()
        i = 1
        field_name = 'ingredient_%s' % (i,)
        while self.cleaned_data.get(field_name):
           ingredient = self.cleaned_data[field_name]
           if ingredient in ingredients:
               self.add_error(field_name, 'Duplicate')
           else:
               ingredients.add(ingredient)

           i += 1
           field_name = 'ingredient_%s' % (i,)
        self.cleaned_data['ingredients'] = ingredients




    

