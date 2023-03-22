from django.urls import path
from blog.views import (
    CreateBlogAPIView,
    BlogListAPIView,
    UpdateBlogAPIView,
    DeleteBlogAPIView,
    CommentAPIView,
    SearchAPIView,
)
urlpatterns = [
    # Creat-blog API endpoint
    path("create-blog/",
         CreateBlogAPIView.as_view(),
         name="createblog"),

    # List-blogs Published API endpoint
    path("list-all-blogs/",
         BlogListAPIView.as_view(),
         name="listallblogs"),

    # Update Blog API endpoint
    path("update-blog/<int:id>/",
         UpdateBlogAPIView.as_view(),
         name="updateblog"),

    # Soft Delete Blog API endpoint
    path("soft-delete-blog/<int:id>/",
         DeleteBlogAPIView.as_view(),
         name="softdeleteblog"),

    # Comment Blog API endpoint
    path("implement-comment/<int:id>/",
         CommentAPIView.as_view(),
         name="implementcomment"),

    # Search Blogs API endpoint
    path("search-blogs/",
         SearchAPIView.as_view(),
         name="searchblogs"),
]
