from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user in the database.
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
