from audioop import reverse
from re import search

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST

from django.db.models import Count

from django.contrib.postgres.search import TrigramSimilarity


from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    FormView,
)

from django.core.mail import send_mail

from taggit.models import Tag

from .models import Post, Comment

from .forms import EmailPostForm, PostForm, CommentForm, SearchForm


# Create your views here.
def index(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug,
        )
        posts_list = posts_list.filter(tags__in=[tag])

    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/index.html",
        {
            "posts": posts,
            "tag": tag,
        },
    )


# class PostListView(ListView):
#     model = Post
#     template_name = "blog/index.html"
#     context_object_name = "posts"
#     paginate_by = 5


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm


def post_detail(request, pk: int):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED,
    )
    # List of active comments for this blog
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


class PostEmailView(FormView):
    template_name = "blog/email_share.html"
    form_class = EmailPostForm
    success_url = "/thanks"

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
            return render(
                request,
                self.template_name,
                {
                    "post": post,
                    "form": form,
                    "sent": sent,
                },
            )

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        sent = False
        return render(
            request,
            self.template_name,
            {
                "post": post,
                "form": self.form_class,
                "sent": sent,
            },
        )


# class CommentCreateView(CreateView):
#     template_name = "blog/post_comment.html"
#     model = Comment
#     form_class = CommentForm


@require_POST
def post_comment_create(request, pk: int):
    post = get_object_or_404(
        Post,
        pk=pk,
        status=Post.Status.PUBLISHED,
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "blog/post_comment.html",
        context={
            "post": post,
            "form": form,
            "comment": comment,
        },
    )


def post_search(request):
    form = SearchForm(request.GET or None)
    query = request.GET.get("query")
    results = []

    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # search_vector = SearchVector(
            #     "title",
            #     weight="A",
            # ) + SearchVector(
            #     "body",
            #     weight="B",
            # )
            # search_query = SearchQuery(query)
            # results = (
            #     Post.published.annotate(
            #         search=search_vector,
            #         rank=SearchRank(search_vector, search_query),
            #     )
            #     .filter(rank__gte=0.3)
            #     .order_by("-rank")
            # )

            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity(
                        "title",
                        query,
                    )
                )
                .filter(similarity__gte=0.1)
                .order_by("-similarity")
            )

    return render(
        request,
        "blog/search.html",
        context={
            "form": form,
            "query": query,
            "results": results,
        },
    )
