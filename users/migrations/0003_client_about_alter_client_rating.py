# Generated by Django 4.2.4 on 2023-08-19 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_worker_client_candidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
