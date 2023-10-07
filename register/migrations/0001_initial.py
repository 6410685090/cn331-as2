# Generated by Django 4.2.5 on 2023-10-07 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='-', max_length=64)),
                ('lastname', models.CharField(default='-', max_length=64)),
                ('student_id', models.CharField(default='-', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=64)),
                ('subject_id', models.CharField(max_length=5)),
                ('semester', models.CharField(max_length=2)),
                ('year', models.CharField(max_length=4)),
                ('seat', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('student', models.ManyToManyField(blank=True, related_name='cstudent', to='register.student')),
            ],
        ),
    ]
