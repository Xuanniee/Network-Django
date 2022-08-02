from django.contrib import admin

from .models import User, UserProfile, Post, PostComment

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Post)
# admin.site.register(Follower)
# admin.site.register(Following)
admin.site.register(PostComment)


