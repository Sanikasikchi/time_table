# Generated by Django 4.0.5 on 2022-09-05 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='sort_order',
            field=models.IntegerField(default=1),
        ),
    ]
