from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.serializers import CommentSerializer
from core.models import Post, Comment
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createComment(request, post_id):
    author = request.user
    post = Post.objects.get(id=post_id)
    text = request.data.get('text')
    
    if not post:
        return Response({"error": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if not text:
        return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    comment = Comment(author=author, post=post, text=text)
    comment.save()
    
    return Response({"message": "Post commented."}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([AllowAny])
def getComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if not comment:
        return Response({"error": "Comment does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if comment.author != request.user:
        return Response({"error": "You do not have permission."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response({"error": "Comment does not exist."}, status=status.HTTP_400_BAD_REQUEST)