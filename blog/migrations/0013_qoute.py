# Generated by Django 3.0.8 on 2021-06-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210425_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
    ]
