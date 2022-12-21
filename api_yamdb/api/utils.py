import csv
from reviews.models import Category, Genre, Title


def load_data(request):
    with open('category.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            print('Record has been done')
