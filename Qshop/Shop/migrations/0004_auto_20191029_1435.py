# Generated by Django 2.1.8 on 2019-10-29 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_goods_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='picture',
            field=models.ImageField(default='images/gougou.png', upload_to='images'),
        ),
    ]
