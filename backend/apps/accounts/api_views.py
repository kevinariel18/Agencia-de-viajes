from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_role():
            return User.objects.all().select_related("city")
        return User.objects.filter(pk=user.pk)
