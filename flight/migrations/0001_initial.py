# Generated by Django 4.0.4 on 2022-06-08 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'airlines',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'airports',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=50)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.airline')),
                ('destination_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='flight.airport')),
                ('origin_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='flight.airport')),
            ],
            options={
                'db_table': 'routes',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('price', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.route')),
            ],
            options={
                'db_table': 'flights',
            },
        ),
        migrations.AddField(
            model_name='airport',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.region'),
        ),
    ]
