import jwt
from django.shortcuts import get_object_or_404
from config.settings import SECRET_KEY

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from users.views import token_refresh

class ProgressView(APIView):
    def post(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION', False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            
            progress = request.data.get('progress')  # 프론트에서 받아온 진도 값
            progress = int(progress)
            
            if progress < 0:
                return Response({'error': '진도 값은 음수일 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # User 모델의 progress 필드 업데이트
            user.progress = progress
            user.save()

            response_data = {'message': '진도가 성공적으로 업데이트되었습니다.'}
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "You need to refresh"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            # 유저 정보 체크 부분
            token = request.META.get('HTTP_AUTHORIZATION', False)[7:]
            if token:
                token = str(token).encode("utf-8")
            access = token
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            current_progress = user.progress
            return Response({'progress': current_progress}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "You need to refresh"}, status=status.HTTP_400_BAD_REQUEST)

