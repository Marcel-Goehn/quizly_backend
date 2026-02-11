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
        """
        Checks if the entered email already exists. If so, a validation error will be raised.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def validate(self, attrs):
        """
        Compares the password and confirmed password. If they don't match, 
        a validation error will be raised.
        """
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError("Password's don't match. Please repeat the process.")
        return attrs
    
    def create(self, validated_data):
        """
        Custom create method has to be used, so that when creating a user, the password will
        be hashed.
        """
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        return User.objects.create_user(username=username, email=email, password=password)