#Form Fridge
from django import forms
from django.forms.formsets import BaseFormSet
from fridge.models import Fridge, FridgeIngredient
from dal import autocomplete
from ingredient.models import Ingredient
from django.shortcuts import render
from django.contrib.auth.models import User

#Form for adding a new type of ingredient to the users fridge.
class AddNewIngredientTypeForm(forms.Form):
    #Field that decides which fridge the ingredient is inserted to. Is hidden as this field will be set to the users fridge. 
    fridge = forms.ModelChoiceField(queryset = Fridge.objects.all(), widget=forms.HiddenInput())

    # Field that decides which new type of ingredient will be inserted. Choices is all ingredients in the matega database, has an autocomplete function connected.
    ingredient = forms.ModelChoiceField(queryset = Ingredient.objects.all(), widget=autocomplete.ModelSelect2(
        url='fridge:ingredientautocomplete',attrs={'class' : 'ingredient'}))

    #the number of ingredients of this type added.
    quantity = forms.FloatField(min_value = 0.0, widget=forms.NumberInput(attrs={'class' : 'ingredient'}))
    #overriding the initialize function to set the fridge to the current users fridge.
    def __init__(self, user, *args, **kwargs):
        super(AddNewIngredientTypeForm, self).__init__( *args, **kwargs)
        self.initial['fridge'] = user.fridge
       
    #creates a FridgeIngredient object based on the information from the form.
    def save(self):
        data = self.cleaned_data
        fridge = FridgeIngredient(fridge = data['fridge'], ingredient = data['ingredient'], quantity = data['quantity'])
        return fridge.save()
    

#A fridge that the user can acess and see whats stored there. Made as a form so that the user can manually update the quantity of his ingredients should he choose too.
class UpdateFridgeForm(forms.Form):
    #initializes the form and creates a field for every ingredient type in the users fridge.
    def __init__(self, user, *args, **kwargs):
        super(UpdateFridgeForm, self).__init__( *args, **kwargs)
        self.initial['fridge'] = user.fridge
        fridgeingredients = FridgeIngredient.objects.filter(fridge = user.fridge)
        y = 0
        for i in fridgeingredients:
            y= i.ingredient.name
            #the field contains the quantity of the ingrediant type and the name of the field is set to the ingredienttypes name.  
            self.fields['%s' %y] = forms.FloatField(min_value = 0.0, widget=forms.NumberInput(attrs={'class' : 'ingredient'}), initial = i.quantity)