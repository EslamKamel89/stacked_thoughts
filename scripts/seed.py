
from datetime import datetime
from typing import List, TypedDict

from blog.models import Author, Post, Tag


class Blog(TypedDict):
    slug: str
    title: str
    image: str
    excerpt: str
    content: str
    author: str
    date: datetime
    tags:list[str]


BLOGS:list[Blog] = [
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
        "tags": ["django", "beginners", "setup"],
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
        "tags": ["django", "templates", "frontend"],
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
        "tags": ["django", "static", "deployment"],
    },
]

def seed() :
    print('Seeding started.................................')
    Post.objects.all().delete()
    Tag.objects.all().delete()
    Author.objects.all().delete()
    for blog in BLOGS :
        fullname = blog['author'].strip()
        parts = fullname.split(' ')
        first = parts[0]
        last = parts[1] if len(parts) > 0 else ''
        author = Author.objects.create(first_name = first  , last_name=last , email = f"{first}_{last}@gmail.com")
        post = Post.plain.create(
            title=blog["title"],
            slug="",
            excerpt=blog["excerpt"],
            content=blog["content"],
            image=blog["image"],
            author=author,
        )
        blog_tags = blog.get('tags' , [])
        tag_objects:list[Tag] = []
        for caption in blog_tags:
            tag_obj,_ = Tag.objects.get_or_create(caption=caption.lower())
            tag_objects.append(tag_obj)
        post.tags.set(tag_objects) # type: ignore


    print('Seeding Finished................................')

if __name__ == "__main__" :
    seed()
