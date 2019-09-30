from django.test import TestCase, RequestFactory, Client
from utilities.utilities import populate_db, setup_view, login_client_user, logout_client_user
from django.contrib.auth.models import User

class RequestTests(TestCase):

    def test_setUp(self):
        #populates the database
        populate_db()
        #sets the client
        self.client = Client(enforce_csrf_checks=False)
        #logs in the user 'admin' made in populate_db
        login_client_user(self)
        #logs the user 'admin out
        logout_client_user(self)


    def test_user_must_log_in(self):
        self.client = Client(enforce_csrf_checks=False)
        response = self.client.get('/homepage/')
        self.assertContains(response, "You need to be logged in to view this page")

    def test_user_has_logged_in(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        user = User.objects.get(username = 'admin')
        login_client_user(self)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        
    def test_user_has_logged_out(self):
        populate_db()
        self.client = Client(enforce_csrf_checks=False)
        user = User.objects.get(username = 'admin')
        login_client_user(self)
        logout_client_user(self)
        response = self.client.get('/homepage/')
        self.assertContains(response, "You need to be logged in to view this page")
        

    def test_homepage(self):
        self.client = Client(enforce_csrf_checks=False)
        login_client_user(self)
        response = response = self.client.get('')
        self.assertTrue(response.status_code == 200)
        self.assertContains(response, 'Matega')