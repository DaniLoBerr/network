from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Enables asymmetric following between users via a ManyToMany
    relationship. A user can follow multiple users and be followed by
    multiple users without automatic reciprocity.

    :attr following: Users that this user follows. Uses
        related_name='followers' to access followers.
    :type following: ManyToManyField
    """
    following = models.ManyToManyField(
        "self",
        blank=True,
        related_name="followers",
        symmetrical=False,
    )

    def __str__(self):
        """Return the user's username."""
        return self.username


class Post(models.Model):
    """Model representing individual posts created by users.
    
    :attr user: The user that published the post.
    :type user: ForeignKey
    :attr content: The text content of the post.
    :type content: str
    :attr created_at: The date and time when the post was created.
    :type created_at: DateTimeField
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return the poster's username and creation date."""
        return f"Post by {self.user.username} at {self.created_at}"


class Like(models.Model):
    """Model representing individual likes placed by users on posts.
    
    :attr user: The user that placed the like.
    :type user: ForeignKey
    :attr post: The post that received the like.
    :type post: ForeignKey
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        """Return a string representation of the like."""
        return f"{self.user.username} liked {self.post.user.username}'s post."