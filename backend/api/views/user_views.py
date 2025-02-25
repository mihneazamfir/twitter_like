from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.models import User
from core.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def getUserProfile(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def followUser(request, username):
    author = request.user
    target = User.objects.get(username=username)
    
    if author is target:
        return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    if not target:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if target in author.follows.all():
        return Response({"error": "Follow already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    author.follows.add(target)
    return Response({"message": "User followed."}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollowUser(request, username):
    author = request.user
    target = User.objects.get(username=username)
    
    if author is target:
        return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    if not target:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    if not (target in author.follows.all()):
        return Response({"error": "You are already not following this user."}, status=status.HTTP_400_BAD_REQUEST)
    
    author.follows.remove(target)
    return Response({"message": "User unfollowed."}, status=status.HTTP_201_CREATED)