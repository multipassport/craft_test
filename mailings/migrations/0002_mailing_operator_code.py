# Generated by Django 3.2.14 on 2022-07-31 10:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='operator_code',
            field=models.IntegerField(default=911, validators=[django.core.validators.MinValueValidator(900), django.core.validators.MaxValueValidator(999)], verbose_name='код оператора'),
            preserve_default=False,
        ),
    ]
