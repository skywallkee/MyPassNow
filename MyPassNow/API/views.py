from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, ProfileSerializer, PasswordSerializer
from .models import Profile, Password

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers

def apiRoot(request):
    return HttpResponse("/api/users/ - all users<br/>/api/user/&lt;username&gt;/ - user")

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True, context={'request': request})
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            username = request.data["username"]
            serializer.save()
            user = User.objects.filter(username=username).first()
            user.set_password(request.  data["password"])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserObj(APIView):
    """
    List a user and modify it.
    """
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_user(username)
        serializer = UserSerializer(user, context={'request': request})
        if not request.user.is_authenticated or not request.user.username == username or (request.user.username != username and not request.user.is_staff):
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_user(username)
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.is_authenticated or not request.user.username == username or (request.user.username != username and not request.user.is_staff):
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            password = user.password
            if not user.check_password(request.data["password"]):
                raise serializers.ValidationError({"password": "invalid password"})
            serializer.save()
            user = self.get_user(username)
            user.password = password
            user.save()
            if "new_password" in request.data and user.check_password(request.data["password"]):
                user.set_password(request.data["new_password"])
                user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)