from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response
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
