# Generated by Django 2.1.2 on 2019-03-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alias',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(default=1, upload_to='cover'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('man', '남성'), ('woman', '여성')], default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='introduce',
            field=models.TextField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
