# Generated by Django 4.0.5 on 2023-04-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_teacher_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='last_login',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
