# Generated by Django 3.0.3 on 2020-03-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRcodeConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_width', models.FloatField(default=1.57)),
                ('font_size', models.FloatField(default=0.25)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
