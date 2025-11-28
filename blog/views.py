from typing import Any, Dict

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Post


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model=Post
    context_object_name = 'posts'
    ordering = ['-id']
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().prefetch_related('tags')[:1]

class BlogsView(ListView):
    template_name = 'blog/all-blogs.html'
    model = Post
    context_object_name = 'posts'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'posts' : Post.objects.prefetch_related('tags')}

class BlogDetailView(DetailView):
    template_name = 'blog/post-details.html'
    model=Post
    context_object_name = 'post'


