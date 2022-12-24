from django.core.management.base import BaseCommand
import csv

from reviews.models import User


class Command(BaseCommand):
    help = 'This command uploads users data'

    def handle(self, *args, **options):
        with open('static/data/users.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'name':
                    continue
                User.objects.get_or_create(
                    username=str(row[1]),
                    email=str(row[2]),
                    role=str(row[3]),
                    bio=str(row[4]),
                    first_name=str(row[5]),
                    last_name=str(row[6])
                )
            return 'The users have been uploaded'
