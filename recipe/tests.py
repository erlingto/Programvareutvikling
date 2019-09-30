from django.test import TestCase, RequestFactory, Client
from utilities.utilities import populate_db, setup_view, login_client_user, logout_client_user
from django import forms
from fridge.models import Fridge, FridgeIngredient
from ingredient.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from django.contrib.auth.models import User
from django.utils import timezone
from recipe.models import RatingRecipe, Recipe
from recipe.views import RecipeIndexView
# Create your tests here.
class RequestTests(TestCase):

    #test that the setup functions runs
    def test_setUp(self):
        #populates the database
        populate_db()
        #sets the client
        self.client = Client(enforce_csrf_checks=False)
        #logs in the user 'admin' made in populate_db
        login_client_user(self)
    
    #checks that the model is created as it should from populates_test_db()
    def test_model_recipe(self):
        populate_db()
        recipe = Recipe.objects.get(pk = 1)
        self.assertTrue(recipe.name == 'Kanelstang og vann')
        self.assertTrue(recipe.recipe_text == 'Hell vann over stang og nyt')
        self.assertTrue(recipe.difficulty == 1)

    #checks that the model is created as it should from populates_test_db()
    def test_model_ingredient(self):
        populate_db()
        ingredient = Ingredient.objects.get(pk = 100)
        self.assertTrue(ingredient.name == 'Kanelstang')
        self.assertTrue(ingredient.typething == 'pc')
        self.assertTrue(ingredient.id == 100)

    #checks that the model is created as it should from populates_test_db()
    def test_model_RecipeIngredient(self):
        populate_db()
        recipe = Recipe.objects.get(pk = 1)
        ingredient = Ingredient.objects.get(pk = 100)
        recingredient  = RecipeIngredient.objects.get(recipe = recipe, ingredient = ingredient)
        self.assertTrue(recingredient.recipe == recipe)
        self.assertTrue(recingredient.quantity == 1)
        self.assertTrue(recingredient.ingredient == ingredient)
    
    #checks that the recipe page shows the corresponding recipe to the pk given in url
    def test_Recipe_Page(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        response = self.client.get('/recipe/1/')
        self.assertContains(response, "Kanelstang og vann")

    #test to check if the page where all the recipes are listed really shows all the recipes
    def test_Recipe_List_all(self):
        #populate_db() creates a recipe the user admin can make as he has the ingredients needed in his fridge
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        #creates an ingredient that will not be added to the users fridge
        ingredientNotHave = Ingredient.objects.get(id = 101)
        #creates a recipe the user will not be able to make
        recipeCantMake = Recipe.objects.create(
            id = 10,
            name = "recipeCantMake",
            recipe_text = 'lag iskrem', 
            difficulty = 4, 
            pub_date = timezone.now()
        )
        #connects the ingredient to the recipe through recipeingredient
        ringredient = RecipeIngredient.objects.create(ingredient = ingredientNotHave, recipe = recipeCantMake, quantity = 3)
        response = self.client.get('/recipe/show_all_recipes/')
        #check that the recipe we can make is in the list
        self.assertContains(response, "Kanelstang og vann")
        #check that the recipe we cant make is still in the list, as this list shows all recipes in the database
        self.assertTrue('recipeCantMake' in response.rendered_content)


    #tests that the page where the sorted recipes are listed only shows the recipes the user can make
    def test_Recipe_List_sorted(self):
        #populate_db() creates a recipe the user admin can make as he has the ingredients needed in his fridge
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        #creates an ingredient that will not be added to the users fridge
        ingredientNotHave = Ingredient.objects.get(id = 101)
        #creates a recipe the user will not be able to make
        recipeCantMake = Recipe.objects.create(
            id = 10,
            name = "recipeCantMake",
            recipe_text = 'lag iskrem', 
            difficulty = 4, 
            pub_date = timezone.now()
        )
        #connects the ingredient to the recipe through recipeingredient
        ringredient = RecipeIngredient.objects.create(ingredient = ingredientNotHave, recipe = recipeCantMake, quantity = 3)
        response = self.client.get('/recipe/')
        #checks that the recipe we can make is in the list
        self.assertContains(response, "Kanelstang og vann")
        #checsk that the recipe is not in the list
        self.assertFalse('recipeCantMake' in response.rendered_content) 

    #tests that the page where the sorted recipes are listed only shows the recipes the user can make
    def test_makeRecipeButton(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        #logs in the user 'admin'
        login_client_user(self)
        ingredient = Ingredient.objects.get(pk = 101)
        user = User.objects.get(username = 'admin')
        #creates a fridgeingredient object that we will check the value of after we run the makeRecipe view
        fingredient = FridgeIngredient.objects.create(ingredient = ingredient, fridge = Fridge.objects.get(user = user), quantity = 2)
        #Creates a recipe that we will 'make'
        Tricolor = Recipe.objects.create(
            id = 10,
            recipe_text = 'lag iskrem', 
            difficulty = 4, 
            pub_date = timezone.now()
        )
        #creates a recipeingredient object connected to the recipe. The quantity of this will be removed from the fridge
        ringredient = RecipeIngredient.objects.create(ingredient = ingredient, recipe = Tricolor, quantity = 3)
        #runs the view
        response = self.client.post('/recipe/10/remove-ingredients-from-fridge/')
        #queries for the fridgeingredient we made earlier
        checkfridgeingredient =  FridgeIngredient.objects.get(fridge = user.fridge, ingredient = ingredient)
        #checks the value   
        #as the quantity of fridgeingredient < recipeingredient the fridgeingredient quantity should be set to 0 as our function should not give negative quantities
        self.assertTrue(checkfridgeingredient.quantity == 0)
    
    