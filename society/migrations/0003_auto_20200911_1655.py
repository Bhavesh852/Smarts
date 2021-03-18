# Generated by Django 3.0.8 on 2020-09-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0002_profile_uname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('email', models.CharField(default='', max_length=70)),
                ('phone', models.CharField(default='', max_length=50)),
                ('msg', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]