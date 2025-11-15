
from django.db import models

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
    title = models.CharField(max_length=255)
    excerpt = models.TextField(blank=True , null=True)
    image = models.ImageField(blank=True , null=True)
    content = models.TextField()
    author = models.ForeignKey(Author , on_delete=models.CASCADE , related_name='posts')
    tags = models.ManyToManyField("Tag" , through='PostTag' , related_name='posts' , blank=True) # type: ignore
    objects = PostManager()
    plain:models.Manager['Post'] = models.Manager()

    def __str__(self)->str :
        return f"{self.title} <{self.author.first_name} {self.author.last_name}>"

    class Meta : # type: ignore
        ordering = ['-created_at']


class Tag(BaseModel) :
    caption = models.CharField(max_length=50 , unique=True)
    def __str__(self)->str :
        return self.caption.capitalize()

class PostTag(BaseModel) :
    tag = models.ForeignKey(Tag , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)

    class Meta : # type: ignore
        constraints = [
            models.UniqueConstraint(fields=['tag' , 'post'] , name='unique_post_tag')
        ]
