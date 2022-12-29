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
    )
    list_display = (
        'name',
        'category',
        'description',
        'year',
        'жанры',
    )
    search_fields = (
        'name',
        'category',
    )
    list_filter = (
        'category',
        'genre',
    )
    empty_value_display = '-пусто-'

    def жанры(self, obj):
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
