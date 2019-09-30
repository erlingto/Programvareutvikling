from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FloatField, CharField, BooleanField
from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer, ModelSerializer

from recipe.models import Recipe

# Serializer validates and formats data
class RecipeSerializer(Serializer):

    # Defines what we expect to receive of data
    id = IntegerField()
    name = CharField()

    # Makes an instance of the recipe model with the data thats been validated
    def create(self, validated_data):
        recipe = Recipe(
            id=validated_data["id"],
            name=validated_data["name"]
        )
        return recipe

    # can override this function to set our own requirements for the data, as of now theres none
    def validate(self, data):

        data = super(RecipeSerializer, self).validate(data)

        return data