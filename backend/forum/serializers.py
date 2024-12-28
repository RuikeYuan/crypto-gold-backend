from rest_framework import serializers
from .models import Thread, Post

# Thread Serializer
class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for the Thread model.
    """
    class Meta:
        model = Thread
        fields = ['id', 'title', 'created_at']  # Include necessary fields

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    class Meta:
        model = Post
        fields = ['id', 'content', 'thread', 'created_at']  # Include necessary fields

    # Optional: Custom validation for the content field
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value
