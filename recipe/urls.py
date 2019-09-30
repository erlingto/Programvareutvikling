from django.urls import re_path, path
from recipe.views import RecipeIndexView, RecipeListView, AllRecipeListView, RatingRecipeView, RecipeFormView
from django.views.generic import TemplateView


app_name = "recipe"
# Defines the url paths related to the recipe app
urlpatterns = [

    path('', RecipeListView.as_view(), name="recipe_list"),
    path('add_recipe/', RecipeFormView.as_view(), name = 'add_recipe'),
    path("<int:pk>/", RecipeIndexView.as_view(), name="recipe"),
    path('<int:pk>/remove-ingredients-from-fridge/', RecipeIndexView.make_recipe, name='make_recipe'),
    path('show_all_recipes/', AllRecipeListView.as_view(), name ='show_all_recipes'),    
    path('<int:pk>/rating/', RatingRecipeView.as_view(), name = "rating"),
    path('count_clicks/', RecipeFormView.button_click, name='buttonclick')
]
