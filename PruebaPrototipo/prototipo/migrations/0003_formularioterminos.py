# Generated by Django 2.1.2 on 2018-11-09 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototipo', '0002_auto_20181026_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormularioTerminos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Palabra', models.CharField(max_length=200)),
            ],
        ),
    ]
