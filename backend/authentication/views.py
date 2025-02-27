from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from core.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    
    return Response({"error": "Invalid credentials"}, status=400)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status = 201)
        
    return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({"message": "Logged out successfully."}, status=200)
    
    except Exception:
        return Response({"error": "Invalid refresh token."}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)
        
        new_token = RefreshToken(refresh_token).access_token
        return Response({"access": str(new_token)})

    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=400)