from datetime import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

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
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=max(len(choice[1]) for choice in CHOICES),
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
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default=' '
    )

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

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class AbstractModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='категория'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
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
        max_length=64,
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


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
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
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Не более 1 ревью на произведение у автора'
            ),
        ]

    def __str__(self):
        return self.text


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


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    text = models.TextField(
        verbose_name='текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
