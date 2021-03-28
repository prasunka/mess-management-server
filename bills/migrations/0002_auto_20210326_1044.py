# Generated by Django 3.1.7 on 2021-03-26 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_from',
            field=models.DateTimeField(),
        ),
    ]
