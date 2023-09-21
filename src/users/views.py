from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import UserRegisterSerializer

User = get_user_model()


class UserViewSet(GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    @action(["post"], detail=False, serializer_class=UserRegisterSerializer)
    def register(self, request, *args, **kwargs):
        """Register new user by username and password."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
