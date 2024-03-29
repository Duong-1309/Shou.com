# Generated by Django 3.1.7 on 2021-02-23 11:05

import cloudinary.models
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE'), ('other', 'OTHER')], help_text='Giới tính', max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_modified',
            field=models.DateTimeField(blank=True, help_text='date last modified', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, help_text='phone number', max_length=12, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='File image', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='user',
            name='picture_url',
            field=models.URLField(blank=True, help_text='image url', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='url',
            field=models.CharField(blank=True, db_index=True, help_text='Địa chỉ tùy chỉnh đến trang cá nhân https://shou.com/user-url', max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
