from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Like, Post
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like(request, post_id):
    author = request.user
    post = Post.objects.get(id=post_id)
    
    if not post:
        return Response({"error": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if Like.objects.filter(author=author, post=post).exists():
        return Response({"error": "Like already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    like = Like(author=author, post=post)
    like.save()
    
    return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unlike(request, post_id):
    author = request.user
    post = Post.objects.get(id=post_id)
    
    try:
        like = Like.objects.get(author=author, post=post)
        like.delete()
        return Response({"message": "Like deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({"error": "Like does not exist."}, status=status.HTTP_400_BAD_REQUEST)