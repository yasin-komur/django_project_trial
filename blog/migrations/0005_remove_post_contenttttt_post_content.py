# Generated by Django 4.0.6 on 2022-08-03 11:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_content_post_contenttttt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='contenttttt',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]