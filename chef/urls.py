from django.urls import re_path, path
from django.views.generic import TemplateView
from chef.views import ApplicationFormView, ApplicationList, chefStatus



app_name = "chef"
# Url paths
urlpatterns = [
    path("application/", ApplicationFormView.as_view(), name='application'),
    path("list/", ApplicationList.as_view(), name='applicationList'),
    path("application/response", chefStatus.as_view(), name='chefStatus')
]
