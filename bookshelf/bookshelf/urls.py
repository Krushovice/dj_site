"""
URL configuration for bookshelf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from django.conf import settings
from django.conf.urls.static import static


from django.urls import path, include

from django.views.generic import TemplateView

from blog.sitemaps import PostSitemap, TagSitemap

sitemaps = {
    "posts": PostSitemap,
    "tags": TagSitemap,
}
urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="index.html",
        ),
        name="index",
    ),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path(
        "blog/",
        include(
            "blog.urls",
            namespace="blog",
        ),
    ),
    path(
        "account/",
        include(
            "account.urls",
            namespace="account",
        ),
    ),
    path(
        "books/",
        include(
            "book.urls",
            namespace="book",
        ),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "social-auth/",
        include(
            "social_django.urls",
            namespace="social",
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
