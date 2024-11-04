from django.shortcuts import render, get_object_or_404

from .models import Book

# Create your views here.


def index(request):
    books = Book.objects.all()

    return render(
        request,
        "book/index.html",
        context={"books": books},
    )
