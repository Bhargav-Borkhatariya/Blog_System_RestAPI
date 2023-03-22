from blog.utils import get_blog_object
from django.utils import timezone
from rest_framework.views import APIView
from blog.models import BlogPost
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from blog.serializers import BlogSerializer


class CreateBlogAPIView(APIView):
    """
    API endpoint that allows a logged-in user to create a new blog post.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Create a new blog post for the authenticated user.

        Parameters:
        request (Request): The incoming request object.

        Returns:
        Response: JSON response containing the serialized blog post
            if the post is created successfully.
            Error response if the request data is invalid.
        """
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "status": True,
                "message": "Blog Created Successfully.",
                "data": serializer.data,
            }, status=HTTP_201_CREATED)
        return Response({
                "status": False,
                "error": serializer.errors,
                "data": None,
            }, status=HTTP_400_BAD_REQUEST)


class BlogListAPIView(APIView):
    """
    API endpoint that allows to get all published blog posts.
    """
    def get(self, request):
        """
        Retrieve all published blog posts.

        Returns:
        Response: JSON response containing the serialized blog posts.
        """
        blogs = BlogPost.objects.filter(status="published", deleted_at=None)
        serializer = BlogSerializer(blogs, many=True)
        return Response({
            "status": True,
            "message": "All Published Post Are listed below",
            "data": serializer.data,
        }, status=HTTP_200_OK)


class UpdateBlogAPIView(APIView):
    """
    API view that allows updating a single blog post by ID.

    Only the author of the blog post is allowed to update it.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        """
        Updates a single blog post by ID.

        Args:
            request (Request): A Django REST Framework request object
                    containing the blog post ID and updated data.
            pk (int): The ID of the blog post to be updated.

        Returns:
            Response: A JSON response containing the serialized blog post,
                    along with a success message.
        """
        blog_post = get_blog_object.get_object(id)
        if blog_post.author == request.user:
            serializer = BlogSerializer(
                blog_post,
                data=request.data,
                partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response({
                    "status": True,
                    "message": "Blog Post updated successfully.",
                    "data": serializer.data
                }, status=HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "error": serializer.errors,
                    "data": None,
                }, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    "status": False,
                    "message": "You Have No Rights to Update.[OnlyAuthor]",
                    "data": None,
                }, status=HTTP_401_UNAUTHORIZED)


class DeleteBlogAPIView(APIView):
    """
    API view that soft deletes a single blog post by ID.

    Only the author of the blog post is allowed to soft delete it.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        """
        Soft deletes a single blog post by ID.

        Args:
            request (Request): A Django REST Framework request object
                    containing the blog post ID.
            id (int): The ID of the blog post to be soft deleted.

        Returns:
            Response: A JSON response containing the serialized blog post,
                    along with a success message.
        """
        blog_post = get_blog_object.get_object(id)
        if blog_post.author == request.user:
            if blog_post.deleted_at:
                return Response({
                    "status": False,
                    "message": "Blog post has already been soft-deleted.",
                    "data": None
                }, status=HTTP_400_BAD_REQUEST)

            blog_post.deleted_at = timezone.now()
            blog_post.save()

            return Response({
                "status": True,
                "message": "Blog post soft-deleted successfully.",
                "data": None
            }, status=HTTP_200_OK)
        else:
            return Response({
                    "status": False,
                    "message": "You Have No Rights to Delete.[OnlyAuthor]",
                    "data": None,
                }, status=HTTP_401_UNAUTHORIZED)