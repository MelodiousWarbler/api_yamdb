from datetime import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    ABSTRACT_NAME_LENGTH,
    CODE_LENGTH, EMAIL_LENGTH,
    NAME_LENGTH, SLUG_LENGTH
)
from reviews.validators import validate_username


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),
)


class User(AbstractUser):
    username = models.CharField(
        'имя пользователя',
        validators=(validate_username,),
        max_length=NAME_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'email',
        max_length=EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=max(
            max(len(choice), len(_choice)) for choice, _choice in CHOICES
        ),
        choices=CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=NAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=NAME_LENGTH,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=CODE_LENGTH,
        null=True,
        blank=False,
        default=' '
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class AbstractModel(models.Model):
    name = models.CharField(
        max_length=ABSTRACT_NAME_LENGTH,
        verbose_name='категория'
    )
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_LENGTH,
        verbose_name='slug'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Category(AbstractModel):

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class Genre(AbstractModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=ABSTRACT_NAME_LENGTH,
        verbose_name='название'
    )
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(dt.now().year)],
        db_index=True,
        verbose_name='год производства'
    )
    description = models.TextField(
        blank=True,
        verbose_name='описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='категория',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class ReviewAndCommentsModel(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        abstract = True


class Review(ReviewAndCommentsModel):
    score = models.PositiveSmallIntegerField(
        # В redoc'е нет значения по-умолчанию, поэтому будем оптимистами
        default=10,
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10'),
        ],
        verbose_name='Оценка',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta(ReviewAndCommentsModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Не более 1 ревью на произведение у автора'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(ReviewAndCommentsModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )

    class Meta(ReviewAndCommentsModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
