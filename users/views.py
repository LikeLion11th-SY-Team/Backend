import jwt
import json, string, random
from .models import User
from .jwt_serializers import SpartaTokenObtainPairSerializer,UserModelSerializer,UserSignUpSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from config.settings import SECRET_KEY,EMAIL_HOST_USER
from posts.models import Post,Comment
from posts.serializers import CommentListSerializer,PostListSerializer

@api_view(['GET'])
def token_refresh(refresh):
    if refresh:
        try:
            refresh = RefreshToken(refresh)
            access = refresh.access_token

            return Response(
                {
                    "token": 
                        {
                            'access': str(access),
                            'refresh': str(refresh)
                        }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    def post(self, request):
        data             = json.loads(request.body)
        try:
            data['username'] = data.pop('id')
            data['password'] = data.pop('pw')
            data['nick_name'] = data.pop('nickname')
            data['email'] = data.pop('fullEmail')
            data['phone_number'] = data['phoneNumber']
            phone_number = data['phone_number']
            email        = data['email']
            if phone_number != "" and User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {"message":"Duplicate_PhoneNumber"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            elif email != "" and User.objects.filter(email=email).exists():
                return Response(
                    {"message":"Duplicate_UserEmail"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer_class = UserSignUpSerializer(data=data)
                if serializer_class.is_valid():
                    user = serializer_class.save()
                    token = SpartaTokenObtainPairSerializer.get_token(user)
                    refresh_token = str(token)
                    access_token = str(token.access_token)
                    return Response({
                            "message": "Signup Success",
                            "access":access_token,
                            "refresh":refresh_token
                        },
                        status = status.HTTP_200_OK)
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message":"KEY_ERROR"}, status = 400)

class UserAPIView(APIView):
    # 토큰으로 로그인
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response({'user':serializer.data}, status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserModelSerializer(instance=user)
                return Response(
                            {   
                                'user': serializer.data,
                                "token":{
                                    "access":access,
                                    "refresh":refresh
                                }
                            },
                            status = status.HTTP_200_OK)
            return res
    # id pw 로 로그인
    def post(self, request):
        user = authenticate(
            username=request.data.get("id"), password=request.data.get("pw")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            # jwt 토큰 접근
            token = SpartaTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            if user.is_reseted:
                res =  Response({
                    "message": "Login Success, Password Reset Required",
                    "token":{
                        "access":access_token,
                        "refresh":refresh_token
                    }
                    },status = status.HTTP_200_OK)
            else:
                res =  Response({
                    "message": "Login Success",
                    "token":{
                        "access":access_token,
                        "refresh":refresh_token
                    }
                    },status = status.HTTP_200_OK)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # 로그아웃
    def delete(self, request):
        logout(request)
        res =  Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie('access')
        res.delete_cookie('refresh')
        return res
    
## 아이디 중복 api
@api_view(['POST'])
def checkDuplicatedID(request):
    data = json.loads(request.body)
    if User.objects.filter(username = data['id']).exists():
        return Response({
            "message": "Duplicated id"
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "message": "Accepted"
        }, status=status.HTTP_200_OK)

## 아이디 중복 api
@api_view(['POST'])
def checkDuplicatedNickname(request):
    data = json.loads(request.body)
    if User.objects.filter(nick_name = data['nickname']).exists():
        return Response({
            "message": "Duplicated nickname"
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
        "message": "Accepted"
        }, status=status.HTTP_200_OK)

## 닉네임 요청
@api_view(['GET'])
def getNickname(request):
    if request.method == 'GET':
        try:
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response(serializer.data['nick_name'], status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserModelSerializer(instance=user)
                res = Response(
                        {
                            "nickname" : serializer.data['nick_name'],
                            "message": "Success",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status=status.HTTP_200_OK
                    )
            return res


class UserinfoView(APIView):
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserModelSerializer(instance=user)
                res= Response(
                        {
                            "userInfo" : serializer.data,
                            "message": "Success",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status=status.HTTP_200_OK
                    )
            return res
    def patch(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            data=request.data
            phone_number = request.POST.get('phone_number', default=None)
            email        = request.POST.get('email', default=None)
            if phone_number and User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {"message":"Duplicate_PhoneNumber"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            elif email and User.objects.filter(email=email).exists():
                return Response(
                    {"message":"Duplicate_UserEmail"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            
            serializer = UserModelSerializer(instance=user,data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            res = token_refresh(request.COOKIES.get('refresh', None))
            if res.status_code==200:
                access = res.data["access"]
                refresh = res.data["refresh"]
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                data=request.data
                phone_number = request.POST.get('phone_number', default=None)
                email        = request.POST.get('email', default=None)
                if phone_number and User.objects.filter(phone_number=phone_number).exists():
                    return Response(
                        {
                            "message":"Duplicate_PhoneNumber",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )
                elif email and User.objects.filter(email=email).exists():
                    return Response(
                        {
                            "message":"Duplicate_UserEmail",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )
                
                serializer = UserModelSerializer(instance=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                res = Response(
                        {
                            "userInfo" : serializer.data,
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status=status.HTTP_200_OK
                    )
            return res
        
@api_view(['POST']) 
def changePassword(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)


        user_info = json.loads(request.body)
        current_pw = user_info["current_password"]
        new_pw = user_info["new_password"]

        if user.check_password(current_pw):
            user.set_password(new_pw)
            user.is_reseted = False
            user.save()
            return Response({"message": "Password change success"}, status=status.HTTP_200_OK)
        else: 
            return Response({"message": "Current password is different"},status=status.HTTP_400_BAD_REQUEST)
    except(jwt.exceptions.ExpiredSignatureError):
        # 토큰 만료 시 토큰 갱신
        res = token_refresh(request.COOKIES.get('refresh', None))
        if res.status_code==200:
            access = res.data["access"]
            refresh = res.data["refresh"]
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            user_info = json.loads(request.body)
            current_pw = user_info["current_password"]
            new_pw = user_info["new_password"]

            if user.check_password(current_pw):
                user.set_password(new_pw)
                user.save()
                res = Response(
                        {
                            "message": "Password change success",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status=status.HTTP_200_OK
                    )
            else: 
                res = Response(
                        {
                            "message": "Current password is different",
                            "token":{
                                "access":access,
                                "refresh":refresh
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return res
        

@api_view(['GET'])
def myPosts(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        mypost_list = Post.objects.filter(writer=user)
        myposts = []
        for post in mypost_list:
            myposts.append(PostListSerializer(instance=post).data)
            myposts[-1].pop('writer')
            myposts[-1].pop('likes')
        return Response(
            {
                "message": "Success",
                'myposts': myposts
            },
            status=status.HTTP_200_OK
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

            myposts = Post.objects.filter(writer=user)

            res = Response(
                {
                    "message": "Success",
                    "token":{
                        "access":access,
                        "refresh":refresh
                    },
                    "myposts": myposts
                }, 
                status=status.HTTP_200_OK
            )
        return res

@api_view(['GET'])
def myComments(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        mycomment_list = Comment.objects.filter(commenter=user)
        mycomments = []
        for comment in mycomment_list:
            mycomments.append(CommentListSerializer(instance=comment).data)
            mycomments[-1].pop('commenter')
            mycomments[-1].pop('post')
        return Response(
            {
                "message": "Success",
                'mycomments': mycomments
            },
            status=status.HTTP_200_OK
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

            myposts = Post.objects.filter(writer=user)

            res = Response(
                {
                    "message": "Success",
                    "token":{
                        "access":access,
                        "refresh":refresh
                    },
                    "myposts": myposts
                }, 
                status=status.HTTP_200_OK
            )
        return res

    
@api_view(['GET'])
def myLikes(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
        if token:
            token = str(token).encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        likepost_list = user.like_posts.all()
        likeposts = []
        for post in likepost_list:
            likeposts.append(PostListSerializer(instance=post).data)
            likeposts[-1].pop('writer')
            likeposts[-1].pop('likes')
        return Response(
            {
                "message": "Success",
                'likeposts': likeposts
            },
            status=status.HTTP_200_OK
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
            likepost_list = user.post_set.all()
            likeposts = []
            for post in likepost_list:
                likeposts.append(PostListSerializer(instance=post).data)
                likeposts[-1].pop('writer')
                likeposts[-1].pop('likes')
            res = Response(
                {
                    "message": "Success",
                    "token":{
                        "access":access,
                        "refresh":refresh
                    },
                    'likeposts': likeposts
                },
                status=status.HTTP_200_OK
            )
        return res

class ForgetIDView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        email = json.loads(request.body)['email']
        user = User.objects.get(email = email)
        if user is not None:
            method_email = EmailMessage(
                'Your ID is in the email',
                str(user.username),
                EMAIL_HOST_USER,
                [email],
            )
            method_email.send(fail_silently=False)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

def randomConfirmKey():
    string_pool = string.ascii_letters+string.digits
    result = "" # 결과 값
    for i in range(16) :
        # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합을 한다.
        result += random.choice(string_pool)
    return result

class ForgetPasswordView(APIView):
    def get(self, request):
        pass
    def post(self, request):
        email = json.loads(request.body)['email']
        username = json.loads(request.body)['username']
        user = User.objects.get(email = email,username=username)
        randomPW = randomConfirmKey()
        if user is not None:
            method_email = EmailMessage(
                'Your tmp Password is in the email',
                randomPW,
                EMAIL_HOST_USER,
                [email],
            )
            method_email.send(fail_silently=False)
            user.is_reseted = True
            user.set_password(randomPW)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)