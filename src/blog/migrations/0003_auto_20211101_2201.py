# Generated by Django 3.2.8 on 2021-11-01 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211101_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='coverImage',
            field=models.ImageField(default='blog1.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]