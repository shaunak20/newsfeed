# Generated by Django 3.0.3 on 2020-05-15 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_stocknews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexes',
            name='pnlper',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
