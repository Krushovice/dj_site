from django.contrib.auth.models import User
from django.db import models

from bookshelf import settings


# Create your models here.


class Book(models.Model):

    class Meta:
        ordering = ["-title"]
        indexes = [
            models.Index(fields=["-title"]),
        ]

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_books",
        blank=True,
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        "Author",
        related_name="author_books",
        on_delete=models.CASCADE,
    )
    isbn = models.CharField(max_length=32, unique=True, blank=True)
    genre = models.CharField(max_length=255)

    ratings = models.ManyToManyField(User, through="BookRating")

    def __str__(self):
        return self.title


class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=1,
    )

    class Meta:
        unique_together = ("book", "user")

    def __str__(self):
        return f"{self.book}, rating:{self.rating}"


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
