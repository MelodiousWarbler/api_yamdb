import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data.get('email', False):
            if User.objects.filter(email=data['email']):
                raise serializers.ValidationError(
                    {'email': 'Данный email уже зарегистрирован'}
                )
        if data.get('username', False):
            if User.objects.filter(username=data['username']):
                raise serializers.ValidationError(
                    {'username': 'Данный username уже зарегистрирован'}
                )
        return data

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def validate(self, data):
        errors = {}

        if not data.get('username', False):
            errors['username'] = 'Это поле обязательно'
        if not data.get('email', False):
            errors['email'] = 'Это поле обязательно'
        user = data.get('username', False)
        if user.lower() == 'me':
            raise serializers.ValidationError('Username "me" недопустимо')
        if re.search(r'^[\w.@+-]+$', user) is None:
            raise ValidationError(
                (f'Не допустимые символы <{user}> в нике.'),
                params={'value': user},
            )
        if errors:
            raise serializers.ValidationError(errors)

        if User.objects.filter(email=data['email']):
            user = User.objects.get(email=data['email'])
            if user.username != data['username']:
                raise serializers.ValidationError(
                    {'email': 'Данный email уже зарегистрирован'}
                )
        elif User.objects.filter(username=data['username']):
            user = User.objects.get(username=data['username'])
            if user.email != data['email']:
                raise serializers.ValidationError(
                    {'username': 'Данный user уже зарегистрирован'}
                )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )
    raiting = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'raiting',
            'description',
            'genre',
            'category',
            'raiting'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'raiting',
            'description',
            'genre',
            'category'
        )


class CurrentTitleIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        default=CurrentTitleIdDefault()
    )

    def validate_score(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                'Оценка должна быть целочисленной!')
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10 (включительно)')
        return value

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
