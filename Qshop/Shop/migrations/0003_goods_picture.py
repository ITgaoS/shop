# Generated by Django 2.1.8 on 2019-10-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_auto_20191029_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='picture',
            field=models.ImageField(default='img/gougou.png', upload_to='shop/img'),
        ),
    ]
