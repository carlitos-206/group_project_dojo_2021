# Generated by Django 3.2.4 on 2021-06-29 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicAPP', '0002_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='joined',
            field=models.ManyToManyField(related_name='members', to='musicAPP.Users'),
        ),
    ]
