from django.contrib.auth import get_user_model
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the database.
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
