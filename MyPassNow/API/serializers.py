from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, Password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'password']

    def valid_username(self, data):
        if not "username" in data:
            raise serializers.ValidationError("must provide a username")
        if len(data['username']) < 3:
            raise serializers.ValidationError("username must have at least 3 characters")

    def valid_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("password must have at least 8 characters")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("password must have at least one number")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("password must have at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("password must have at least one lowercase letter")
    
    def validate(self, data):
        self.valid_username(data)
        if not "password" in data:
            raise serializers.ValidationError("must provide a password")
        self.valid_password(data["password"])
        if "new_password" in data:
            self.valid_password(data["new_password"])
        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail',queryset=User.objects.all())
    class Meta:
        model = Profile
        fields = ['url', 'user']


class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Password
        fields = ['url', 'website', 'username', 'password', 'password_db_key']