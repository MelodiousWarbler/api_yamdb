from rest_framework import viewsets
from rest_framework.views import APIView

from .serializers import (
    GetTokenSerializer,
    NotAdminSerializer,
    SignUpSerializer,
    UsersSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    pass


class APIGetToken(APIView):
    pass


class APISignup(APIView):
    pass
