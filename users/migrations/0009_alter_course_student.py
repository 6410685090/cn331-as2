# Generated by Django 4.2.5 on 2023-09-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_student_courses_course_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='add', to='users.student'),
        ),
    ]
