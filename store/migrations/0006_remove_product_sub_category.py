# Generated by Django 3.1.5 on 2021-01-25 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210125_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
    ]