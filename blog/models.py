
from typing import Any

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

# Create your models here.

class BaseModel(models.Model) :
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        abstract= True

class Author(BaseModel) :
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self)->str :
        return f"{self.first_name} {self.last_name} <{self.email}>"
    class Meta: # type: ignore
        constraints = [
            models.UniqueConstraint(fields=['first_name' , 'last_name'] , name="unique_author_fullname")
        ]

class PostManager(models.Manager["Post"]):
    def get_queryset(self):
        return super().get_queryset().select_related('author')


class Post (BaseModel) :
    title = models.CharField(max_length=150)
    excerpt = models.TextField(blank=True , null=True)
    image = models.CharField(blank=True , null=True , max_length=255)
    content = models.TextField(validators=[
        MinLengthValidator(10)
    ])
    slug = models.SlugField(unique=True , db_index=True)
    author = models.ForeignKey(Author , on_delete=models.SET_NULL , null=True, related_name='posts')
    tags = models.ManyToManyField(# type: ignore
        "Tag" ,
        related_name='posts' ,
        blank=True ,
        # through='PostTag'
    )
    objects = PostManager()
    plain:models.Manager['Post'] = models.Manager()

    def __str__(self)->str :
        author_name = (
           f" <{self.author.first_name} {self.author.last_name}>"
           if self.author else ""
        )
        return f"{self.title}{author_name}"

    def save(self , *args:Any , **kwargs:Any):
        if not self.slug and self.title :
            slug = slugify(self.title)
            i = 1
            while Post.objects.filter(slug=slug).exists() :
                i +=1
            slug = f"{slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta : # type: ignore
        ordering = ['-created_at']


class Tag(BaseModel) :
    caption = models.CharField(max_length=50 , unique=True)

    def __str__(self)->str :
        return self.caption.capitalize()

# class PostTag(BaseModel) :
#     tag = models.ForeignKey(Tag , on_delete=models.CASCADE)
#     post = models.ForeignKey(Post , on_delete=models.CASCADE)

#     class Meta : # type: ignore
#         constraints = [
#             models.UniqueConstraint(fields=['tag' , 'post'] , name='unique_post_tag')
#         ]
