# Generated by Django 4.0 on 2022-01-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdg', '0002_article_project_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]