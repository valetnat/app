# Generated by Django 4.2.1 on 2023-06-25 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]