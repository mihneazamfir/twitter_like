from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    follows = models.ManyToManyField('self')
    
    def __str__(self):
        return f"{self.username}"
    
    def create_user(self, first_name, last_name, username, email, password)

class Post(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    
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