import json,jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from .models import Post,Comment
from .serializers import PostSerializer,CommentCreateSerializer,CommentSerializer,PostCreateSerializer
from users.models import User
from users.views import token_refresh

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
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                post = get_object_or_404(Post, pk=post_pk)
                data = request.data
                serializer = CommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(post=post,commenter=user)
                    res =  Response(
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
                else:
                    res = Response(
                        {
                            "message":"Comment is not valid",
                            "token": {
                                "access": access,
                                "refresh": refresh
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return res
        
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
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                comment = get_object_or_404(Comment, pk=comment_pk)
                serializer = CommentSerializer(instance=comment,data=request.data,partial=True)
                if serializer.is_valid(raise_exception=True) and comment.commenter==user:
                    comment = serializer.save()
                    res = Response(
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
                else:
                    res = Response(
                        {
                            "message":"Comment is not valid",
                            "token": {
                                    "access": access,
                                    "refresh": refresh,
                            },
                        },
                        status=400
                    )
            return res
    

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
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                comment = get_object_or_404(Comment, pk=comment_pk)
            
                if comment.commenter==user:
                    comment.delete()
                    res = Response(
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
                    res = Response(
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

class PostView(APIView):
    def get(self, request, category):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            if not user:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

            posts = Post.objects.filter(category=category)
            data = PostSerializer(posts, many=True).data
            for post in data:
                post.pop('writer')
                post.pop('likes')
                post.pop('contents')

            return Response(data)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                
                posts = Post.objects.filter(category=category)
                data = PostSerializer(posts, many=True).data
                for post in data:
                    post.pop('writer')
                    post.pop('likes')
                    post.pop('contents')
                data.append({"token":{
                                    "access": access,
                                    "refresh": refresh
                                }})
                res = Response(data)
            return res
                
    def post(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(writer=user)
                serializer = PostSerializer(instance=get_object_or_404(Post,pk=serializer.data["pk"]))
                data = serializer.data
                data.pop("writer")
                data.pop("likes")
                return Response(data, status=status.HTTP_201_CREATED)
            return Response({'error': '글 작성에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                serializer = PostCreateSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(writer=user)
                    serializer = PostSerializer(instance=get_object_or_404(Post,pk=serializer.data["pk"]))
                    data = serializer.data
                    data.pop("writer")
                    data.pop("likes")
                    data["token"] = {
                                        "access": access,
                                        "refresh": refresh
                                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                return Response({'error': '글 작성에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return res
    
    @api_view(['GET'])
    def view_detail(request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            if not user:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            data = PostSerializer(post).data
            data.pop("writer")
            data.pop("likes")
            return Response(data,status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)

                if not user:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
                try:
                    post = Post.objects.get(pk=post_pk)
                except Post.DoesNotExist:
                    return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                data = PostSerializer(post).data
                data.pop("writer")
                data.pop("likes")
                data["token"] = {
                                    "access": access,
                                    "refresh": refresh
                                }
                return Response(data,status=status.HTTP_200_OK)
            return res
    def put(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            if not user:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                post = Post.objects.get(pk=post_pk)
            except Post.DoesNotExist:
                return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            if post.writer != user:
                return Response({'error': '글 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = PostSerializer(post, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data.pop("writer")
                data.pop("likes")
                return Response(data)
            return Response({'error': '글 수정에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                if not user:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

                try:
                    post = Post.objects.get(pk=post_pk)
                except Post.DoesNotExist:
                    return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                
                if post.writer != user:
                    return Response({'error': '글 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

                serializer = PostSerializer(post, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    data.pop("writer")
                    data.pop("likes")
                    data["token"] = {
                                        "access": access,
                                        "refresh": refresh
                                    }
                    return Response(data)
                return Response({'error': '글 수정에 실패하였습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            return res
    def delete(self, request, post_pk):
        try:
            # 유저 정보 체크 부분
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
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
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                if not user:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

                try:
                    post = Post.objects.get(pk=post_pk)
                except Post.DoesNotExist:
                    return Response({'error': '해당 글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                
                if post.writer != user:
                    return Response({'error': '글 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

                post.delete()
                data = {"token":
                        {
                            "access": access,
                            "refresh": refresh
                        }
                }
                return Response(data,status=status.HTTP_204_NO_CONTENT)
            return res

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
        res = token_refresh(request.COOKIES.get('refresh', None))
        if res.status_code==200:
            access = res.data["access"]
            refresh = res.data["refresh"]
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            post = get_object_or_404(Post, pk=post_pk)
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            res = Response(
                {
                    "message":"Success",
                    "token": {
                        "access": access,
                        "refresh": refresh,
                    },
                },
                status=status.HTTP_200_OK
            )
        return res