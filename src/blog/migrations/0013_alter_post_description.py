# Generated by Django 3.2.8 on 2021-11-17 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(default='This is a post description'),
        ),
    ]