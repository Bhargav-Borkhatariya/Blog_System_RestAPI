from django.contrib import admin
from blog.models import BlogPost, Category, Comment


class CommentInline(admin.StackedInline):
    """
    Allows comments to be added to a blog post in the admin panel.
    """
    model = Comment
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Customizes the display and behavior of the BlogPost model in the admin panel.
    """
    inlines = [CommentInline]
    list_display = ("id", "title", "category", "author", "created_on", "deleted_at")
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the display and behavior of the Category model in the admin panel.
    """
    list_display = ("id", "name")
    list_filter = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Customizes the display and behavior of the Comment model in the admin panel.
    """
    list_display = ("author", "blog_post", "email", "created_at")
    list_filter = ("created_at",)
