from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user in the database.
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class AboutMeView(generics.RetrieveAPIView):
    """
    View user credentials for the JWT in header.
    """
    serializer_class = UserSerializer

    def get_object(self):
        """Retrieve the user's credentials"""
        return self.request.user
