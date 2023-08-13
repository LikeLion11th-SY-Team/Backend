import jwt
import json
from .models import User
from .jwt_serializers import SpartaTokenObtainPairSerializer,UserModelSerializer,UserSignUpSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY
import bcrypt


class SpartaTokenObtainPairView(TokenObtainPairView):
    serializer_class = SpartaTokenObtainPairSerializer

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
                    return Response(
                        {
                            "message": "Signup Success",
                            "token": {
                                "access": access_token,
                                "refresh": refresh_token,
                            },
                        },
                        status = status.HTTP_200_OK,
                    )
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message":"KEY_ERROR"}, status = 400)

class UserAPIView(APIView):
    # 토큰으로 로그인
    def get(self, request):
        try:
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).split()[1].encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                serializer = UserModelSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError
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
            return Response(
                {
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
    
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
            token = request.COOKIES.get('access',False)
            if token:
                token = str(token).split()[1].encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response(serializer.data['nick_name'], status=status.HTTP_200_OK)
        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh',False)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserModelSerializer(instance=user)
                return Response(
                        {
                            "nickname" : serializer.data['nick_name'],
                            "message": "Success",
                            "token": {
                                "access": access,
                                "refresh": refresh,
                            },
                        },
                        status=status.HTTP_200_OK
                    )
            raise jwt.exceptions.InvalidTokenError


class UserinfoView(APIView):
    def get(self, request):
        try:
            token = request.COOKIE.get('access',False)
            if token:
                token = str(token).split()[1].encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserModelSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                serializer = UserModelSerializer(instance=user)
                return Response(
                        {
                            "userInfo" : serializer.data,
                            "message": "Success",
                            "token": {
                                "access": access,
                                "refresh": refresh,
                            },
                        },
                        status=status.HTTP_200_OK
                    )
            raise jwt.exceptions.InvalidTokenError
    def patch(self, request):
        try:
            token = request.COOKIE.get('access',False)
            if token:
                token = str(token).split()[1].encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            data=request.data
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
            serializer = UserModelSerializer(instance=user,data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                serializer = UserModelSerializer(instance=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                        {
                            "userInfo" : serializer.data,
                            "token": {
                                "access": access,
                                "refresh": refresh,
                            },
                        },
                        status=status.HTTP_200_OK
                    )
            raise jwt.exceptions.InvalidTokenError
        
@api_view(['POST']) 
def changePassword(request):
    try:
        token = request.COOKIE.get('access',False)
        if token:
            token = str(token).split()[1].encode("utf-8")
        access = token
        payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)


        user_info = json.loads(request.body)
        current_pw = user_info["current_password"]
        new_pw = user_info["new_password"]

        if user.check_password(current_pw):
            user.set_password(new_pw)
            
            user.save()
            return Response({"message": "Password change success"}, status=status.HTTP_200_OK)
        else: 
            return Response({"message": "Current password is different"},status=status.HTTP_400_BAD_REQUEST)
    except(jwt.exceptions.ExpiredSignatureError):
        # 토큰 만료 시 토큰 갱신
        data = {'refresh': request.COOKIE.get('refresh',None)}
        serializer = TokenRefreshSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            access = serializer.data.get('access', None)
            refresh = serializer.data.get('refresh', None)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            user_info = json.loads(request.body)
            current_pw = user_info["current_password"]
            new_pw = user_info["new_password"]

            if user.check_password(current_pw):
                user.set_password(new_pw)
                user.save()
                return Response(
                        {
                            "message": "Password change success",
                            "token": {
                                "access": access,
                                "refresh": refresh,
                            }
                        },
                        status=status.HTTP_200_OK
                    )
            else: 
                return Response(
                        {
                            "message": "Current password is different",
                            "token": {
                                "access": access,
                                "refresh": refresh,
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        raise jwt.exceptions.InvalidTokenError

@api_view(['POST'])
def recoveryID(request):
    pass

@api_view(['POST'])
def recoveryPassword(request):
    pass