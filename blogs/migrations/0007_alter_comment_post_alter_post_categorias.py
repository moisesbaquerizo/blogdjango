# Generated by Django 5.1.1 on 2024-10-06 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blogs.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='categorias',
            field=models.ManyToManyField(related_name='posts', to='blogs.category'),
        ),
    ]
