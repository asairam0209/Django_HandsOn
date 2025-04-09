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


class UserRegistrationSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=RoleModel.objects.all(),
        source='role',
        write_only=True
    )

    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'role_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = AuthUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        return user


class TicketManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketManager
        # fields = "__all__"
        exclude = ['clientId', 'role']

        read_only_fields = ['createdAt']

    def create(self, validated_data):
        user = self.context['request'].user
        return TicketManager.objects.create(**validated_data, clientId=user, role=user.role)
