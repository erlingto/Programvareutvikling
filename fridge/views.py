from django.shortcuts import render
from dal import autocomplete
from fridge.models import Fridge, FridgeIngredient
from ingredient.models import Ingredient
from django.views.generic.edit import FormView, UpdateView
from fridge.forms import AddNewIngredientTypeForm, UpdateFridgeForm
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.db import transaction
from django.views import generic
from django.urls import reverse
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
 
#defines the autocomplete function of the ingredient type field.
class IngredientAutoComplete(autocomplete.Select2QuerySetView): 
    def  get_queryset(self):
        if not self.request.user.is_authenticated:
            return Ingredient.objects.none()    
        qs = Ingredient.objects.all()
        #filters the list based on the input in the field
        if self.q: 
            qs = qs.filter(name__istartswith=self.q)
        return qs

#The view that runs the add more ingredients Form.
class AddNewIngredientTypeFormView(LoginRequiredMixin, FormView):
    # Connected to the "LoginRequiredMixin, which redirects a user if not logged in
    login_url = '/login/'
    #the html page the form will be displayed on
    template_name = 'fridge/addToFridge.html'
    #the form displayed
    form_class = AddNewIngredientTypeForm

    #override the get_context_data to include additional information the form needs
    def get_context_data(self, **kwargs):
        context = super(AddNewIngredientTypeFormView, self).get_context_data(**kwargs)
        #the form needs to know which fridge belongs to the user
        context['fridge'] = self.request.user.fridge
        #the ingredients the user can add to his fridge 
        context['ingredients'] = Ingredient.objects.all()
        #what ingredients is already in the fridge
        context['fridgeingredients'] = FridgeIngredient.objects.filter(fridge = self.request.user.fridge)
        return context

    #updates the keyword arguments to contain the user
    def get_form_kwargs(self):
        kwargs = super(AddNewIngredientTypeFormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    #checks the input information from the user and handles it accordingly
    def form_valid(self, form_class):
        f=None
         #if the user adds an ingredient type thats already in the fridge, the input quantity is added ontop     
        try:    
            f = FridgeIngredient.objects.get(fridge=form_class.cleaned_data['fridge'], ingredient = form_class.cleaned_data['ingredient'])
            f.quantity += form_class.cleaned_data['quantity']
            f.save()
        #if the user adds an ingredient type thats not in the fridge already a new FridgeIngredient object is created
        except FridgeIngredient.DoesNotExist:
            form_class.save()
            pass
        
        return HttpResponseRedirect('/fridge/1/')

#the view that runs the UpdateFridgeForm, this is the form that lets the user see what is in his fridge aswell as update the quantity of his ingredients
class FridgeView(LoginRequiredMixin, generic.FormView):
    # Connected to the "LoginRequiredMixin, which redirects a user if not logged in
    login_url = '/login/'
    template_name = 'fridge/fridge.html'
    form_class = UpdateFridgeForm

    #override the get_context_data to include additional information the form needs 
    def get_context_data(self, **kwargs):
        context = super(FridgeView, self).get_context_data(**kwargs)
        #what fridge belongs to the user
        context['fridge'] = self.request.user.fridge
        #the ingredient models
        context['ingredients'] = Ingredient.objects.all()
        #what fridgeingredients is already connected to the fridge
        context['fridgeingredients'] = FridgeIngredient.objects.filter(fridge = self.request.user.fridge)     
        return context
    
    #override the get_form_kwargs to update the keyword arguments to include the user
    def get_form_kwargs(self):
        kwargs = super(FridgeView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    #saves every field in the fridge and updates the FridgeIngredient-objects quantity 
    def form_valid(self, form_class):
        fridgeingredients = FridgeIngredient.objects.filter(fridge = self.request.user.fridge)
        for i in fridgeingredients:
            f = FridgeIngredient.objects.get(fridge=self.request.user.fridge, ingredient = i.ingredient)
            f.quantity = form_class.cleaned_data[i.ingredient.name]
            f.save()
        return HttpResponseRedirect('/homepage/')





@receiver(user_signed_up)
def createNewFridge(request, user, **kwargs):
    Fridge.objects.create(user=user)    

