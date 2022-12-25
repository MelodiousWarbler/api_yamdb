from django.contrib import admin

from .models import Category, Genre, Title, User


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


class GenreInlineAdmin(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [
        GenreInlineAdmin
    ]
    fields = (
        'name',
        'category',
        'description',
        'year',
        'raiting',
        'genre',
    )
    list_display = (
        'name',
        'category',
        'description',
        'year',
        'get_genre',
        'raiting'
    )
    search_fields = (
        'name',
        'category',
        'raiting'
    )
    list_filter = (
        'category',
        'genre',
    )
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]


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
