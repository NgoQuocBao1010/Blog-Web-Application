# Generated by Django 3.2.8 on 2021-11-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20211101_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='coverImage',
            field=models.ImageField(default='blog1.jpg', upload_to='posts/'),
        ),
    ]