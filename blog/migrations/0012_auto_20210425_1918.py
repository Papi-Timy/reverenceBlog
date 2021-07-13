# Generated by Django 3.0.8 on 2021-04-25 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ForeignKey(
                default='1', on_delete=django.db.models.deletion.CASCADE, to='blog.Category'),
            preserve_default=False,
        ),
    ]