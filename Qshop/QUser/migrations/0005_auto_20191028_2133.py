# Generated by Django 2.1.8 on 2019-10-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QUser', '0004_auto_20191028_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
    ]
