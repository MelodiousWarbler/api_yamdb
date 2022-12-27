import re

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


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


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


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
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
