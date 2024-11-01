from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


from .models import Profile

# Create your views here.


@login_required
def get_profile(request):
    current_user = request.user
    return render(
        request,
        "account/profile.html",
        {
            "section": "profile",
            "user": current_user,
        },
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                "account/register_done.html",
                {"new_user": new_user},
            )

    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        "account/register.html",
        {"user_form": user_form},
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST,
        )
        profile_form = ProfileEditForm(
            instance=request.user,
            data=request.POST,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                "Profile updated successfully",
            )
        else:
            messages.error(
                request,
                "Error updating your profile",
            )

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)

    return render(
        request,
        "account/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
