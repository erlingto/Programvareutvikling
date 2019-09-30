from django.db import models


#Ingredient type model. Examples: Banana, sugar, apple, everything that goes in the fridge is regarded as an ingredient
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    KILOGRAM = 'kg'
    LITRE = 'l'
    PIECE = 'pc'

    AMOUNT_TYPE = (
        (PIECE, 'pc'),
        (LITRE, 'l'),
        (KILOGRAM, 'kg')
    )

    typething = models.TextField(max_length = 3, choices = AMOUNT_TYPE)
     

    #to_string function
    def __str__(self):
        return "%s" % self.name
