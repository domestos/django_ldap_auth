# Generated by Django 3.0.3 on 2020-03-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0002_auto_20200310_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodeconfig',
            name='font_size',
            field=models.DecimalField(decimal_places=2, default=0.25, max_digits=19),
        ),
        migrations.AlterField(
            model_name='qrcodeconfig',
            name='img_width',
            field=models.DecimalField(decimal_places=2, default=1.57, max_digits=19),
        ),
    ]