# Generated by Django 5.0.4 on 2024-05-29 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_consult_handler'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantPercentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
