from datetime import datetime
from typing import Dict, Generator, List, TypedDict

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render


class Blog(TypedDict):
    slug: str
    title: str
    image: str
    excerpt: str
    content: str
    author: str
    date: datetime


BLOGS: List[Blog] = [
    {
        "slug": "first-steps-with-django",
        "title": "First Steps with Django",
        "image": "django-first-steps.png",
        "excerpt": "Getting started with projects, apps, and the development server.",
        "content": (
            "Starting your first Django project can feel overwhelming, "
            "but it’s surprisingly smooth once you grasp the core structure. "
            "In this guide, we’ll create a project, set up an app, and explore "
            "how Django’s `runserver` command ties everything together for local development."
        ),
        "author": "Eslam Kamel",
        "date": datetime(2025, 11, 3, 10, 30),
    },
    {
        "slug": "template-inheritance-like-a-pro",
        "title": "Template Inheritance Like a Pro",
        "image": "templates.png",
        "excerpt": "Build maintainable UIs with extends, blocks, and includes.",
        "content": (
            "Django’s template inheritance is a powerful way to avoid duplication. "
            "By using `extends` and `block` tags, you can structure your HTML layouts "
            "so that pages share a consistent look while still allowing per-page customization. "
            "This pattern makes your templates cleaner and easier to maintain as your project grows."
        ),
        "author": "Nadia Youssef",
        "date": datetime(2025, 11, 2, 14, 45),
    },
    {
        "slug": "static-files-that-scale",
        "title": "Static Files that Scale",
        "image": "static-files.png",
        "excerpt": "Global vs app static files, configuration tips, and best practices.",
        "content": (
            "Managing static files in Django goes beyond placing them in a single folder. "
            "Understanding the difference between `STATICFILES_DIRS` and app-level `static/` folders "
            "helps ensure scalability and maintainability. "
            "We’ll also explore the best practices for deployment using WhiteNoise or cloud storage."
        ),
        "author": "Omar Farouk",
        "date": datetime(2025, 11, 1, 9, 15),
    },
]

def get_latest_blogs(n:int = 1) ->List[Blog] :
    sorted_blogs = sorted(BLOGS, key=lambda b:b['date'])
    return sorted_blogs[-n:]

def find_blog_by_slug(slug:str)->Blog|None:
    gen: Generator[Blog, None, None]  =  (blog for blog in BLOGS if blog['slug'] == slug)
    # blog_list: list[Blog]  =  [blog for blog in BLOGS if blog['slug'] == slug]
    blog : Blog|None = next(gen , None)
    return blog



def starting_page(request:HttpRequest)->HttpResponse :
    context:Dict[str, List[Blog]] = {'blogs' : get_latest_blogs()}
    return render(request , 'blog/index.html' , context)

def blogs(request:HttpRequest)->HttpResponse :
    context:Dict[str, List[Blog]] = {'blogs' : BLOGS}
    return render(request, 'blog/all-blogs.html' , context)

def blog_detail(request:HttpRequest , slug:str)->HttpResponse :
    blog:Blog|None = find_blog_by_slug(slug)
    if blog is None :
        # return render(request , '404.html' )
        raise Http404('Page not found')
    context:Dict[str, Blog] = {'blog':blog}
    return render(request , 'blog/blog-details.html' , context)




