from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username.")
        if not email:
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    follows = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # Ensures email is required when creating superusers

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post #{self.id} by {self.author.username}"  # Fixed author reference


class Tag(models.Model):
    text = models.CharField(max_length=50, unique=True)
    shown_in_posts = models.ManyToManyField(Post, related_name="tags")  # Changed related_name to "tags"

    def __str__(self):
        return f"#{self.text}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")  # Made related_name clearer
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"like by {self.author.username} to post #{self.post.id}"


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # Pluralized related_name
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # Pluralized related_name

    def __str__(self):
        return f"comment by {self.author.username} on post #{self.post.id}"
