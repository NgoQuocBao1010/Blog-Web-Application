from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-dateCreated"]

    def __str__(self):
        return f"Post {self.title} from {self.user}"


class Comments(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commentor} on post {self.post.title} "
