from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from .models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )

    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]

    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )

    reader = DictReader(csv_file)

    orders = list()
    order_products = list()

    for row in reader:
        orders.append(
            Order(
                user=User.objects.get(username=row.get('user')),
                delivery_address=row['delivery_address'],
                promocode=row['promocode']
            )
        )

        order_products.append(row["products"])

    total_orders_data = zip(orders, order_products)

    Order.objects.bulk_create(orders)

    for order, product_pks in total_orders_data:
        for pk in product_pks.split(','):
            order.products.add(Product.objects.get(pk=pk))

    return orders
