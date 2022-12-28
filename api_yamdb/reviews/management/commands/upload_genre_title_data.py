from django.core.management.base import BaseCommand
import csv

from reviews.models import GenreTitle


class Command(BaseCommand):
    help = 'This command uploads genre-title data'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'title_id' and row[2] == 'genre_id':
                    continue
                GenreTitle.objects.get_or_create(
                    title_id=int(row[1]),
                    genre_id=int(row[2])
                )
            return 'The genre-title data has been uploaded'
