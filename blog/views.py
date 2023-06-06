from blog.utils import get_blog_object
from rest_framework.views import APIView
from blog.models import BlogPost, Comment
from authentication.utils import send_email
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from blog.serializers import BlogSerializer, CommentSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class BlogPostPagination(PageNumberPagination):
    """
    Custom pagination class for blog posts.
    """

    # Set the number of items to display per page
    page_size = 1


class BlogAPISet1View(APIView):
    """
    (1)
    API endpoint that allows a logged-in user to create a new blog post.

    (2)
    And also provide list of published blogs.
    """

    authentication_classes = [TokenAuthentication]

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
            return Response(
                {
                    "status": True,
                    "message": "Blog Created Successfully.",
                    "data": serializer.data,
                },
                status=HTTP_201_CREATED,
            )
        return Response(
            {
                "status": False,
                "error": serializer.errors,
                "data": None,
            },
            status=HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        """
        Retrieve all published blog posts with comments using pagination.

        Returns:
        Response: JSON response containing the serialized blog posts and their comments.
        """
        # Retrieve all published blog posts
        blogs = BlogPost.objects.filter(status="published", deleted_at=False)

        # Instantiate the paginator
        paginator = BlogPostPagination()

        # Get the paginated result page based on the requested page number
        result_page = paginator.paginate_queryset(blogs, request)

        # Serialize the paginated blog posts using BlogSerializer
        serializer = BlogSerializer(result_page, many=True)

        # Initialize an empty list to hold the serialized blog posts with comments
        data = []

        # Iterate over each serialized blog post and retrieve its comments
        for blog in serializer.data:
            comments = Comment.objects.filter(blog_post=blog["id"])

            # Serialize the comments using CommentSerializer
            comment_serializer = CommentSerializer(comments, many=True)

            # Add the serialized comments to the current blog post dictionary
            blog["comments"] = comment_serializer.data

            # Append the updated blog post dictionary to the data list
            data.append(blog)

        # Return a paginated JSON response containing the serialized blog posts and their comments
        return paginator.get_paginated_response(
            {
                "status": True,
                "message": "All Published Posts Are Listed Below",
                "data": data,
            }
        )


class BlogAPISet2View(APIView):
    """
    (1)
    API view that allows updating a single blog post by ID.

    Only the author of the blog post is allowed to update it.

    (2)
    API view that soft deletes a single blog post by ID.

    Only the author of the blog post is allowed to soft delete it.

    (3)
    API view to handle creation of comments on a blog post.
    """

    authentication_classes = [TokenAuthentication]

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
            serializer = BlogSerializer(blog_post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "status": True,
                        "message": "Blog Post updated successfully.",
                        "data": serializer.data,
                    },
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "status": False,
                        "error": serializer.errors,
                        "data": None,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "status": False,
                    "message": "You Have No Rights to Update.[OnlyAuthor]",
                    "data": None,
                },
                status=HTTP_401_UNAUTHORIZED,
            )

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
                return Response(
                    {
                        "status": False,
                        "message": "Blog post has already been soft-deleted.",
                        "data": None,
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

            blog_post.deleted_at = True
            blog_post.save()

            return Response(
                {
                    "status": True,
                    "message": "Blog post soft-deleted successfully.",
                    "data": None,
                },
                status=HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": False,
                    "message": "You Have No Rights to Delete.[OnlyAuthor]",
                    "data": None,
                },
                status=HTTP_401_UNAUTHORIZED,
            )

    def post(self, request, id):
        """
        Create a new comment on the specified blog post.

        Args:
            request: The HTTP request object.
            post_id: The ID of the blog post to add the comment to.

        Returns:
            A JSON response with the status of the comment creation
            and any relevant data.

        """
        blog_post = get_blog_object.get_object(id)

        # Get the current user and use their name and email for the comment
        commenter = request.user.username
        email = request.user.email

        # Get the comment content from the request data
        content = request.data.get("comment")

        # Create a new comment dict with the data
        comment = {
            "author": commenter,
            "email": email,
            "content": content,
            "blog_post": blog_post.id,
        }

        # Serialize the comment data
        serializer = CommentSerializer(data=comment)

        # Save the comment to the database and return the serialized data
        if serializer.is_valid():
            serializer.save()
            send_email.send_posted_comment_email(blog_post, content, commenter)
            return Response(
                {
                    "status": True,
                    "message": "Comment posted successfully.",
                    "data": None,
                },
                status=HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": False,
                    "error": serializer.errors,
                    "data": None,
                },
                status=HTTP_400_BAD_REQUEST,
            )


class SearchAPIView(APIView):
    """
    API View for searching blog posts by title or category name.
        """
    def get(self, request):
        """
        Returns a list of blog posts that match the search query.

        Parameters:
        request (Request): The incoming request object.

        Returns:
        Response: JSON response containing the list of matching blog posts.
            Error response if the search query is missing or invalid.
        """

        search_query = request.query_params.get("search")

        if search_query:
            # If a search query is provided, filter the BlogPost objects based on the query
            blog_posts = BlogPost.objects.filter(
                Q(title__exact=search_query) | Q(category__name__exact=search_query),
                status="published",
                deleted_at=False,
            )
        else:
            # Otherwise, retrieve all published blog posts
            blog_posts = BlogPost.objects.filter(
                status="published",
                deleted_at=False,
            )
        # Instantiate the paginator
        paginator = BlogPostPagination()

        # Get the paginated result page based on the requested page number
        result_page = paginator.paginate_queryset(blog_posts, request)

        # Serialize the paginated blog posts using BlogSerializer
        serializer = BlogSerializer(result_page, many=True)

        # Loop through each blog post and retrieve its associated comments using CommentSerializer
        data = []
        for blog in serializer.data:
            comments = Comment.objects.filter(blog_post=blog["id"])
            comment_serializer = CommentSerializer(comments, many=True)
            blog["comments"] = comment_serializer.data
            data.append(blog)

        # Return a JSON response containing all matching blog posts and their comments
        if search_query:
            message = f"Result for '{search_query}'"
        else:
            message = "List of blogs"

        return paginator.get_paginated_response(
            {
                "status": True,
                "message": message,
                "data": data,
            }
        )
