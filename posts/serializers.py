from rest_framework import serializers

from users.jwt_serializers import UserModelSerializer
from . import models

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["pk","content","post","commenter","created_at","updated_at"]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["pk","content","post","commenter"]
        read_only_fields = ["post","commenter"]

class PostSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = models.Post
        fields = ["pk","writer","title","contents","created_at","updated_at","view_count","likes","comments"]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ["title","category","contents"]