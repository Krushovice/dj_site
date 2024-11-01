from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls.conf import include

from . import views

app_name = "account"


urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    # login / logout urls
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(),
    #     name="login",
    # ),
    # path(
    #     "logout/",
    #     auth_views.LogoutView.as_view(next_page="account:login"),
    #     name="logout",
    # ),
    # # change password urls
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # # reset password urls
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(),
    #     name="password_reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    path("", include("django.contrib.auth.urls")),
    path("profile/", views.get_profile, name="profile"),
    path("register/", views.register, name="register"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]
