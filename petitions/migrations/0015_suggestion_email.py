# Generated by Django 4.2.3 on 2023-07-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0014_signature_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='email',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
