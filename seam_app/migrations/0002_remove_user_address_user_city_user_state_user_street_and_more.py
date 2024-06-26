# Generated by Django 4.2.11 on 2024-03-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seam_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
