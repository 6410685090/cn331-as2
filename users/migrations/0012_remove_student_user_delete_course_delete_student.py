# Generated by Django 4.2.5 on 2023-10-07 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_course_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]