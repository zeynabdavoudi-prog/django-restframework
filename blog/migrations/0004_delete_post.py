# Generated by Django 5.1.1 on 2024-09-06 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
