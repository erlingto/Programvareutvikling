from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FloatField, CharField, BooleanField
from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer, ModelSerializer

from ingredient.models import Ingredient

# Serializer validerer og formaterer data
class IngredientSerializer(Serializer):

    # Definerer hva vi forventer å motta
    name = CharField()

    # Lager en instans av Ingredient-modellen med data som har blitt validert
    def create(self, validated_data):
        ingredient = Ingredient(
            name=validated_data["name"]
        )
        return ingredient

    # Validerer data gjennon conditions vi setter selv (her er det ingen)
    def validate(self, data):

        # Ikke spør pls
        data = super(IngredientSerializer, self).validate(data)

        return data

    # Denne greia er egentlig magi, ikke tenk så mye på det