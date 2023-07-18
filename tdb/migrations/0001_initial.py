# Generated by Django 3.2.5 on 2022-05-01 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('runner', '0001_initial'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(unique=True)),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('cache_dir', models.CharField(max_length=200)),
                ('TestRunner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='runner.testrunner')),
                ('TrainRunner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='runner.trainrunner')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
        ),
    ]