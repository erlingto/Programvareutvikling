from django.contrib import admin

from chef.models import Application
#Creates a django premade page in admin for editing models you register here
admin.site.register(Application)