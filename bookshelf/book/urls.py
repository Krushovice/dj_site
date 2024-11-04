from django.urls import path

from . import views


app_name = "books"

urlpatterns = [
    path("", views.index, name="index"),
    # path("top-list/", views.top_list, name="top_list"),
]
