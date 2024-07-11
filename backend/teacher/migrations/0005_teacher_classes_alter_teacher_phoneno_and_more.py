# Generated by Django 4.0.5 on 2023-04-17 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0010_alter_classes_timetable_classes_and_more'),
        ('teacher', '0004_teacher_phoneno_teacher_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='classes',
            field=models.ManyToManyField(to='classes.classes'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phoneNo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='prn',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
