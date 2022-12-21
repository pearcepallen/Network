from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
#    def __str__(self):
    #    return f"{self.id}: {self.username}"
    # pass
    id = models.AutoField(primary_key=True)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }

class Following(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following_user")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return f"User: {self.user} | Following: {self.following}"

    class Meta:
        unique_together = ["user", "following"]

    def clean(self):
        if self.user == self.following:
            raise ValidationError("Cannot follow self")

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    user = models.ForeignKey("User", on_delete=models.CASCADE)
        
    def __str__(self):
       return f"{self.post}: User{self.user}"

    class Meta:
        unique_together = ["post", "user"]
