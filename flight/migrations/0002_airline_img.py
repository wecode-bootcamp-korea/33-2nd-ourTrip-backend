# Generated by Django 4.0.4 on 2022-06-08 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='airline',
            name='img',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
