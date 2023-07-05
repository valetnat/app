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
#         self.stdout.write("Start demo select fields")
#         product_values = Product.objects.values("pk", "name")
#
#         for p_value in product_values:
#             print(p_value)
#
#         self.stdout.write(f"Done")


class Command(BaseCommand):

    def handle(self, *args, **options):
        # with transaction.atomic():  # decorator or context manager
        #     ...
        self.stdout.write("Start demo select fields")
        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)

        self.stdout.write(f"Done")

# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         # with transaction.atomic():  # decorator or context manager
#         #     ...
#         self.stdout.write("Start demo select fields")
#         users_info = User.objects.values_list("pk", "username")
#
#         for user_info in users_info:
#             print(user_info)
#
#         self.stdout.write(f"Done")


class Command(BaseCommand):

    def handle(self, *args, **options):
        # with transaction.atomic():  # decorator or context manager
        #     ...
        self.stdout.write("Start demo select fields")
        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)

        self.stdout.write(f"Done")