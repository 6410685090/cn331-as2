# Generated by Django 4.2.5 on 2023-09-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_student_lastname_student_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='student', to='users.student'),
        ),
    ]
