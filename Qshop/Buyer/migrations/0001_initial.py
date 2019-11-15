# Generated by Django 2.1.8 on 2019-11-04 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('QUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_user', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=32)),
                ('good_price', models.FloatField()),
                ('goods_picture', models.ImageField(upload_to='buyer/images')),
                ('good_number', models.IntegerField()),
                ('good_total', models.FloatField()),
                ('good_store', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_number', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_total', models.FloatField(default=0)),
                ('goods_picture', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Pay_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32)),
                ('order_time', models.DateTimeField(auto_now=True)),
                ('order_number', models.IntegerField()),
                ('order_total', models.FloatField(default=0)),
                ('order_state', models.IntegerField(default=0)),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QUser.User')),
            ],
        ),
        migrations.AddField(
            model_name='order_info',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Pay_order'),
        ),
        migrations.AddField(
            model_name='order_info',
            name='order_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QUser.User'),
        ),
    ]
