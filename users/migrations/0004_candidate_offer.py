# Generated by Django 4.2.4 on 2024-08-13 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_client_about_alter_client_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='offer',
            field=models.TextField(null=True),
        ),
    ]
