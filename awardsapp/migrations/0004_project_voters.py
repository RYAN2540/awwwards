# Generated by Django 3.1.7 on 2021-04-08 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awardsapp', '0003_auto_20210408_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='voters',
            field=models.IntegerField(default=0),
        ),
    ]