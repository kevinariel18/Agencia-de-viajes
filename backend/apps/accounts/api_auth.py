from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserCreateSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user and user.status == "ACTIVE":
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response({"detail": "Credenciales inválidas."}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    logout(request)
    return Response({"detail": "Sesión cerrada."})


@api_view(["POST"])
@permission_classes([AllowAny])
def api_register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response(UserSerializer(request.user).data)


urlpatterns = [
    path("login/", api_login, name="api-login"),
    path("logout/", api_logout, name="api-logout"),
    path("register/", api_register, name="api-register"),
    path("me/", api_me, name="api-me"),
]
