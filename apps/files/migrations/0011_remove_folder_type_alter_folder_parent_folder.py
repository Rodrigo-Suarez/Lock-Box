# Generated by Django 5.1.4 on 2025-01-17 19:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0010_rename_author_filehistory_history_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='type',
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent_folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_folders', to='files.folder'),
        ),
    ]
