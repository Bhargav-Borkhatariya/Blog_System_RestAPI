from django.db import models
from authentication.models import User


class Category(models.Model):
    """
    Model storing the blog post category.

    Attributes:
        name: The name of the category.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    Model representing a blog post.

    Attributes:
        author (ForeignKey): A reference to the User who wrote the blog post.
        title (CharField): The title of the blog post.
        content (TextField): The content of the blog post.
        category (CharField): The category of the blog post.
        image (ImageField): An image associated with the blog post.
        status (CharField): The status of the blog post, either "draft" or "published".
        created_on (DateTimeField): The date and time when the blog post was created.
        updated_on (DateTimeField): The date and time when the blog post was last updated.
    """

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_at = models.BooleanField(default=None)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
