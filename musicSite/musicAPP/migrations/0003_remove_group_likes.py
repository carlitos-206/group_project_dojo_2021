# Generated by Django 2.2 on 2021-07-01 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicAPP', '0002_group_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='likes',
        ),
    ]