# Generated by Django 3.0.8 on 2021-03-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0006_auto_20210310_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='reply',
            field=models.CharField(default='', max_length=255),
        ),
    ]