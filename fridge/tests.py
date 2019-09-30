from django.test import TestCase, RequestFactory, Client
from utilities.utilities import populate_db, setup_view, login_client_user, logout_client_user
from django import forms
from fridge.forms import AddNewIngredientTypeForm, UpdateFridgeForm
from fridge.models import Fridge, FridgeIngredient
from ingredient.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from django.contrib.auth.models import User
from django.utils import timezone
from recipe.models import RatingRecipe, Recipe
from recipe.views import RecipeIndexView
# Create your tests here.
class RequestTests(TestCase):

    def test_setUp(self):
        #populates the database
        populate_db()
        #sets the client
        self.client = Client(enforce_csrf_checks=False)
        #logs in the user 'admin' made in populate_db
        login_client_user(self)

    #tests the model instance of fridge made from populate_db() test to ensure model attributes etc behave properly
    def test_model_fridge(self):
        populate_db()
        user = User.objects.get(username = 'admin')
        fridge = user.fridge
        fridge.name = 'Fridgerino'

    #tests the model instance of fridgeingredient made from populate_db() test to ensure model attributes etc behave properly
    def test_model_fridgeIngredient(self):
        populate_db()
        user = User.objects.get(username = 'admin')
        fridge = user.fridge
        ingredient = Ingredient.objects.get(pk = 100)
        fringredient = FridgeIngredient.objects.get(fridge = fridge, ingredient = ingredient)
        self.assertTrue(fringredient.ingredient == ingredient)
        self.assertTrue(fringredient.quantity == 500)
        self.assertTrue(fringredient.fridge == fridge)
    

    def test_addNewIngredient_positive_quantity(self):
        #tests that u can add positive amounts of quantity, checks that form.is_valid() is true for positive values in the quantity field 
        populate_db()
        user = User.objects.get(username = 'admin')
        ingredient = Ingredient.objects.get(pk = 101)
        form_data = {'fridge': user.fridge.pk, 'ingredient': ingredient.pk, 'quantity': 30.0}
        form = AddNewIngredientTypeForm(user, form_data)
        self.assertTrue(form['fridge'].initial == user.fridge)
        self.assertTrue(form.is_valid())

    def test_addNewIngredient_negative_quantity(self):
        #tests that u cant add negative amounts of quantity, checks that form.is_valid() is false for negative values in the quantity field 
        populate_db()
        user = User.objects.get(username = 'admin')
        ingredient = Ingredient.objects.get(pk = 101)
        form_data = {'fridge': user.fridge.pk, 'ingredient': ingredient.pk, 'quantity': -30.0}
        form = AddNewIngredientTypeForm(user, form_data)
        self.assertTrue(form['fridge'].initial == user.fridge)
        self.assertFalse(form.is_valid())

    def test_updateNewIngredient_negative_quantity(self):
        #tests that the form is not valid when you input negative values in the quantity field in fridge
        populate_db()
        user = User.objects.get(username = 'admin')
        fridge = user.fridge
        ingredientis = Ingredient.objects.get(id = 101)
        ingredientkanel = Ingredient.objects.get(id = 100)
        fringredientis = FridgeIngredient(fridge = fridge, ingredient = ingredientis, quantity = 0)
        fringredientkanel = FridgeIngredient.objects.get(ingredient = ingredientkanel)
        form_data = {'fridge': fridge.pk, 'Is': 30.0, 'Kanelstang': -10}
        TestUpdateFridgeForm = UpdateFridgeForm(user, form_data)
        self.assertFalse(TestUpdateFridgeForm.is_valid())

    
    def test_updateNewIngredient_positive_quantity(self):
        #tests that the form is valid when you input positive values in the quantity in fridge
        populate_db()
        user = User.objects.get(username = 'admin')
        fridge = user.fridge
        ingredientis = Ingredient.objects.get(id = 101)
        ingredientkanel = Ingredient.objects.get(id = 100)
        fringredientis = FridgeIngredient(fridge = fridge, ingredient = ingredientis, quantity = 0)
        fringredientkanel = FridgeIngredient.objects.get(ingredient = ingredientkanel)
        form_data = {'fridge': fridge.pk, 'Is': 30.0, 'Kanelstang': 10}
        TestUpdateFridgeForm = UpdateFridgeForm(user, form_data)
        self.assertTrue(TestUpdateFridgeForm.is_valid())

    def test_addNewIngredientTypeForm_submit(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        user = User.objects.get(username = 'admin')
        ingredient = Ingredient.objects.get(pk = 101)
        # Use follow=true since there will be a redirect after processing
        post_data = {
            'fridge': user.fridge.pk,
            'ingredient': ingredient.pk,
            'quantity': 3
        }
        response = self.client.post('/fridge/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        ingredientInFridge = FridgeIngredient.objects.get(fridge = user.fridge, ingredient = ingredient)
        self.assertTrue(ingredientInFridge.quantity == 3)

    def test_UpdateFridgeForm_submit(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self) 
        user = User.objects.get(username = 'admin')
        ingredient = Ingredient.objects.get(pk = 100) #pk = 100 is ingredient "Kanelstang"
        # Use follow=true since there will be a redirect after processing
        post_data = {
            'Kanelstang': 3,
            'fridge': user.fridge.pk
        }
        response = self.client.post('/fridge/1/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        ingredientInFridge = FridgeIngredient.objects.get(fridge = user.fridge, ingredient = ingredient)
        self.assertTrue(ingredientInFridge.quantity == 3)



  
    def test_Recipe_Page(self):
        #checks that the urls give the right page
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        response = self.client.get('/fridge/')
        self.assertContains(response, "Add/remove groceries")

    def test_addNewIngredient_Page(self):
        #checks that the urls give the right page
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        response = self.client.get('/fridge/1/')
        self.assertContains(response, "fridge")


    
        

    