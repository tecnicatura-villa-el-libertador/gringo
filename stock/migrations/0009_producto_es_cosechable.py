# Generated by Django 2.0.2 on 2018-10-25 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_auto_20181025_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='es_cosechable',
            field=models.BooleanField(default=False, help_text='Es resutado del producido de una campaña ?'),
        ),
    ]
