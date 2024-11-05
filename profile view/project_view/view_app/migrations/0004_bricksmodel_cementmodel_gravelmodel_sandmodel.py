# Generated by Django 5.1.2 on 2024-11-05 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_app', '0003_rename_uploader_name_imagemodel_uploaded_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bricksmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_bricks', models.IntegerField()),
                ('no_of_bricks_used', models.IntegerField()),
                ('no_of_bricks_left', models.IntegerField()),
                ('bricks_arrival_date', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cementmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_bags', models.IntegerField()),
                ('no_of_bags_used', models.IntegerField()),
                ('no_of_bags_left', models.IntegerField()),
                ('bags_arrival_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Gravelmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_trucks_of_gravel', models.IntegerField()),
                ('no_of_trucks_used', models.IntegerField()),
                ('no_of_trucks_left', models.IntegerField()),
                ('trucks_arrival_date', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sandmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Total_trucks', models.IntegerField()),
                ('no_of_trucks_used', models.IntegerField()),
                ('no_of_trucks_left', models.IntegerField()),
                ('trucks_arrival_date', models.IntegerField()),
            ],
        ),
    ]
