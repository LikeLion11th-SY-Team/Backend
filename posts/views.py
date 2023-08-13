import json,jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from .models import Post,Comment
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer,CommentCreateSerializer
from users.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

### CRUD 구현
### 게시판 분류를 어떻게 할 지 정해야 시작가능할 듯
### url로 나눌 것인지, ?category={id} 등으로 받아올 것인지...

class CommentView(APIView):
    def post(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIE.get('access',False)
            if token:
                token = str(token).split()[1].encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            #댓글 저장 부분
            post = get_object_or_404(Post, pk=post_pk)
            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                comment = serializer.save(commit=False)
                comment.post = post
                comment.commenter = user
                comment.save()
                return Response({"message":"Success"}, status = 200)
            return Response({"message":"Comment is not valid"},status=400)
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIE.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                post = get_object_or_404(Post, pk=post_pk)
                serializer = CommentCreateSerializer(data=request.data)
                if serializer.is_valid():
                    comment = serializer.save(commit=False)
                    comment.post = post
                    comment.commenter = user
                    comment.save()
                    return Response(
                        {
                            "message":"Success",
                            "token": {
                                    "access": access,
                                    "refresh": refresh,
                            },
                        }, status = 200
                    )
                return Response({"message":"Comment is not valid"},status=400)
            raise jwt.exceptions.InvalidTokenError
        
    def patch(self, request, post_pk,comment_pk):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user == comment.user:
                #comment = #comment_form.save(commit=False)
                #comment.save()
                return Response({"message":"Success"}, status = 200)
            return Response({"message":"Not a commenter"},status=400)
        return Response({"message":"Not a valid user"},status=400)
    

    def delete(request, article_pk, comment_pk):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user == comment.user:
                comment.delete()
                return Response({"message":"Success"}, status = 200)
            return Response({"message":"Not a commenter"},status=400)
        return Response({"message":"Not a valid user"},status=400)

@api_view(['POST'])
def likes(request, post_pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_pk)
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response({"message":"Success"}, status = 200)
    return Response({"message":"Please Login"}, status = 400)