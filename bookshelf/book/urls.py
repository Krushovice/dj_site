from django.urls import path

from . import views


pp_name = "book"

urlpatterns = [
    path("", views.index, name="index"),
    # path("top-list/", views.top_list, name="top_list"),
]
