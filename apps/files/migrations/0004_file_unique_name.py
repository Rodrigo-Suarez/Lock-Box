# Generated by Django 5.1.4 on 2025-01-12 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_alter_file_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='unique_name',
            field=models.CharField(default='', verbose_name=255),
            preserve_default=False,
        ),
    ]
