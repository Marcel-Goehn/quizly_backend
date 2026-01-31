from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "confirmed_password", "email"]
        extra_kwargs = {
            "email": {"required": True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError("Password's don't match. Please repeat the process.")
        return attrs
    
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        return User.objects.create_user(username=username, email=email, password=password)