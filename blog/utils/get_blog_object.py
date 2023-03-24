from blog.models import BlogPost
from rest_framework.exceptions import NotFound


def get_object(id):
    try:
        return BlogPost.objects.get(id=id, deleted_at=False)
    except BlogPost.DoesNotExist:
        raise NotFound({
            "status": False,
            "message": "Blog Post Does Not Exist.",
            "data": None
        })
