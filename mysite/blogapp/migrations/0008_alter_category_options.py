# Generated by Django 4.2.1 on 2023-06-25 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
