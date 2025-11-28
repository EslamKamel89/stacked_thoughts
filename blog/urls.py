from __future__ import annotations

from django.urls import URLPattern, path

from . import views

urlpatterns : list[URLPattern] = [
    path('' , views.StartingPageView.as_view() , name='blog_home') ,
    path('blogs/' , views.BlogsView.as_view() , name="all_blogs") ,
    path('blogs/<slug:slug>' , views.BlogDetailView.as_view() , name='blog_detail')
]

