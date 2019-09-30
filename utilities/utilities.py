from django.utils import timezone
from django.contrib.auth.models import User
from fridge.models import Fridge, FridgeIngredient
from ingredient.models import Ingredient
from recipe.models import Recipe, RatingRecipe, RecipeIngredient

def populate_db():
    """
    Adds records to an empty test database
    """
    # Add user
    user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='secret666')

    # Add ingredient
    kanelstang = Ingredient.objects.create(
        id = 100,
        name='Kanelstang',
        typething='pc'
    )

    Is = Ingredient.objects.create(
        id = 101,
        name ='is',
        typething='pc'
    )

    # Add fridge
    fridge = Fridge.objects.create(
        user=user,
        name='Fridgerino')

    # Add ingredient to fridge
    fringredient = FridgeIngredient.objects.create(
        fridge=fridge,
        ingredient=kanelstang,
        quantity= 500
    )

    # Add recipe
    recipe = Recipe.objects.create(
        id=1,
        name='Kanelstang og vann',
        recipe_text='Hell vann over stang og nyt',
        difficulty=1,
        pub_date=timezone.now()
    )

    # Add ingredient to recipe
    recingredient = RecipeIngredient.objects.create(
        ingredient=kanelstang,
        recipe=recipe,
        quantity=1
    )

    # Rates a recipe
    rating = RatingRecipe.objects.create(
        rating=5,
        recipe=recipe,
        user=user
    )


def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

def login_client_user(self):
    self.client.login(username='admin', password='secret666')
    return self

def logout_client_user(self):
    self.client.logout()
    return self


# more common functionality below

