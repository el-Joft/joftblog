# Generated by Django 2.0.2 on 2018-05-06 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20180506_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='name',
            new_name='parent',
        ),
    ]