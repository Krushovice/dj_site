from datetime import timedelta

from django.db.models import Count, Q, Avg

from django.utils import timezone

from django.shortcuts import render

from django.views.generic import ListView

from .models import Book

# Create your views here.


class IndexView(ListView):
    model = Book
    template_name = "book/index.html"
    context_object_name = "book_list"


class BestBooksListView(ListView):
    model = Book
    template_name = "book/top_list.html"

    def get_queryset(self):
        today = timezone.now()

        start_of_last_week = today - timedelta(
            days=today.weekday() + 7
        )  # Понедельник прошлой недели
        end_of_last_week = start_of_last_week + timedelta(
            days=7
        )  # Воскресенье прошлой недели

        # Фильтруем книги и аннотируем с средним рейтингом
        top_list = (
            Book.objects.annotate(
                avg_rating=Avg(
                    "book_ratings__rating",
                    filter=Q(
                        book_ratings__created_at__gte=start_of_last_week,
                        book_ratings__created_at__lt=end_of_last_week,
                    ),
                )
            )
            .filter(avg_rating__gte=4)  # Фильтруем по среднему рейтингу
            .order_by("-avg_rating")[:10]
        )
        return top_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_list"] = self.get_queryset()
        return context
