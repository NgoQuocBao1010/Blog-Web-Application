from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    coverImage = models.ImageField(default="blog1.jpg", upload_to="posts/")
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-dateCreated"]

    def __str__(self):
        return f"Post {self.title} from {self.author}"


class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dateCreated"]

    def __str__(self):
        return f"Comment by {self.commentor} on post {self.post.title} "
