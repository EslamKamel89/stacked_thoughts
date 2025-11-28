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
    def shared_context(self  ,request:HttpRequest , slug:str):
        post = Post.objects.get(slug=slug)
        comments = post.comments.all().order_by('-id') # type: ignore
        stored_posts = request.session.get('stored_posts' , [])
        is_read_later:bool = post.id in stored_posts # type: ignore
        return {'post':post , 'comments':comments , 'is_read_later':is_read_later}

    def get(self , request:HttpRequest , slug:str):
        context = self.shared_context(request , slug)
        form = CommentForm()
        context['form'] = form
        return render(request , 'blog/post-details.html' , context)

    def post(self , request:HttpRequest , slug:str):
        context = self.shared_context(request , slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = context['post']
            comment.save()
            return HttpResponseRedirect(reverse('blog_detail' , args=[slug]))
        context['form'] = form
        return render(request, 'blog/post-details.html' , context)


class ReadLaterView(View):
    def post(self , request: HttpRequest):
        post_id = int(request.POST.get('post_id' , '-1'))
        post = get_object_or_404(Post , pk=post_id)
        stored_posts:list[int] = request.session.get('stored_posts' , [])
        if post.id not in stored_posts : # type: ignore
            stored_posts.append(post.id) # type: ignore
            request.session['stored_posts'] = stored_posts
        return HttpResponseRedirect('/')
    def get(self , request:HttpRequest):
        stored_posts:list[int] = request.session.get('stored_posts' , [])
        posts = Post.objects.filter(id__in=stored_posts).prefetch_related('tags')
        return render(request, 'blog/stored-posts.html' , {"posts" : posts})








