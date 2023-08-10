from rest_framework import serializers

from users.jwt_serializers import UserModelSerializer
from . import models

class PostSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)

    class Meta:
        model = models.Post
        field = ("pk","writer","title","contents","created_at","updated_at","view_count","likes")

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        field = ("title","category","contents")