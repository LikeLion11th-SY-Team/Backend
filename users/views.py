from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render,redirect
from .models import User
from django.http import JsonResponse
from django.views import View
import json
import bcrypt

# FBV ver
def loginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate( username=username, password=password)
        if user is not None:
            print("인증성공")
            login(request,user)
        else:
            print("인증실패")
    return render(request, "users/login_test.html")

def logoutView(request):
    logout(request)

    #지금은 테스트를 위에 로그인으로, 메인 페이지 나오면 그때 메인페이지로 동작할 듯
    return redirect("users:login")

def signupView(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message":"Duplicate_UserID"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message":"Duplicate_UserEmail"}, status=400)
        if not ('@' in email) or not ('.' in email):
            return JsonResponse({"message":"Enter a valid UserEmail"}, status=400)

        if request.POST['password']==request.POST['password_check']:
            user = User.objects.create(username=username,email=email,password=password)
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request,user)
            return render(request, "users/login.html")
        return render(request,'users/signup_test.html')
    return render(request, "users/signup_test.html")



# CBV ver
# json to json, not render in post
class SignupView(View):
    def post(self, request):
        
        # 밑의 주석 코드는 서버 가동 시 실제로 사용될 코드 (프론트이 json파일을 가져오는 코드)
        #data = json.loads(request.body)
        # 밑의 코드는 테스트를 위해 json이 아닌 request 메세지를 그대로 받는 코드
        data = request.POST

        try:
            # 데이터 추출
            username = data['username']
            email = data['email']
            password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()
            phone_number = data['phone_number']
            first_name = data['first_name']
            last_name = data['last_name']

            ## 비밀번호 및 아이디의 유효성 검사는 프론트엔드에서 하는 것으로 가정
            # id 중복
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message":"Duplicate_UserID"}, status=400)
            # email 유효성
            if not ('@' in email) or not ('.' in email):
                return JsonResponse({"message":"Enter a valid UserEmail"}, status=400)            
            # email 중복
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"Duplicate_UserEmail"}, status=400)
            
            #정보 전달, 저장
            user = User.objects.create(username=username,email=email,password=password)
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            #회원가입 후 로그인 유지로 결정난 경우 하단 코드 실행
            #login(request,user)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status = 400)
    
    def get(self, request):
        return render(request, "users/signup_test.html")
    
class LoginView(View):
    def post(self, request):
        
        # 밑의 주석 코드는 서버 가동 시 실제로 사용될 코드 (프론트이 json파일을 가져오는 코드)
        #data = json.loads(request.body)
        # 밑의 코드는 테스트를 위해 json이 아닌 request 메세지를 그대로 받는 코드
        data = request.POST

        try:
            username = data['username']
            password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()
            user = authenticate( username=username, password=password)
            if user is not None:
                print("인증성공")
                login(request,user)
                return JsonResponse({"message":"SUCCESS"} , status = 200)
            print("인증실패")
            return JsonResponse({"message":"Wrong ID or Password"} , status = 200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status = 400)
    
    def get(self, request):
        return render(request, "users/login_test.html")