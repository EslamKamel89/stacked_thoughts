from django.contrib import admin

from .models import Author, Post, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('first_name' , 'last_name'  , 'email')
    search_fields = ('first_name' , 'last_name' , 'email')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin): # type: ignore
    list_display=('caption',)
    search_fields=('caption',)


@admin.register(Post)
class  PostAdmin(admin.ModelAdmin): # type: ignore
    list_display =('title' , 'excerpt' , 'image' , 'content' , 'slug' , 'created_at')
    search_fields =('title' , 'content' , 'excerpt')
    list_filter =('tags' , 'author')
    prepopulated_fields = {'slug':('title',)}
    filter_horizontal = ('tags',)

