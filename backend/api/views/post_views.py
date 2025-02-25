from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import User, Post, Tag
from core.serializers import PostSerializer, LikeSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    serializer = PostSerializer(data=request.data)
    author = User.objects.get(username=request.user.username)
    tags = request.data.get("tags", [])
    for tag_name in tags:
        tag, _ = Tag.objects.get_or_create(text=tag_name.lower())
        serializer.tags.add(tag)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePost(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author != request.user:
            return Response({"error": "You can only delete your own posts."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPost(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def getPosts(request):
    posts = Post.objects.all().order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getUserPosts(request, user_username):
    try:
        user = User.objects.get(username=user_username)
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLikes(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)