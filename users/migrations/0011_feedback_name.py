# Generated by Django 4.2.4 on 2024-09-15 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_feedback_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='dima', max_length=100),
            preserve_default=False,
        ),
    ]
