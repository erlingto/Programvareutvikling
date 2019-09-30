from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from fridge.models import Fridge
from django.db.models.signals import post_save

# Create your views here.
"""
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    response = HttpResponse("Logged in")
    return response

def register(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username, email, password)
    user.save()
"""