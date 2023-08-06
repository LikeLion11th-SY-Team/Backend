from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager as DjangoUserManager


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
    nick_name = models.CharField("닉네임", max_length=10,default="익명")
    own_name = models.CharField("회원 이름", max_length=10, blank=True,default="")
    phone_number =models.CharField("휴대폰 번호", max_length=11, blank=True,default="")
    email = models.EmailField("이메일 주소", null=True,default=None)
    created_at = models.DateTimeField( auto_now_add = True)
    REQUIRED_FIELDS = []
    objects = UserManager()