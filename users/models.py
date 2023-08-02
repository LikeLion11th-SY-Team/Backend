from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager as DjangoUserManager


## 함수 재정의
class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password,**extra_fields):
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username,email,password,**extra_fields)
    
    def create_superuser(self, username, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username,email,password,**extra_fields)
    
# 메인 유저 모델
class User(AbstractUser):
    phone_number =models.CharField(verbose_name='phone_number', max_length=11)
    objects = UserManager()