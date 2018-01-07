# Generated by Django 2.0 on 2018-01-07 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecweb', '0012_auto_20180107_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('listening', 'Listening'), ('reading', 'Reading')], max_length=50)),
                ('attendances', models.ManyToManyField(blank=True, to='ecweb.Student')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecweb.ClassRoom')),
            ],
        ),
    ]
