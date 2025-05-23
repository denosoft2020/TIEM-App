# Generated by Django 5.1.6 on 2025-03-30 11:18

import welcome.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0008_post_saved_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to=welcome.models.cover_photo_path),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default.jpg', upload_to=welcome.models.user_profile_picture_path),
        ),
    ]
