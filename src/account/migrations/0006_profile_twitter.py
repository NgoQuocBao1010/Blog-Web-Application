# Generated by Django 3.2.8 on 2021-11-14 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]