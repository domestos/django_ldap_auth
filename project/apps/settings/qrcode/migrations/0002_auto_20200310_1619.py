# Generated by Django 3.0.3 on 2020-03-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodeconfig',
            name='img_width',
            field=models.DecimalField(decimal_places=10, default=1.57, max_digits=19),
        ),
    ]
