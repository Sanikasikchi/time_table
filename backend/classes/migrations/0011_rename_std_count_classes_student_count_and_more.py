# Generated by Django 4.0.5 on 2023-04-18 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0010_alter_classes_timetable_classes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classes',
            old_name='std_count',
            new_name='student_count',
        ),
        migrations.RenameField(
            model_name='classes_timetable_period',
            old_name='sub',
            new_name='subject',
        ),
    ]
