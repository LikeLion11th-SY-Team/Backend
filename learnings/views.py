import jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import LearningProgress
from users.models import User
from users.views import token_refresh

class ProgressView(APIView):
    def post(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            progress = request.data.get('progress')  # 프론트에서 보낸 진도 값
            progress = int(progress)
            
            if progress < 0:
                return Response({'error': '진도 값은 음수일 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            learning_progress, created = LearningProgress.objects.get_or_create(user=user)
            learning_progress.progress = progress
            learning_progress.save()

            response_data = {'message': '진도가 성공적으로 업데이트되었습니다.'}
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION',False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access,SECRET_KEY,algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            progress = request.data.get('progress')  # 프론트에서 보낸 진도 값
            progress = int(progress)
            try:
                learning_progress = LearningProgress.objects.get(user=user)
                current_progress = learning_progress.progress
                return Response({'progress': current_progress}, status=status.HTTP_200_OK)
            except LearningProgress.DoesNotExist:
                return Response({'error': '진도 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"message" : "You need to refresh"},status=status.HTTP_400_BAD_REQUEST)
        

