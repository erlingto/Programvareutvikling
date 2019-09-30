from django.test import TestCase, RequestFactory, Client
from utilities.utilities import populate_db, setup_view, login_client_user, logout_client_user
from django import forms
from chef.models import Application
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your tests here.

class RequestTests(TestCase):
    
    def test_setUp(self):
        #populates the database
        populate_db()
        #sets the client
        self.client = Client(enforce_csrf_checks=False)
        #logs in the user 'admin' made in populate_db
        login_client_user(self)

    def test_form_application(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self) 
        user = User.objects.get(username = 'admin')
        # Use follow=true since there will be a redirect after processing
        post_data = {
            'text': "I want to become a chef",
        }
        response = self.client.post('/chef/application/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        application = Application.objects.get(user = user)
        self.assertTrue(application.text == "I want to become a chef")

    def test_application_model(self):
        populate_db()
        user = User.objects.get(username = 'admin')
        application = Application.objects.create(user = user, text ="I want to become a chef")
        application_check = Application.objects.get(user = user)
        self.assertTrue(application_check.text == 'I want to become a chef')
        toString = application_check.__str__() 
        self.assertTrue(toString == 'Application from admin')

'''
    def test_application_accept(self):
        populate_db()
        self.factory = RequestFactory()
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self) 
        user = User.objects.get(username = 'admin')
        application = Application.objects.create(user = user, text ="I want to become a chef")
        # Use follow=true since there will be a redirect after processing
        post_data = {
            'user' :"admin",
            'response': "accepted"
        }
        request = self.factory.post('/chef/application/response', post_data)
        applicationcheck = Application.objects.get(user = user)
        self.assertTrue(user.groups.filter(name='Kokk').exists())
'''