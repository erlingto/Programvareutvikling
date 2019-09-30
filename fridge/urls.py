from django.urls import re_path, path
from fridge.views import IngredientAutoComplete, AddNewIngredientTypeFormView, FridgeView
from django.views.generic import TemplateView


app_name = "fridge"
#The url paths
urlpatterns = [
    path("ingredient-autocomplete/", IngredientAutoComplete.as_view(), name='ingredientautocomplete'), 
    path("", AddNewIngredientTypeFormView.as_view(), name = 'fridgeformview'),
    path("<int:pk>/", FridgeView.as_view(), name = 'fridgelist'), 
    path('added_in_fridge/', TemplateView.as_view(template_name="fridge/added_in_fridge.html"), name="add_ingredients")
]            