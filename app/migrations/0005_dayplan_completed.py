# Generated by Django 5.1.3 on 2024-11-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_dayplan_score_alter_task_category_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayplan',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
