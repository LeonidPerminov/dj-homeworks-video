import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = csv.DictReader(file, delimiter=';')
            for phone in phones:
                Phone.objects.create(
                    id=int(phone['id']),
                    name=phone['name'],
                    image=phone['image'],
                    price=int(phone['price']),
                    release_date=phone['release_date'],
                    lte_exists=phone['lte_exists'].lower() == 'true',
                    slug=slugify(phone['name'])
                )
        self.stdout.write(self.style.SUCCESS('✅ Данные успешно импортированы'))




