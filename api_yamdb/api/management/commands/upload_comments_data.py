import csv

from django.core.management.base import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):
    help = 'This command uploads all comments'

    def handle(self, *args, **options):
        with open('static/data/comments.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'review_id':
                    continue
                Comment.objects.get_or_create(
                    review_id=row[1],
                    text=row[2],
                    author_id=int(row[3]),
                    pub_date=row[4]
                )
            return 'All comments have been uploaded'
