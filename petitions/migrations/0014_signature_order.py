# Generated by Django 4.2.3 on 2023-07-15 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0013_alter_suggestion_suggestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]