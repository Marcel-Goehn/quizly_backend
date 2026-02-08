from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema, inline_serializer

from .serializers import RegistrationSerializer


@extend_schema(
    request=RegistrationSerializer,
    responses={201: inline_serializer(
        name="RegistrationSuccessResponse",
        fields={
            "detail": serializers.CharField()
        }
    )},
    description="Registers a new user."
)
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = RegistrationSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User created successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    description="Takes a set of user credentials and returns an access and refresh JSON web token pair as HTTP Only Cookies to prove the authentication of those credentials.",
    responses={200: inline_serializer(
        name="LoginSuccessResponse",
        fields={
            "detail": serializers.CharField(),
            "user": inline_serializer(
                name="UserInlineSerializer",
                fields={
                    "id": serializers.IntegerField(),
                    "username": serializers.CharField(),
                    "email": serializers.EmailField()
                }
            )
        }
    )}
)
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")
        access = response.data.get("access")

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        try:
            user = User.objects.get(username=request.data["username"])
        except User.DoesNotExist:
            return Response("User not found.")

        response.data = {
            "detail": "Login successfully!",
            "user": {
                "id": user.pk,
                "username": user.username,
                "email": user.email
            }
        }
        return response


@extend_schema(
    description="Authentication Required. Logs a user out and deletes acces + refresh token.",
    request=None,
    responses={200: inline_serializer(
        name="LogoutResponseSerializer",
        fields={
            "detail": serializers.CharField()
        }
    )}
)
class LogoutView(APIView):
    def post(self, request):
        response = Response(
            {
                "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
            }
        )
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return response


@extend_schema(
    request=None,
    responses={200: inline_serializer(
        name="ResponseRefreshTokenSerializer",
        fields={
            "detail": serializers.CharField(),
            "access": serializers.CharField()
        }
    )},
    description="Authentication Required. Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid."
)
class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {"detail": "Refresh token invalid"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = serializer.validated_data.get("access")
        response = Response(
            {
                "detail": "Token refreshed",
                "access": "new_access_token"
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return response
