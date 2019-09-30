from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer

# Klasse for å behandle API requests
class IngredientView(APIView):

    # Definerer hva som skjer ved en GET-request
    def get(self, request):

        # Hvis ingrediensen finnes henter vi den, hvis ikke sender vi en "404 not found"-error
        ingredient = get_object_or_404(Ingredient, id=request.GET.get('id', False))

        # Kjører serializeren på ingrediensen
        serializer = IngredientSerializer(instance=ingredient)

        # Returnerer dataen pluss en "200 OK"-melding
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Definerer hva som skjer ved en POST-request
    def post(self, request):

        # Validerer data gjennom serializer først
        serializer = IngredientSerializer(data=request.data)

        # Hvis alt er good lagres det og vi får dataene + en "201 CREATED"-melding tilbake
        if serializer.is_valid():
            ingredient = serializer.create(serializer.validated_data)
            ingredient.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Hvis ikke får vi dataene + en "400 BAD REQUEST"-error tilbake
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
