# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from allauth.socialaccount.models import SocialAccount
# # from user.models import User as UserModel

# class KakaoLoginView(APIView):

#     def post(self, request):
#         email = request.data.get("email")

#         try:
#             # 기존에 가입된 유저와 쿼리해서 존재하면서, socialaccount에도 존재하면 로그인
#             # user = UserModel.objects.get(email=email) => db 테이블 이름을 아직 정하지 않음
#             social_user = SocialAccount.objects.filter(user=user).first()

#             if social_user:
#                 # 카카오로 가입된 유저가 로그인하는 경우
#                 if social_user.provider == "kakao":
#                     # JWT Access Token 발급
#                     refresh = RefreshToken.for_user(user)
#                     return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "로그인 성공"}, status=status.HTTP_200_OK)
#                 else:
#                     # 카카오로 가입되지 않은 유저가 카카오로 로그인하려는 경우 에러 반환
#                     return Response({"error": "카카오로 가입된 유저가 아닙니다. 카카오로 로그인을 시도해주세요."}, status=status.HTTP_400_BAD_REQUEST)

#             else:
#                 # 이메일로 가입된 유저가 카카오로 로그인하려는 경우 에러 반환
#                 return Response({"error": "이메일로 가입된 유저가 아닙니다. 이메일로 로그인을 시도해주세요."}, status=status.HTTP_400_BAD_REQUEST)

#         except UserModel.DoesNotExist:
#             # 이메일로 가입되지 않은 유저가 카카오로 로그인하려는 경우 카카오 회원가입 로직으로 이동
#             # 카카오 회원가입을 위한 로직 구현
#             nickname = generate_random_nickname()  # 랜덤 닉네임 생성
#             new_user = UserModel.objects.create(
#                 nickname=nickname,  # 랜덤 닉네임 사용
#                 email=email,
#             )
#             SocialAccount.objects.create(
#                 user_id=new_user.id,
#             )
#             # JWT Access Token 발급
#             refresh = RefreshToken.for_user(new_user)
#             return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "카카오 회원가입 및 로그인 성공"}, status=status.HTTP_201_CREATED)
