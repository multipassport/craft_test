# Generated by Django 3.2.14 on 2022-07-31 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_mailing_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='mailing',
            name='tags',
        ),
        migrations.AddField(
            model_name='customer',
            name='tag',
            field=models.CharField(default='', max_length=20, verbose_name='тэг'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailing',
            name='tag',
            field=models.CharField(default='', max_length=20, verbose_name='тэг'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]