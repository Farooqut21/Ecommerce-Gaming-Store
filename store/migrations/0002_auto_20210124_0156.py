# Generated by Django 3.1.5 on 2021-01-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(default=0, help_text='Number format:0300-1234567'),
        ),
    ]
