# Generated by Django 5.0.4 on 2024-04-18 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='icon',
            field=models.ImageField(default='default/about_icon.png', upload_to='about_icons/'),
        ),
    ]
