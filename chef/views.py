from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth.models import Group
from django.views.generic import DetailView, FormView, ListView, View
from django.contrib.auth.context_processors import auth
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from chef.serializers import ApplicationSerializer
from chef.models import Application
from chef.forms import ApplicationForm


# TODO: make secure
class ApplicationView(APIView):

    # Defines reeponse to a GET request
    def get(self, request):

        # Get the application for the user who initiated the request
        data = get_object_or_404(Application, user=request.user)
        serializer = ApplicationSerializer(instance=data)
        # Returns the formatted data
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Defines reponse to a POST request
    def post(self, request):

        # Gets ID from form and connects it to a user
        userid = request.data["user"]
        user = get_object_or_404(User, id=userid)

        # Checks if the user has an application already, and deletes it if so
        a = Application.objects.filter(user=user)
        if a.exists():
            a.delete()

        # Runs it through the serializer
        serializer = ApplicationSerializer(data=request.data)

        # Creates and saves the application object and connects it to the retrieved user
        if serializer.is_valid():
            application = serializer.create(serializer.validated_data)
            application.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Error handler
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deletes the application
    def delete(self, request):

        # Gets ID from form and connects it to a user
        userid = request.data["user"]
        user = get_object_or_404(User, id=userid)

        # If everything is ok, the apllication is deleted and we get an "200 ok" message back
        if (request.user == user):

            a = Application.objects.get(user=user)
            a.delete()
            return Response(status=status.HTTP_200_OK)

        # If not we get an "401 UNAUTHORIZED" error back 
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# TODO: make secure
class AppResponseView(APIView):

    # Only admins can do this
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def post(self, request):

        # Gets ID from form and connects it to a user
        userid = request.data["user"]
        user = get_object_or_404(User, id=userid)

        # Accept chef
        if (request.data["response"] == "accepted"):
            # Adds the user to the "chef" group
            group = Group.objects.get(name='Kokk')
            user.groups.add(group)
            #deletes the application instance as it is now accepted
            a = Application.objects.get(user=user)
            a.delete()
            # Returns a response and redirects
            return Response(status=status.HTTP_202_ACCEPTED)

        # Reject chef
        elif(request.data["response"] == "rejected"):
            # deletes the application as its now rejected
            a = Application.objects.get(user=user)
            a.delete()
            # Returns a response and redirects
            return Response(status=status.HTTP_200_OK)

        # Bad request if data is wrong
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    # Returns all of the applications as JSON objects
    def get(self, request):

        applications = Application.objects.all()

        serializer = ApplicationSerializer(applications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# View for handing the "native" application
class ApplicationFormView(LoginRequiredMixin, FormView):
    # Connected to the "LoginRequiredMixin, which redirects a user if not logged in
    login_url = '/login/'
    # Defines the template to use
    template_name = 'chef/application.html'
    # Defines the Form class to use in forms.py
    form_class = ApplicationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    # Makes a new application object or overrides the current one connected to the user if it already exists
    def form_valid(self, form_class):
        a = None
        try:
            a = Application.objects.get(user=self.request.user)
            a.text = form_class.cleaned_data['text']
            a.save()
        except Application.DoesNotExist:
            form_class.save()
            pass

        return render(self.request, 'homepage/homepage.html')


# View for "native" application
class ApplicationList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Application


# Function for handling application responses
class chefStatus(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):

        if request.user.is_staff:

            username = request.POST['user']
            user = get_object_or_404(User, username=username)

            # Accept chef
            if (request.POST['status'] == "approved"):
                # Adds the user to the "chef" group

                group = Group.objects.get(name='Kokk')
                user.groups.add(group)
                #deletes the application instance as it is now accepted
                a = Application.objects.get(user=user)
                a.delete()
                # Returns a response and redirects
                return HttpResponseRedirect("/chef/list/")

            # Reject chef
            elif (request.POST['status'] == "declined"):
                #deletes the application instance as it is now rejeted
                a = Application.objects.get(user=user)
                a.delete()
                # Returns a response and redirects
                return HttpResponseRedirect("/chef/list/")
            return HttpResponseBadRequest(status=400)

        else:
            return HttpResponseRedirect("/homepage/")