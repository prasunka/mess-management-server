# Generated by Django 3.1.7 on 2021-03-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='order_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]