# Generated by Django 4.0 on 2022-03-27 09:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_shopuserprofile_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 9, 59, 36, 908294, tzinfo=utc)),
        ),
    ]