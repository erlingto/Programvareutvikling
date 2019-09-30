from django.shortcuts import get_object_or_404, render
from recipe.models import Recipe, RecipeIngredient, RatingRecipe
from recipe.forms import RatingRecipeForm
from ingredient.models import Ingredient
from fridge.models import FridgeIngredient, Fridge
from django.views import generic
from django.utils import timezone
from django.template import Context
from django.views.generic.edit import FormView, UpdateView
from recipe.forms import RecipeForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Avg
# Create your views here.
    
class RatingRecipeView(generic.FormView): 
    template_name = 'recipe/rating.html'
    form_class = RatingRecipeForm


    

#View for showing the recipe, made as a form to allow the user to rate the recipe
class RecipeIndexView(LoginRequiredMixin, generic.FormView):
    # Connected to the "LoginRequiredMixin, which redirects a user if not logged in
    login_url = '/login/'
    template_name = 'recipe/recipe.html'
    form_class = RatingRecipeForm

    def get_form_kwargs(self): 
        kwargs = super(RecipeIndexView,self).get_form_kwargs() 
        kwargs.update({'user' : self.request.user})
        kwargs.update(self.kwargs)
        return kwargs

#Gets the information the recipe needs acess to
    def get_context_data(self, **kwargs):
        context = super(RecipeIndexView, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()
        #takes in the whole recipeingredient table, the html page does the sorting based on which recipe is viewed
        context['recipeingredients'] = RecipeIngredient.objects.all()
        context['recipe'] = Recipe.objects.get(pk = self.kwargs['pk'])
        recipe = Recipe.objects.get(pk = self.kwargs['pk'])

        #calculates the average of the ratings on the recipes
        RecipeRating = None
        RecipeRating = RatingRecipe.objects.filter(recipe = recipe)
        if RecipeRating:
            avg=0
            teller = 0
            for i in RecipeRating:
                avg += i.rating
                teller += 1
            avg = avg/teller
            context['rating'] = avg
        else:
            context['rating'] = "No Rating"
        return context

    def form_valid(self, form_class):
        f = None
        #checks if the user has rated the recipe before if it has it 
        try:    
            f = RatingRecipe.objects.get(user=form_class.cleaned_data['user'], recipe=form_class.cleaned_data['recipe'])
            f.rating = form_class.cleaned_data['rating']
            f.save()     
        except RatingRecipe.DoesNotExist:
            form_class.save()
        return HttpResponseRedirect('/recipe/show_all_recipes/')

        
    #Make Recipe button that removes the ingredients in the recipe from the fridge
    def make_recipe(self, pk):
        user = self.user
        fridgeingredient = FridgeIngredient.objects.filter(fridge = user.fridge)
        recipe = Recipe.objects.get(id = pk)
        recipeingredients = RecipeIngredient.objects.filter(recipe = recipe)
        for z in recipeingredients:
            for i in fridgeingredient:
                if i.ingredient == z.ingredient:
                    i.quantity -= z.quantity
                    if i.quantity < 0: 
                        i.quantity = 0
                    i.save()
        return redirect('/fridge/1/')

class RecipeListView(LoginRequiredMixin, generic.ListView):
    # Connected to the "LoginRequiredMixin, which redirects a user if not logged in
    login_url = '/login/'
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'latest_recipe_list'
    
    def get_queryset(self):
        user = self.request.user
        #creates a list of ids that will contain the ids of the recipes the user can make
        list_of_ids =[]
        Recipes = Recipe.objects.all()
        RecipeIngredients = RecipeIngredient.objects.all() 
        FridgeIngredients = FridgeIngredient.objects.filter(fridge = user.fridge)
        #iterate through all the recipes
        for x in Recipes:
            #variable to keep track of how many ingredients in the recipe the user has got in his fridge "canMake"
            okIngredient = 0
            RecipeIngredients = RecipeIngredient.objects.filter(recipe = x)
        #iterate through all the ingredients in the recipe
            for y in RecipeIngredients:
                #variable that keeps track of whether or not all the ingredient in the recipe has been checked or not
                checked = 0
                for z in FridgeIngredients:
                    #Går gjennom alle ingredienser i kjøleskapet
                    if y.ingredient == z.ingredient:
                    #checks if the ingredient type exists in the fridge
                        checked = 1
                        if  y.quantity <= z.quantity:
                            #checks if the user has enough of said ingredient to make the recipe
                            okIngredient += 1
                        else:   
                            pass
                #if everything is okay the id of the recipe gets added to the list of id    
                if checked == 0:
                    okIngredient = 0
            if okIngredient == RecipeIngredients.count():
                list_of_ids.append(x.id)
                #the function returns a filtering of the recipe objects table based on the ids contained in the list of ids
        return Recipe.objects.filter(id__in=list_of_ids)

    

#view for the Recipeform that we didnt finish
class RecipeFormView(FormView):
    template_name = 'recipe/add_recipe.html'
    form_class = RecipeForm
    buttonclick = 0

    def button_click(self, request, buttonclick):
        buttonclick +=1
        return buttonclick
        

    def form_valid(self, form_class):
        form_class.save()
        return HttpResponseRedirect('/homepage/')


#simple view to show all recipes in the database
class AllRecipeListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'recipe/recipe_list_all.html'
    context_object_name = 'latest_recipe_list'
    queryset = Recipe.objects.all()
