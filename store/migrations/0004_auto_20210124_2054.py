# Generated by Django 3.1.5 on 2021-01-24 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210124_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaser',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchaser', to=settings.AUTH_USER_MODEL),
        ),
    ]