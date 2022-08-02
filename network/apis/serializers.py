from rest_framework import serializers

from network.models import User, Post


# Create Serializers for Models
class UserEasySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'following_list', )

class PostEasySerializer(serializers.ModelSerializer):
    author = UserEasySerializer(required=False, read_only=True)
    likes_list = UserEasySerializer(many=True, required=False, read_only=True)

    # Specify Model and Fields
    class Meta:
        model = Post
        fields = ('post_id', 'post_content', 'post_timestamp', 'post_edited', 'post_edited_timestamp', 'likes_list', 'author', 'post_num_likes', )

# Not Used for Now
class PostSerializer(serializers.Serializer):
    post_content = serializers.CharField()
    post_timestamp = serializers.DateTimeField()
    post_edited = serializers.BooleanField()
    post_edited_timestamp = serializers.DateTimeField()