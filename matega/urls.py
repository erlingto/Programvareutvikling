from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls import url
from chef.views import ApplicationFormView


#fetches the url paths from the different apps, aswell as homepage and password_reset
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('allauth.urls')),
    re_path(r"^$", TemplateView.as_view(template_name="matega/index.html"), name="index"),
    url('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    #Apps
    path('chef/', include('chef.urls')),
    path('homepage/', TemplateView.as_view(template_name="homepage/homepage.html"), name="homepage"),
    path('password_reset/', TemplateView.as_view(template_name="account/password_reset.html"), name="account_password_reset"),
    path('recipe/', include('recipe.urls')),
    path('fridge/', include('fridge.urls')), 
    
]