from django.contrib import admin
from blog.models import BlogPost, Category, Comment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "author", "created_on")
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "blog_post", "email", "created_at")
