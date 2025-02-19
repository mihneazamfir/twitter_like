from django.shortcuts import render
from .models import User, Post, Like, Comment, Tag
from rest_framework import generics
from .serializers import UserSerializer, PostSerializer, TagSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

