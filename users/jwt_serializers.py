from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

class SpartaTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        return token
class UserSignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(validated_data['username'],validated_data['password'],
            **{
                'nick_name': validated_data['nick_name'],
                'own_name': validated_data['own_name'],
                'phone_number': validated_data['phone_number'],
                'email': validated_data['email']
            })
        user.save()
        return user

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','nick_name','own_name','phone_number','email','is_social']
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['password'],
            {
                'nick_name': validated_data['nick_name'],
                'own_name': validated_data['own_name'],
                'phone_number': validated_data['phone_number'],
                'email': validated_data['email']
            })
        user.save()
        return user