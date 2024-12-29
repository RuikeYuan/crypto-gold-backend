from rest_framework import serializers
from .models import Thread, Post

# Thread Serializer
class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'user', 'created_at']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'thread', 'content', 'user', 'created_at']
