from rest_framework import viewsets, pagination
from rest_framework.views import APIView

from api.serializers import (
    GetTokenSerializer,
    NotAdminSerializer,
    SignUpSerializer,
    UsersSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from api.permissions import isAdminOrOnlyRead
from reviews.models import Category, Genre, Title


class UsersViewSet(viewsets.ModelViewSet):
    pass


class APIGetToken(APIView):
    pass


class APISignup(APIView):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = isAdminOrOnlyRead
    pagination_class = pagination.LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = isAdminOrOnlyRead
    pagination_class = pagination.LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = isAdminOrOnlyRead
    pagination_class = pagination.LimitOffsetPagination
