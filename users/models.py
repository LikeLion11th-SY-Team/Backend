from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager as DjangoUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

## 함수 재정의
class UserManager(DjangoUserManager):
    def _create_user(self, username,password, **extra_fields):
        print(username)
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,username, password,**extra_fields):
        print(username)
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        user = self._create_user(username,password,**extra_fields)
        return user
    
    def create_superuser(self, username, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        user = self._create_user(username,password,**extra_fields).save()
        return user
    
# 메인 유저 모델
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True
    )
    nick_name = models.CharField("닉네임", max_length=10,default="익명")
    phone_number =models.CharField("휴대폰 번호", max_length=11, blank=True,default="")
    email = models.EmailField("이메일 주소", null=True,default=None)
    created_at = models.DateTimeField( auto_now_add = True)
    is_social = models.BooleanField("소셜로그인 유저",default=False)
    social_id = models.CharField("소셜로그인 ID",max_length=20,default="")
    

    BOOKMARK = 0
    SIGNUP = 1
    LOGIN = 2
    COMMUNITY = 3
    WRITE = 4
    COMMUNICATE = 5
    MYPAGE = 6
    PROGRESS_CHOICES = [
        (BOOKMARK, "Bookmark"),
        (SIGNUP, "Signup"),
        (LOGIN, "Login"),
        (COMMUNITY, "Community"),
        (WRITE, "Write"),
        (COMMUNICATE, "Communicate"),
        (MYPAGE,"Mypage"),
    ]
    progress = models.IntegerField(
        choices=PROGRESS_CHOICES,
        default=BOOKMARK,
    )

    REQUIRED_FIELDS = []
    objects = UserManager()