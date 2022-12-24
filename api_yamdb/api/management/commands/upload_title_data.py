from django.core.management.base import BaseCommand
import csv

from reviews.models import Title


class Command(BaseCommand):
    help = 'This command uploads titles data'

    def handle(self, *args, **options):
        with open('static/data/titles.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'name' and row[2] == 'year':
                    continue
                Title.objects.get_or_create(
                    name=str(row[1]),
                    year=str(row[2]),
                    category_id=int(row[3])
                )
            return 'The titles have been uploaded'
