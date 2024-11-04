from django.contrib import admin

from book.models import Book, BookRating, Author


# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "genre"]
    list_filter = ["author", "ratings"]
    search_fields = ["title"]
    raw_id_fields = ["author"]
    ordering = ["title"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
    list_filter = ["last_name"]
    search_fields = ["last_name"]
    ordering = ["last_name"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ["rating", "book", "user"]
    list_filter = ["rating"]
    ordering = ["rating"]
    show_facets = admin.ShowFacets.ALWAYS
