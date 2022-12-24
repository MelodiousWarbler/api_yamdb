from django.contrib import admin

from .models import Category, Genre, Title, Review, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'category',
        'genre',
        'descriptions',
    )
    list_display = (
        'name',
        'category',
        'description',
    )
    search_fields = (
        'name',
        'category',
        'genre',
    )
    list_filter = (
        'category',
        'genre',
    )
    filter_horizontal = (
        'genre',
    )
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Category)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = (
        'text',
        'score',
        'title',
        'author',
    )
    list_display = (
        'title',
        'author',
        'score',
    )
    search_fields = (
        'title',
        'author',
        'score',
    )
    list_filter = (
        'title',
        'author',
        'score',
    )
    empty_value_display = '-пусто-'
