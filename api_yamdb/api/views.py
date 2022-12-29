from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from api.filters import TitleFilter
from api.permissions import (
    AdminOnly,
    IsAdminOrReadOnly,
    IsUserAdminModeratorAuthorOrReadOnly,
)
from api.mixins import ListCreateDestroyViewSet
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    NotAdminSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UsersSerializer,
)
from reviews.models import Category, Genre, Review, Title, User


OCCUPIED_EMAIL = 'Электронная почта уже занята!'
OCCUPIED_USERNAME = 'Имя пользователя уже занято!'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = NotAdminSerializer(request.user)
        if request.method == 'PATCH':
            serializer = NotAdminSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        user.confirmation_code = ' '
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get_or_create(
                username=data['username'], email=data['email']
            )
        except AuthenticationFailed:
            error = (
                OCCUPIED_EMAIL
                if User.objects.filter(email=data['email']).exists()
                else OCCUPIED_USERNAME
            )
            raise AuthenticationFailed(error)
        data = {
            'email_body': (
                f'Доброго дня, {user[0].username}.'
                f'\nКод подтверждения доступа к API: '
                f'{user[0].confirmation_code}'
            ),
            'to_email': user[0].email,
            'email_subject': 'Код подтверждения для доступа к API'
        }
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsUserAdminModeratorAuthorOrReadOnly,)

    def __get_review_by_id(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        review = self.__get_review_by_id()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.__get_review_by_id()
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsUserAdminModeratorAuthorOrReadOnly,)

    def __get_title_by_id(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        title = self.__get_title_by_id()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.__get_title_by_id()
        serializer.save(author=self.request.user, title=title)
