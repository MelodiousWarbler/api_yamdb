from django.core.management.base import BaseCommand
import csv

from reviews.models import Genre


class Command(BaseCommand):
    help = 'This command uploads genre data'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'name' and row[2] == 'slug':
                    continue
                Genre.objects.get_or_create(
                    name=str(row[1]),
                    slug=str(row[2])
                )
            return 'Genre data has been uploaded'
