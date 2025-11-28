from typing import Any, Dict

from django.db.models.manager import BaseManager
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Post


def get_latest_posts(n:int = 1) ->BaseManager[Post] :
    posts= Post.objects.prefetch_related('tags').order_by('-id')[:n]
    return posts

class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model=Post
    context_object_name = 'posts'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # context =  super().get_context_data(**kwargs)
        return {'posts' : get_latest_posts()}

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


