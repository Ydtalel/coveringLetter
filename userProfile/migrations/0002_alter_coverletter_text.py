# Generated by Django 4.2.3 on 2023-07-31 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coverletter',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
