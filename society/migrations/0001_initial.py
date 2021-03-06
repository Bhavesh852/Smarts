# Generated by Django 3.0.8 on 2020-09-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_img', models.ImageField(default='', upload_to='society/images')),
                ('profile_name', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('permanent_address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=20)),
                ('state', models.CharField(default='', max_length=20)),
                ('gender', models.CharField(default='', max_length=10)),
                ('female_members', models.IntegerField(default=0)),
                ('male_members', models.IntegerField(default=0)),
                ('wing', models.CharField(default='', max_length=2)),
                ('flat_no', models.IntegerField(default=0)),
                ('phone1', models.IntegerField(default=0)),
                ('phone2', models.IntegerField(default=0)),
            ],
        ),
    ]
