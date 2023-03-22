from rest_framework.views import APIView
from blog.models import BlogPost
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, BasePermission
from blog.serializers import BlogSerializer


# Custom Permission Class
class IsAuthor(BasePermission):
    """
    Custom permission to allow only the author of a blog post to update it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the author of the blog post.
        return obj.author == request.user


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
        blogs = BlogPost.objects.filter(status="published")
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

    permission_classes = [IsAuthor]

    def get_object(self, id):
        try:
            return BlogPost.objects.get(id=id)
        except BlogPost.DoesNotExist:
            raise NotFound({
                "status": False,
                "message": "Blog Post Does Not Exist.",
                "data": None
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request, id):
        """
        Updates a single blog post by ID.

        Args:
            request (Request): A Django REST Framework request object containing the blog post ID and updated data.
            pk (int): The ID of the blog post to be updated.

        Returns:
            Response: A JSON response containing the serialized blog post, along with a success message.
        """
        blog_post = self.get_object(id)

        serializer = BlogSerializer(blog_post, data=request.data, partial=True)
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
