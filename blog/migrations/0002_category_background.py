# Generated by Django 3.0.8 on 2021-02-01 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='background',
            field=models.ImageField(default='test', upload_to=''),
            preserve_default=False,
        ),
    ]
