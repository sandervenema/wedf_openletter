# Generated by Django 4.2.3 on 2023-07-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0012_suggestion_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='suggestion',
            field=models.TextField(max_length=10000),
        ),
    ]
