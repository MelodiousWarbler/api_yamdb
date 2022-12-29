import csv

from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'This command uploads category data'

    def handle(self, *args, **options):
        with open('static/data/category.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'name' and row[2] == 'slug':
                    continue
                Category.objects.get_or_create(
                    name=row[1],
                    slug=row[2]
                )
            return 'Category data has been uploaded'
