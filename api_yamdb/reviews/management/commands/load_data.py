import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User)


def category_data():
    with open('static/data/category.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Категории были добавлены.')


def genre_data():
    with open('static/data/genre.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2]
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Жанры были добавлены.')


def users_data():
    with open('static/data/users.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Пользователи были добавлены.')


def titles_data():
    with open('static/data/titles.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=int(row[3])
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Произведение были добавлены.')


def genre_title_data():
    with open('static/data/genre_title.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                GenreTitle.objects.get_or_create(
                    id=row[0],
                    title_id=int(row[1]),
                    genre_id=int(row[2])
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Жанры для произведений были добавлены.')


def review_data():
    with open('static/data/review.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                Review.objects.get_or_create(
                    id=row[0],
                    title_id=int(row[1]),
                    text=row[2],
                    author_id=int(row[3]),
                    score=int(row[4]),
                    pub_date=row[5])
            except ValueError:
                print(ValueError("Неверные данные!"))
            except IntegrityError:
                print(IntegrityError(
                    ("Пользовательно только единожды может написать"
                     " ревью на это произведение!")
                )
                )
        print('Обзоры были добавлены.')


def comments_data():
    with open('static/data/comments.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'id':
                continue
            try:
                Comment.objects.get_or_create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author_id=int(row[3]),
                    pub_date=row[4]
                )
            except ValueError:
                print(ValueError('Неверные данные!'))
        print('Комментарии были добавлены.')


class Command(BaseCommand):
    help = 'This command uploads data'

    def handle(self, *args, **options):
        funcs = [
            category_data,
            genre_data,
            users_data,
            titles_data,
            genre_title_data,
            review_data,
            comments_data
        ]
        for func in funcs:
            try:
                func()
            except FileNotFoundError:
                print(
                    FileNotFoundError(
                        f'Файл {func.__name__[:-5]}.csv не найден!'
                    )
                )
