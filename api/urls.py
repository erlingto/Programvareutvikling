from django.urls import path, include

from ingredient.views import IngredientView
from chef.views import ApplicationView, AppResponseView, ApplicationFormView


app_name = "api"

# Definerer urls
urlpatterns = [

    # Sier at api/ingredient svarer med IngredientView-filen vi har
    path("ingredient/", IngredientView.as_view(), name="ingredient"),
    path("application/", ApplicationView.as_view(), name="rest_application"),
    path("appresponse/", AppResponseView.as_view(), name="appresponse"),
]