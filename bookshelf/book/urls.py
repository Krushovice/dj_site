from django.urls import path

from . import views


app_name = "books"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("top-list/", views.BestBooksListView.as_view(), name="top_list"),
]
