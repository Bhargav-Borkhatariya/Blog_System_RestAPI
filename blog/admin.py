from django.contrib import admin
from blog.models import BlogPost, Category, Comment


# Register your models here.
admin.site.register((BlogPost, Category, Comment))
