import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User)


class Command(BaseCommand):
    help = 'This command uploads data'

    def handle(self, *args, **options):
        with open('static/data/category.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                Category.objects.get_or_create(
                    name=row[1],
                    slug=row[2]
                )
            print('Category data has been uploaded')

        with open('static/data/genre.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                Genre.objects.get_or_create(
                    name=row[1],
                    slug=row[2]
                )
            print('Genre data has been uploaded')

        with open('static/data/users.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                User.objects.get_or_create(
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
            print('Users have been uploaded')

        with open('static/data/titles.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                Title.objects.get_or_create(
                    name=row[1],
                    year=row[2],
                    category_id=int(row[3])
                )
            print('Titles have been uploaded')

        with open('static/data/genre_title.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                GenreTitle.objects.get_or_create(
                    title_id=int(row[1]),
                    genre_id=int(row[2])
                )
            print('Genre-title data has been uploaded')

        with open('static/data/review.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                try:
                    Review.objects.get_or_create(
                        title_id=int(row[1]),
                        text=row[2],
                        author_id=int(row[3]),
                        score=int(row[4]),
                        pub_date=row[5])
                except ValueError:
                    continue
                except IntegrityError:
                    continue
            print('Reviews have been uploaded')

        with open('static/data/comments.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'id':
                    continue
                try:
                    Comment.objects.get_or_create(
                        review_id=row[1],
                        text=row[2],
                        author_id=int(row[3]),
                        pub_date=row[4]
                    )
                except ValueError:
                    continue
                except IntegrityError:
                    continue
            print('Comments have been uploaded')
