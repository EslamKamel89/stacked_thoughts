from typing import Dict, List, TypedDict

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render


class Blog(TypedDict):
    slug:str
    title:str
    image:str
    excerpt:str
    content:str

BLOGS: List[Blog] = [
    {
        "slug": "first-steps-with-django",
        "title": "First Steps with Django",
        "image": "blog/images/django-first-steps.jpg",
        "excerpt": "Getting started with projects, apps, and runserver.",
        "content": "Full blog content goes here...",
    },
    {
        "slug": "template-inheritance-like-a-pro",
        "title": "Template Inheritance Like a Pro",
        "image": "blog/images/templates.jpg",
        "excerpt": "Build maintainable UIs with extends, blocks, and includes.",
        "content": "Full blog content goes here...",
    },
    {
        "slug": "static-files-that-scale",
        "title": "Static Files that Scale",
        "image": "blog/images/static-files.jpg",
        "excerpt": "Global vs app static, STATICFILES_DIRS, and best practices.",
        "content": "Full blog content goes here...",
    },
]
def get_latest_blogs(n:int = 3) ->List[Blog] :
    return BLOGS[:n]

def find_blog_by_slug(slug:str)->Blog|None:
    for blog in BLOGS :
        if blog['slug'] == slug :
            return blog
    return None

def starting_page(request:HttpRequest)->HttpResponse :
    context:Dict[str, List[Blog]] = {'blogs' : get_latest_blogs()}
    return render(request , 'blog/index.html' , context)
def blogs(request:HttpRequest)->HttpResponse :
    context:Dict[str, List[Blog]] = {'blog' : BLOGS}
    return render(request, 'blog/all-blogs.html' , context)
def blog_detail(request:HttpRequest , slug:str)->HttpResponse :
    blog:Blog|None = find_blog_by_slug(slug)
    if blog is None :
        raise Http404('Page not found')
    context:Dict[str, Blog] = {'blog':blog}
    return render(request , 'blog/blog-details.html' , context)



