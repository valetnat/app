from typing import Sequence

from django.db import transaction
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order, Product


# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         # with transaction.atomic():  # decorator or context manager
#         #     ...
#         self.stdout.write("Start demo bulk actions")
#
#         info = [
#             ('Smartphone_1', 199),
#             ('Smartphone_2', 299),
#             ('Smartphone_3', 399),
#
#         ]
#
#         products = [
#             Product(name=name, price=price)
#             for name, price in info
#         ]
#         print(products)
#         result = Product.objects.bulk_create(products)
#
#         print(result)
#
#         for obj in result:
#             print(obj)
#         self.stdout.write(f"Done")


class Command(BaseCommand):

    def handle(self, *args, **options):
        # with transaction.atomic():  # decorator or context manager
        #     ...
        self.stdout.write("Start demo bulk actions")
        # Get all instances where name contains "Smartphone",
        # afterwards the field 'discount' will be updated allover them
        result = Product.objects.filter(
            name__contain='Smartphone'
        ).update(discount=10)

        print(result)

        self.stdout.write(f"Done")