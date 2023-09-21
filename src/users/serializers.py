from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def save(self, **kwargs):
        kwargs = self.validated_data
        obj = User(username=kwargs["username"])
        obj.set_password(kwargs["password"])
        obj.save()
        self.instance = obj
        return obj
