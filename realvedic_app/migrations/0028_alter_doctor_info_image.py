# Generated by Django 4.1.5 on 2023-02-08 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realvedic_app', '0027_doctor_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_info',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]