# Generated by Django 5.0.4 on 2024-05-24 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_tempconsultation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consult',
            name='status',
        ),
        migrations.AddField(
            model_name='consult',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
