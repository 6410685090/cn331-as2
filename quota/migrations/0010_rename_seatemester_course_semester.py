# Generated by Django 4.2.5 on 2023-09-20 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quota', '0009_rename_semester_course_seatemester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='seatemester',
            new_name='semester',
        ),
    ]
