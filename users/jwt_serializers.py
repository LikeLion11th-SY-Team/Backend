from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

class SpartaTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['email'] = user.email

        return token


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['id'],
            email = validated_data['emailId'] + '@' + validated_data['platformAddress'],
            password = validated_data['pw']
        )
        user.nick_name = validated_data['nickname']
        #user.name = validated_data['name']
        user.phone_number = validated_data['phone_number']
        user.save()
        return user