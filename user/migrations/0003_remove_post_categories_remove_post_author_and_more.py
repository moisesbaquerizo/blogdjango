# Generated by Django 5.1.1 on 2024-10-08 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_category_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]