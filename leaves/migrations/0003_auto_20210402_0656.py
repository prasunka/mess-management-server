# Generated by Django 3.1.7 on 2021-04-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_leave_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='duration',
            field=models.IntegerField(blank=True),
        ),
    ]
