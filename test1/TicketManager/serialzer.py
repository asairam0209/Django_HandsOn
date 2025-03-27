from rest_framework import serializers
from .models import AuthUser, RoleModel, TicketManager
from django.contrib.auth.hashers import make_password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'role']
        extra_kwargs = {
            'password':
                {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class TicketManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketManager
        fields = '__all__'
