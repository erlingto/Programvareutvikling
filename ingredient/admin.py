from django.contrib import admin

from ingredient.models import Ingredient

# Registrerer Ingrediens-modellen i admin-panelet
admin.site.register(Ingredient)