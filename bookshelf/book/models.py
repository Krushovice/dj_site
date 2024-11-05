from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.template.context_processors import static

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

    genre = models.CharField(max_length=255)

    ratings = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="BookRating",
    )

    def avg_rating(self) -> float | int:
        ratings = self.book_ratings.aggregate(Avg("rating"))
        if ratings["rating__avg"]:
            return round(ratings["rating__avg"], 1)
        return 0

    def __str__(self):
        return self.title


class BookRating(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="book_ratings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=1,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("book", "user")

    def __str__(self):
        return f"{self.book}, rating:{self.rating}"


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
