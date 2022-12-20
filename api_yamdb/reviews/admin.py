from django.contrib import admin

from .models import User, Title, Category, Genre


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
        'title',
        'category',
        'genre',
    )
    list_display = (
        'title',
        'category',
    )
    search_fields = (
        'title',
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
        'description',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


admin.site.register(Category)
