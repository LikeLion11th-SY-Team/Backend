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

class PostListSerializer(PostSerializer):
    writer = serializers.StringRelatedField()
    writer_nickname = serializers.CharField(source='writer.nick_name',read_only=True)
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.IntegerField(source='likes.count',read_only=True)
    class Meta(PostSerializer.Meta):
        fields = ['pk','title','writer_nickname','created_at','likes_count','writer','likes']
        depth=1

class CommentListSerializer(CommentSerializer):
    post = serializers.StringRelatedField()
    post_pk = serializers.IntegerField(source='post.pk',read_only=True)
    commenter = serializers.StringRelatedField()
    commenter_nickname = serializers.CharField(source='commenter.nick_name',read_only=True)
    class Meta(CommentSerializer.Meta):
        fields = ['pk','post_pk','commenter_nickname','content','created_at','updated_at','post','commenter']
        depth=1