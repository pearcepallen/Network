from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField()

    def serialize(self):
        return {
            "username": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "like": self.like
        }
