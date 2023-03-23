from django.contrib import admin
from .models import BlogPost, Category, Comment

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_on')
    list_filter = ('category',)

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register((Category, Comment))
