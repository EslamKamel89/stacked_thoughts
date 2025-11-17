from typing import Dict

from django.db.models.manager import BaseManager
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

# from django.
from blog.models import Post


def get_latest_posts(n:int = 1) ->BaseManager[Post] :
    posts= Post.objects.prefetch_related('tags').order_by('-id')[:n]
    return posts

def find_post_by_slug(slug:str)->Post|None:
    post = Post.objects.prefetch_related('tags').filter(slug=slug).first()
    return post



def starting_page(request:HttpRequest)->HttpResponse :
    context:Dict[str, BaseManager[Post]] = {'blogs' : get_latest_posts()}
    return render(request , 'blog/index.html' , context)

def blogs(request:HttpRequest)->HttpResponse :
    context:Dict[str, BaseManager[Post]] = {'blogs' : Post.objects.prefetch_related('tags')}
    return render(request, 'blog/all-blogs.html' , context)

def blog_detail(request:HttpRequest , slug:str)->HttpResponse :
    post:Post|None = find_post_by_slug(slug)
    if post is None :
        # return render(request , '404.html' )
        raise Http404('Page not found')
    context:Dict[str, Post] = {'blog':post}
    return render(request , 'blog/blog-details.html' , context)




