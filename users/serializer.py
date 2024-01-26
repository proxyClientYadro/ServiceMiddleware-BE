from typing import Type

from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('uuid', 'email', 'password', 'created_at',)
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data) -> Type['UserModel']:
        user = UserModel.objects.create_user(**validated_data)
        return user