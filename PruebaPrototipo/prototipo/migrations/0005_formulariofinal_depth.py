# Generated by Django 2.1.2 on 2018-11-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototipo', '0004_formulariofinal'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulariofinal',
            name='Depth',
            field=models.IntegerField(default=1),
        ),
    ]
