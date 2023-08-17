import json,jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from .models import Post,Comment
from .serializers import PostSerializer, PostCreateSerializer,CommentCreateSerializer,CommentSerializer
from users.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



### CRUD 구현
### 게시판 분류를 어떻게 할 지 정해야 시작가능할 듯
### url로 나눌 것인지, ?category={id} 등으로 받아올 것인지...

class CommentView(APIView):
    def post(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            #댓글 저장 부분
            post = get_object_or_404(Post, pk=post_pk)
            data = request.data
            serializer = CommentCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post,commenter=user)
                return Response(
                    {
                        "message":"Success",
                        "comment":serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            return Response(
                    {
                        "message":"Comment is not valid",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                post = get_object_or_404(Post, pk=post_pk)
                data = request.data
                serializer = CommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(post=post,commenter=user)
                    return Response(
                        {
                            "message":"Success",
                            "comment":serializer.data,
                            "token":{
                                "access": access,
                                "refresh": refresh
                            },
                        },
                        status = status.HTTP_200_OK
                    )
                return Response(
                        {
                            "message":"Comment is not valid",
                            "token": {
                                "access": access,
                                "refresh": refresh
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            raise jwt.exceptions.InvalidTokenError
        
    def put(self, request, comment_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            #댓글 저장 부분
            comment = get_object_or_404(Comment,pk=comment_pk)
            serializer = CommentSerializer(instance=comment,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True) and comment.commenter==user:
                comment = serializer.save()
                return Response(
                    {
                        "message":"Success",
                        "comment":serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            return Response({"message":"Comment is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                comment = get_object_or_404(Comment, pk=comment_pk)
                serializer = CommentSerializer(instance=comment,data=request.data,partial=True)
                if serializer.is_valid(raise_exception=True) and comment.commenter==user:
                    comment = serializer.save()
                    return Response(
                        serializer.data,
                        {
                            "message":"Success",
                            "comment":serializer.data,
                            "token": {
                                    "access": access,
                                    "refresh": refresh,
                            },
                        },
                        status = status.HTTP_200_OK
                    )
                return Response({"message":"Comment is not valid"},status=400)
            raise jwt.exceptions.InvalidTokenError
    

    def delete(self, request, comment_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            comment = get_object_or_404(Comment, pk=comment_pk)
            if comment.commenter==user:
                comment.delete()
                return Response(
                    {
                        "message":"Success",
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message":"Different Commenter",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                comment = get_object_or_404(Comment, pk=comment_pk)
            
                if comment.commenter==user:
                    comment.delete()
                    return Response(
                        {
                            "message":"Success",
                            "token": {
                                    "access": access,
                                    "refresh": refresh,
                            },
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "message":"Different Commenter",
                            "token": {
                                    "access": access,
                                    "refresh": refresh,
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            raise jwt.exceptions.InvalidTokenError


@api_view(['GET'])
def like_post(request, post_pk):
    try:
        # 유저 정보 체크 부분
        token = request.COOKIES.get('access',False)
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        
        #좋아요 부분
        post = get_object_or_404(Post, pk=post_pk)
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response({"message":"Success"},status=status.HTTP_200_OK)
    except(jwt.exceptions.ExpiredSignatureError):
        # 토큰 만료 시 토큰 갱신
        data = {'refresh': request.COOKIES.get('refresh', None)}
        serializer = TokenRefreshSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            access = serializer.data.get('access', None)
            refresh = serializer.data.get('refresh', None)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            post = get_object_or_404(Post, pk=post_pk)
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            return Response(
                {
                    "message":"Success",
                    "token": {
                        "access": access,
                        "refresh": refresh,
                    },
                },
                status=status.HTTP_200_OK
            )
        raise jwt.exceptions.InvalidTokenError

class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        user, access = handle_token(request)
        if not user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        posts = Post.objects.filter(category=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        user, access = handle_token(request)
        if not user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': '글 작성에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    def view_detail(self, request, post_pk):
        user, access = handle_token(request)
        if not user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_pk):
        user, access = handle_token(request)
        if not user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        if post.writer != user:
            return Response({'error': '글 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': '글 수정에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        user, access = handle_token(request)
        if not user:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        if post.writer != user:
            return Response({'error': '글 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)