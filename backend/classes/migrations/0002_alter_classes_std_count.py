# Generated by Django 3.2 on 2023-04-14 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='std_count',
            field=models.IntegerField(null=True),
        ),
    ]
