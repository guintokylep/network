from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    postUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postUser")
    postDescription = models.TextField(blank=True)
    likers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name="user")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "postUser": self.postUser.username,
            "postUserId": self.postUser.id,
            "postDescription": self.postDescription,
            "likers": self.likers ,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }

class Profile(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userId")
    following = models.ManyToManyField(
        User, blank=True, null=True, related_name="following"
    )
    followers = models.ManyToManyField(
        User, blank=True,null=True, related_name="followers"
    )

    def serialize(self):
        return {
            "userId": self.userId.id,
            "username": self.user.username,
            "followers": self.followers,
            "following": self.following
        }