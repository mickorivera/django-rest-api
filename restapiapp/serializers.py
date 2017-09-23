from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'url',)
        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RestrictedUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'url',)
        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
            'last_name': {'write_only': True}
        }


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active',)


class RestrictedUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'is_active',)


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'is_active',)
        read_only_fields = ('first_name',)


class UserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active',)
        read_only_fields = ('email', 'is_active', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
