# Generated by Django 2.2 on 2019-04-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototipo', '0007_auto_20190312_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeiSpa30Synset',
            fields=[
                ('offset', models.CharField(max_length=17, primary_key=True, serialize=False)),
                ('pos', models.CharField(max_length=1)),
                ('sons', models.IntegerField()),
                ('status', models.CharField(max_length=1)),
                ('lexical', models.CharField(max_length=1)),
                ('instance', models.IntegerField()),
                ('gloss', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField()),
                ('levelfromtop', models.IntegerField(db_column='levelFromTop')),
                ('mark', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'wei_spa-30_synset',
                'managed': False,
            },
        ),
    ]