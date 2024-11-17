from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import UserProfileForm


@login_required
def user_profile(request):
    user_profile = request.user.profile
    return render(request, "user_profiles/profile.html", {"profile": user_profile})


@login_required
def edit_profile(request):
    user_profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "user_profiles/edit_profile.html", {"form": form})
