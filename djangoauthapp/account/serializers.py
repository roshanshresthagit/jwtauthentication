from rest_framework import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style = {'input_type':'password'},write_only =True)
    class Meta:
        model = User
        fields = ('email','name','password','password2','tc')
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't matched")
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length= 255)
    class Meta:
        model= User
        fields =['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length= 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']

    def validate(self, attrs):
        user = self.context.get('user')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if  password != password2:
            raise serializers.ValidationError("Password and confirm passowrd doesn;t match")
        user.set_password(password)
        user.save()
        return attrs
    
class SenderPasswordResetEmailSerializer(serializers.Serializer):
    email= serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/rest/'+uid+'/'+token
            return attrs
        else:
            raise ValidationErr('You are not Registered User')








