# Generated by Django 2.2.26 on 2022-03-07 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('CityID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=64)),
                ('Tag', models.CharField(max_length=64)),
                ('Description', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ReviewID', models.AutoField(primary_key=True, serialize=False)),
                ('Rating', models.IntegerField(default=0)),
                ('Price', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=2048)),
                ('City', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UKCB.City')),
            ],
        ),
    ]
