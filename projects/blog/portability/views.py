from django.shortcuts import render

from portability.models import Post


def home(request):
    """Home page view."""
    posts = Post.objects.all().order_by("-date")
    context = {"posts": posts}
    return render(request, "index.html", context)


def article(request, slug):
    """Article page view."""
    return render(request, f"posts/{slug}.html", {"slug": slug})
