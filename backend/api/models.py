from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        
        if not username:
            raise ValueError('User must have an username.')
        user = self.model(username=self.normalize_email(username), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100, unique=True)
    follows = models.ManyToManyField('self')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"post #{self.id} by {self.username}"

class Tag(models.Model):
    
    text = models.CharField(max_length=50)
    shown_in_posts = models.ManyToManyField(Post, related_name="posts")
    
    def __str__(self):
        return f"#{self.text}"
    
class Like(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post-likes")
    user = models.ForeignKey(User, related_name="user-likes")
    
    def __str__(self):
        return f"like by {self.user} to {self.post}"
    
class Comment(models.Model):
    
    text = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post-comment")
    user = models.ForeignKey(User, related_name="user-comment")
    
    def __str__(self):
        return f"comment by {self.user} to {self.post}"