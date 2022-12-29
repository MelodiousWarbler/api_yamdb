from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        validators = []


class NotAdminSerializer(UsersSerializer):

    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)


class GetTokenSerializer(UsersSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validate_username],)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(UsersSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                'Этот адрес электронной почты уже зарегестрирован!'
            )
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!'
            )
        return data

    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value or value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fieilds = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
