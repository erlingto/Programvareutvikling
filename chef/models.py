from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#Model (or a table) to represent applications to become a chef containing a text and a relation to the user applying.
class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="application", blank=False, null=False)
    text = models.CharField(max_length=1000)

    class Meta:
        ordering = ["-user"]

    #__str__(self) functions should represent the current instance as a string    
    def __str__(self):
        string = "Application from "+self.user.username
        return string

