# Generated by Django 2.1 on 2019-02-19 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
