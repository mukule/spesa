# Generated by Django 5.0.4 on 2024-04-18 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_panel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
    ]
