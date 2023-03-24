from django.urls import path
from blog.views import (
    BlogAPISet1View,
    BlogAPISet2View,
    SearchAPIView,
)
urlpatterns = [
    # User's Blog API for create and list blog API endpoint
    path("blog-api-set1/",
         BlogAPISet1View.as_view(),
         name="blogapiset1"),

    # User's Blog API for update, delete and comment on blog API endpoint
    path("blog-api-set2/<int:id>/",
         BlogAPISet2View.as_view(),
         name="blogapiset2"),

    # Search Blogs API endpoint
    path("search-blogs/",
         SearchAPIView.as_view(),
         name="searchblogs"),
]
