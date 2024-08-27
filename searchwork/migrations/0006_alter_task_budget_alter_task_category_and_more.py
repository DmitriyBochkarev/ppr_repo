# Generated by Django 4.2.4 on 2024-08-27 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchwork', '0005_task_category_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='budget',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Земля', 'Земля'), ('Канашка', 'Канашка'), ('Вода', 'Вода'), ('Электрика', 'Электрика')], default='Земля', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('Исполнительная документация', 'Исполнительная документация'), ('Проектная/рабочая документация', 'Проектная/рабочая документация'), ('ПОС', 'ПОС'), ('ППР/ППРК', 'ППР/ППРК'), ('Геодезия', 'Геодезия')], default='Исполнительная документация', max_length=200),
        ),
    ]