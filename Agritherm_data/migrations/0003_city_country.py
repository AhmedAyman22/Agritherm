# Generated by Django 4.2.1 on 2023-05-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agritherm_data', '0002_remove_city_id_alter_city_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.CharField(default='', max_length=25),
        ),
    ]
