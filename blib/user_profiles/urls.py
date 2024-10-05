from django.urls import path
from django.views.generic import TemplateView
from .views import user_profile, edit_profile

app_name = 'user_profiles'

urlpatterns = [
    path('', user_profile, name='profile'),
    path("update/", edit_profile, name="edit_profile"),
]
