# Generated by Django 4.2.3 on 2023-07-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_participant_district_alter_participant_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='school_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
