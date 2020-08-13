from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import ModelFormMixin
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import SearchForm, CommentForm


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')

        if title:
            context['title'] = title
            context['count'] = Post.objects.filter(
                title__icontains=title,
                published_date__lte=timezone.now(),
                live=True
            ).count()

        return context

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title:
            return Post.objects.filter(
                title__icontains=title,
                published_date__lte=timezone.now(),
                live=True
            )
        else:
            return Post.objects.filter(
                published_date__lte=timezone.now(),
                live=True
            )


class CategoryView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/category.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context

    def get_queryset(self):
        return Post.objects.filter(
            category__name=self.kwargs.get('category'),
            published_date__lte=timezone.now(),
            live=True
        )


class ArticleView(ModelFormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/article.html'

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:article', pk=post_pk)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            post_id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        return Post.objects.filter(
            id=self.kwargs.get('pk'),
            published_date__lte=timezone.now(),
            live=True
        )
