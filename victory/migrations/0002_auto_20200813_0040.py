# Generated by Django 3.0.7 on 2020-08-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('victory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='victory',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
