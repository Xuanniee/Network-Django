from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    # Inherits from AbstractUser so it already have Username, Password, E-mail etc
    id = models.BigAutoField(primary_key=True)
    following_list = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="Followers")

    def __str__(self):
        if not self.id:
            return "Anonymous"
        return f"Username: {self.username}; Email: {self.email}; Following List: {self.following_list}"

class UserProfile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    # Size of Uploads can be limited / controlled in forms.py
    profile_picture = models.ImageField(upload_to='uploads', default="uploads/Default-Profile.png", null=True)
    # follower_count = models.PositiveIntegerField()
    # following_count =  models.PositiveBigIntegerField()

    # One to One R/S as each User can only have 1 Profile and vice versa
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="User_Profile")

    def __str__(self):
        return f"{self.profile_id} belongs to User {self.user}"

class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    post_content = models.TextField()
    post_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Post_Created")
    post_edited = models.BooleanField(default=False)
    post_edited_timestamp = models.DateTimeField(auto_now=True, verbose_name="Post_Edited", null=True, blank=True)    # Only updated for Model.save(). May be empty as may not be edited
    post_num_likes = models.IntegerField(default=0)

    # A Post can be liked by many Users. A User can like many Posts
    post_likes_list = models.ManyToManyField(User, related_name="Posts_Liked")

    # Many to One R/S (FK only MtO) Many Posts to One User (Must Define In Posts)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Author")

    class Meta:
        # Minus Sign for Reverse Chronological Order
        ordering = ['-post_timestamp']

    def __str__(self):
        return f"Post {self.post_id}:\
                 Edited: {self.post_edited}. If True, it was edited on {self.post_edited_timestamp}\
                 Likes List: {self.post_likes_list}\
                 Posted by: {self.user}\
                 Content: {self.post_content}"

class PostComment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    comment_content = models.TextField()
    comment_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Comment_Created")
    comment_edited_timestamp = models.DateTimeField(auto_now=True, verbose_name="Comment_Edited")

    # Many Comments to One Post/One User
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Original_Post")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commentator")

    # Metadata for the Comments Model
    class Meta:
        ordering = ['comment_timestamp']

    def __str__(self):
        if not self.commentator:
            return "Anonymous"
        return f"Comment by {self.commentator.username} on {self.post}"