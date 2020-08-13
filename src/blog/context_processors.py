from django.utils import timezone
from .models import Category, Post
from .forms import SearchForm


def common(request):
    context = {
        'categories': Category.objects.all(),
        'latests': Post.objects.filter(
            published_date__lte=timezone.now(),
            live=True
        )[:5],
        'search_form': SearchForm(request.GET)
    }
    return context
