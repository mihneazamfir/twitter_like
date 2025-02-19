from rest_framework import serializers
from .models import User, Post, Like, Comment, Tag
from django.contrib.auth import get_user_model, authenticate

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=['username', 'password', 'last_name', 'first_name', 'email', 'follows']
        extra_kwargs = {'password': {'write-only': True, 'min_length': 8}}
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['id']
        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['id', 'text', 'shown_in_posts']
        read_only_fields = ['id']
        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']
        read_only_fields = ['id']
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'user']
        read_only_fields = ['id']