# Generated by Django 3.1 on 2020-08-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Token'),
        ),
    ]
