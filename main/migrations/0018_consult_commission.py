# Generated by Django 5.0.4 on 2024-05-29 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_consultantpercentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='consult',
            name='commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
