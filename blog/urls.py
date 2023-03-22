from django.urls import path
from blog.views import CreateBlogAPIView, BlogListAPIView, UpdateBlogAPIView

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
]
