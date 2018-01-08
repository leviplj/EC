# Generated by Django 2.0 on 2018-01-03 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecweb', '0009_auto_20171230_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500)),
                ('title', models.CharField(max_length=50)),
                ('start_event', models.DateField()),
                ('end_event', models.DateField(blank=True)),
                ('address', models.CharField(max_length=250)),
                ('neighborhood', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('local_lat', models.CharField(blank=True, max_length=250, null=True)),
                ('local_long', models.CharField(blank=True, max_length=250, null=True)),
                ('limit', models.IntegerField(blank=True)),
                ('teacher', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ecweb.Teacher')),
            ],
        ),
    ]