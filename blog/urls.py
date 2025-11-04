from __future__ import annotations

from django.urls import URLPattern, path

from . import views

urlpatterns : list[URLPattern] = [
    path('' , views.starting_page , name='blog_home') ,
    path('blogs/' , views.blogs , name="all_blogs") ,
    path('blogs/<slug:slug>' , views.blog_detail , name='blog_detail')
]

