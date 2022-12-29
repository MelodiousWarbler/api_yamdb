import csv

from django.core.management.base import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    help = 'This command uploads the reviews'

    def handle(self, *args, **options):
        with open('static/data/review.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'title_id':
                    continue
                # print(int(row[1]), row[2], int(row[3]), int(row[4]), row[5])
                if row[1] == 'title_id':
                    continue
                Review.objects.get_or_create(
                    title_id=int(row[1]),
                    text=row[2],
                    author_id=int(row[3]),
                    score=int(row[4]),
                    pub_date=row[5]
                )
            print('DONE')
