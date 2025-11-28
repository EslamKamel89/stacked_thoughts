from typing import Any, Dict

from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.forms import CommentForm
from blog.models import Comment, Post


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

class BlogDetailView(View):
    def get(self , request:HttpRequest , slug:str):
        post = Post.objects.get(slug=slug)
        form = CommentForm()
        context = {'form':form , 'post':post , 'comments':post.comments.all().order_by('-id')} # type: ignore
        return render(request , 'blog/post-details.html' , context)
    def post(self , request:HttpRequest , slug:str):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog_detail' , args=[slug]))
        context = {'form':form , 'post':post ,'comments':post.comments.all().order_by('-id')} # type: ignore
        return render(request, 'blog/post-details.html' , context)


class ReadLaterView(View):
    def post(self , request: HttpRequest):
        post_id = int(request.POST.get('post_id' , '-1'))
        post = get_object_or_404(Post , pk=post_id)





