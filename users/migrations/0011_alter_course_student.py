# Generated by Django 4.2.5 on 2023-10-06 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_course_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='cstudent', to='users.student'),
        ),
    ]
