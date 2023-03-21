from django.urls import path
from blog.views import CreateBlogAPIView

urlpatterns = [
    # Creat-blog API endpoint
    path("create-blog/",
         CreateBlogAPIView.as_view(),
         name="createblog"),
]
