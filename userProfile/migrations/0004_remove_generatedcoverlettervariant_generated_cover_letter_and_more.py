# Generated by Django 4.2.3 on 2023-08-01 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0003_generatedcoverletter_generatedcoverlettervariant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generatedcoverlettervariant',
            name='generated_cover_letter',
        ),
        migrations.DeleteModel(
            name='GeneratedCoverLetter',
        ),
        migrations.DeleteModel(
            name='GeneratedCoverLetterVariant',
        ),
    ]