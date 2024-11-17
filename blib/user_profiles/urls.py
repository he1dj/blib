from django.urls import path

from .views import edit_profile
from .views import user_profile

app_name = "user_profiles"

urlpatterns = [
    path("", user_profile, name="profile"),
    path("/update", edit_profile, name="edit_profile"),
]
