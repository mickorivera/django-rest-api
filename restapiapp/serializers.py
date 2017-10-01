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

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


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

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'is_active',)
        read_only_fields = ('first_name', )
