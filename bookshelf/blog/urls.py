from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "tag/<slug:tag_slug>/",
        views.index,
        name="post_index_by_tag",
    ),
    path(
        "<int:pk>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "<int:pk>/comment/",
        views.post_comment_create,
        name="post_comment",
    ),
    path(
        "<int:pk>/share/",
        views.PostEmailView.as_view(),
        name="post_share",
    ),
    path(
        "create/",
        views.CreatePostView.as_view(),
        name="post_create",
    ),
]
