from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_superuser(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=True,
        )
